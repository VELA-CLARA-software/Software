import yaml, collections, subprocess, os, math, re, sys
from shutil import copyfile
import numpy as np
from FrameworkHelperFunctions import *
from getGrids import *
import SimulationFramework.Modules.read_beam_file as rbf
from collections import defaultdict
from Framework_ASTRA import ASTRA
from Framework_Elegant import Elegant
from Framework_CSRTrack import CSRTrack

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))

yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return OrderedDict(z)

from collections import Iterable
def flatten(coll):
    for i in coll:
            if isinstance(i, Iterable) and not isinstance(i, basestring):
                for subc in flatten(i):
                    yield subc
            else:
                yield i

def clean_directory(folder):
    for the_file in os.listdir(folder):
        file_path = os.path.join(folder, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            #elif os.path.isdir(file_path): shutil.rmtree(file_path)
        except Exception as e:
            print(e)

class Framework(object):

    def __init__(self, subdir='test', overwrite=None, runname='CLARA_240', master_lattice_location=None, clean=False):
        super(Framework, self).__init__()
        self.lineIterator = 0
        self.basedirectory = os.getcwd()
        if master_lattice_location is None:
            self.master_lattice_location = (os.path.relpath(os.path.dirname(os.path.abspath(__file__)) + '/../MasterLattice/')+'/').replace('\\','/')
            # print 'self.master_lattice_location = ', self.master_lattice_location
        else:
            self.master_lattice_location = master_lattice_location
        self.filedirectory = os.path.dirname(os.path.abspath(__file__))
        self.subdir = subdir
        self.overwrite = overwrite
        self.runname = runname
        self.subdirectory = self.basedirectory+'/'+subdir
        self.globalSettings = dict()
        self.fileSettings = dict()
        self._elements = dict()
        self.groups = dict()
        self.astra = ASTRA(framework=self, directory=self.subdir)
        self.elegant = Elegant(framework=self, directory=self.subdir)
        self.CSRTrack = CSRTrack(framework=self, directory=self.subdir)
        if not os.path.exists(self.subdirectory):
            os.makedirs(self.subdirectory)
        else:
            if clean == True:
                clean_directory(self.subdirectory)
        if self.overwrite == None:
            if not os.path.exists(self.subdirectory):
                os.makedirs(self.subdirectory)
                self.overwrite = True
            else:
                response = raw_input('Overwrite existing directory ? [Y/n]')
                self.overwrite = True if response in {'','y','Y','yes','Yes','YES'} else False
        self.astraFiles = []

    def loadElementsFile(self, input):
        if isinstance(input,(list,tuple)):
            filename = input
        else:
            filename = [input]
        for f in filename:
            stream = file(self.master_lattice_location + f, 'r')
            elements = yaml.load(stream)['elements']
            stream.close()
            for name, elem in elements.iteritems():
                self.addElement(name, elem)

    def isevaluable(self, s):
        try:
            eval(s)
            return True
        except:
            return False

    def expand_substitution(self, param, subs={}):
        if isinstance(param,(str)):
            regex = re.compile('\$(.*)\$')
            s = re.search(regex, param)
            if s:
                if self.isevaluable(s.group(1)) is True:
                    replaced_str = eval(re.sub(regex, s.group(1), param))
                else:
                    replaced_str = re.sub(regex, s.group(1), param)
                for key in subs:
                    replaced_str = replaced_str.replace(key, subs[key])
                return replaced_str
            else:
                return param
        else:
            return param

    def loadSettings(self, filename='short_240.settings'):
        """Load Lattice Settings from file"""
        self._elements = OrderedDict()
        self.elementOrder = []
        stream = file(self.master_lattice_location+filename, 'r')
        settings = yaml.load(stream)
        self.globalSettings = settings['global']
        self.generatorFile = self.master_lattice_location + self.globalSettings['generatorFile'] if 'generatorFile' in self.globalSettings else None
        self.fileSettings = settings['files']
        elements = settings['elements']
        self.groups = settings['groups']
        stream.close()
        for name, elem in elements.iteritems():
            self.addElement(name, elem)

    def addElement(self, name, element, subelement=False):
        if name == 'filename':
            self.loadElementsFile(element)
        else:
            self._elements[name] = element
            if subelement:
                return [name]
            if 'sub_elements' in element:
                subelements = [name]
                for name, elem in element['sub_elements'].iteritems():
                    subelements += self.addElement(name, elem, True)
                self.elementOrder.append(subelements)
            else:
                self.elementOrder.append(name)

    def deleteFromList(self, inputlist, element):
        newlist = []
        for l in inputlist:
            if isinstance(l,(list,tuple)):
                tmplist = self.deleteFromList(l, element)
                if not tmplist == []:
                    newlist.append(tmplist)
            elif not l == element:
                newlist.append(l)
        return newlist

    def deleteElement(self, name):
        del self._elements[name]
        self.elementOrder = self.deleteFromList(self.elementOrder, name)

    def deleteElementIndex(self, index=None):
        self.deleteElement(self.getElementAt(index)[0])

    def deleteElementsBetween(self, start, end):
        startindex = self.elementIndex(start)
        endindex = self.elementIndex(end)
        flatelementOrder = list(flatten(self.elementOrder))
        for e in flatelementOrder[min([startindex, endindex]): max([startindex, endindex])]:
            self.deleteElement(e)

    def selectElementsBetween(self,start, end):
        selectedElements = []
        startindex = self.elementIndex(start)
        endindex = self.elementIndex(end)
        flatelementOrder = list(flatten(self.elementOrder))
        for e in flatelementOrder[min([startindex, endindex]):1+max([startindex, endindex])]:
            selectedElements.append([e, self.getElement(e)])
        # for e in flatelementOrder[1+max([startindex, endindex]):]:
        #     selectedElements.append([e, self.getElement(e)])
        return selectedElements

    def elementIndex(self, element):
        flatelementOrder = list(flatten(self.elementOrder))
        if element in flatelementOrder:
            return flatelementOrder.index(element)
        else:
            raise NameError
            return -1

    def getElementAt(self, index):
        flatelementOrder = list(flatten(self.elementOrder))
        element = flatelementOrder[index]
        data = self._elements[element]
        return [element, data]

    def previousElement(self, element):
        index = self.elementIndex(element)
        return self.getElementAt(index - 1)

    def nextElement(self, element):
        index = self.elementIndex(element)
        return self.getElementAt(index + 1)

    @property
    def elements(self):
        elements = OrderedDict()
        for k in self.elementOrder:
            if isinstance(k, (list, tuple)):
                for s in k:
                    elements[s] = self._elements[s]
            else:
                elements[k] = self._elements[k]
        return elements

    @property
    def master_elements(self):
        elements = OrderedDict()
        for k in self.elementOrder:
            if isinstance(k, (list, tuple)):
                elements[k[0]] = self._elements[k[0]]
            else:
                elements[k] = self._elements[k]
        return elements

    def getFileSettings(self, file, block, default={}):
        """Return the correct settings 'block' from 'file' dict if exists else return empty dict"""
        if file in self.fileSettings and block in self.fileSettings[file]:
            return self.fileSettings[file][block]
        else:
            return default

    def getSettingsBlock(self, dict, block):
        """Return the correct settings 'block' from dict if exists else return empty dict"""
        if block in dict:
            return dict[block]
        else:
            return {}

    def modifyFile(self, filename, setting, value):
        if filename in self.fileSettings:
            if isinstance(setting, (list,tuple)):
                dic = self.fileSettings[filename]
                for key in setting[:-1]:
                    dic = dic.setdefault(key, {})
                dic[setting[-1]] = value
            elif not setting in self.fileSettings:
                self.fileSettings[setting] = {}
                self.fileSettings[filename][setting] = value

    def getElement(self, element='', setting=None, default=[]):
        """return 'element' from the main elements dict"""
        if element in self._elements:
            if setting is not None:
                if setting in self._elements[element]:
                    setvalue = self._elements[element][setting]
                    if self.isevaluable(setvalue):
                        return eval(setvalue)
                    else:
                        return setvalue
                else:
                    return default
            else:
                return self._elements[element]
        else:
            return default

    def modifyElement(self, element='', setting='', value=''):
        """return 'element' from the main elements dict"""
        element = self.getElement(element)
        if setting in element:
            element[setting] = value

    def getElementType(self, type='', setting=None):
        """return 'element' from the main elements dict"""
        elems = []
        for name, element in self._elements.viewitems():
            if 'type' in element and element['type'] == type:
                elems.append(name)
                # print element
        elems = sorted(elems, key=lambda x: self._elements[x]['position_start'][2])
        if setting is not None:
            return [self._elements[x][setting] for x in elems]
        else:
            return elems

    def setElementType(self, type='', setting=None, values=[]):
        """return 'element' from the main elements dict"""
        elems = self.getElementType(type)
        if len(elems) == len(values):
            for e, v  in zip(elems, values):
                self._elements[e][setting] = v
        else:
            raise ValueError

    def getElementsBetweenS(self, elementtype=None, output={}, zstart=None, zstop=None):
        # zstart = zstart if zstart is not None else getParameter(output,'zstart',default=0)
        if zstart is None:
            zstart = getParameter(output,'zstart',default=None)
            if zstart is None:
                startelem = getParameter(output,'start_element',default=None)
                if startelem is None or startelem not in self._elements:
                    zstart = 0
                else:
                    zstart = self._elements[startelem]['position_start'][2]
        # zstop = zstop if zstop is not None else getParameter(output,'zstop',default=0)
        if zstop is None:
            zstop = getParameter(output,'zstop',default=None)
            if zstop is None:
                endelem = getParameter(output,'end_element',default=None)
                if endelem is None or endelem not in self._elements:
                    zstop = 0
                else:
                    zstop = self._elements[endelem]['position_end'][2]

        if elementtype is not None:
            elements = findSetting('type',elementtype,dictionary=self._elements)
        else:
            elements = list(self._elements.iteritems())

        elements = sorted([[s[1]['position_start'][2],s[0]] for s in elements if s[1]['position_start'][2] >= zstart and s[1]['position_start'][2] <= zstop])
        return [e[1] for e in elements]

    def getGroup(self, group=''):
        """return all elements in a group from the main elements dict"""
        elements = []
        if group in self.groups:
            groupelements = self.groups[group]['elements']
            for e in groupelements:
                elements.append([e,self.getElement(e)])
        return elements

    def xform(self, theta, tilt, length, x, r):
        """Calculate the change on local coordinates through an element"""
        theta = theta if abs(theta) > 1e-9 else 1e-9
        tiltMatrix = np.matrix([
            [np.cos(tilt), -np.sin(tilt), 0],
            [np.sin(tilt), np.cos(tilt), 0],
            [0, 0, 1]
        ])
        angleMatrix = np.matrix([
            [length/theta*(np.cos(theta)-1)],
            [0],
            [length/theta*np.sin(theta)]
        ])
        dx = np.dot(r, angleMatrix)
        rt = np.transpose(r)
        n = rt[1]*np.cos(tilt)-rt[0]*np.sin(tilt)
        crossMatrix = np.matrix([
            np.cross(rt[0], n),
            np.cross(rt[1], n),
            np.cross(rt[2], n)
        ])*np.sin(theta)
        rp = np.outer(np.dot(rt,n), n)*(1-np.cos(theta))+rt*np.cos(theta)+crossMatrix
        return [np.array(x + dx), np.array(np.transpose(rp))]

    def elementPositions(self, elements, startpos=None, startangle=0):
        """Calculate element positions for the given 'elements'"""
        anglesum = [startangle]
        localXYZ = np.identity(3)
        if startpos is None:
            startpos = elements[elements.keys()[0]]['position_start']
            if len(startpos) == 1:
                startpos = [0,0,startpos]
        x1 = np.matrix(np.transpose([startpos]))
        x = [np.array(x1)]
        if startangle is not 0:
            localXYZ = self.xform(startangle, 0, 0, x1, localXYZ)[1]
        for name, d in elements.iteritems():
            angle = self.getElement(name,'angle', default=0)
            anglesum.append(anglesum[-1]+angle)
            x1, localXYZ = self.xform(angle, 0, getParameter(d,'length'), x1, localXYZ)
            x.append(x1)
        # print 'anglesum = ', anglesum
        return zip(x, anglesum[:-1], elements), localXYZ

    def createDrifts(self, elements, startpos=None, zerolengthdrifts=False):
        """Insert drifts into a sequence of 'elements'"""
        positions = []
        elementno = 0
        newelements = OrderedDict()
        for name, e in elements:
            pos = np.array(e['position_start'])
            positions.append(pos)
            # length = np.array(e['position_end'])
            positions.append(e['position_end'])
        if not startpos == None:
            positions.prepend(startpos)
        else:
            positions = positions[1:]
            positions.append(positions[-1])
            positions[-1][2] + 1e-6
        driftdata = zip(elements, list(chunks(positions, 2)))
        # print 'driftdata = ', driftdata
        for e, d in driftdata:
            newelements[e[0]] = e[1]
            if len(d) > 1:
                length = d[1][2] - d[0][2]
                if length > 0 or zerolengthdrifts is True:
                    elementno += 1
                    name = 'drift'+str(elementno)
                    self._elements[name] = {'length': length, 'type': 'drift',
                     'position_start': list(d[0]),
                     'position_end': list(d[1])
                    }
                    newelements[name] = self._elements[name]
        return newelements

    def setDipoleAngle(self, dipole, angle=0):
        """Set the dipole angle for a given 'dipole'"""
        name, d = dipole
        if getParameter(d,'entrance_edge_angle') == 'angle':
            d['entrance_edge_angle'] = np.sign(d['angle'])*angle
        if getParameter(d,'exit_edge_angle') == 'angle':
            d['exit_edge_angle'] = np.sign(d['angle'])*angle
        d['angle'] = np.sign(d['angle'])*angle
        return [name, d]

    def createRunProcessInputFiles(self, files=None, write=True, run=True, preprocess=True, postprocess=True):
        if not isinstance(files, (list, tuple)):
            files = self.fileSettings.keys()
        for f in files:
            if 'code' in self.fileSettings[f]:
                code = self.fileSettings[f]['code']
                if code.upper() == 'ASTRA':
                    filename = self.subdirectory+'/'+f+'.in'
                    if write:
                        saveFile(filename, lines=self.astra.createASTRAFileText(f))
                    if preprocess:
                        self.astra.preProcesssASTRA()
                    if run:
                        self.astra.runASTRA(filename)
                    if postprocess:
                        self.astra.postProcesssASTRA()
                elif code.upper() == 'CSRTRACK':
                    filename = self.subdirectory+'/'+f+'.in'
                    if write:
                        saveFile(filename, lines=self.CSRTrack.createCSRTrackFileText(f))
                    if preprocess:
                        self.CSRTrack.preProcesssCSRTrack()
                    if run:
                        self.CSRTrack.runCSRTrack(filename)
                    if postprocess:
                        self.CSRTrack.convertCSRTrackOutput()
                elif code.upper() == 'ELEGANT':
                    if write:
                        self.elegant.createElegantFile(f)
                    if preprocess:
                        self.elegant.preProcesssElegant()
                    if run:
                        self.elegant.runElegant(f)
                    if postprocess:
                        self.elegant.postProcesssElegant()
                    # if preprocess:
                    #     self.CSRTrack.preProcesssCSRTrack()
                    # if run:
                    #     self.CSRTrack.runCSRTrack(filename)
                    # if postprocess:
                    #     self.CSRTrack.convertCSRTrackOutput()
                else:
                    print 'Code Not Recognised - ', code
                    raise NameError

    def createInputFiles(self):
        for f in self.fileSettings.keys():
            filename = self.subdirectory+'/'+f+'.in'
            if 'code' in self.fileSettings[f]:
                code = self.fileSettings[f]['code']
                if code.upper() == 'ASTRA':
                    saveFile(filename, lines=self.astra.createASTRAFileText(f))
                if code.upper() == 'CSRTRACK':
                    saveFile(filename, lines=self.CSRTrack.createCSRTrackFileText(f))
            else:
                saveFile(filename, lines=self.astra.createASTRAFileText(f))

    def postProcessInputFiles(self):
        for f in self.fileSettings.keys():
            if 'code' in self.fileSettings[f]:
                code = self.fileSettings[f]['code']
                if code.upper() == 'ASTRA':
                    try:
                        self.astra.createASTRAFileText(f)
                        self.astra.postProcesssASTRA()
                    except:
                        pass
                if code.upper() == 'CSRTRACK':
                    self.CSRTrack.createCSRTrackFileText(f)
                    self.CSRTrack.postProcesssCSRTrack()

    def runInputFiles(self, files=None):
        if not isinstance(files, (list, tuple)):
            files = self.fileSettings.keys()
        for f in files:
            if f in self.fileSettings.keys():
                filename = f+'.in'
                # print 'Running file: ', f
                if 'code' in self.fileSettings[f]:
                    code = self.fileSettings[f]['code']
                    if code.upper() == 'ASTRA':
                        self.astra.runASTRA(filename)
                    if code.upper() == 'CSRTRACK':
                        self.CSRTrack.runCSRTrack(filename)
                        self.CSRTrack.convertCSRTrackOutput(f)
            else:
                print 'File does not exist! - ', f

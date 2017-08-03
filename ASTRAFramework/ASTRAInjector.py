import yaml, collections, subprocess, os
import numpy

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))

yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

class ASTRAInjector(object):

    def __init__(self, subdir='test'):
        super(ASTRAInjector, self).__init__()
        self.lineIterator = 0
        self.astraCommand = ['astra']
        self.basedirectory = os.getcwd()
        self.subdir = subdir
        self.subdirectory = self.basedirectory+'/'+subdir
        if not os.path.exists(self.subdirectory):
            os.makedirs(self.subdirectory)

    def loadSettings(self, filename='short_240.settings'):
        self.settings = {}
        stream = file(filename, 'r')
        settings = yaml.load(stream)
        self.globalSettings = settings['global']
        self.fileSettings = settings['files']
        stream.close()

    def readFile(self, fname=None):
        with open(fname) as f:
            content = f.readlines()
        return content

    def lineReplaceFunction(self, line, findString, replaceString, i=None):
        if findString in line:
            self.lineIterator += 1
            if not i == None:
                return line.replace('$'+findString+'$', str(replaceString[i]))
            else:
                return line.replace('$'+findString+'$', str(replaceString))
        else:
            return line

    def replaceString(self, lines=[], findString=None, replaceString=None):
        if isinstance(replaceString,list):
            self.lineIterator = 0
            return [self.lineReplaceFunction(line, findString, replaceString, self.lineIterator) for line in lines]
        else:
            return [self.lineReplaceFunction(line, findString, replaceString) for line in lines]

    def saveFile(self, lines=[], filename='runastratemp.in'):
        stream = file(filename, 'w')
        for line in lines:
            stream.write(line)
        stream.close()

    def applySettings(self):
        for f, s in self.fileSettings.iteritems():
            newfilename = f
            if not newfilename[-3:-1] == '.in':
                newfilename = newfilename+'.in'
            lines = self.readFile(f)
            os.chdir(self.subdirectory)
            for var, val in s.iteritems():
                lines = self.replaceString(lines, var, val)
            for var, val in self.globalSettings.iteritems():
                lines = self.replaceString(lines, var, val)
            self.saveFile(lines, newfilename)
            self.runASTRA(newfilename)
            os.chdir(self.basedirectory)

    def runASTRA(self, filename=''):
        command = self.astraCommand + [filename]
        subprocess.call(command)

    def defineASTRACommand(self,command=['astra']):
        self.astraCommand = command

    def setInitialDistribution(self, filename='../1k-250pC-76fsrms-1mm_TE09fixN12.ini'):
        self.globalSettings['initial_distribution'] = filename

    def createInitialDistribution(self, npart=1000, charge=250, generatorCommand=None):
        astragen = ASTRAGenerator(self.subdir, charge, npart)
        if not generatorCommand == None:
            astragen.defineGeneratorCommand(generatorCommand)
        elif os.name == 'nt':
            astragen.defineGeneratorCommand(['../generator_7June2007'])
        else:
            astragen.defineGeneratorCommand(['/opt/ASTRA/generator'])
        inputfile = astragen.generateBeam()
        self.setInitialDistribution(inputfile)
        self.globalSettings['charge'] = charge/1000.0
        scgrid = getGrids(npart)
        for scvar in ['SC_2D_Nrad','SC_2D_Nlong','SC_3D_Nxf','SC_3D_Nyf','SC_3D_Nzf']:
            self.globalSettings[scvar] = scgrid.gridSizes

class ASTRAGenerator(object):

    def __init__(self, subdir='test', charge=250, npart=1000):
        super(ASTRAGenerator, self).__init__()
        self.lineIterator = 0
        self.generatorBaseFile = 'generator.in'
        self.charge = charge
        self.npart = npart
        self.generatorCommand = ['generator']
        self.basedirectory = os.getcwd()
        self.subdir = subdir
        self.subdirectory = self.basedirectory+'/'+self.subdir
        if not os.path.exists(self.subdirectory):
            os.makedirs(self.subdirectory)

    def generateBeam(self):
        self.createSettings()
        self.createGeneratorInput()
        return '../'+self.subdir+'/'+self.settings['filename']

    def readFile(self, fname=None):
        with open(fname) as f:
            content = f.readlines()
        return content

    def lineReplaceFunction(self, line, findString, replaceString):
        if findString in line:
            return line.replace('$'+findString+'$', str(replaceString))
        else:
            return line

    def replaceString(self, lines=[], findString=None, replaceString=None):
        return [self.lineReplaceFunction(line, findString, replaceString) for line in lines]

    def saveFile(self, lines=[], filename='generatortemp.in'):
        stream = file(filename, 'w')
        for line in lines:
            stream.write(line)
        stream.close()

    def particleSuffix(self):
        suffix = str(int(round(self.npart/1e9))) + 'G'
        if self.npart < 1e9:
            suffix = str(int(round(self.npart/1e6))) + 'M'
        if self.npart < 1e6:
            suffix = str(int(round(self.npart/1e3))) + 'k'
        if self.npart < 1e3:
            suffix = str(int(round(self.npart)))
        return suffix

    def createSettings(self):
        self.settings = {}
        self.settings['charge'] = self.charge/1000.0
        self.settings['number_particles'] = self.npart
        self.settings['filename'] = self.particleSuffix() + '-' + str(self.charge) + 'pC-76fsrms-1mm_TE09fixN12.ini'

    def createGeneratorInput(self):
        lines = self.readFile(self.generatorBaseFile)
        os.chdir(self.subdirectory)
        for var, val in self.settings.iteritems():
            lines = self.replaceString(lines, var, val)
        self.saveFile(lines, 'generator.in')
        self.runGenerator('generator.in')
        os.chdir(self.basedirectory)

    def runGenerator(self, filename=''):
        command = self.generatorCommand + [filename]
        comm = subprocess.Popen(command,stdin=subprocess.PIPE,stdout=subprocess.PIPE)
        for line in iter(comm.stdout.readline,''):
            if 'phase-space distribution saved to file' in line.rstrip():
                comm.stdin.write('\n')
        print 'here!'

    def defineGeneratorCommand(self,command=['generator']):
        self.generatorCommand = command

class getGrids(object):

    def __init__(self, npart=1000):
        self.powersof8 = numpy.asarray([ 2**(j) for j in range(1,20) ])
        self.n = npart
        self.gridSizes = self.getGridSizes(int(self.n))

    def getGridSizes(self):
        return self.gridSizes

    def getGridSizes(self, x):
        self.x = abs(x)
        self.cuberoot = int(round(self.x ** (1. / 3)))
        return max([1,self.find_nearest(self.powersof8, self.cuberoot)])

    def find_nearest(self, array, value):
        self.array = array
        self.value = value
        self.idx = (numpy.abs(self.array - self.value)).argmin()
        return self.array[self.idx]

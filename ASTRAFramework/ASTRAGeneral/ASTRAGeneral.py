import yaml, collections, subprocess, os
import numpy as np
from operator import add

_mapping_tag = yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG

def dict_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def dict_constructor(loader, node):
    return collections.OrderedDict(loader.construct_pairs(node))

yaml.add_representer(collections.OrderedDict, dict_representer)
yaml.add_constructor(_mapping_tag, dict_constructor)

class ASTRA(object):

    def __init__(self, subdir='test'):
        super(ASTRA, self).__init__()
        self.lineIterator = 0
        self.astraCommand = ['astra']
        self.basedirectory = os.getcwd()
        self.subdir = subdir
        self.subdirectory = self.basedirectory+'/'+subdir
        if not os.path.exists(self.subdirectory):
            os.makedirs(self.subdirectory)

    def loadSettings(self, filename='short_240.settings'):
        stream = file(filename, 'r')
        settings = yaml.load(stream)
        self.globalSettings = settings['global']
        self.fileSettings = settings['files']
        self.elements = settings['elements']
        self.groups = settings['groups']
        stream.close()

    def getElement(self, element=''):
        if element in self.elements:
            return self.elements[element]
        else:
            return []

    def getGroup(self, group=''):
        elements = []
        if group in self.groups:
            groupelements = self.groups[group]['elements']
            for e in groupelements:
                elements.append([e,self.getElement(e)])
        return elements

    def findSetting(self, setting, value, dictionary=None):
        settings = []
        if dictionary == None:
            elements = self.elements
        else:
            elements = dictionary
        for l, e in elements.items():
            if setting in e.keys() and value in e[setting]:
                settings.append([l,e])
        return settings

    def findSettingValue(self, setting, dictionary=None):
        return [k[setting] for k in self.findSetting(setting, '', dictionary)]

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

    def chop(self, expr, max=1e-9):
        if expr.shape[1] > 1:
            return [[i if abs(i) > max else 0 for i in e] for e in expr]
        else:
            return [i if abs(i) > max else 0 for i in expr]

    def getParameter(elem, param, default=0):
        return elem[param] if param in elem else default

    def xform(self, theta, tilt, length, x, r):
        theta = theta if abs(theta) > 1e-6 else 1e-6
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

    def elementPositions(self, elements, startpos=None):
        anglesum = [0]
        localXYZ = np.identity(3)
        if startpos == None:
            startpos = elements[0][1]['position']
            if len(startpos) == 1:
                startpos = [0,0,startpos]
        x1 = np.matrix(np.transpose([startpos]))
        x = [np.array(x1)]
        for name, d in elements:
            angle = self.getParameter(d,'angle',default=1e-9)/180*np.pi
            anglesum.append(anglesum[-1]+angle)
            x1, localXYZ = self.xform(angle, 0, self.getParameter(d,'length'), x1, localXYZ)
            x.append(x1)
        return zip(x, anglesum[1:], elements), localXYZ

    def chunks(self, l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def sortByPositionFunction(self, element):
        return float(element[1]['position'][2])

    def rotationMatrix(self, theta):
        c, s = np.cos(theta), np.sin(theta)
        return np.matrix([[c, 0, -s], [0, 1, 0], [s, 0, c]])

    def createDrifts(self, elements, startpos=None):
        positions = []
        elementno = 0
        for name, e in elements:
            pos = np.array(e['position'])
            positions.append(pos)
            length = np.array([0,0,e['length']])
            positions.append(pos+length)
        if not startpos == None:
            positions.prepend(startpos)
        else:
            positions = positions[1:]
            positions.append(positions[-1]+[0,0,0.1])
        driftdata = list(self.chunks(positions, 2))
        for d in driftdata:
            if len(d) > 1:
                elementno += 1
                length = d[1][2] - d[0][2]
                elements.append(['drift'+str(elementno),
                                {'length': length, 'type': 'drift',
                                 'position': list(d[0])
                                }])
        return sorted(elements, key=self.sortByPositionFunction)

    def getParameter(self, elem, param, default=0):
        return elem[param] if param in elem else default

    def setDipoleAngle(self, dipole, angle=0):
        name, d = dipole
        d['angle'] = np.sign(d['angle'])*angle
        return [name, d]

    def createASTRAChicane(self, group, dipoleangle=None, width=0.2, gap=0.02):
        dipoles = self.getGroup(group)
        if not dipoleangle == None:
            dipoles = [self.setDipoleAngle(d,dipoleangle) for d in dipoles]
        dipoles = self.createDrifts(dipoles)
        dipolepos, localXYZ = self.elementPositions(dipoles)
        dipolepos = list(self.chunks(dipolepos,2))
        corners = [0,0,0,0]
        dipoleno = 0
        for elems in dipolepos:
            dipoleno += 1
            p1, psi1, nameelem1 = elems[0]
            p2, psi2, nameelem2 = elems[1]
            name, d = nameelem1
            angle1 = self.getParameter(nameelem1[1],'angle')
            angle2 = self.getParameter(nameelem2[1],'angle')
            length = self.getParameter(d,'length')
            e1 = self.getParameter(d,'e1')
            e2 = self.getParameter(d,'e2')
            width = self.getParameter(d,'width',default=width)
            gap = self.getParameter(d,'gap',default=gap)
            rbend = 1 if d['type'] == 'rdipole' else 0
            rho = d['length']/angle1 if 'length' in d and angle1 > 1e-9 else 0
            theta = -1*psi1+e1-rbend*rho*angle1/2.0
            corners[0] = np.array(map(add,np.transpose(p1),np.dot([width*length,0,0], self.rotationMatrix(theta))))[0,0]
            corners[3] = np.array(map(add,np.transpose(p1),np.dot([-width*length,0,0], self.rotationMatrix(theta))))[0,0]
            theta = -1*psi2-e2-rbend*rho*angle1/2.0
            corners[1] = np.array(map(add,np.transpose(p2),np.dot([width*length,0,0], self.rotationMatrix(theta))))[0,0]
            corners[2] = np.array(map(add,np.transpose(p2),np.dot([-width*length,0,0], self.rotationMatrix(theta))))[0,0]
            dipolenostr = str(dipoleno)
            chicanetext = "D_Type("+dipolenostr+")='horizontal'\n"+\
            "D_Gap(1,"+dipolenostr+")="+str(gap)+",\n"+\
            "D_Gap(2,"+dipolenostr+")="+str(gap)+",\n"+\
            "D1("+dipolenostr+")=("+str(corners[0][0])+","+str(corners[0][2])+"),\n"+\
            "D2("+dipolenostr+")=("+str(corners[1][0])+","+str(corners[1][2])+"),\n"+\
            "D3("+dipolenostr+")=("+str(corners[2][0])+","+str(corners[2][2])+"),\n"+\
            "D4("+dipolenostr+")=("+str(corners[3][0])+","+str(corners[3][2])+"),\n"+\
            "D_radius("+dipolenostr+")="+str(rho)+"\n"
        return chicanetext

    def createASTRAQuad(self, quadname, n=1):
        quad        = self.getElement(quadname)
        k1          = str(self.getParameter(quad,'k1'))
        length      = str(self.getParameter(quad,'length'))
        x,y,s       =     self.getParameter(quad,'position')
        bore        = str(self.getParameter(quad,'bore_size', default=0.01))
        smooth      = str(self.getParameter(quad,'smooth', default=3))

        quadtext = 'Q_K('+str(n)+')='+k1+', Q_length('+str(n)+')='+length+',\n'+\
        'Q_pos('+str(n)+')='+str(s)+', Q_smooth('+str(n)+')='+smooth+', Q_bore('+str(n)+')='+bore+'\n'
        return quadtext

    def createASTRASolenoid(self, solname, n=1):
        sol         = self.getElement(solname)
        definition  = str(self.getParameter(sol,'field_definition'))
        length      = str(self.getParameter(sol,'length'))
        x,y,s       =     self.getParameter(sol,'position')
        amplitude   = str(self.getParameter(sol,'field_amplitude'))
        smooth      = str(self.getParameter(sol,'smooth', default=10))

        soltext = 'FILE_BFieLD('+str(n)+')='+definition+', MaxB('+str(n)+')='+amplitude+',\n'+\
        'S_pos('+str(n)+')='+str(s)+', S_xoff('+str(n)+')='+str(x)+', S_yoff('+str(n)+')='+str(y)+', S_smooth('+str(n)+')='+smooth+'\n'
        return soltext

    def createASTRACavity(self, cavname, n=1):
        cav         = self.getElement(cavname)
        definition  = str(self.getParameter(cav,'field_definition'))
        length      = str(self.getParameter(cav,'length'))
        x,y,s       =     self.getParameter(cav,'position')
        amplitude   = str(float(self.getParameter(cav,'field_amplitude'))/1e6)
        frequency   = str(float(self.getParameter(cav,'frequency'))/1e6)
        phase       = str(self.getParameter(cav,'phase'))
        cells       = str(self.getParameter(cav,'number_of_cells', default=1))
        smooth      = str(self.getParameter(cav,'smooth', default=10))

        cavtext = 'FILE_EFieLD('+str(n)+')='+definition+', Nue('+str(n)+')='+str(frequency)+'\n'+\
        'MaxE('+str(n)+')='+amplitude+', Phi('+str(n)+')='+phase+', C_numb('+str(n)+')='+cells+'\n'+\
        'C_pos('+str(n)+')='+str(s)+', C_xoff('+str(n)+')='+str(x)+', C_yoff('+str(n)+')='+str(y)+', C_smooth('+str(n)+')='+smooth+'\n'
        return cavtext

    def createASTRAScreen(self, screenname, n=1):
        screen         = self.getElement(screenname)
        x,y,s          =     self.getParameter(screen,'position')

        screentext = 'Screen('+str(n)+')='+str(s)+'\n'
        return screentext

    def formatOptionalString(self, parameter, string):
        return ' '+string+'='+parameter+'\n' if parameter != 'None' else ''

    def createOptionalString(self, set, string, inputstring=None):
        val = str(self.getParameter(set,string,default=None))
        if inputstring is None:
            return self.formatOptionalString(val,string)
        else:
            inputstring += self.formatOptionalString(val,string)

    def createASTRANewRunBlock(self, settings=None, input=None, charge=None):
        if settings is None:
            settings = self.fileSettings['test.in.111']['settings']
        if input is None:
            input = self.fileSettings['test.in.111']['input']
        if charge == None:
            charge = self.fileSettings['test.in.111']['charge']
        title           = str(self.getParameter(settings,'title',default='trial'))
        runno           = str(self.getParameter(settings,'run_no',default=1))
        loop            = str(self.getParameter(settings,'Loop',default=False))
        lprompt         = str(self.getParameter(settings,'Lprompt',default=False))
        distribution    = str(self.getParameter(input,'particle_definition',default=''))
        Qbunch          = str(float(self.getParameter(charge,'total_charge',default=250))/1000.0)
        zstart          = str(self.getParameter(settings,'start_position',default=0))
        zstop           = str(self.getParameter(settings,'end_position',default=0))
        accuracy        = str(self.getParameter(settings,'accuracy',default=4))
        highres = True if accuracy > 4 else False
        nred            = str(self.getParameter(charge,'N_red',default=None))
        lmag            = str(self.getParameter(charge,'Lmagnetized',default=None))
        emits           = str(self.getParameter(charge,'EmitS',default=None))
        tremits           = str(self.getParameter(charge,'TR_emitS',default=None))
        phaseS           = str(self.getParameter(charge,'PhaseS',default=None))
        trackS           = str(self.getParameter(charge,'TrackS',default=None))
        refS           = str(self.getParameter(charge,'RefS',default=None))
        tcheckS           = str(self.getParameter(charge,'TcheckS',default=None))
        cathodeS           = str(self.getParameter(charge,'CathodeS',default=None))
        trackall         = str(self.getParameter(charge,'Track_All',default=None))
        phasescan           = str(self.getParameter(charge,'Phase_Scan',default=None))
        autophase           = str(self.getParameter(charge,'Auto_Phase',default=None))
        checkrefpart           = str(self.getParameter(charge,'Check_Ref_Part',default=None))
        zphase           = str(self.getParameter(charge,'Zphase',default=None))
        zemit           = str(self.getParameter(charge,'Zemit',default=None))
        hmax           = str(self.getParameter(charge,'H_max',default=None))
        hmin           = str(self.getParameter(charge,'H_min',default=None))

        optionalvars = ['N_red','Lmagnetized','EmitS','TR_emitS','PhaseS','TrackS','RefS','TcheckS','CathodeS','Track_All','Phase_Scan','Auto_Phase','Check_Ref_Part', \
        'Zphase','Zemit','H_max','H_min']

        newruntext = '&NEWRUN\n' +\
        ' Loop='+str(loop)+'\n' + \
        ' Lprompt='+str(lprompt)+'\n' + \
        ' Head='+str(title)+'\n' + \
        ' Run='+str(runno)+'\n' + \
        ' Distribution='+str(distribution)+'\n' + \
        ' high_res='+str(highres)+'\n' + \
        ' ZStart='+str(zstart)+'\n' + \
        ' ZStop='+str(zstop)+'\n' + \
        ' Qbunch='+str(Qbunch)+'\n'# + \
        for var in optionalvars:
            self.createOptionalString(settings, var, inputstring=newruntext)
        newruntext += '/\n'

        return newruntext

    def createASTRAChargeBlock(self, charge=None):
        if charge == None:
            charge = self.fileSettings['test.in.111']['charge']
        loop        = str(self.getParameter(charge,'Loop',default=False))
        totalQ      = str(self.getParameter(charge,'total_charge',default=250))
        cathode     = str(self.getParameter(charge,'cathode',default=False))
        mode        = str(self.getParameter(charge,'space_charge_mode',default='2D'))
        lspch       = False if mode == False else True
        lspch2d     = True if lspch and mode != '3D' else False
        lspch3d     = True if lspch and not lspch2d else False
        if lspch2d:
            nrad    = str(self.getParameter(charge,'SC_2D_Nrad',default=6))
            nlong   = str(self.getParameter(charge,'SC_2D_Nlong',default=6))
        else:
            nxf     = str(self.getParameter(charge,'SC_3D_Nxf',default=6))
            nyf     = str(self.getParameter(charge,'SC_3D_Nyf',default=6))
            nzf     = str(self.getParameter(charge,'SC_3D_Nzf',default=6))
        maxscale    = str(self.getParameter(charge,'Max_scale',default=0.1))
        maxcount    = str(self.getParameter(charge,'Max_count',default=100))
        cellvar     = str(self.getParameter(charge,'Cell_var',default=None))
        mingrid     = str(self.getParameter(charge,'min_grid',default=None))
        smoothx     = str(self.getParameter(charge,'Smooth_x',default=None))
        smoothy     = str(self.getParameter(charge,'Smooth_y',default=None))
        smoothz     = str(self.getParameter(charge,'Smooth_z',default=None))

        chargetext = '&CHARGE\n' +\
        ' Loop='+str(loop)+'\n' + \
        ' LSPCH='+str(lspch)+'\n' + \
        ' LSPCH3D='+str(lspch3d)+'\n'
        if lspch and lspch2d:
            chargetext += ' Nrad='+nrad+', Nlong_in='+nlong+'\n'
        elif lspch and lspch3d:
            chargetext += ' Nxf='+nxf+', Nyf='+nyf+'Nzf='+nzf+'\n'
        chargetext += ' Lmirror='+cathode+'\n'
        chargetext += ' Max_scale='+maxscale+'\n'
        chargetext += ' Max_count='+maxcount+'\n'
        chargetext += self.formatOptionalString(cellvar,'Cell_var')
        chargetext += self.formatOptionalString(mingrid,'min_grid')
        chargetext += self.formatOptionalString(smoothx,'Smooth_x')
        chargetext += self.formatOptionalString(smoothy,'Smooth_y')
        chargetext += self.formatOptionalString(smoothz,'Smooth_z')
        chargetext += '/\n'

        return chargetext

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
        self.powersof8 = np.asarray([ 2**(j) for j in range(1,20) ])
        self.n = npart
        self.gridSizes = self.calculateGridSizes(int(self.n))

    def getGridSizes(self):
        return self.gridSizes

    def calculateGridSizes(self, x):
        self.x = abs(x)
        self.cuberoot = int(round(self.x ** (1. / 3)))
        return max([1,self.find_nearest(self.powersof8, self.cuberoot)])

    def find_nearest(self, array, value):
        self.array = array
        self.value = value
        self.idx = (np.abs(self.array - self.value)).argmin()
        return self.array[self.idx]

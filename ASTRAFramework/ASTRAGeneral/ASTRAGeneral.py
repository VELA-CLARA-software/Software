import yaml, collections, subprocess, os
import numpy as np
from operator import add
from ASTRAHelperFunctions import *
import ASTRAGenerator as GenPart
from ASTRARules import *
from getGrids import *

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
        """Load Lattice Settings from file"""
        stream = file(filename, 'r')
        settings = yaml.load(stream)
        self.globalSettings = settings['global']
        self.fileSettings = settings['files']
        self.elements = settings['elements']
        self.groups = settings['groups']
        stream.close()

    def getFileSettings(self, file, block):
        """Return the correct settings 'block' from 'file' dict if exists else return empty dict"""
        if file in self.fileSettings and block in self.fileSettings[file]:
            return self.fileSettings[file][block]
        else:
            return {}

    def getElement(self, element=''):
        """return 'element' from the main elements dict"""
        if element in self.elements:
            return self.elements[element]
        else:
            return []


    def getElementsBetweenS(self, elementtype, output={}, zstart=None, zstop=None):
        zstart          =     zstart if zstart is not None else getParameter(output,'zstart',default=0)
        zstop           =     zstop if zstop is not None else getParameter(output,'zstop',default=0)

        elements = findSetting('type',elementtype,dictionary=self.elements)
        elements = [s[0] for s in elements if s[1]['position_start'][2] >= zstart and s[1]['position_start'][2] <= zstop]

        return elements

    def getGroup(self, group=''):
        """return all elements in a group from the main elements dict"""
        elements = []
        if group in self.groups:
            groupelements = self.groups[group]['elements']
            for e in groupelements:
                elements.append([e,self.getElement(e)])
        return elements

    def runASTRA(self, filename=''):
        """Run the ASTRA program with input 'filename'"""
        command = self.astraCommand + [filename]
        subprocess.call(command)

    def defineASTRACommand(self,command=['astra']):
        """Modify the defined ASTRA command variable"""
        self.astraCommand = command

    def setInitialDistribution(self, filename='../1k-250pC-76fsrms-1mm_TE09fixN12.ini'):
        """Modify the 'initial_distribution' global setting"""
        self.globalSettings['initial_distribution'] = filename

    def createInitialDistribution(self, npart=1000, charge=250, generatorCommand=None):
        """Create an initiail dostribution of 'npart' particles of 'charge' pC"""
        astragen = GenPart.ASTRAGenerator(self.subdir, charge, npart)
        if not generatorCommand == None:
            astragen.defineGeneratorCommand(generatorCommand)
        elif os.name == 'nt':
            astragen.defineGeneratorCommand(['../generator_7June2007'])
        else:
            astragen.defineGeneratorCommand(['/opt/ASTRA/generator'])
        inputfile = astragen.generateBeam()
        self.setInitialDistribution(inputfile)
        self.globalSettings['total_charge'] = charge/1000.0
        scgrid = getGrids(npart)
        for scvar in ['SC_2D_Nrad','SC_2D_Nlong','SC_3D_Nxf','SC_3D_Nyf','SC_3D_Nzf']:
            self.globalSettings[scvar] = scgrid.gridSizes

    def xform(self, theta, tilt, length, x, r):
        """Calculate the change on local coordinates through an element"""
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
        """Calculate element positions for the given 'elements'"""
        anglesum = [0]
        localXYZ = np.identity(3)
        if startpos == None:
            startpos = elements[0][1]['position_start']
            if len(startpos) == 1:
                startpos = [0,0,startpos]
        x1 = np.matrix(np.transpose([startpos]))
        x = [np.array(x1)]
        for name, d in elements:
            angle = getParameter(d,'angle',default=1e-9)/180*np.pi
            anglesum.append(anglesum[-1]+angle)
            x1, localXYZ = self.xform(angle, 0, getParameter(d,'length'), x1, localXYZ)
            x.append(x1)
        return zip(x, anglesum[1:], elements), localXYZ

    def createDrifts(self, elements, startpos=None):
        """Insert drifts into a sequence of 'elements'"""
        positions = []
        elementno = 0
        for name, e in elements:
            pos = np.array(e['position_start'])
            positions.append(pos)
            length = np.array([0,0,e['length']])
            positions.append(pos+length)
        if not startpos == None:
            positions.prepend(startpos)
        else:
            positions = positions[1:]
            positions.append(positions[-1]+[0,0,0.1])
        driftdata = list(chunks(positions, 2))
        for d in driftdata:
            if len(d) > 1:
                elementno += 1
                length = d[1][2] - d[0][2]
                elements.append(['drift'+str(elementno),
                                {'length': length, 'type': 'drift',
                                 'position_start': list(d[0])
                                }])
        return sorted(elements, key=sortByPositionFunction)

    def setDipoleAngle(self, dipole, angle=0):
        """Set the dipole angle for a given 'dipole'"""
        name, d = dipole
        d['angle'] = np.sign(d['angle'])*angle
        return [name, d]

    def createASTRAChicane(self, group, dipoleangle=None, width=0.2, gap=0.02):
        """Create a 4 dipole chicane in ASTRA with the correct edge points"""
        chicanetext = ''
        dipoles = self.getGroup(group)
        if not dipoleangle is None:
            dipoles = [self.setDipoleAngle(d,dipoleangle) for d in dipoles]
        dipoles = self.createDrifts(dipoles)
        dipolepos, localXYZ = self.elementPositions(dipoles)
        dipolepos = list(chunks(dipolepos,2))
        corners = [0,0,0,0]
        dipoleno = 0
        for elems in dipolepos:
            dipoleno += 1
            p1, psi1, nameelem1 = elems[0]
            p2, psi2, nameelem2 = elems[1]
            name, d = nameelem1
            angle1 = getParameter(nameelem1[1],'angle')
            angle2 = getParameter(nameelem2[1],'angle')
            length = getParameter(d,'length')
            e1 = getParameter(d,'e1')
            e2 = getParameter(d,'e2')
            width = getParameter(d,'width',default=width)
            gap = getParameter(d,'gap',default=gap)
            rbend = 1 if d['type'] == 'rdipole' else 0
            rho = d['length']/angle1 if 'length' in d and angle1 > 1e-9 else 0
            theta = -1*psi1+e1-rbend*rho*angle1/2.0
            corners[0] = np.array(map(add,np.transpose(p1),np.dot([width*length,0,0], rotationMatrix(theta))))[0,0]
            corners[3] = np.array(map(add,np.transpose(p1),np.dot([-width*length,0,0], rotationMatrix(theta))))[0,0]
            theta = -1*psi2-e2-rbend*rho*angle1/2.0
            corners[1] = np.array(map(add,np.transpose(p2),np.dot([width*length,0,0], rotationMatrix(theta))))[0,0]
            corners[2] = np.array(map(add,np.transpose(p2),np.dot([-width*length,0,0], rotationMatrix(theta))))[0,0]
            dipolenostr = str(dipoleno)
            chicanetext += "D_Type("+dipolenostr+")='horizontal'\n"+\
            "D_Gap(1,"+dipolenostr+")="+str(gap)+",\n"+\
            "D_Gap(2,"+dipolenostr+")="+str(gap)+",\n"+\
            "D1("+dipolenostr+")=("+str(corners[0][0])+","+str(corners[0][2])+"),\n"+\
            "D2("+dipolenostr+")=("+str(corners[1][0])+","+str(corners[1][2])+"),\n"+\
            "D3("+dipolenostr+")=("+str(corners[2][0])+","+str(corners[2][2])+"),\n"+\
            "D4("+dipolenostr+")=("+str(corners[3][0])+","+str(corners[3][2])+"),\n"+\
            "D_radius("+dipolenostr+")="+str(rho)+"\n"
        return chicanetext

    def createASTRAQuad(self, quadname, n=1):
        """Create an ASTRA quadrupole string"""
        quad        = self.getElement(quadname)
        k1          = str(getParameter(quad,'k1'))
        length      = str(getParameter(quad,'length'))
        x,y,s       =     getParameter(quad,'position_start')
        bore        = str(getParameter(quad,'bore_size', default=0.01))
        smooth      = str(getParameter(quad,'smooth', default=3))

        quadtext = 'Q_K('+str(n)+')='+k1+', Q_length('+str(n)+')='+length+',\n'+\
        'Q_pos('+str(n)+')='+str(s)+', Q_smooth('+str(n)+')='+smooth+', Q_bore('+str(n)+')='+bore+'\n'
        return quadtext

    def createASTRASolenoid(self, solname, n=1):
        """Create an ASTRA solenoid string"""
        sol         = self.getElement(solname)
        definition  = str(getParameter(sol,'field_definition'))
        length      = str(getParameter(sol,'length'))
        x,y,s       =     getParameter(sol,'position_start')
        amplitude   = str(getParameter(sol,'field_amplitude'))
        smooth      = str(getParameter(sol,'smooth', default=10))

        soltext = 'FILE_BFieLD('+str(n)+')=\''+definition+'\', MaxB('+str(n)+')='+amplitude+',\n'+\
        'S_pos('+str(n)+')='+str(s)+', S_xoff('+str(n)+')='+str(x)+', S_yoff('+str(n)+')='+str(y)+', S_smooth('+str(n)+')='+smooth+'\n'
        for var in ASTRARules['SOLENOID']:
            soltext += createOptionalString(sol, var, n)
        return soltext

    def createASTRACavity(self, cavname, n=1):
        """Create an ASTRA cavity string"""
        cav         = self.getElement(cavname)
        definition  = str(getParameter(cav,'field_definition'))
        length      =     getParameter(cav,'length')
        x,y,s       =     getParameter(cav,'position_start')
        amplitude   = str(float(getParameter(cav,'field_amplitude'))/1e6)
        frequency   = str(float(getParameter(cav,'frequency'))/1e6)
        phase       = str(getParameter(cav,'phase'))
        cells       =     getParameter(cav,'number_of_cells')
        celllength  =     getParameter(cav,'cell_length')
        if cells is 0 and celllength > 0:
                cells = round((length-celllength)/celllength)
        smooth      = str(getParameter(cav,'smooth', default=10))

        cavtext = 'FILE_EFieLD('+str(n)+')=\''+definition+'\', Nue('+str(n)+')='+str(frequency)+'\n'+\
        'MaxE('+str(n)+')='+amplitude+', Phi('+str(n)+')='+phase+', \n'+\
        'C_pos('+str(n)+')='+str(s)+', C_xoff('+str(n)+')='+str(x)+', C_yoff('+str(n)+')='+str(y)+', C_smooth('+str(n)+')='+smooth
        if cells > 0:
            cavtext += ', C_numb('+str(n)+')='+str(cells)+'\n'
        cavtext += '\n'
        for var in ASTRARules['CAVITY']:
            cavtext += createOptionalString(cav, var, n)
        return cavtext

    def createASTRAScreen(self, screenname, n=1):
        """Create an ASTRA screen string"""
        screen         = self.getElement(screenname)
        x,y,s          =     getParameter(screen,'position_start')

        screentext = 'Screen('+str(n)+')='+str(s)+'\n'
        return screentext

    def createASTRANewRunBlock(self, settings={}, input={}, charge={}):
        """Create an ASTRA NEWRUN Block string"""
        title           = str(getParameter(settings,'title',default='trial'))
        runno           = str(getParameter(settings,'run_no',default=1))
        loop            = str(getParameter(settings,'Loop',default=False))
        lprompt         = str(getParameter(settings,'Lprompt',default=False))
        distribution    = str(getParameter(input,'particle_definition',default=''))
        if distribution == 'initial_distribution':
            distribution = self.globalSettings['initial_distribution']
        else:
            distribution = self.subdir+'/'+distribution
        print 'qbunch = ', getParameter([self.globalSettings,settings],'total_charge',default=250)
        Qbunch          = str(getParameter([self.globalSettings,settings],'total_charge',default=250))
        zstart          =     getParameter(settings,'zstart',default=0)
        zstop           =     getParameter(settings,'zstop',default=0)
        accuracy        = str(getParameter([self.globalSettings,settings],'accuracy',default=4))
        highres = True if accuracy > 4 else False

        newruntext = '&NEWRUN\n' +\
        ' Loop='+str(loop)+'\n' + \
        ' Lprompt='+str(lprompt)+'\n' + \
        ' Head=\''+str(title)+'\'\n' + \
        ' Run='+str(runno)+'\n' + \
        ' Distribution=\''+str(distribution)+'\'\n' + \
        ' high_res='+str(highres)+'\n' + \
        ' Qbunch='+str(Qbunch)+'\n'
        for var in ASTRARules['NEWRUN']:
            newruntext += createOptionalString([self.globalSettings['ASTRAsettings'],settings], var)
        newruntext += '/\n'

        return newruntext

    def createASTRAOutputBlock(self, output={}, settings={}):
        """Create an ASTRA OUTPUT Block string"""

        screens = self.getElementsBetweenS('screen', output=output)
        print 'screens = ', screens

        outputtext = '&OUTPUT\n'
        for var in ASTRARules['OUTPUT']:
            outputtext += createOptionalString([self.globalSettings['ASTRAsettings'],settings, output], var)
        for i,s in enumerate(screens):
            outputtext += ' '+self.createASTRAScreen(s,i+1)
        outputtext += '/\n'

        return outputtext

    def createASTRAChargeBlock(self, charge={}, settings={}):
        """Create an ASTRA CHARGE Block string"""
        loop        = str(getParameter(charge,'Loop',default=False))
        mode        = str(getParameter(charge,'space_charge_mode',default='2D'))
        lspch       = False if mode == False else True
        lspch2d     = True if lspch and mode != '3D' else False
        lspch3d     = True if lspch and not lspch2d else False
        if lspch2d:
            nrad    = str(getParameter([charge,self.globalSettings],'SC_2D_Nrad',default=6))
            nlong   = str(getParameter([charge,self.globalSettings],'SC_2D_Nlong',default=6))
        else:
            nxf     = str(getParameter([charge,self.globalSettings],'SC_3D_Nxf',default=6))
            nyf     = str(getParameter([charge,self.globalSettings],'SC_3D_Nyf',default=6))
            nzf     = str(getParameter([charge,self.globalSettings],'SC_3D_Nzf',default=6))

        chargetext = '&CHARGE\n' +\
        ' Loop='+str(loop)+'\n' + \
        ' LSPCH='+str(lspch)+'\n' + \
        ' LSPCH3D='+str(lspch3d)+'\n'
        if lspch and lspch2d:
            chargetext += ' Nrad='+nrad+', Nlong_in='+nlong+'\n'
        elif lspch and lspch3d:
            chargetext += ' Nxf='+nxf+', Nyf='+nyf+', Nzf='+nzf+'\n'

        for var in ASTRARules['CHARGE']:
            chargetext += createOptionalString([self.globalSettings['ASTRAsettings'], settings, charge], var)
        chargetext += '/\n'

        return chargetext

    def createASTRAScanBlock(self, scan={}, settings={}):
        """Create an ASTRA SCAN Block string"""
        loop        = str(getParameter(scan,'Loop',default=False))
        lscan       = str(getParameter(scan,'LScan',default=False))

        scantext = '&SCAN\n' +\
        ' Loop='+str(loop)+'\n' +\
        ' LScan='+str(lscan)+'\n'
        for var in ASTRARules['SCAN']:
            scantext += createOptionalString([self.globalSettings['ASTRAsettings'], settings, scan], var)
        scantext += '/\n'

        return scantext

    def createASTRAApertureBlock(self, aperture={}, settings={}):
        """Create an ASTRA APERTURE Block string"""
        loop        = str(getParameter(aperture,'Loop',default=False))
        lapert      = str(getParameter(aperture,'LApert',default=False))

        aperturetext = '&APERTURE\n' +\
        ' Loop='+str(loop)+'\n' +\
        ' LApert='+str(lapert)+'\n'
        for var in ASTRARules['APERTURE']:
            aperturetext += createOptionalString([self.globalSettings['ASTRAsettings'], settings, aperture], var)
        aperturetext += '/\n'

        return aperturetext

    def createASTRACavityBlock(self, cavity={}, output={}):
        """Create an ASTRA APERTURE Block string"""
        loop        = str(getParameter(cavity,'Loop',default=False))
        lefield        = str(getParameter(cavity,'LEField',default=True))

        cavitytext = '&CAVITY\n' +\
        ' Loop='+str(loop)+'\n' +\
        ' LEField='+str(lefield)+'\n'

        cavities = self.getElementsBetweenS('cavity', output=output)

        for i,s in enumerate(cavities):
            cavitytext += ' '+self.createASTRACavity(s,i+1)
        cavitytext += '/\n'

        return cavitytext

    def createASTRASolenoidBlock(self, solenoid={}, output={}):
        """Create an ASTRA SOLENOID Block string"""
        loop        = str(getParameter(solenoid,'Loop',default=False))
        lbfield        = str(getParameter(solenoid,'LBField',default=True))


        solenoidtext = '&SOLENOID\n' +\
        ' Loop='+str(loop)+'\n' +\
        ' LBField='+str(lbfield)+'\n'

        solenoids = self.getElementsBetweenS('solenoid', output=output)

        for i,s in enumerate(solenoids):
            solenoidtext += ' '+self.createASTRASolenoid(s,i+1)
        solenoidtext += '/\n'

        return solenoidtext

    def createASTRAQuadrupoleBlock(self, quad={}, output={}):
        """Create an ASTRA QUADRUPOLE Block string"""
        loop        = str(getParameter(quad,'Loop',default=False))
        lquad        = str(getParameter(quad,'LQuad',default=True))

        quadrupoletext = '&QUADRUPOLE\n' +\
        ' Loop='+str(loop)+'\n' +\
        ' LQuad='+str(lquad)+'\n'

        quadrupoles = self.getElementsBetweenS('quadrupole', output=output)

        for i,s in enumerate(quadrupoles):
            quadrupoletext += ' '+self.createASTRAQuad(s,i+1)
        quadrupoletext += '/\n'

        return quadrupoletext

    def createASTRAFileText(self, file):
        settings = self.getFileSettings(file,'settings')
        input = self.getFileSettings(file,'input')
        output = self.getFileSettings(file,'output')
        charge = self.getFileSettings(file,'charge')
        scan = self.getFileSettings(file,'scan')
        aperture = self.getFileSettings(file,'aperture')
        cavity = self.getFileSettings(file,'cavity')
        solenoid = self.getFileSettings(file,'solenoid')
        quadrupole = self.getFileSettings(file,'quadrupole')

        astrafiletext = ''
        astrafiletext += self.createASTRANewRunBlock(settings, input, charge)
        astrafiletext += self.createASTRAOutputBlock(output, settings)
        astrafiletext += self.createASTRAChargeBlock(charge, settings)
        astrafiletext += self.createASTRAScanBlock(scan, settings)
        astrafiletext += self.createASTRAApertureBlock(aperture, settings)
        astrafiletext += self.createASTRACavityBlock(cavity, output)
        astrafiletext += self.createASTRASolenoidBlock(solenoid, output)
        astrafiletext += self.createASTRAQuadrupoleBlock(quadrupole, output)
        return astrafiletext

    def createASTRAFiles(self):
        for f in self.fileSettings.keys():
            filename = self.subdirectory+'/'+f+'.in'
            print filename
            saveFile(filename, lines=self.createASTRAFileText(f))
            self.runASTRA(filename)

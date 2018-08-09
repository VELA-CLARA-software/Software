import yaml, collections, subprocess, os, math, re, sys, copy
from shutil import copyfile
import numpy as np
import SimulationFramework.Modules.read_beam_file as rbf
from FrameworkHelperFunctions import *

class CSRTrack(object):

    def __init__(self, framework=None, directory='test'):
        super(CSRTrack, self).__init__()
        self.subdir = directory
        self.framework = framework
        self.beam = rbf.beam()
        self.CSRTrackCommand = ['csrtrack']

    def runCSRTrack(self, filename=''):
        """Run the CSRTrack program with input 'filename'"""
        print 'self.subdir = ', [os.path.relpath(filename,self.subdir)]
        copyfile(filename, self.subdir+'/'+'csrtrk.in')
        command = self.CSRTrackCommand + ['csrtrk.in']
        print 'command = ', command
        with open(os.devnull, "w") as f:
            subprocess.call(command, stdout=f, cwd=self.subdir)

    def preProcesssCSRTrack(self):
        if self.zstart[0] is not None:
            self.convert_HDF5_beam_to_astra_beam(self.subdir, self.filename, self.zstart)

    def convert_HDF5_beam_to_astra_beam(self, subdir, filename, screen):
        if len(screen) > 2:
            name, pos, pos0 = screen
        else:
            name, pos = screen
            pos0 = pos
        HDF5filename = name + '.hdf5'
        astrabeamfilename = name + '.astra'
        self.beam.read_HDF5_beam_file(subdir + '/' + HDF5filename)
        self.beam.write_astra_beam_file(subdir + '/' + astrabeamfilename, normaliseZ=False)

    def convertCSRTrackOutput(self, f=None):
        if f is None:
            f = self.filename
        output = self.framework.getFileSettings(f,'output')
        distributionname    = '$output[\'end_element\']$'
        regex = re.compile('\$(.*)\$')
        s = re.search(regex, distributionname)
        if s:
            sub = self.framework.astra.formatASTRAStartElement(eval(s.group(1)))
            distributionname = re.sub(regex, sub, distributionname)
        outputdistribution = distributionname+'.astra'
        options = self.framework.getFileSettings(f,'CSRTrack_Options')
        monitor = self.framework.getSettingsBlock(options,'monitor')
        # print monitor
        inputdistribution    = str(getParameter(monitor,'name',default=''))
        regex = re.compile('\$(.*)\$')
        s = re.search(regex, inputdistribution)
        if s:
            sub = self.framework.astra.formatASTRAStartElement(eval(s.group(1)))
            inputdistribution = re.sub(regex, sub, inputdistribution)
        self.beam.convert_csrtrackfile_to_astrafile(self.subdir+'/'+inputdistribution, self.subdir+'/'+outputdistribution)
        self.convert_astra_beam_to_HDF5_beam(self.subdir, self.filename, distributionname)

    def convert_astra_beam_to_HDF5_beam(self, subdir, filename, name):
        astrabeamfilename = name+'.astra'
        self.beam.read_astra_beam_file(subdir + '/' + astrabeamfilename, normaliseZ=False)
        if self.global_offset is None or []:
            self.global_offset = [0,0,0]
        self.beam.rotate_beamXZ(-1*self.global_rotation, preOffset=[0,0,0], postOffset=-1*np.array(self.global_offset))
        HDF5filename = name + '.hdf5'
        self.beam.write_HDF5_beam_file(subdir + '/' + HDF5filename, centered=False, sourcefilename=astrabeamfilename, rotation=self.global_rotation)

    def defineCSRTrackCommand(self, command=['csrtrack']):
        """Modify the defined ASTRA command variable"""
        self.CSRTrackCommand = command

    def setInitialDistribution(self, filename='../1k-250pC-76fsrms-1mm_TE09fixN12.ini'):
        """Modify the 'initial_distribution' global setting"""
        self.framework.globalSettings['initial_distribution'] = filename

    def createCSRTrackChicane(self, group, dipoleangle=None, width=0.2, gap=0.02):
        """Create a 4 dipole chicane in CSRTrack with the correct edge points"""
        chicanetext = ''
        dipoles = self.framework.getGroup(group)
        if not dipoleangle is None:
            dipoleangle = float(dipoleangle)
            dipoles = [self.framework.setDipoleAngle(d, dipoleangle) for d in dipoles]
        dipoles = self.framework.createDrifts(dipoles, zerolengthdrifts=True)
        dipolepos, localXYZ = self.framework.elementPositions(dipoles)
        dipolepos = list(chunks(dipolepos,2))
        corners = [0,0,0,0]
        dipoleno = 0
        lastangle = 0
        for elems in dipolepos:
            dipoleno += 1
            p1, psi1, nameelem1 = elems[0]
            p2, psi2, nameelem2 = elems[1]
            name = nameelem1
            angle1 = self.framework.getElement(nameelem1,'angle')
            angle2 = self.framework.getElement(nameelem2,'angle')
            length = self.framework.getElement(name,'length')
            rbend = 1 if self.framework.getElement(name,'type') == 'rdipole' else 0
            e1 = self.framework.getElement(name,'entrance_edge_angle', default=0)
            e1 = e1 if rbend is 0 else e1 + angle1/2.0
            e2 = self.framework.getElement(name,'exit_edge_angle', default=0)
            e2 = e2 if rbend is 0 else e2 + angle2/2.0
            width = self.framework.getElement(name,'width',default=width)
            gap = self.framework.getElement(name,'gap',default=gap)
            rho = length/angle1 if abs(angle1) > 1e-9 else 0
            np.transpose(p1)
            chicanetext += """    dipole{
    position{rho="""+str(p1[2,0])+""", psi="""+str(chop(e1+psi1))+""", marker=d"""+str(dipoleno)+"""a}
    properties{r="""+str(rho)+"""}
    position{rho="""+str(p2[2,0])+""", psi="""+str(chop(e2-psi2))+""", marker=d"""+str(dipoleno)+"""b}
    }
    """
        return chicanetext

    def createCSRTrackParticlesBlock(self, particles={}, originaloutput={}):
        """Create an CSRTrack Particles Block string"""

        output = copy.deepcopy(originaloutput)

        distribution    = str(getParameter(particles,'array',default=''))
        regex = re.compile('\$(.*)\$')
        s = re.search(regex, distribution)
        if s:
            distribution = re.sub(regex, self.framework.astra.formatASTRAStartElement(eval(s.group(1))), distribution)

        zstart = getParameter(output,'zstart',default=None)
        if zstart is None:
            startelem = getParameter(output,'start_element',default=None)
            if startelem is None or startelem not in self.framework.elements:
                zstart = [0,0,0]
                self.zstart = [None, zstart, zstart]
            else:
                zstart = self.framework.elements[startelem]['position_start']
                originaloutput['zstart'] = zstart[2]
                self.zstart = [startelem, zstart, zstart]
        elif not isinstance(zstart, (list, tuple)):
            zstart = [0,0, zstart]
            self.zstart = [None, zstart, zstart]
        else:
            self.zstart = [None, zstart, zstart]

        zstart = self.framework.astra.rotateAndOffset(zstart, self.global_offset, self.global_rotation)
        self.zstart[1] = zstart
        output['zstart'] = zstart[2]


        del particles['array']
        particlestext = ''

        particlestext += 'particles{\n'
        for param, val in particles.iteritems():
            particlestext+= str(param)+' = '+str(val)+'\n'
        particlestext+= str('array')+' = '+str(distribution)+'\n'
        particlestext+= '}\n'

        return particlestext

    def createCSRTrackForcesBlock(self, forces={}):
        """Create an CSRTrack forces Block string"""

        forcestext = ''

        forcestext += 'forces{\n'

        for param, val in forces.iteritems():
            forcestext+= str(param)+' = '+str(val)+'\n'

        forcestext+= '}\n'

        return forcestext

    def createCSRTrackTrackStepBlock(self, trackstep={}):
        """Create an CSRTrack trackstep Block string"""

        tracksteptext = ''

        tracksteptext += 'track_step{\n'

        for param, val in trackstep.iteritems():
            tracksteptext+= str(param)+' = '+str(val)+'\n'

        tracksteptext+= '}\n'

        return tracksteptext

    def createCSRTrackTrackerBlock(self, tracker={}):
        """Create an CSRTrack tracker Block string"""

        trackertext = ''

        trackertext += 'tracker{\n'

        for param, val in tracker.iteritems():
            trackertext+= str(param)+' = '+str(val)+'\n'

        trackertext+= '}\n'

        return trackertext

    def createCSRTrackMonitorBlock(self, monitor={}, output={}):
        """Create an CSRTrack monitor Block string"""

        monitortext = ''

        monitortext += 'monitor{\n'

        distribution    = str(getParameter(monitor,'name',default=''))
        regex = re.compile('\$(.*)\$')
        s = re.search(regex, distribution)
        if s:
            sub = self.framework.astra.formatASTRAStartElement(eval(s.group(1)))
            distribution = re.sub(regex, sub, distribution)

        monitor = {i:monitor[i] for i in monitor if i!='name'}
        self.monitorName = distribution
        monitortext+= str('name')+' = '+str(distribution)+'\n'
        for param, val in monitor.iteritems():
            monitortext+= str(param)+' = '+str(val)+'\n'

        monitortext+= '}\n'

        return monitortext

    def createCSRTrackOnlineMonitorBlock(self, omon={}):
        """Create an CSRTrack OnlineMonitor Block string"""

        omontext = ''

        for name, params in omon.iteritems():

            omontext += 'online_monitor{\n'+'name = '+name+',\n'

            for param, val in params.iteritems():
                omontext+= str(param)+' = '+str(val)+'\n'
            omontext+= '}\n'

        return omontext

    def createCSRTrackChicaneBlock(self, groups, dipoles):
        """Create an CSRTrack DIPOLE Block string"""
        loop = False
        ldipole = False

        for g in groups:
            if g in self.framework.groups:
                # print 'group!'
                if self.framework.groups[g]['type'] == 'chicane':
                    if all([i for i in self.framework.groups[g] if i in dipoles]):
                        ldipole = True

        dipoletext = "io_path{logfile = log.txt}\n\n    lattice{\n"

        for g in groups:
            if g in self.framework.groups:
                # print 'group!'
                if self.framework.groups[g]['type'] == 'chicane':
                    if all([i for i in self.framework.groups[g] if i in dipoles]):
                        dipoletext += self.createCSRTrackChicane(g, **groups[g])

        dipoletext += "    }\n"

        return dipoletext

    def createCSRTrackFileText(self, file):
        self.filename = file
        options = self.framework.getFileSettings(file,'CSRTrack_Options')
        # input = self.framework.getFileSettings(file,'input')
        output = self.framework.getFileSettings(file,'output')

        self.global_offset = self.framework.getFileSettings(file,'global_offset', [0,0,0])
        self.global_offset = self.framework.expand_substitution(self.global_offset)

        self.starting_rotation = self.framework.getFileSettings(file,'starting_rotation', 0)
        self.starting_rotation = self.framework.expand_substitution(self.starting_rotation)

        dipoles = self.framework.getElementsBetweenS('dipole', output)
        self.global_rotation = -self.starting_rotation
        for d in dipoles:
            self.global_rotation -= self.framework.getElement(d,'angle')


        online_monitors = self.framework.getSettingsBlock(options,'online_monitors')
        particles = self.framework.getSettingsBlock(options,'particles')
        forces = self.framework.getSettingsBlock(options,'forces')
        trackstep = self.framework.getSettingsBlock(options,'track_step')
        tracker = self.framework.getSettingsBlock(options,'tracker')
        monitor = self.framework.getSettingsBlock(options,'monitor')

        groups = self.framework.getFileSettings(file,'groups')

        CSRTrackfiletext = ''
        CSRTrackfiletext += self.createCSRTrackChicaneBlock(groups, dipoles)
        CSRTrackfiletext += self.createCSRTrackOnlineMonitorBlock(online_monitors)
        CSRTrackfiletext += self.createCSRTrackParticlesBlock(particles, output)
        CSRTrackfiletext += self.createCSRTrackForcesBlock(forces)
        CSRTrackfiletext += self.createCSRTrackTrackStepBlock(trackstep)
        CSRTrackfiletext += self.createCSRTrackTrackerBlock(tracker)
        CSRTrackfiletext += self.createCSRTrackMonitorBlock(monitor, output)
        CSRTrackfiletext += 'exit\n'
        # print 'CSRTrackfiletext = ', CSRTrackfiletext
        return CSRTrackfiletext

    def createCSRTrackFiles(self):
        for f in self.fileSettings.keys():
            filename = self.subdirectory+'/'+f+'.in'
            # print filename
            saveFile(filename, lines=self.createCSRTrackFileText(f))

    def runCSRTrackFiles(self, files=None):
        if isinstance(files, (list, tuple)):
            for f in files:
                if f in self.fileSettings.keys():
                    filename = f+'.in'
                    # print 'Running file: ', f
                    self.runCSRTrack(filename)
                else:
                    print 'File does not exist! - ', f
        else:
            for f in self.fileSettings.keys():
                filename = f+'.in'
                # print 'Running file: ', f
                self.runCSRTrack(filename)

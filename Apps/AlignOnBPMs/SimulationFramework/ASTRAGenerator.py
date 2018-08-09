import subprocess, os
from FrameworkHelperFunctions import *

class ASTRAGenerator(object):

    def __init__(self, subdir='test', charge=250, npart=1000, overwrite=None, generatorFile='generator.in'):
        super(ASTRAGenerator, self).__init__()
        self.lineIterator = 0
        self.generatorBaseFile = generatorFile
        self.charge = charge
        self.npart = npart
        self.overwrite = overwrite
        self.generatorCommand = ['generator']
        self.basedirectory = os.getcwd()
        self.subdir = subdir
        self.subdirectory = self.basedirectory+'/'+self.subdir
        if not os.path.exists(self.subdirectory):
            os.makedirs(self.subdirectory)

    def generateBeam(self):
        self.createSettings()
        self.createGeneratorInput()
        return self.settings['filename']

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
        self.settings['filename'] = self.particleSuffix() + '-' + str(self.charge) + 'pC.ini'

    def createGeneratorInput(self):
        lines = self.readFile(self.generatorBaseFile)
        for var, val in self.settings.iteritems():
            lines = self.replaceString(lines, var, val)
        if self.overwrite:
            self.saveFile(lines, self.subdir+'/'+'generator.in')
            self.runGenerator('generator.in')

    def runGenerator(self, filename=''):
        command = self.generatorCommand + [filename]
        with open(os.devnull, "w") as f:
            subprocess.call(command, stdout=f, cwd=self.subdir)

    def defineGeneratorCommand(self,command=['generator']):
        self.generatorCommand = command

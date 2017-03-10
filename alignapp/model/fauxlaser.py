#This is bespkoe for Frank
# v1.0 (10.11.2016)
# To use this import is into you code that is connected to VM
# Import into the model section of your App
#
#import fauxlaser as fl
#
#laser = fl.fauxLaserController(66)
#
##now to change laser position (lets say in y) and have it effect BPM01 and YAG01
#
#laser.setYposition(-9)
##This will set the Y value on the Virtual cathode to be -9, and -594 (using the factor '66' which was set when initiating the controller) for BPM01 and YAG01

from epics import caget,caput
import numpy as np

class fauxLaserController():
    def __init__(self,C,bpm,mod):
            self.x=0
            self.y=0
            self.C = np.zeros((2,2))
            self.bpmc = bpm
            self.model = mod
            print 'Using Faux Laser Controller...', self.C[0, 0]

    def setXpositionf(self,x):# This needs to be rewritten with a proper controller to control the mirrors. Set between -10 and 10
        self.x=x*1.0
        print "I am FALSELY setting the laser x position"
        #BPM01
#        caput('VM-EBT-INJ-DIA-BPMC-02:X',[self.C*self.x])
#        caput('VM-EBT-INJ-DIA-BPMC-02:X',[123])
#        print "CAKE", self.C[0, 0]
#        self.bpmc.setX('BPM02',self.C[0, 0]*self.x + self.C[0, 1]*self.y)
#        self.bpmc.setY('BPM02',self.C[1, 0]*self.x + self.C[1, 1]*self.y)
        #YAG01
#        caput('VM-EBT-INJ-DIA-CAM-02:CAM:X',self.C*self.x)
        #Virtual cathode
#        caput('VM-EBT-INJ-DIA-CAM-01:CAM:X',self.x)

    def setYpositionf(self,y):# This needs to be rewritten with a proper controller to control the mirrors.Set between -10 and 10
        self.y=y*1.0
        print "I am FALSELY setting the laser y position"
        #BPM01
#        caput('VM-EBT-INJ-DIA-BPMC-02:Y',[self.C*self.y])
#        self.bpmc.setY('BPM02',self.C[0, 0]*self.y)
        #Yag01
#        caput('VM-EBT-INJ-DIA-CAM-02:CAM:Y',self.C*self.y)
        #Virtual cathode
#        caput('VM-EBT-INJ-DIA-CAM-01:CAM:Y',self.y)


    def setbeampos(self):
        print "I'm setting the beam position from the laser controller", self.C
        dumbx = self.C[0, 0]*self.x + self.C[0, 1]*self.y
        dumby = self.C[1, 0]*self.x + self.C[1, 1]*self.y
        print "the beam x, y", dumbx, dumby
#        self.bpmc.setX('BPM02',self.C[0, 0]*self.x + self.C[0, 1]*self.y)
#        self.bpmc.setY('BPM02',self.C[1, 0]*self.x + self.C[1, 1]*self.y)
        self.bpmc.setX('BPM02',dumbx)
        self.bpmc.setY('BPM02',dumby)
#        self.bpmc.setX('BPM02',678.9)
#        self.bpmc.setY('BPM02',798.9)

    def setbeampos2(self):
        print "I'm setting the beam position from the laser controller 2", self.C
# run the astra stuff
        self.model.vm(001, 10, 1320, 0.076, 0.25, 0.25, "F", 0.0, 1800, 1, 0.228, -0.14, 0.138, -0.230, self.x, self.y)
#        print "the beam x, y", dumbx, dumby
#        self.bpmc.setX('BPM02',self.C[0, 0]*self.x + self.C[0, 1]*self.y)
#        self.bpmc.setY('BPM02',self.C[1, 0]*self.x + self.C[1, 1]*self.y)
#        self.bpmc.setX('BPM02',dumbx)
#        self.bpmc.setY('BPM02',dumby)
#        self.bpmc.setX('BPM02',678.9)
#        self.bpmc.setY('BPM02',798.9)





    def setXposition(self,x):
        pass

    def setYposition(self,y):
        pass

        

    def getXposition(self):#
        return self.x

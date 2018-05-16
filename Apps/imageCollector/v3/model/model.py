import sys,os
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\root_v5.34.34\\bin\\'
#import VELA_CLARA_Camera_DAQ_Control as daq
import os
from epics import caget, caput
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
#import enum_ext

#import members_as_pyobjects_test
import VELA_CLARA_Camera_DAQ_Control as daq

import VELA_CLARA_Camera_IA_Control as ia



class Model():
    def __init__(self):
        self.comment = 'Hello World!!    and the Llamas in the Universe :)'
        self.cap = daq.CAPTURE_STATE
        self.wr = daq.WRITE_STATE
        self.initDAQ = daq.init()
        self.initIA = ia.init()
        self.initDAQ.setVerbose()
        self.initIA.setVerbose()
        self.camerasDAQ = self.initDAQ.physical_CLARA_Camera_DAQ_Controller()
        self.camerasIA = self.initIA.physical_CLARA_Camera_IA_Controller()
        self.selectedCameraDAQ = [self.camerasDAQ.getSelectedDAQRef()]
        self.selectedCameraIA = [self.camerasIA.getSelectedIARef()]
        print("Model Initialized")

    def setStepSize(self, stepSize):
        print(stepSize)
        self.camerasIA.setStepSize(stepSize)

    def setMask(self, x,y, xRad, yRad):
        print 'python setMask called'
        self.camerasIA.setMask(x,y,xRad,yRad)

    def useBkgrnd(self, use):
        print(use)
        self.camerasIA.useBackground(use)

    def useNPoint(self, use):
        print(use)
        self.camerasIA.useNPoint(use)

    def setBkgrnd(self, step):
        print("Setting a new background...")
        self.camerasIA.setBackground()

    def analyse(self):
        if self.selectedCameraIA[0].IA.analysisState== 0:
            self.camerasIA.startAnalysis()
        elif self.selectedCameraIA[0].IA.analysisState == 1:
            self.camerasIA.stopAnalysis()


    def acquire(self):
        if self.camerasDAQ.isNotAcquiring(self.selectedCameraDAQ[0].name):
            self.camerasDAQ.startAcquiring()
        elif self.camerasDAQ.isAcquiring(self.selectedCameraDAQ[0].name):
            self.camerasDAQ.stopAcquiring()

    def collectAndSave(self, numberOfImages):
        if self.camerasDAQ.isAcquiring(self.selectedCameraDAQ[0].name):
            self.camerasDAQ.collectAndSave(numberOfImages)
            #self.camerasDAQ.collectAndSaveJPG()
        elif self.selectedCameraDAQ[0].DAQ.captureState == self.cap.CAPTURING:
            self.camerasDAQ.killCollectAndSave()
           # self.camerasDAQ.killCollectAndSaveJPG()

    def feedback(self,use):
        if use is True:
            height = 2160#self.selectedCameraIA.IA.imageHeight
            width = 2560#self.selectedCameraIA.IA.imageWidth
            x = self.selectedCameraIA[0].IA.xPix
            y = self.selectedCameraIA[0].IA.yPix
            sX = self.selectedCameraIA[0].IA.xSigmaPix
            sY = self.selectedCameraIA[0].IA.ySigmaPix
            if x-5*sX > 0 and x+5*sX < width and y-5*sY > 0 and y+5*sY < height:
                #print(x-sX)
                #print(y-sY)
                self.setMask(int(x),int(y),int(5*sX),int(5*sY))
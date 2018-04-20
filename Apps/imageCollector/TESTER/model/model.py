import sys
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
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
        #self.Init.setVerbose()
        self.camerasDAQ = self.initDAQ.physical_CLARA_Camera_DAQ_Controller()
        self.camerasIA = self.initIA.physical_CLARA_Camera_IA_Controller()
        self.selectedCameraDAQ = self.camerasDAQ.getSelectedDAQRef()
        self.selectedCameraIA = self.camerasIA.getSelectedIARef()
        print("Model Initialized")

    def useBkgrnd(self, use):
        print(use)
      #  self.camerasIA.useBackground(use)

    def useNPoint(self, use):
        print(use)
     #   self.camerasIA.useNPoint(use)

    def setBkgrnd(self, step):
        print("Setting a new background...")
     #   self.camerasIA.setBackground()

    def analyse(self):
        if self.selectedCameraIA.IA.analysisState== 0:
            self.camerasIA.startAnalysis()
        elif self.selectedCameraIA.IA.analysisState == 1:
            self.camerasIA.stopAnalysis()


    def acquire(self):
        if self.camerasDAQ.isNotAcquiring(self.selectedCameraDAQ.name):
            self.camerasDAQ.startAcquiring()
        elif self.camerasDAQ.isAcquiring(self.selectedCameraDAQ.name):
            self.camerasDAQ.stopAcquiring()

    def collectAndSave(self, numberOfImages):
        if self.camerasDAQ.isAcquiring(self.selectedCameraDAQ.name):
            self.camerasDAQ.collectAndSave(numberOfImages)
            #self.camerasDAQ.collectAndSaveJPG()
        elif self.selectedCameraDAQ.DAQ.captureState == self.cap.CAPTURING:
            self.camerasDAQ.killCollectAndSave()
           # self.camerasDAQ.killCollectAndSaveJPG()

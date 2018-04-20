import sys
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage')

import os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
import VELA_CLARA_Camera_DAQ_Control as daq


class Model():
    def __init__(self):
        self.comment = 'Hello World!!    and the Llamas in the Universe :)'
        self.cap = daq.CAPTURE_STATE
        self.wr = daq.WRITE_STATE
        self.Init = daq.init()
        self.Init.setVerbose()
        self.cameras = self.Init.physical_CLARA_Camera_DAQ_Controller()
        self.selectedCamera = self.cameras.getSelectedDAQRef()
        print("Model Initialized")

    def acquire(self):
        print(self.selectedCamera.DAQ.sensorTemp)
        if self.cameras.isNotAcquiring(self.selectedCamera.name):
            self.cameras.startAcquiring()
        elif self.cameras.isAcquiring(self.selectedCamera.name):
            self.cameras.stopAcquiring()

    def collectAndSave(self, numberOfImages):
        if self.cameras.isAcquiring(self.selectedCamera.name):
            self.cameras.collectAndSave(numberOfImages)
        elif self.selectedCamera.DAQ.captureState == self.cap.CAPTURING:
            self.cameras.killCollectAndSave()

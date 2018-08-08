from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import os,sys
import time
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
import VELA_CLARA_Camera_DAQ_Control as daq
import VELA_CLARA_Camera_IA_Control as camIA


class Model(QObject):
    def __init__(self):
        #QThread.__init__(self)
        self.camInit = camIA.init()
        self.camdaqInit = daq.init()
        self.cameras = self.camdaqInit.physical_CLARA_Camera_DAQ_Controller()
        self.camerasIA = self.camInit.physical_CLARA_Camera_IA_Controller()
        self.camNames = list(self.cameras.getCameraNames())
        #print names
        self.camNames.remove('VC')
        #print names
        for name in self.camNames:
            if self.cameras.isAcquiring(name):
                self.cameras.setCamera(name)
                self.cameras.stopAcquiring()
                time.sleep(1)
        #print name
        self.chosen_camera = 'S01-CAM-01'
        self.cameras.setCamera(self.chosen_camera)
        print '\n\n\n\n\n\nstart acquiring', self.chosen_camera
        self.cameras.startAcquiring()
        self.camerasIA.setCamera(self.chosen_camera)
        time.sleep(2)
        ia = self.camerasIA.getSelectedIARef().IA
        for x in dir(ia):
                    print x, getattr(ia, x)

from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
import os,sys
import time
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
import VELA_CLARA_Camera_DAQ_Control as daq
import VELA_CLARA_Camera_IA_Control as camIA

class Model(QObject):
    def __init__(self):
        self.Init = daq.init()
        self.camInit = camIA.init()
        self.cameras = self.Init.physical_CLARA_Camera_DAQ_Controller()
        self.camerasIA = self.camInit.physical_CLARA_Camera_IA_Controller()

        self.names = list(self.cameras.getCameraNames())
        print self.names
        self.names.remove('VC')
        print self.names

        for name in self.names:
            if self.cameras.isAcquiring(name):
                self.cameras.setCamera(name)
                self.cameras.stopAcquiring()
        #print name

        self.chosen_camera = 'S01-CAM-01'
        self.cameras.setCamera(self.chosen_camera)
        self.cameras.startAcquiring()
        self.camerasIA.setCamera(self.chosen_camera)
        print 'here1'
        print self.cameras.selectedCamera()
        print 'here2'


        self.camx1 = self.camerasIA.getSelectedIARef().IA.x
        print dir(self.camerasIA.getSelectedIARef().IA)

        self.ia = self.camerasIA.getSelectedIARef().IA
        for x in dir(self.ia):
            print x, getattr(self.ia, x)

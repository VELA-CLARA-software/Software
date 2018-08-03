""""Momentum Measurement Procedures for CLARA  PH1"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Ingredients"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
#from epics import caget,caput
import os,sys
import time
#import scipy.constants as physics
#import math as m
#import random as r
#import numpy as np
#from numpy.polynomial import polynomial as P
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
#os.environ["EPICS_CA_SERVER_PORT"]="6000"
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
#sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\OnlineModel-master\\OnlineModel-master')
#os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
#sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\Examples Scripts')
#import SAMPL.v2_developing.sampl as sampl
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"

#import onlineModel
#import VELA_CLARA_Magnet_Control as mag
#import VELA_CLARA_BPM_Control as bpm
#import VELA_CLARA_LLRF_Control as llrf
#import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Camera_IA_Control as camIA
import VELA_CLARA_Camera_DAQ_Control as daq

#import momentumFunctions

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

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

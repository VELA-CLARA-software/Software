""""Momentum Measurement Procedures for CLARA  PH1"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Ingredients"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
from epics import caget,caput
import os,sys
import time
import scipy.constants as physics
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P
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
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Camera_DAQ_Control as daq
import VELA_CLARA_Camera_IA_Control as camIA


import momentumFunctions

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Model(QObject):
    def __init__(self,app,view):
        QThread.__init__(self)
        self.app = app
        self.view = view
        '''variables to hold important values'''
        self.p = 0                        #momentum
        self.I = 0                        #current to bend momentum 45 degrees
        self.pSpread = 0                # momentum spread
        self.ISpread = 0                #current corrensponding to momentum spread
        self.Is = 0.                     #same as ISpread?
        self.predictedMomentum = 0        # value determined by user in GUI
        self.predictedI = 0                #current corresponding to predicted momentum
        self.n=10
        self.dCurrents =[]
        self.dPositions=[]
        self.fCurrents =[]
        self.fPositions=[]
        self.Dispersion=0.
        self.beamSigma=0.

        self.magInit = mag.init()
        self.bpmInit = bpm.init()
        self.pilInit = pil.init()
        self.llrfInit = llrf.init()
        self.camInit = camIA.init()
        self.camdaqInit = daq.init()
        ##self.Vmagnets = self.magInit.VELA_INJ_Magnet_Controller()
        #self.Cmagnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
        self.Cmagnets = self.magInit.physical_CB1_Magnet_Controller()
        self.laser = self.pilInit.physical_PILaser_Controller()
        self.Cbpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
        print 'HERE WE ARE(model_CLARA)!!!!: BPM readout =', str(self.Cbpms.getXFromPV('C2V-BPM01'))
        #self.C2Vbpms = self.bpmInit.virtual_CLARA_2_VELA_BPM_Controller()
        self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
        self.LINAC01 = self.llrfInit.physical_L01_LLRF_Controller()
        self.Cmagnets.switchONpsu('S02-DIP01')
        self.Cmagnets.switchONpsu('S01-HCOR1')
        self.Cmagnets.switchONpsu('S01-HCOR2')
        self.Cmagnets.switchONpsu('S02-HCOR1')
        self.Cmagnets.switchONpsu('S02-HCOR2')
        COR = [self.Cmagnets.getMagObjConstRef('S02-HCOR2')]                                        #create a reference to the corrector
        #x1= self.getXBPM(bctrl, bpm, N)                                            #get the x position on the BPM
        I1 = COR[0].siWithPol
        self.Cmagnets.getSI('S02-HCOR2')
        print '\n\n\n\n\n\n\n\n\n',str(I1)
        self.Cmagnets.switchONpsu('S02-QUAD1')
        self.Cmagnets.switchONpsu('S02-QUAD2')
        # self.SAMPL = onlineModel.SAMPL(V_MAG_Ctrl=self.Vmagnets,
        #                                     C_S01_MAG_Ctrl=self.Cmagnets,
        #                                     C_S02_MAG_Ctrl=self.Cmagnets,
        #                                     C2V_MAG_Ctrl=self.Cmagnets,
        #                                     V_RF_Ctrl=None,
        #                                     C_RF_Ctrl=self.gun,
        #                                     L01_RF_Ctrl=self.LINAC01,
        #                                     messages=False)
        # self.SAMPL.startElement = 'C1-GUN'
        # self.SAMPL.stopElement = 'CV-YAG01'
        # self.SAMPL.initDistrib = 'temp-start.ini'
        # self.SAMPL.initCharge = 0.25
        #self.gun400 = self.llrfInit.physical_VELA_HRRG_LLRF_Controller()
        ##self.cameras = self.camInit.physical_CLARA_Camera_IA_Controller()
        #Setup Virtual Accelerators
        #Cmagnets.switchONpsu('DIP01')
        #cameras.setCamera('C2V-CAM-01')
        ##self.selectedCamera = self.cameras.getSelectedIARef()
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
        # camx1 = self.camerasIA.getSelectedIARef().IA.x
        # print  self.camerasIA.getSelectedIARef().IA
        #
        # print 'camx1', str(camx1)
        # camy1 = self.camerasIA.getSelectedIARef().IA.y
        # print 'camy1', str(camy1)
        # camy1 = self.camerasIA.getSelectedIARef().IA.sigmaX
        # print 'camy1', str(camy1)
        # camy1 = self.camerasIA.getSelectedIARef().IA.sigmaY
        # print 'camy1', str(camy1)
        # camy1 = self.camerasIA.getSelectedIARef().IA.covXY
        # print 'camy1', str(camy1)

        print '\n\n\n\n\n\n'
        #self.Cmagnets.setSI('S02-DIP01',0)#91.6
        # self.gun400.setAmpMVM(70) #set gun10 instead!
        # self.gun400.setPhiDEG(-16)
        # self.LINAC01.setAmpMVM(21)
        # self.LINAC01.setPhiDEG(-9)
        # self.SAMPL = sampl.Setup(V_MAG_Ctrl=None,
        #                     C_S01_MAG_Ctrl=self.Cmagnets,
        #                     C_S02_MAG_Ctrl=self.Cmagnets,
        #                     C2V_MAG_Ctrl=self.Cmagnets,
        #                     LRRG_RF_Ctrl=None,
        #                     HRRG_RF_Ctrl=self.gun400,
        #                     L01_RF_Ctrl=self.LINAC01,
        #                     messages=True)

        #self.SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
        #self.SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
        #self.SAMPL.initDistribFile = '4k-250pC.ini'
        #self.gun.setAmpMVM(65)
        #self.LINAC01.setAmpMVM(20)
        self.func = momentumFunctions.Functions(OM='')
        #print("Model Initialized")

    #Outline of Momentum Measurement Procedure
    def measureMomentumPrelim(self):
        '''1. Preliminaries'''
        #if self.view.checkBox_1.isChecked()==True:
        print 'Setting C2V dipole to zero'
        self.Cmagnets.setSI('S02-DIP01',0)
        time.sleep(1)
        self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
        self.predictedI = self.func.mom2I(self.Cmagnets,
                                        'S02-DIP01',
                                        self.predictedMomentum)
        print('Predicted Current: '+str(self.predictedI))
        print('Predicted Momentum: '+str(self.predictedMomentum))

    def measureMomentumAlign(self):
        '''2. Align Beam through Dipole'''
        #if self.view.checkBox_2.isChecked()==True:
        print 'Aligning on S02-BPM-01 with S01-HCOR-02'
        #self.func.align(self.Cmagnets,'S01-HCOR2',self.Cbpms,'S02-BPM01',0.5)
        self.func.align(self.Cmagnets,'S02-HCOR3',self.Cbpms,'S02-BPM02',0.5)

        #raw_input('Put S02-YAG-02 in, then press enter')
        #print 'Aligning on S02-YAG-02 with S02-HCOR-02'
        #self.func.alignScreen(self.Cmagnets,'S02-HCOR2',self.camerasIA,'S02-CAM-01',13,0.5)
        #raw_input('Take S02-YAG-02 out, then press enter')

        #print 'Aligning on S02-BPM-02 with S02-HCOR-03'
        #self.func.align(self.Cmagnets,'S02-HCOR3',self.Cbpms,'S02-BPM02',0.5) #was 0.000001
        #self.func.align(self.Cmagnets,'S02-VCOR2',self.Cbpms,'S02-BPM02',0.5)
        #align(self,hctrl,hcor, bctrl, bpm, tol, N=10):
        #self.func.align(self.Cmagnets,'VCOR02',self.Cbpms,'BPM02',0.000001)
        #for i in range(3):
            #self.func.align('HCOR01','BPM01',0.000001)
            #self.func.align('HCOR02','BPM02',0.000001)'''
        #print('No alignment here')

    def measureMomentumCentreC2V(self):
        '''3. Centre in Spec. Line'''
        #if self.view.checkBox_3.isChecked()==True:
        self.I = self.func.bendBeam(self.Cmagnets,'S02-DIP01',
                                    self.Cbpms,'C2V-BPM01',
                                    'YAG01',
                                     self.predictedI, 0.1)#0.00001                 # tol=0.0001 (metres)

    def measureMomentumCalcMom(self):
        '''4. Convert Current to Momentum'''
        #if self.view.checkBox_4.isChecked()==True:
            #self.PL.info('4. Calculate Momentum')
        self.p = self.func.calcMom(self.Cmagnets,'S02-DIP01',self.I)
        print self.p

    #Outline of Momentum Spread Measurement Procedure
    def measureMomentumSpreadChecks(self):
        if self.view.checkBox_done_mom.isChecked()==True:
            #1. Checks
            #if self.view.checkBox_1_s.isChecked()==True:
            """1. Checks"""
            #self.p=34.41
            self.I=self.func.mom2I(self.Cmagnets,'S02-DIP01',self.p)
            self.Cmagnets.setSI('S02-DIP01',self.I)
            print 'measureMomentum(step 1), p = ', str(self.p)

    def measureMomentumSpreadMinBeta(self):
        """2. Minimise Beta"""
        #if self.view.checkBox_2_s.isChecked()==True:
        #2.1 Minimize Beta
        self.func.minimizeBeta(self.Cmagnets,'S02-QUAD3',
                                None,'CLA-C2V-DIA-CAM-01',1)
        #self.func.using_move_to_thread(self.Cmagnets,'S02-QUAD3',
        #                        None,'VM-CLA-C2V-DIA-CAM-01',1)
        #'''Re-instate minimising beta with Quad-04 here!!!'''
        #self.func.minimizeBeta2(self.Cmagnets,'S02-QUAD4',
        #                        None,'VM-CLA-C2V-DIA-CAM-01',-1)
        #2.2 Set Dispersion Size on Spec Line
        self.Cmagnets.setSI('S02-DIP01',self.I)
        #minimizeBeta(self,qctrl,quad,sctrl,screen,init_step,N=1):

    def measureMomentumSpreadSetDispSize(self):
        """3. Set Dispersion Size"""
        '''Fix Dispersion section needs work!'''
        print 'does nothing'
        #from model_VELA:
        #self.func.fixDispersion(self.magnets,'QUAD06',None,'VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
        #fixDispersion(self,qctrl,quad,sctrl,screen,step_size,N=1):
        #self.func.fixDispersion('QUAD0','VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
        #self.func.fixDispersion('QUAD0','VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
        #ONLY in REAL LIFE
        #self.func.magnets.degauss('DIP01')

    def measureMomentumSpreadCalcDisp(self):
        """3. Calculate Dispersion """
        #if self.view.checkBox_3_s.isChecked()==True:
        #self.Dispersion,beamSigma = self.func.findDispersion(self.Cmagnets,'DIP02',None,'VM-CLA-C2V-DIA-CAM-01',self.I,5,0.1)
        #self.Dispersion,self.beamSigma,
        #self.dCurrents,self.dPositions,
        #self.fCurrents,
        #self.fPositions =
        # Don't know why the above didn't work, that's why it's returned to x then unpacked below
        x = self.func.findDispersion(self.Cmagnets,
                                                'S02-DIP01',
                                                None,
                                                'CLA-C2V-DIA-CAM-01',
                                                self.I,10,0.1)
        print x[0]
        self.Dispersion = x[0]
        self.beamSigma = x[1]
        self.dCurrents = x[2]
        self.dPositions = x[3]
        self.fCurrents = x[4]
        self.fPositions = x[5]
        print(self.beamSigma)
        print(self.Dispersion)
        print(self.dCurrents)
        print(self.dPositions)
        print(self.fCurrents)
        print(self.fPositions)
        self.Is = self.beamSigma/self.Dispersion
        print(self.Is)
        #Haven't done errors yet

    def measureMomentumSpreadCalc(self):
        """5. Calculate Momentum Spread """
        #if self.view.checkBox_4_s.isChecked()==True:
        self.pSpread = self.func.calcMomSpread(self.Cmagnets,'S02-DIP01',self.Is,self.I)
        #a = self.func.calcMomSpread(self.Cmagnets,'DIP01',self.Is,self.I)
        #print a
        #else:
        #    print 'Not confirmed momentum measurement'

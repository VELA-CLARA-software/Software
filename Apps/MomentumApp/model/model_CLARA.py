""""Momentum Measurement Procedures for CLARA  PH1"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Ingredients"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from epics import caget,caput
import os,sys
import time
import scipy.constants as physics
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\OnlineModel-master\\OnlineModel-master')
#os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\Examples Scripts')
import SAMPL.v2_developing.sampl as sampl
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"

#import onlineModel
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Camera_IA_Control as camIA

import momentumFunctions

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Model():
    def __init__(self,view):
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
        self.Vmagnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        self.Cmagnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
        self.laser = self.pilInit.virtual_PILaser_Controller()
        self.Cbpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
        print 'HERE WE ARE(model_CLARA)!!!!: BPM readout =', str(self.Cbpms.getXFromPV('C2V-BPM01'))
        #self.C2Vbpms = self.bpmInit.virtual_CLARA_2_VELA_BPM_Controller()
        self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
        self.LINAC01 = self.llrfInit.virtual_L01_LLRF_Controller()
        self.Cmagnets.switchONpsu('DIP01')
        self.Cmagnets.switchONpsu('S01-HCOR1')
        self.Cmagnets.switchONpsu('S01-HCOR2')
        self.Cmagnets.switchONpsu('S02-HCOR01')
        self.Cmagnets.switchONpsu('S02-HCOR02')
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
        self.gun400 = self.llrfInit.virtual_VELA_HRRG_LLRF_Controller()
        self.cameras = self.camInit.virtual_CLARA_Camera_IA_Controller()
        #Setup Virtual Accelerators
        #Cmagnets.switchONpsu('DIP01')
        #cameras.setCamera('C2V-CAM-01')
        self.selectedCamera = self.cameras.getSelectedIARef()
        self.Cmagnets.setSI('DIP01',-91.6)
        self.gun400.setAmpMVM(70)
        self.gun400.setPhiDEG(-16)
        self.LINAC01.setAmpMVM(21)
        self.LINAC01.setPhiDEG(-9)
        self.SAMPL = sampl.Setup(V_MAG_Ctrl=None,
                            C_S01_MAG_Ctrl=self.Cmagnets,
                            C_S02_MAG_Ctrl=self.Cmagnets,
                            C2V_MAG_Ctrl=self.Cmagnets,
                            LRRG_RF_Ctrl=None,
                            HRRG_RF_Ctrl=self.gun400,
                            L01_RF_Ctrl=self.LINAC01,
                            messages=True)

        self.SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
        self.SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
        self.SAMPL.initDistribFile = '4k-250pC.ini'
        self.gun.setAmpMVM(65)
        self.LINAC01.setAmpMVM(20)
        self.func = momentumFunctions.Functions(OM=self.SAMPL)
        print("Model Initialized")

    #Outline of Momentum Measurement Procedure
    def measureMomentum(self):
        '''1. Preliminaries'''
        if self.view.checkBox_1.isChecked()==True:
            self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
            self.predictedI = self.func.mom2I(self.Cmagnets,
                                            'DIP01',
                                            self.predictedMomentum)
            print('Predicted Current: '+str(self.predictedI))
            print('Predicted Momentum: '+str(self.predictedMomentum))

        '''2. Align Beam through Dipole'''
        if self.view.checkBox_2.isChecked()==True:
            #for i in range(3):
                #self.func.align('HCOR01','BPM01',0.000001)
                #self.func.align('HCOR02','BPM02',0.000001)'''
            print('No alignment here')

        '''3. Centre in Spec. Line'''
        if self.view.checkBox_3.isChecked()==True:
            self.I = self.func.bendBeam(self.Cmagnets,'DIP01',
                                        self.Cbpms,'C2V-BPM01',
                                        'YAG01',
                                         self.predictedI, 0.00001)                 # tol=0.0001 (metres)

        '''4. Convert Current to Momentum'''
        if self.view.checkBox_4.isChecked()==True:
            #self.PL.info('4. Calculate Momentum')
            self.p = self.func.calcMom(self.Cmagnets,'DIP01',self.I)
            print self.p
    #Outline of Momentum Spread Measurement Procedure
    def measureMomentumSpread(self):
        if self.view.checkBox_done_mom.isChecked()==True:
            #1. Checks
            if self.view.checkBox_1_s.isChecked()==True:
                """1. Checks"""
                #self.p=34.41
                self.I=self.func.mom2I(self.Cmagnets,'DIP01',self.p)
                self.Cmagnets.setSI('DIP01',self.I)
                print 'measureMomentum(step 1), p = ', str(self.p)
            """2. Set Dispersion"""
            if self.view.checkBox_2_s.isChecked()==True:
                #2.1 Minimize Beta
                self.func.minimizeBeta2(self.Cmagnets,'S02-QUAD3',
                                        None,'VM-CLA-C2V-DIA-CAM-01',1)
                #'''Re-instate minimising beta with Quad-04 here!!!'''
                self.func.minimizeBeta2(self.Cmagnets,'S02-QUAD4',
                                        None,'VM-CLA-C2V-DIA-CAM-01',-1)
                #2.2 Set Dispersion Size on Spec Line
                self.Cmagnets.setSI('DIP01',self.I)
                #minimizeBeta(self,qctrl,quad,sctrl,screen,init_step,N=1):

                '''Fix Dispersion section needs work!'''
                #from model_VELA:
                #self.func.fixDispersion(self.magnets,'QUAD06',None,'VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
                #fixDispersion(self,qctrl,quad,sctrl,screen,step_size,N=1):
                #self.func.fixDispersion('QUAD0','VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
                #self.func.fixDispersion('QUAD0','VM-EBT-INJ-DIA-CAM-05:CAM',-0.05)
                #ONLY in REAL LIFE
                #self.func.magnets.degauss('DIP01')

            """3. Calculate Dispersion """
            if self.view.checkBox_3_s.isChecked()==True:
                #self.Dispersion,beamSigma = self.func.findDispersion(self.Cmagnets,'DIP02',None,'VM-CLA-C2V-DIA-CAM-01',self.I,5,0.1)
                #self.Dispersion,self.beamSigma,
                #self.dCurrents,self.dPositions,
                #self.fCurrents,
                #self.fPositions =
                # Don't know why the above didn't work, that's why it's returned to x then unpacked below
                x = self.func.findDispersion(self.Cmagnets,
                                                        'DIP01',
                                                        None,
                                                        'VM-CLA-C2V-DIA-CAM-01',
                                                        self.I,5,0.1)
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

            """4. Calculate Momentum Spread """
            if self.view.checkBox_4_s.isChecked()==True:
                self.pSpread = self.func.calcMomSpread(self.Cmagnets,'DIP01',self.Is,self.I)
                #a = self.func.calcMomSpread(self.Cmagnets,'DIP01',self.Is,self.I)
                #print a
        else:
            print 'Not confirmed momentum measurement'

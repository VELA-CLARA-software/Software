""""Momentum Measurement Procedures for CLARA  PH1"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Ingredients"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
from PyQt4 import QtGui
from epics import caget,caput
import os,sys
import time
import scipy.constants as physics
import math as m
import random as r
import numpy as np
from numpy.polynomial import polynomial as P
import datetime
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
#os.environ["EPICS_CA_SERVER_PORT"]="6000"
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\ASTeC\\Projects\\VELA\\Software\\OnlineModel')
sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\OnlineModel-master\\OnlineModel-master')
#os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
sys.path.append('C:\\Users\\djd63\\Desktop\\VA workshop\\Examples Scripts')
#import SAMPL.v2_developing.sampl_noprint as sampl
#sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stagetim')
#sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
sys.path.append('C:\\Users\\djd63\\Desktop\\Release')
#sys.path.append('C:\\Users\\djd63\\Documents\\GitHub\\Software\\Apps\\AlignOnBPMs\\model')
#os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
#sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\')
#import onlineModel
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
#import VELA_CLARA_LLRF_Control as llrf
#import VELA_CLARA_PILaser_Control as pil
#import VELA_CLARA_Camera_IA_Control as camIA

import momentumFunctions as momentumFunctions

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Model(QObject):
    def __init__(self,app,view):
        QThread.__init__(self)
        self.app = app
        self.view = view
        '''variables to hold important values'''
        self.bpm_list = ['S01-BPM01', 'S02-BPM01', 'S02-BPM02', 'C2V-BPM01', \
        'INJ-BPM04', 'INJ-BPM05', 'BA1-BPM01', 'BA1-BPM02', 'BA1-BPM03', 'BA1-BPM04']
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
        self.Q_WCM = []
        for r in np.arange(0, 10, 1):
            row = str(r+1)
            setattr(self, 'liveTarget'+row, 'GOOD')
        self.magInit = mag.init()
        self.bpmInit = bpm.init()
        #self.bpmInit.setVerbose()
        #self.pilInit = pil.init()
        #self.llrfInit = llrf.init()
        #self.camInit = camIA.init()
        #self.Vmagnets = self.magInit.physical_VELA_INJ_Magnet_Controller()
        #self.Cmagnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
        #self.Cmagnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
        self.Cmagnets = self.magInit.physical_C2B_Magnet_Controller()
        #self.laser = self.pilInit.physical_PILaser_Controller()
        #self.Cbpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
        self.Cbpms = self.bpmInit.physical_C2B_BPM_Controller()

        #print 'HERE WE ARE(model_CLARA)!!!!: BPM readout =', str(self.Cbpms.getXFromPV('C2V-BPM01'))
        #self.C2Vbpms = self.bpmInit.physical_CLARA_2_VELA_BPM_Controller()
        #self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
        #self.LINAC01 = self.llrfInit.physical_L01_LLRF_Controller()
        # self.Vmagnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        # self.Cmagnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
        # self.laser = self.pilInit.virtual_PILaser_Controller()
        # self.Cbpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
        # #print 'HERE WE ARE(model_CLARA)!!!!: BPM readout =', str(self.Cbpms.getXFromPV('C2V-BPM01'))
        # #self.C2Vbpms = self.bpmInit.virtual_CLARA_2_VELA_BPM_Controller()
        # self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
        # self.LINAC01 = self.llrfInit.virtual_L01_LLRF_Controller()
        #self.Cmagnets.switchONpsu('DIP01')
        #self.Cmagnets.switchONpsu('S01-HCOR1')
        #self.Cmagnets.switchONpsu('S01-HCOR2')
        #self.Cmagnets.switchONpsu('S02-HCOR01')
        #self.Cmagnets.switchONpsu('S02-HCOR02')
        #self.Cmagnets.switchONpsu('S02-QUAD1')
        #self.Cmagnets.switchONpsu('S02-QUAD2')
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
        #self.gun400 = self.llrfInit.virtual_VELA_HRRG_LLRF_Controller()
        #self.cameras = self.camInit.virtual_CLARA_Camera_IA_Controller()
        #Setup Virtual Accelerators
        #Cmagnets.switchONpsu('DIP01')
        #cameras.setCamera('C2V-CAM-01')
        #self.selectedCamera = self.cameras.getSelectedIARef()
        # self.Cmagnets.setSI('DIP01',-91.6)
        # self.gun400.setAmpMVM(70)
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
        #
        # self.SAMPL.startElement = 'CLA-HRG1-GUN-CAV'
        # self.SAMPL.stopElement = 'CLA-C2V-DIA-SCR-01-W'
        # self.SAMPL.initDistribFile = '4k-250pC.ini'
        # self.gun.setAmpMVM(65)
        # self.LINAC01.setAmpMVM(20)
        # self.func = momentumFunctions.Functions(OM=self.SAMPL)
        self.func = momentumFunctions.Functions()
        self.setPosAxisBounds()
        self.setQAxisMax()
        #print("Model Initialized")

    def stepCurrent2(self,ctrl,xory, upordown, row):
        #print xory
        #print upordown
        #magnet = ''
        #step = 0
        if xory == 'x' and upordown == 'up':
            #print '1'
            magnet = str(getattr(self.view, 'comboBox_H_'+row).currentText())
            step = float(getattr(self.view, 'doubleSpinBox_step_'+row).value())
        elif xory == 'x' and upordown == 'down':
            #print '2'
            magnet = str(getattr(self.view, 'comboBox_H_'+row).currentText())
            step = -float(getattr(self.view, 'doubleSpinBox_step_'+row).value())
        elif xory == 'y' and upordown == 'up':
            #print '3'
            magnet = str(getattr(self.view, 'comboBox_V_'+row).currentText())
            step = float(getattr(self.view, 'doubleSpinBox_step_'+row).value())
        elif xory == 'y' and upordown == 'down':
            #print '4'
            magnet = str(getattr(self.view, 'comboBox_V_'+row).currentText())
            step = -float(getattr(self.view, 'doubleSpinBox_step_'+row).value())
        else:
            print 'Invalid input'
        self.func.stepCurrent(ctrl,magnet,step)
        #print magnet
        #print step

    #Outline of Momentum Measurement Procedure
    def setPosAxisBounds(self):
        #print 'in setPosAxisBounds'
        self.posAxisBounds = float(self.view.lineEdit_posAxisBounds.text())

    def setQAxisMax(self):
        #print 'in setPosAxisBounds'
        self.qAxisMax = float(self.view.lineEdit_qAxisMax.text())
#
            #getattr(self, 'positionGraph_'+row).setOpts(x=self.xdict.keys(), height=[1*self.model.Cbpms.getXFromPV(bpm_name),1*self.model.Cbpms.getYFromPV(bpm_name)])

    def setAllTol(self):
        #print 'here'
        self.tol_all = float(getattr(self.view, 'doubleSpinBox_tol_all').value())
        for r, bpm_name in enumerate(self.bpm_list):#np.arange(0, 10, 1):
            row = str(r+1)
            #setattr(self.view, 'doubleSpinBox_tol_'+row, self.tol_all)
            getattr(self.view, 'doubleSpinBox_tol_'+row).setValue(self.tol_all)

    def setAllInitStep(self):
        self.step_all = float(getattr(self.view, 'doubleSpinBox_step_all').value())
        for r, bpm_name in enumerate(self.bpm_list):
            row = str(r+1)
            getattr(self.view, 'doubleSpinBox_step_'+row).setValue(self.step_all)

    def measureMomentumPrelim(self):
        '''1. Preliminaries'''
        #if self.view.checkBox_1.isChecked()==True:
        print 'Setting C2V dipole to zero'
        self.Cmagnets.setSI('S02-DIP01',0)
        time.sleep(1)
        self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
        self.predictedI = self.func.mom2I(self.Cmagnets,
                                        'DIP01',
                                        self.predictedMomentum)
        print('Predicted Current: '+str(self.predictedI))
        print('Predicted Momentum: '+str(self.predictedMomentum))

    def measureMomentumAlign(self):
        self.func.align(self.Cmagnets,'S02-HCOR2',self.Cbpms,'S02-BPM02',0.5)

    def measureMomentumAlign_2(self):
        self.func.align2(self.Cmagnets,'S01-HCOR1',self.Cbpms,'S01-BPM01',0.05)

    def Align_x(self, row):
        self.Align('x', row)

    def Align_y(self, row):
        self.Align('y', row)

    def Align_both(self, row):
        self.Align('x', row)
        self.Align('y', row)

    def Align(self, xory, row):
        row = str(row)
        self.bpm2align = str(getattr(self.view, 'comboBox_'+row).currentText())
        #print self.bpm2align
        self.targetx = float(getattr(self.view, 'doubleSpinBox_x_'+row).value())
        self.targety = float(getattr(self.view, 'doubleSpinBox_y_'+row).value())
        if xory == 'x':
            self.target = self.targetx
            self.cor = str(getattr(self.view, 'comboBox_H_'+row).currentText())
            self.bpmVal = self.Cbpms.getXFromPV(self.bpm2align)
        else:
            self.target = self.targety
            self.cor = str(getattr(self.view, 'comboBox_V_'+row).currentText())
            self.bpmVal = self.Cbpms.getYFromPV(self.bpm2align)
        self.tol = float(getattr(self.view, 'doubleSpinBox_tol_'+row).value())
        self.initstep = float(getattr(self.view, 'doubleSpinBox_step_'+row).value())
        if abs(self.bpmVal) > self.tol:
            self.func.align4(self.Cmagnets,self.cor,self.Cbpms,self.bpm2align,self.target,self.tol,xory,self.initstep)
        else:
            print 'Already aligned'

    def combobox_bpm(self,text):
        print text

    def steer_H(self, row, userinput):
        #print 'steer_H', userinput
        if userinput == True:
            #print '.....User H input.....'
            row = str(row)
            #self.target = float(getattr(self.view, 'doubleSpinBox_H_'+row).value())
            self.target = float(getattr(self.view, 'lineEdit_HC_'+row).text())
            #self.targety = float(getattr(self.view, 'doubleSpinBox_V_'+row).value())
            self.cor = str(getattr(self.view, 'comboBox_H_'+row).currentText())
            #self.func.setCurrent(self.Cmagnets,self.cor,self.target)
            self.Cmagnets.setSI(self.cor,self.target)
            time.sleep(0.5)
        else:
            #print '.....Non-user H input.....'
            pass

    def steer_V(self, row, userinput):
        #print 'steer_V', userinput
        if userinput == True:
            #print '.....User V input.....'
            row = str(row)
            #self.targetx = float(getattr(self.view, 'doubleSpinBox_H_'+row).value())
            self.target = float(getattr(self.view, 'lineEdit_VC_'+row).text())
            self.cor = str(getattr(self.view, 'comboBox_V_'+row).currentText())
            #self.func.setCurrent(self.Cmagnets,self.cor,self.target)
            self.Cmagnets.setSI(self.cor,self.target)
            time.sleep(0.5)
        else:
            #print '.....Non-user V input.....'
            pass

    def get_H(self, row):
        row = str(row)
        #self.target = float(getattr(self.view, 'doubleSpinBox_H_'+row).value())
        #self.targety = float(getattr(self.view, 'doubleSpinBox_V_'+row).value())
        self.cor = str(getattr(self.view, 'comboBox_H_'+row).currentText())
        return self.Cmagnets.getSI(self.cor)

    def get_V(self, row):
        row = str(row)
        #self.target = float(getattr(self.view, 'doubleSpinBox_V_'+row).value())
        #self.targety = float(getattr(self.view, 'doubleSpinBox_V_'+row).value())
        self.cor = str(getattr(self.view, 'comboBox_V_'+row).currentText())
        return self.Cmagnets.getSI(self.cor)

    def measureMomentumCentreC2V(self):
        self.I = self.func.bendBeam(self.Cmagnets,'DIP01',
                                    self.Cbpms,'C2V-BPM01',
                                    'YAG01',
                                     self.predictedI, 0.00001)                 # tol=0.0001 (metres)

    def measureMomentumCalcMom(self):
        self.p = self.func.calcMom(self.Cmagnets,'DIP01',self.I)
        print self.p

    # def measureMomentum(self):
    #     # '''1. Preliminaries'''
    #     # if self.view.checkBox_1.isChecked()==True:
    #     #     print 'Setting C2V dipole to zero'
    #     #     self.Cmagnets.setSI('S02-DIP01',0)
    #     #     time.sleep(1)
    #     #     self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
    #     #     self.predictedI = self.func.mom2I(self.Cmagnets,
    #     #                                     'DIP01',
    #     #                                     self.predictedMomentum)
    #     #     print('Predicted Current: '+str(self.predictedI))
    #     #     print('Predicted Momentum: '+str(self.predictedMomentum))
    #
    #     '''2. Align Beam through Dipole'''
    #     if self.view.checkBox_2.isChecked()==True:
    #         self.func.align(self.Cmagnets,'S02-HCOR2',self.Cbpms,'S02-BPM02',0.5)
    #         #for i in range(3):
    #             #self.func.align('HCOR01','BPM01',0.000001)
    #             #self.func.align('HCOR02','BPM02',0.000001)'''
    #         #print('No alignment here')
    #
    #     '''3. Centre in Spec. Line'''
    #     if self.view.checkBox_3.isChecked()==True:
    #         self.I = self.func.bendBeam(self.Cmagnets,'DIP01',
    #                                     self.Cbpms,'C2V-BPM01',
    #                                     'YAG01',
    #                                      self.predictedI, 0.00001)                 # tol=0.0001 (metres)
    #
    #     '''4. Convert Current to Momentum'''
    #     if self.view.checkBox_4.isChecked()==True:
    #         #self.PL.info('4. Calculate Momentum')
    #         self.p = self.func.calcMom(self.Cmagnets,'DIP01',self.I)
    #         print self.p
    # #Outline of Momentum Spread Measurement Procedure
    def measureMomentumSpreadChecks(self):
        if self.view.checkBox_done_mom.isChecked()==True:
            #1. Checks
            #if self.view.checkBox_1_s.isChecked()==True:
            """1. Checks"""
            #self.p=34.41
            self.I=self.func.mom2I(self.Cmagnets,'DIP01',self.p)
            self.Cmagnets.setSI('DIP01',self.I)
            print 'measureMomentum(step 1), p = ', str(self.p)
    def measureMomentumSpreadMinBeta(self):
            """2. Minimise Beta"""
            #if self.view.checkBox_2_s.isChecked()==True:
            #2.1 Minimize Beta
            test_continue = 0
            print 'test_continue0', test_continue
            self.func.minimizeBeta2(self.Cmagnets,'S02-QUAD3',
                                    None,'VM-CLA-C2V-DIA-CAM-01',1)
            #self.func.minBetaThread(self.Cmagnets,'S02-QUAD3',
            #                        None,'VM-CLA-C2V-DIA-CAM-01',1)
            #while test_continue < 1:
            #    print 'test_continue', test_continue
            #    time.sleep(1)
            #'''Re-instate minimising beta with Quad-04 here!!!'''
            #self.func.minimizeBeta2(self.Cmagnets,'S02-QUAD4',
            #                        None,'VM-CLA-C2V-DIA-CAM-01',-1)
            #2.2 Set Dispersion Size on Spec Line
            self.Cmagnets.setSI('DIP01',self.I)
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
            """4. Calculate Dispersion """
            #if self.view.checkBox_3_s.isChecked()==True:
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
            self.pSpread = self.func.calcMomSpread(self.Cmagnets,'DIP01',self.Is,self.I)
                #a = self.func.calcMomSpread(self.Cmagnets,'DIP01',self.Is,self.I)
                #print a
            #else:
            #    print 'Not confirmed momentum measurement'

    def set(self):
        for r, bpm_name in enumerate(self.bpm_list):#np.arange(0, 10, 1):
            row = str(r+1)
            #b = a[r].split()
            #print b[0]
            #print self.Cbpms.getBPMXBuffer(str(getattr(self.view, 'comboBox_'+row).currentText()))
            if len(self.Cbpms.getBPMQBuffer(bpm_name)) > 0 and str(self.Cbpms.getStatusBuffer(bpm_name)[-1]) == 'GOOD':
                # use buffer
                #getattr(self.view, 'doubleSpinBox_x_'+row).setValue(np.mean(self.Cbpms.getBPMXBuffer(str(getattr(self.view, 'comboBox_'+row).currentText()))))
                #getattr(self.view, 'doubleSpinBox_y_'+row).setValue(np.mean(self.Cbpms.getBPMYBuffer(str(getattr(self.view, 'comboBox_'+row).currentText()))))
                #use live
                getattr(self.view, 'doubleSpinBox_x_'+row).setValue(np.mean(self.Cbpms.getXFromPV(str(getattr(self.view, 'comboBox_'+row).currentText()))))
                getattr(self.view, 'doubleSpinBox_y_'+row).setValue(np.mean(self.Cbpms.getYFromPV(str(getattr(self.view, 'comboBox_'+row).currentText()))))
                setattr(self, 'liveTarget'+row, str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1]))
            else:
                getattr(self.view, 'doubleSpinBox_x_'+row).setValue(0)
                getattr(self.view, 'doubleSpinBox_y_'+row).setValue(0)
                setattr(self, 'liveTarget'+row, 'BAD')
                #setattr(self, 'liveTarget'+row, str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1]))
            # getattr(self.view, 'doubleSpinBox_x_'+row).setValue(1*self.Cbpms.getXFromPV(str(getattr(self.view, 'comboBox_'+row).currentText())))
            # getattr(self.view, 'doubleSpinBox_y_'+row).setValue(1*self.Cbpms.getYFromPV(str(getattr(self.view, 'comboBox_'+row).currentText())))
            # setattr(self, 'liveTarget'+row, str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1]))

            #getattr(self.view, 'doubleSpinBox_y_'+row).setValue(float(self.view.label_V_1.text()))
            #getattr(self.view, 'doubleSpinBox_tol_'+row).setValue(float(b[2]))
            #getattr(self.view, 'doubleSpinBox_step_'+row).setValue(float(b[3]))

    def set_0(self):
        for r, bpm_name in enumerate(self.bpm_list):#np.arange(0, 10, 1):
            row = str(r+1)
            #b = a[r].split()
            #print b[0]
            getattr(self.view, 'doubleSpinBox_x_'+row).setValue(0.0)
            getattr(self.view, 'doubleSpinBox_y_'+row).setValue(0.0)
            #setattr(self, 'liveTarget'+row, 0)
            #if len(self.Cbpms.getBPMQBuffer(bpm_name)) > 0 and str(self.Cbpms.getStatusBuffer(bpm_name)[-1]) == 'GOOD':
            setattr(self, 'liveTarget'+row, 'GOOD')
            #else:
                #setattr(self, 'liveTarget'+row, 'BAD')
                #setattr(self, 'liveTarget'+row, str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1]))
            #getattr(self.view, 'doubleSpinBox_tol_'+row).setValue(float(b[2]))
            #getattr(self.view, 'doubleSpinBox_step_'+row).setValue(float(b[3]))

    # def save(self):
    #     #self.filename = QtGui.QFileDialog::getOpenFileName
    #     #print self.filename
    #     self.savefile=QtGui.QFileDialog.getSaveFileName()
    #     print self.savefile
    #     row = 1
    #     open(self.savefile,'w').writelines(self.getall(row))
    #     for row, bpm in enumerate(self.bpm_list)#np.arange(2,11,1):
    #         open(self.savefile,'a').writelines(self.getall(row, bpm))

    def getall(self, row, bpm):
        row = str(row)
        self.save_targetx = str(getattr(self.view, 'doubleSpinBox_x_'+row).value())
        self.save_targety = str(getattr(self.view, 'doubleSpinBox_y_'+row).value())
        self.save_tol = str(getattr(self.view, 'doubleSpinBox_tol_'+row).value())
        self.save_initstep = str(getattr(self.view, 'doubleSpinBox_step_'+row).value())
        # self.save_hcor = str(getattr(self.view, 'doubleSpinBox_H_'+row).value())
        # self.save_vcor = str(getattr(self.view, 'doubleSpinBox_V_'+row).value())
        self.save_hcor = str(getattr(self.view, 'label_HC_'+row).text())
        self.save_vcor = str(getattr(self.view, 'label_VC_'+row).text())
        self.save_isLive = str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1])
        items = [self.save_targetx, self.save_targety, self.save_tol, self.save_initstep, self.save_hcor, self.save_vcor, self.save_isLive]
        items = map(lambda x: x + ' ', items)
        items[-1] = items[-1]+'\n'
        print items
        return items

    def save_positions(self):
        #self.filename = QtGui.QFileDialog::getOpenFileName
        #print self.filename
        #QtGui.QFileDialog.saveAsDialog(this)
        dateandtime=str(datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S'))
        #print dateandtime
        #dateandtime=str(143434234)
        self.savefile=QtGui.QFileDialog.getSaveFileName(None, '', '//apclara1/ControlRoomApps/Release/Data/BPMburts/'+dateandtime, '*.txt')
        print self.savefile
        #row = 1
        #open(self.savefile,'w').writelines(self.getall2(row))
        #for row, bpm in enumerate(self.bpm_list[0]):# in np.arange(2,11,1)
        #    print row, bpm
    #        open(self.savefile,'w').writelines(self.getall2(row, bpm))
        for r, bpm in enumerate(self.bpm_list):# in np.arange(2,11,1):
            if r == 0:
                open(self.savefile,'w').writelines(self.getall2(r, bpm))
            else:
                open(self.savefile,'a').writelines(self.getall2(r, bpm))

    def getall2(self, row, bpm_name):
        row = str(row+1)
        # self.save_targetx = str(self.Cbpms.getXFromPV(str(getattr(self.view, 'comboBox_'+row).currentText())))
        # self.save_targety = str(self.Cbpms.getYFromPV(str(getattr(self.view, 'comboBox_'+row).currentText())))
        if len(self.Cbpms.getBPMQBuffer(bpm_name)) > 0 and str(self.Cbpms.getStatusBuffer(bpm_name)[-1]) == 'GOOD':
            # use buffer
            #self.save_targetx = str(np.mean(self.Cbpms.getBPMXBuffer(str(getattr(self.view, 'comboBox_'+row).currentText()))))
            #self.save_targety = str(np.mean(self.Cbpms.getBPMYBuffer(str(getattr(self.view, 'comboBox_'+row).currentText()))))
            # use live
            self.save_targetx = str(np.mean(self.Cbpms.getXFromPV(str(getattr(self.view, 'comboBox_'+row).currentText()))))
            self.save_targety = str(np.mean(self.Cbpms.getYFromPV(str(getattr(self.view, 'comboBox_'+row).currentText()))))
            self.save_isLive = str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1])
        else:
            self.save_targetx = str(0)
            self.save_targety = str(0)
            self.save_isLive = 'BAD'
            #self.save_isLive = str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1])
        #self.save_tol = str(getattr(self.view, 'doubleSpinBox_tol_'+row).value())
        #self.save_initstep = str(getattr(self.view, 'doubleSpinBox_step_'+row).value())
        #self.save_hcor = str(getattr(self.view, 'label_HC_'+row).text())
        #self.save_vcor = str(getattr(self.view, 'label_VC_'+row).text())
        #self.save_isLive = str(self.Cbpms.getStatusBuffer((str(getattr(self.view, 'comboBox_'+row).currentText())))[-1])
        #items = [self.save_targetx, self.save_targety, self.save_tol, self.save_initstep, self.save_hcor, self.save_vcor, self.save_isLive]
        items = [self.save_targetx, self.save_targety, self.save_isLive]
        items = map(lambda x: x + ' ', items)
        items[-1] = items[-1]+'\n'
        print items
        return items

    def load(self):
        self.loadfile=QtGui.QFileDialog.getOpenFileName(None, '', '//apclara1/ControlRoomApps/Release/Data/BPMburts/', '*.txt')
        print self.loadfile
        #firstline = open(self.loadfile,'r').readline()
        #print firstline
        #r = 0
        with open(str(self.loadfile)) as f:
            #r = r + 1
            #row = str(r)
            a = f.readlines()
            for r in np.arange(0, len(a), 1):
                row = str(r+1)
                b = a[r].split()
                #print b[0]
                getattr(self.view, 'doubleSpinBox_x_'+row).setValue(float(b[0]))
                getattr(self.view, 'doubleSpinBox_y_'+row).setValue(float(b[1]))
                #setattr(self, 'tol'+row, b[2])
                setattr(self, 'liveTarget'+row, b[2])
                #getattr(self.view, 'doubleSpinBox_tol_'+row).setValue(float(b[2]))
                #getattr(self.view, 'doubleSpinBox_step_'+row).setValue(float(b[3]))
                # Commenting out setting correctors
                #getattr(self.view, 'doubleSpinBox_H_'+row).setValue(float(b[4]))
                #getattr(self.view, 'doubleSpinBox_V_'+row).setValue(float(b[5]))

    def WCM(self):
        self.Q_WCM.append(self.func.WCM())
        #print self.Q_WCM
        #time.sleep(1)
        if len(self.Q_WCM) > 20:
            #print 'here1', self.Q_WCM
            self.Q_WCM = self.Q_WCM[-20:]
            #print 'here2', self.Q_WCM
            #time.sleep(1)

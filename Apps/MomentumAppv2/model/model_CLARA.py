""""Momentum Measurement Procedures for CLARA  PH1"""

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
"""Ingredients"""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
from PyQt4.QtGui import QApplication
from epics import caget,caput
import os,sys
import time
import scipy.constants as physics
import math as m
import random as r
import numpy as np
from functools import partial
#from numpy.polynomial import polynomial as P
#import subprocess
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
#sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release')
#os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
#sys.path.append('C:\\Users\\djd63\\Desktop\\Release')
sys.path.append('C:\\Users\\djd63\\Documents\\GitHub\\Software\\Apps\\MomentumAppv2\\model')
#sys.path.append('C:\\Users\\djd63\\Desktop\\Release\\root_v5.34.34\\bin\\')
#import onlineModel
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_PILaser_Control as pil
#import VELA_CLARA_Camera_DAQ_Control as daq
#import VELA_CLARA_Camera_IA_Control as camIA
import VELA_CLARA_Screen_Control as scrn
import VELA_CLARA_Camera_Control as cam
import VELA_CLARA_Shutter_Control as shut

import momentumFunctions
#import bpm_recalibrate
#import test

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Model(QObject):
    def __init__(self,app,view):
        super(Model, self).__init__()
        #QThread.__init__(self)
        self.app = app
        self.view = view
        '''variables to hold important values'''
        self.approx_p = 0                        #momentum
        self.approxI = 0                        #current to bend momentum 45 degrees
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
        self.dipole = str(self.view.comboBox_dipole.currentText())
        self.cor1 = 'S02-HCOR1'
        self.cor2 = 'S02-HCOR2'
        self.bpm1 = 'S02-BPM02'
        #print self.dipole

        self.magInit = mag.init()
        self.bpmInit = bpm.init()
        self.pilInit = pil.init()
        self.llrfInit = llrf.init()
        #self.camInit = camIA.init()
        #self.camdaqInit = daq.init()
        self.camInit = cam.init()
        self.shutInit = shut.init()
        self.scrnInit = scrn.init()
        ##self.Vmagnets = self.magInit.VELA_INJ_Magnet_Controller()
        #self.Cmagnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
        self.Cmagnets = self.magInit.physical_CB1_Magnet_Controller()
        self.laser = self.pilInit.physical_PILaser_Controller()
        #self.Cbpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
        self.Cbpms = self.bpmInit.physical_C2B_BPM_Controller()
        #print 'HERE WE ARE(model_CLARA)!!!!: BPM readout =', str(self.Cbpms.getXFromPV('C2V-BPM01'))
        #self.C2Vbpms = self.bpmInit.virtual_CLARA_2_VELA_BPM_Controller()
        self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
        self.LINAC01 = self.llrfInit.physical_L01_LLRF_Controller()
        self.shut = self.shutInit.physical_PIL_Shutter_Controller()
        #self.scrn = self.scrnInit.physical_CLARA_PH1_Screen_Controller()
        self.scrn = self.scrnInit.physical_C2B_Screen_Controller()
        self.cam = self.camInit.physical_CLARA_Camera_Controller()
        # 23/7/18 all these should be on already really...
        #self.Cmagnets.switchONpsu('S02-DIP01')
        #self.Cmagnets.switchONpsu('S01-HCOR1')
        #self.Cmagnets.switchONpsu('S01-HCOR2')
        #self.Cmagnets.switchONpsu('S02-HCOR1')
        #self.Cmagnets.switchONpsu('S02-HCOR2')
        #COR = [self.Cmagnets.getMagObjConstRef('S02-HCOR2')]                                        #create a reference to the corrector
        #x1= self.getXBPM(bctrl, bpm, N)                                            #get the x position on the BPM

        #Set corrector to zero
        #I1 = COR[0].siWithPol
        #self.Cmagnets.getSI('S02-HCOR2')
        #print '\n\n\n\n\n\n\n\n\n',str(I1)
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
        #self.gun400 = self.llrfInit.physical_VELA_HRRG_LLRF_Controller()
        ##self.cameras = self.camInit.physical_CLARA_Camera_IA_Controller()
        #Setup Virtual Accelerators
        #Cmagnets.switchONpsu('DIP01')
        #cameras.setCamera('C2V-CAM-01')
        ##self.selectedCamera = self.cameras.getSelectedIARef()

        #self.cameras = self.camdaqInit.physical_CLARA_Camera_DAQ_Controller()
        #self.camerasIA = self.camInit.physical_CLARA_Camera_IA_Controller()
        #self.camNames = list(self.cameras.getCameraNames())

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

        #print '\n\n\n\n\n\n'
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
        #self.func = momentumFunctions.Functions(OM='')
        self.func = momentumFunctions.Functions(self)
        self.dipCurrent=[]
        self.BPMPosition=[]
        self.dipCurrent2 = []
        self.BPMPosition2 = []
        self.dipCurrent3 = []
        self.BPMPosition3 = []
        #print("Model Initialized")
        self.selectRF()

    def selectRF(self):
        if self.view.comboBox_selectRF.currentIndex() == 0:
            self.predictedMomentum = 5.0
            self.initialCurrentStep = 0.02
            #self.view.label_predictMom.setText(self.predictedMomentum)
            self.predictedI = self.func.mom2I(self.Cmagnets, self.dipole,self.predictedMomentum)
            self.view.doubleSpinBox_p.setValue(float(self.predictedMomentum))
            self.view.doubleSpinBox_I.setValue(float(self.predictedI))
        elif self.view.comboBox_selectRF.currentIndex() == 1:
            self.predictedMomentum = 35.0
            self.initialCurrentStep = 0.1
            #self.view.label_predictMom.setText(self.predictedMomentum)
            self.predictedI = self.func.mom2I(self.Cmagnets, self.dipole,self.predictedMomentum)
            self.view.doubleSpinBox_p.setValue(float(self.predictedMomentum))
            self.view.doubleSpinBox_I.setValue(float(self.predictedI))

    def selectCurrent(self):
        #self.p = self.func.calcMom(self.Cmagnets,'S02-DIP01',self.I)
        #self.predictedI = float(self.view.lineEdit_selectCurrent.text())
        self.predictedI = float(self.view.doubleSpinBox_I.value())
        #self.view.label_predictMom.setText(self.predictedMomentum)
        self.predictedMomentum = self.func.calcMom(self.Cmagnets,self.dipole,self.predictedI)
        self.view.doubleSpinBox_p.setValue(float(self.predictedMomentum))
        self.view.doubleSpinBox_I.setValue(float(self.predictedI))

    def selectMom(self):
        #self.p = self.func.calcMom(self.Cmagnets,'S02-DIP01',self.I)
        #self.predictedMomentum = float(self.view.lineEdit_selectMom.text())
        self.predictedMomentum = float(self.view.doubleSpinBox_p.value())
        #self.view.label_predictMom.setText(self.predictedMomentum)
        self.predictedI = self.func.mom2I(self.Cmagnets, self.dipole,self.predictedMomentum)
        self.view.doubleSpinBox_p.setValue(float(self.predictedMomentum))
        self.view.doubleSpinBox_I.setValue(float(self.predictedI))

    def useCurrent(self):
        self.predictedI = self.Cmagnets.getSI(self.dipole)
        self.predictedMomentum = self.func.calcMom(self.Cmagnets,self.dipole,self.predictedI)
        self.view.doubleSpinBox_I.setValue(float(self.predictedI))
        #self.view.label_predictMom.setText(str(self.predictedMomentum))
        #self.predictedI = self.func.mom2I(self.Cmagnets, 'S02-DIP01',self.predictedMomentum)

    def useRF(self):
        print 'This does nothing yet'



    def roughGetCurrentRange(self):
        self.roughMinI = 0.8*self.predictedI
        self.roughMaxI = 1.2*self.predictedI
        self.view.lineEdit_roughCurrentMin.setText("%.2f" % self.roughMinI)
        self.view.lineEdit_roughCurrentMax.setText("%.2f" % self.roughMaxI)

    def roughGetRFRange(self):
        self.roughMinRF = self.predictedRF/2
        self.roughMaxRF = 1.05*self.predictedRF
        self.view.lineEdit_roughRFMin.setText("%.2f" % self.roughMinRF)
        self.view.lineEdit_roughRFMax.setText("%.2f" % self.roughMaxRF)

    # def fineGetCurrentRange(self):
    #     self.fineMinI = 0.95*self.predictedI
    #     self.fineMaxI = 1.05*self.predictedI
    #     self.view.lineEdit_fineCurrentMin.setText("%.2f" % self.fineMinI)
    #     self.view.lineEdit_fineCurrentMax.setText("%.2f" % self.fineMaxI)
    #
    # def fineGetRFRange(self):
    #     self.fineMinRF = 0.95*self.predictedRF
    #     self.fineMaxRF = 1.05*self.predictedRF
    #     self.view.lineEdit_fineRFMin.setText("%.2f" % self.fineMinRF)
    #     self.view.lineEdit_fineRFMax.setText("%.2f" % self.fineMaxRF)

    def fineGetCurrentRange_2(self):
        #self.fineMinI = 0.95*self.approxI
        #self.fineMaxI = 1.05*self.approxI
        self.view.lineEdit_fineCurrentMin.setText("%.2f" % self.fineMinI)
        self.view.lineEdit_fineCurrentMax.setText("%.2f" % self.fineMaxI)

    def fineGetRFRange_2(self):
        self.fineMinRF = 0.95*self.approxRF
        self.fineMaxRF = 1.05*self.approxRF
        self.view.lineEdit_fineRFMin.setText("%.2f" % self.fineMinRF)
        self.view.lineEdit_fineRFMax.setText("%.2f" % self.fineMaxRF)

    def setRoughMinI(self):
        self.roughMinI = float(self.view.lineEdit_roughCurrentMin.text())

    def setRoughMaxI(self):
        self.roughMaxI = float(self.view.lineEdit_roughCurrentMax.text())

    def setRoughMinRF(self):
        self.roughMinRF = float(self.view.lineEdit_roughRFMin.text())

    def setRoughMaxRF(self):
        self.roughMaxRF = float(self.view.lineEdit_roughRFMax.text())

    def setFineMinI(self):
        self.fineMinI = float(self.view.lineEdit_fineCurrentMin.text())

    def setFineMaxI(self):
        self.fineMaxI = float(self.view.lineEdit_fineCurrentMax.text())

    def setFineMinRF(self):
        self.fineMinRF = float(self.view.lineEdit_fineRFMin.text())

    def setFineMaxRF(self):
        self.fineMaxRF = float(self.view.lineEdit_fineRFMax.text())


    #Outline of Momentum Measurement Procedure
    # def measureMomentumPrelim_1(self):
    #     '''1. Preliminaries'''
    #     #if self.view.checkBox_1.isChecked()==True:
    #     print 'Read predicted momentum and calculate predicted current:'
    #     self.predictedMomentum = float(self.view.lineEdit_predictMom.text())
    #     print('Predicted Momentum: '+str(self.predictedMomentum))
    #     self.predictedI = self.func.mom2I(self.Cmagnets,
    #                                     'S02-DIP01',
    #                                     self.predictedMomentum)
    #     print('Predicted Current: '+str(self.predictedI))

    def measureMomentumPrelim_1(self):
        import bpm_recalibrate

    # def measureMomentumPrelim_2(self):
    #     print 'Close the laser shutters'
    #     #self.shut.close('SHUT01')
    #     self.shut.close('SHUT01')
    #     self.shut.close('SHUT02')

        #print 'Setting C2V dipole to zero'
        #self.Cmagnets.setSI('S02-DIP01',0)
        #time.sleep(1)

    def measureMomentumPrelim_3(self):
        self.view.checkBox.setCheckable(False)
        self.view.checkBox_2.setCheckable(False)
        print 'Close the laser shutters'
        #self.shut.close('SHUT01')
        self.shut.close('SHUT01')
        self.shut.close('SHUT02')
        #do degaussing
        print 'Degaussing...'
        self.Cmagnets.degauss(self.dipole,True)
        self.Cmagnets.degauss('S02-QUAD3',True)
        self.Cmagnets.degauss('S02-QUAD4',True)
        self.Cmagnets.degauss('S02-QUAD5',True)
        # while True:
        #     print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing('S02-QUAD3'), \
        #     self.Cmagnets.isDegaussing('S02-QUAD4'), self.Cmagnets.isDegaussing('S02-QUAD5')
        #     time.sleep(0.2)
        while (self.Cmagnets.isDegaussing(self.dipole)==False) and (self.Cmagnets.isDegaussing('S02-QUAD3')==False)\
        and (self.Cmagnets.isDegaussing('S02-QUAD4')==False) and (self.Cmagnets.isDegaussing('S02-QUAD5')==False):
            print 'Waiting to start degaussing...'
            print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing('S02-QUAD3'), \
            self.Cmagnets.isDegaussing('S02-QUAD4'), self.Cmagnets.isDegaussing('S02-QUAD5')
            time.sleep(0.2)
        while (self.Cmagnets.isDegaussing(self.dipole)==True) or (self.Cmagnets.isDegaussing('S02-QUAD3')==True)\
        or (self.Cmagnets.isDegaussing('S02-QUAD4')==True) or (self.Cmagnets.isDegaussing('S02-QUAD5')==True):
            print 'still degaussing...'
            print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing('S02-QUAD3'), \
            self.Cmagnets.isDegaussing('S02-QUAD4'), self.Cmagnets.isDegaussing('S02-QUAD5')
            time.sleep(0.2)
        print 'Degaussing finished'
        print 'Open the laser shutters'
        #self.shut.close('SHUT01')
        self.shut.open('SHUT01')
        self.shut.open('SHUT02')

    def measureMomentumPrelim_3_old(self):
        print 'Close the laser shutters'
        #self.shut.close('SHUT01')
        self.shut.close('SHUT01')
        self.shut.close('SHUT02')
        #do degaussing
        print 'Degaussing...'
        self.Cmagnets.degauss(self.dipole,True)
        self.Cmagnets.degauss('S02-QUAD3',True)
        self.Cmagnets.degauss('S02-QUAD4',True)
        self.Cmagnets.degauss('S02-QUAD5',True)
        time.sleep(1)
        while self.Cmagnets.isDegaussing(self.dipole) == False \
        and self.Cmagnets.isDegaussing('S02-QUAD3') == False \
        and self.Cmagnets.isDegaussing('S02-QUAD4') == False \
        and self.Cmagnets.isDegaussing('S02-QUAD5') == False:
            print 'waiting to start degaussing...'
            print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing('S02-QUAD3'), \
            self.Cmagnets.isDegaussing('S02-QUAD4'), self.Cmagnets.isDegaussing('S02-QUAD5')
            time.sleep(1)
        print 'started degaussing'
        print 'Is degaussing?', self.Cmagnets.isDegaussing(self.dipole)
        print 'Is degaussing?', self.Cmagnets.isDegaussing('S02-QUAD3')
        print 'Is degaussing?', self.Cmagnets.isDegaussing('S02-QUAD4')
        print 'Is degaussing?', self.Cmagnets.isDegaussing('S02-QUAD5')

        while self.Cmagnets.isDegaussing(self.dipole) == True \
        and self.Cmagnets.isDegaussing('S02-QUAD3') == True \
        and self.Cmagnets.isDegaussing('S02-QUAD4') == True \
        and self.Cmagnets.isDegaussing('S02-QUAD5') == True\
        and abs(self.Cmagnets.getSI(self.dipole)) > 0.1:
            print 'still degaussing...'
            #print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing('S02-QUAD3'), \
            #self.Cmagnets.isDegaussing('S02-QUAD4'), self.Cmagnets.isDegaussing('S02-QUAD5')
            print 'Dipole current = ', self.Cmagnets.getSI(self.dipole)
            time.sleep(1)
        print 'Open the laser shutters'
        #self.shut.close('SHUT01')
        self.shut.open('SHUT01')
        self.shut.open('SHUT02')

    # def measureMomentumPrelim_4(self):
    #     print 'Open the laser shutters'
    #     #self.shut.close('SHUT01')
    #     self.shut.open('SHUT01')
    #     self.shut.open('SHUT02')

        #print 'Setting C2V dipole to zero'
        #self.Cmagnets.setSI('S02-DIP01',0)
        #time.sleep(1)





    def measureMomentumAlign_1(self):
        self.view.checkBox.setCheckable(False)
        self.view.checkBox_2.setCheckable(False)
        '''2. Align Beam through Dipole'''
        #if self.view.checkBox_2.isChecked()==True:
        self.target1 = self.view.doubleSpinBox_x_1.value()
        self.tol1 = self.view.doubleSpinBox_tol_1.value()
        print 'Aligning on S02-BPM-02 with S02-HCOR-02'

        if (self.Cbpms.getXFromPV('S02-BPM02')-self.view.doubleSpinBox_x_1.value()) < self.view.doubleSpinBox_tol_1.value():
            self.func.align(self.Cmagnets,'S02-HCOR2',self.Cbpms,'S02-BPM02', self.target1, self.tol1, self.initialCurrentStep)
        else:
            print 'Already aligned'
        #self.func.align(self.Cmagnets,'S02-HCOR2',self.Cbpms,'S02-BPM02',0.5)

        #raw_input('Put in S02-YAG-02, then press enter')
        #print 'Aligning on S02-YAG-02 with S02-HCOR-02'
        #self.func.alignScreen(self.Cmagnets,'S02-HCOR1',self.camerasIA,'S02-CAM-01',13,0.5)

    def measureMomentumAlign_2_A(self):
        #pass
        #cameras.setCamera('C2V-CAM-01')
        ##self.selectedCamera = self.cameras.getSelectedIARef()

        #self.cameras = self.camdaqInit.physical_CLARA_Camera_DAQ_Controller()
        #self.camerasIA = self.camInit.physical_CLARA_Camera_IA_Controller()
        self.camNames = list(self.cam.getCameraNames())

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

        #15/8/18 reinstate this
        #print 'Switch to S02-CAM-02 - do it yourself for now'
        #print self.camNames
        self.camNames.remove('VIRTUAL_CATHODE')
        #print self.camNames

        for name in self.camNames:
            if self.cam.isAcquiring(name):
                #self.cam.setCamera(name)
                self.cam.stopAcquiring(name)
                time.sleep(1)
        #print name
        self.chosen_camera = 'S02-CAM-02'
        #self.cam.setCamera(self.chosen_camera)
        print 'Start acquiring', self.chosen_camera
        self.cam.startAcquiring(self.chosen_camera)
        #self.camerasIA.setCamera(self.chosen_camera)
        time.sleep(1)
        #ia = self.camerasIA.getSelectedIARef().IA
        #for x in dir(ia):
        #    print x, getattr(ia, x)

    def measureMomentumAlign_2_B(self):
        print 'in align 2 B - set mask'
        self.camNames = list(self.cam.getCameraNames())
        print self.camNames
        #cam1 = self.cam.getCameraObj('S02-CAM-02')
        screen = 'S02-CAM-02'
        print 'old values'
        print self.cam.getX(screen)
        print self.cam.getY(screen)
        print self.cam.getMaskX(screen)
        print self.cam.getMaskY(screen)
        print self.cam.getMaskXrad(screen)
        print self.cam.getMaskYrad(screen)
        time.sleep(1)
        print 'setting new values (commented out)'
        self.maskX = int(self.view.lineEdit_maskX.text())
        self.maskY = int(self.view.lineEdit_maskY.text())
        self.maskXRad = int(self.view.lineEdit_maskXRad.text())
        self.maskYRad = int(self.view.lineEdit_maskYRad.text())
        self.cam.setMaskX(self.maskX, screen)
        self.cam.setMaskY(self.maskY, screen)
        self.cam.setMaskXrad(self.maskXRad, screen)
        self.cam.setMaskYrad(self.maskYRad, screen)
        time.sleep(1)
        print 'new values'
        print self.cam.getX(screen)
        print self.cam.getY(screen)
        print self.cam.getMaskX(screen)
        print self.cam.getMaskY(screen)
        print self.cam.getMaskXrad(screen)
        print self.cam.getMaskYrad(screen)

        #self.camNames = list(self.cameras.getCameraNames())
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

    def measureMomentumAlign_2(self):
        #raw_input('Insert S02-YAG-02, then press enter')
        # Insert YAG
        print 'Insert S02-YAG-02'# **change back to -02**'
        screen = 'S02-SCR-02'
        print 'insert YAG'
        self.scrn.insertYAG(screen)
        print 'is screen in?', self.scrn.isYAGIn(screen)
        #self.scrn.moveScreenOut(screen)
        if self.scrn.isYAGIn(screen) is False:
            while True:
                isscreenmoving1 = self.scrn.isScreenMoving(screen)
                print 'Is screen moving?', isscreenmoving1
                QApplication.processEvents()
                time.sleep(1)
                isscreenmoving2 = self.scrn.isScreenMoving(screen)
                if isscreenmoving2 is False and isscreenmoving1 is True:
                    print 'Finished Moving!'
                    break
        else:
            pass

    def measureMomentumAlign_3(self):
        self.view.checkBox.setCheckable(False)
        self.view.checkBox_2.setCheckable(False)
        print 'Aligning on S02-YAG-02 with S02-HCOR-02'
        self.target2 = self.view.doubleSpinBox_x_2.value()
        self.tol2 = self.view.doubleSpinBox_tol_2.value()
        #print 'testing...'
        #print self.target2
        #print self.tol2
        #print self.initialCurrentStep
        if (self.cam.getX('S02-CAM-02')-self.view.doubleSpinBox_x_2.value()) < self.view.doubleSpinBox_tol_2.value():
            self.func.alignOnScreen(self.Cmagnets,'S02-HCOR1',self.cam,'S02-CAM-02',self.target2,self.tol2, self.initialCurrentStep) #was 0.000001
        else:
            print 'Already aligned'
        #self.func.alignOnScreen(self.Cmagnets,'S02-HCOR1',self.camerasIA,'S02-CAM-01',13,0.5)

    def measureMomentumAlign_4(self):
        if (self.cam.getX('S02-CAM-02')-self.view.doubleSpinBox_x_2.value()) < self.view.doubleSpinBox_tol_2.value():
            self.view.checkBox.setCheckable(True)
            self.view.checkBox.setChecked(True)
            #self.view.checkBox.setCheckable(False)

        print 'Retract S02-YAG-02'# **change back to -02**'
        screen = 'S02-SCR-02'
        #self.scrn.moveScreenTo(screen,scrn.SCREEN_STATE.V_RETRACTED)
        self.scrn.moveScreenTo(screen,scrn.SCREEN_STATE.V_RF)
        #time.sleep(5)
        if self.scrn.isYAGIn(screen) is True:
            while True:
                isscreenmoving1 = self.scrn.isScreenMoving(screen)
                print 'Is screen moving?', isscreenmoving1
                QApplication.processEvents()
                time.sleep(1)
                isscreenmoving2 = self.scrn.isScreenMoving(screen)
                if isscreenmoving2 is False and isscreenmoving1 is True:
                    print 'Finished Moving!'
                    break
        elif self.scrn.isYAGIn(screen) is False:
            print 'Screen already out'
        else:
            print 'Error moving screen'

        if (self.Cbpms.getXFromPV('S02-BPM02')-self.view.doubleSpinBox_x_1.value()) < self.view.doubleSpinBox_tol_1.value():
            self.view.checkBox_2.setCheckable(True)
            self.view.checkBox_2.setChecked(True)
            #self.view.checkBox.setCheckable(False)
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
        self.I = self.func.bendBeam(self.Cmagnets,self.dipole,
                                    self.Cbpms,'C2V-BPM01',
                                    'YAG01',
                                     self.fineMinI, self.fineMaxI, 0.1)#0.00001                 # tol=0.0001 (metres)
        self.p = self.func.calcMom(self.Cmagnets,self.dipole,self.I)
        print self.p

    def measureMomentumCentreC2V_2(self):
        '''3. Centre in Spec. Line using screen'''
        #if self.view.checkBox_3.isChecked()==True:
        self.I = self.func.bendBeamScreen(self.Cmagnets,self.dipole,
                                    'C2V-CAM-01',
                                     self.fineMinI, self.fineMaxI, 0.1)#0.00001                 # tol=0.0001 (metres)
        self.p = self.func.calcMom(self.Cmagnets,self.dipole,self.I)
        print self.p

    def measureMomentumCentreC2VApprox(self):
        '''3. Centre in Spec. Line'''
        #if self.view.checkBox_3.isChecked()==True:
        # self.tol3 = self.view.doubleSpinBox_tol_3.value()
        # self.approxI = self.func.bendBeamApprox(self.Cmagnets,self.dipole,
        #                             self.Cbpms,'C2V-BPM01',
        #                             'YAG01',
        #                              self.roughMinI, self.roughMaxI, self.tol3)#0.00001                 # tol=0.0001 (metres)
        self.approxI = self.findDipoleCurrent()
        self.approx_p = self.func.calcMom(self.Cmagnets,self.dipole,self.approxI)
        #print self.approx_p

        #######################################################################
        # based on AutoPhaseCalibv2 model 22/8/18
    def findDipoleCurrent(self):
        # initialise variables for the plots
        # scan 1 - rough scan c2v dipole
        self.dipCurrent = []
        self.BPMPosition = []

        #self.startingDipole = self.Cmagnets.getSI(self.dipole)
        #self.Cmagnets.getSI(self.dipole)
        self.sleepTimeDipole = 0.1
        self.sleepTime = 0.05
        # need to reset data array
        #self.resetDataArray()
        if self.view.comboBox_selectRF.currentIndex() == 0: # gun
            self.dipoleIStep = 0.1
            self.nSamples = 10
            self.getDataFunction = partial(self.func.getBPMPosition, self.Cbpms,'C2V-BPM01')
            #self.getDataFunction = partial(self.func.getXBPM, self.Cbpms,'C2V-BPM01', self.nSamples)
        elif self.view.comboBox_selectRF.currentIndex() == 1: # linac
            self.dipoleIStep = 1
            self.nSamples = 3
            self.getDataFunction = partial(self.func.getBPMPosition, self.Cbpms,'C2V-BPM01')
            #self.getDataFunction = partial(self.func.getXBPM, self.Cbpms,'C2V-BPM01', self.nSamples)

        range = np.arange(self.roughMinI, self.roughMaxI, self.dipoleIStep)
        # data_started = False
        # len_data=[]
        for i,I in enumerate(range):
            print 'I = ', I
            #self.progress.emit(100*i/len(range))
            #if self._abort or self._finished:
            #    return
            self.Cmagnets.setSI(self.dipole, I)
            #self.Cmagnets.getSI(self.dipole)
            while abs(self.Cmagnets.getSI(self.dipole) - I) > 0.05:
                print 'Waiting for dipole, set=', I, 'read=', self.Cmagnets.getSI(self.dipole), 'diff=', abs(self.Cmagnets.getSI(self.dipole) - I)
                QApplication.processEvents()
                time.sleep(self.sleepTimeDipole)
            data, stddata = self.getData() # could replace getData->func.getBPMPosition with func.getXBPM
            print 'data stddata', data, stddata
            if data != 20:
                self.dipCurrent.append(I)
                self.BPMPosition.append(data)
                #data_started = True
            QApplication.processEvents()
            #len_data.append(len(self.dipCurrent2))
            # if data_started == True and len(self.dipCurrent) > 10 and len_data[-1] == len_data[-2] and len_data[-2] == len_data[-3]:
            #     print 'breaking'
            #     break

            #time.sleep(0.1)
            #self.appendDataArray(I, data, stddata)

        #self.doFitDipoleCurrent() #need to add this in
        #self.machine.setDip(self.startingDipole)
        # self.Cmagnets.setSI(self.dipole, self.startingDipole)
        # while abs(self.Cmagnets.getSI(self.dipole) - self.startingDipole) > 0.2:
        #     time.sleep(self.sleepTimeDipole)
        if len(self.BPMPosition) > 1:
            arg_min = np.argmin(self.BPMPosition)
            arg_max = np.argmax(self.BPMPosition)
            #print 'argmax = ', arg_min, self.BPMPosition[arg_min], self.dipCurrent[arg_min]
            #print 'argmax = ', arg_max, self.BPMPosition[arg_max], self.dipCurrent[arg_max]
            self.fineMinI = self.dipCurrent[arg_min]
            self.fineMaxI = self.dipCurrent[arg_max]
            approxI =  (self.dipCurrent[arg_min]+self.dipCurrent[arg_max])/2
            self.fineGetCurrentRange_2()
            self.Cmagnets.setSI(self.dipole, approxI)
            while abs(self.Cmagnets.getSI(self.dipole) - approxI) > 0.2:
                time.sleep(self.sleepTimeDipole)
            return approxI
        else:
            print 'No signal found'
            return 0

    def measureMomentumAlign_1_A(self):
        self.view.checkBox.setCheckable(False)
        self.view.checkBox_2.setCheckable(False)
        '''3. Centre in Spec. Line'''
        self.approxIcor2 = self.findBPMSignal()
        print self.approxIcor2
        #self.approx_p = self.func.calcMom(self.Cmagnets,self.dipole,self.approxI)

    def findBPMSignal(self):
        # scan 2 - scan S02-HCOR2
        self.dipCurrent2 = []
        self.BPMPosition2 = []

        #self.startingHCOR = self.Cmagnets.getSI(self.cor2)
        #self.Cmagnets.getSI(self.dipole)
        self.sleepTimeDipole = 0.1
        self.sleepTime = 0.05

        # if self.view.comboBox_selectRF.currentIndex() == 0: # gun
        self.dipoleIStep = 0.2
        self.nSamples = 3
        self.getDataFunction = partial(self.func.getBPMPosition, self.Cbpms,'S02-BPM02')

        range = np.arange(-3, 3, self.dipoleIStep)
        data_started = False
        # #len1 = 0
        # #len2 = 0
        len_data=[]
        for i,I in enumerate(range):
            #len1 = len2
            print 'I = ', I
            self.Cmagnets.setSI(self.cor2, I)

            while abs(self.Cmagnets.getRI(self.cor2) - I) > 0.05:
                print 'Waiting for corrector, set=', I, 'read=', self.Cmagnets.getRI(self.cor2), 'diff=', abs(self.Cmagnets.getRI(self.cor2) - I)
                time.sleep(self.sleepTimeDipole)
                QApplication.processEvents()
            #print self.Cmagnets.getSI(self.cor2), self.Cmagnets.getRI(self.cor2)
            data, stddata = self.getData()
            print 'data stddata', data, stddata
            if data != 20:
                self.dipCurrent2.append(I)
                self.BPMPosition2.append(data)
                data_started = True
            QApplication.processEvents()
            print len(self.dipCurrent2)
            len_data.append(len(self.dipCurrent2))
            print len_data
            if data_started == True and len(self.dipCurrent2) > 3 and len_data[-1] == len_data[-2] and len_data[-2] == len_data[-3]:
                break


        arg_min = np.argmin(self.BPMPosition2)
        arg_max = np.argmax(self.BPMPosition2)

        #self.fineMinI = self.dipCurrent[arg_min]
        #self.fineMaxI = self.dipCurrent[arg_max]
        #approxI =  (self.dipCurrent2[arg_min]+self.dipCurrent2[arg_max])/2
        # find position nearest zero
        centre = 0
        print abs(np.array(self.BPMPosition2) - centre)
        arg_centre = (np.abs(np.array(self.BPMPosition2) - centre)).argmin()
        approxI = self.dipCurrent2[arg_centre]
        #self.fineGetCurrentRange_2()
        self.Cmagnets.setSI(self.cor2, approxI)
        while abs(self.Cmagnets.getSI(self.cor2) - approxI) > 0.2:
            time.sleep(self.sleepTimeDipole)
        return approxI


		#self.progress.emit(100)

    # def appendDataArray(self, x, y, yStd):
    #     self.crestingData[self.cavity][self.actuator]['xData'].append(x)
    #     self.crestingData[self.cavity][self.actuator]['yData'].append(y)
    #     self.crestingData[self.cavity][self.actuator]['yStd'].append(yStd)
	# 	#self.newData.emit()

    def getData(self):
        # self.data = []
        # while len(self.data) < 2:
        # 	self.data.append(self.getDataFunction())
        # 	time.sleep(self.sleepTime)
        time.sleep(self.sleepTime)
        self.data = []
        while len(self.data) < self.nSamples:
            self.data.append(self.getDataFunction())
            time.sleep(self.sleepTime)
        #print 'ingetData', np.mean(self.data), np.std(self.data)
        return [np.mean(self.data), np.std(self.data)] if np.std(self.data) > 0.001 else [20,0]

    def abort(self):
        self._abort = True

    def finish(self):
        self._finished = True

    def resetAbortFinish(self):
        self._abort = False
        self._finished = False

        #######################################################################

    def measureMomentumCalcMom(self):
        # moved functionality into measureMomentumCentreC2V
        '''4. Convert Current to Momentum'''
        #if self.view.checkBox_4.isChecked()==True:
            #self.PL.info('4. Calculate Momentum')
        self.p = self.func.calcMom(self.Cmagnets,self.dipole,self.I)
        print self.p


    def degaussC2V(self):
        pass
        #do degaussing
        print 'Degaussing...'
        #self.Cmagnets.degauss(self.dipole,True)
        self.Cmagnets.degauss('C2V-QUAD1',True)
        self.Cmagnets.degauss('C2V-QUAD2',True)
        self.Cmagnets.degauss('C2V-QUAD3',True)
        while self.Cmagnets.isDegaussing('C2V-QUAD1') and self.Cmagnets.isDegaussing('C2V-QUAD2') and self.Cmagnets.isDegaussing('C2V-QUAD3'):
            print 'still degaussing...'
            time.sleep(1)

    def insertC2VScreen(self):
        #raw_input('Insert S02-YAG-02, then press enter')
        # Insert YAG
        print 'Insert C2V-YAG-01'# **change back to -02**'
        screen = 'C2V-SCR-01'
        #print 'insert YAG'
        self.scrn.insertYAG(screen)
        print 'is screen in?', self.scrn.isYAGIn(screen)
        #self.scrn.moveScreenOut(screen)
        if self.scrn.isYAGIn(screen) is False:
            while True:
                isscreenmoving1 = self.scrn.isScreenMoving(screen)
                print 'Is screen moving?', isscreenmoving1
                QApplication.processEvents()
                time.sleep(1)
                isscreenmoving2 = self.scrn.isScreenMoving(screen)
                if isscreenmoving2 is False and isscreenmoving1 is True:
                    print 'Finished Moving!'
                    break
        else:
            pass

    def camState2C2V(self):
        self.camNames = list(self.cam.getCameraNames())
        self.camNames.remove('VIRTUAL_CATHODE')
        #print self.camNames

        for name in self.camNames:
            if self.cam.isAcquiring(name):
                #self.cam.setCamera(name)
                self.cam.stopAcquiring(name)
                time.sleep(1)
        #print name
        self.chosen_camera = 'C2V-CAM-01'
        #self.cam.setCamera(self.chosen_camera)
        print 'Start acquiring', self.chosen_camera
        self.cam.startAcquiring(self.chosen_camera)
        #self.camerasIA.setCamera(self.chosen_camera)
        time.sleep(1)
        #ia = self.camerasIA.getSelectedIARef().IA
        #for x in dir(ia):
        #    print x, getattr(ia, x)

    def retractC2VScreen(self):
        print 'Retract C2V-YAG-01'# **change back to -02**'
        screen = 'C2V-SCR-01'
        self.scrn.moveScreenTo(screen,scrn.SCREEN_STATE.V_RETRACTED)
        #time.sleep(5)
        if self.scrn.isYAGIn(screen) is True:
            while True:
                isscreenmoving1 = self.scrn.isScreenMoving(screen)
                print 'Is screen moving?', isscreenmoving1
                QApplication.processEvents()
                time.sleep(1)
                isscreenmoving2 = self.scrn.isScreenMoving(screen)
                if isscreenmoving2 is False and isscreenmoving1 is True:
                    print 'Finished Moving!'
                    break
        else:
            pass

    #Outline of Momentum Spread Measurement Procedure
    def measureMomentumSpreadChecks(self):
        if self.view.checkBox_done_mom.isChecked()==True:
            #1. Checks
            #if self.view.checkBox_1_s.isChecked()==True:
            """1. Checks"""
            #self.p=34.41
            self.I=self.func.mom2I(self.Cmagnets,self.dipole,self.p)
            self.Cmagnets.setSI(self.dipole,self.I)
            print 'measureMomentum(step 1), p = ', str(self.p)

    def measureMomentumSpreadMinBeta(self):
        """2. Minimise Beta"""
        #if self.view.checkBox_2_s.isChecked()==True:
        #2.1 Minimize Beta
        ##self.func.minimizeBeta(self.Cmagnets,'S02-QUAD3',
        #                        None,'CLA-C2V-DIA-CAM-01',1)
        quad1max = 0.5
        quad2max = 0.5
        steps=5
        self.func.minimizeBeta2D(self.Cmagnets,'S02-QUAD1','S02-QUAD2',
                                quad1max,quad2max,steps,None,'CLA-C2V-DIA-CAM-01',1)
        #self.func.using_move_to_thread(self.Cmagnets,'S02-QUAD3',
        #                        None,'VM-CLA-C2V-DIA-CAM-01',1)
        #'''Re-instate minimising beta with Quad-04 here!!!'''
        #self.func.minimizeBeta2(self.Cmagnets,'S02-QUAD4',
        #                        None,'VM-CLA-C2V-DIA-CAM-01',-1)
        #2.2 Set Dispersion Size on Spec Line
        self.Cmagnets.setSI(self.dipole,self.I)
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
                                                self.dipole,
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

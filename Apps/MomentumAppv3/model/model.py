#from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
#from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QObject
from PyQt4.QtGui import QApplication
import datetime
import momentumFunctions
from functools import partial
import numpy as np
import time

import sys
sys.path.append('../../../../Controllers/bin/Release')

import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_Screen_Control as scrn
import VELA_CLARA_Camera_Control as cam
import VELA_CLARA_Shutter_Control as shut

sys.path.append('../../../')
import Software.Procedures.linacTiming as linacTiming
#MCRDELL10
#sys.path.append('../../Procedures')
#import linacTiming


class Model(QObject):
    def __init__(self,app,view,data):
        super(Model, self).__init__()
        self.app = app
        self.view = view
        self.data = data
        self.func = momentumFunctions.Functions(self)

        self.magInit = mag.init()
        self.Cmagnets = self.magInit.physical_CB1_Magnet_Controller()
        self.dipole = 'S02-DIP01'
        self.cor1 = 'S02-HCOR1'
        self.cor2 = 'S02-HCOR2'
        self.s02_quad3 = 'S02-QUAD3'
        self.s02_quad4 = 'S02-QUAD4'
        self.s02_quad5 = 'S02-QUAD5'

        self.bpmInit = bpm.init()
        self.Cbpms = self.bpmInit.physical_C2B_BPM_Controller()
        self.C2Vbpm = 'C2V-BPM01'
        self.S02bpm = 'S02-BPM02'

        self.llrfInit = llrf.init()
        self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
        self.linac1 = self.llrfInit.physical_L01_LLRF_Controller()
        self.Linac01Timing = linacTiming.Linac01Timing()

        self.scrnInit = scrn.init()
        self.scrn = self.scrnInit.physical_C2B_Screen_Controller()
        self.S02screen = 'S02-SCR-02'

        self.camInit = cam.init()
        self.cam = self.camInit.physical_CLARA_Camera_Controller()
        self.S02cam = 'S02-CAM-02'
        self.C2Vcam = 'C2V-CAM-01'

        self.shutInit = shut.init()
        self.shut = self.shutInit.physical_PIL_Shutter_Controller()
        self.shut1 = 'SHUT01'
        self.shut2 = 'SHUT02'

        self.dipCurrent=[]
        self.BPMPosition=[]

        self.dCurrents =[]
        self.dPositions=[]
        self.fCurrents =[]
        self.fPositions=[]
        self.Dispersion=0.
        self.pSpread = 0.

################################################################################
# Converter functions

    def changeBox_p(self, y):
        self.data.values['I_c'] = y
        try:
            self.view.doubleSpinBox_p.valueChanged[float].disconnect(self.changeBox_I)
        except:
            pass
        self.data.values['p_c'] = self.func.I2mom(self.Cmagnets, self.dipole, y)
        self.view.doubleSpinBox_p.setValue(self.data.values['p_c'])
        self.view.doubleSpinBox_p.valueChanged[float].connect(self.changeBox_I)
        print str(datetime.datetime.now())[:-7], ', Converter: I =', self.data.values['I_c'], 'A, p =', self.data.values['p_c'], 'MeV/c'

    def changeBox_I(self, y):
        self.data.values['p_c'] = y
        try:
            self.view.doubleSpinBox_I.valueChanged[float].disconnect(self.changeBox_p)
        except:
            pass
        self.data.values['I_c'] = self.func.mom2I(self.Cmagnets, self.dipole, y)
        self.view.doubleSpinBox_I.setValue(self.data.values['I_c'])
        self.view.doubleSpinBox_I.valueChanged[float].connect(self.changeBox_p)
        print str(datetime.datetime.now())[:-7], ', Converter: I =', self.data.values['I_c'], 'A, p =', self.data.values['p_c'], 'MeV/c'

################################################################################
# Prediction functions

    def useCurrent(self):
        #self.predictedI = self.Cmagnets.getSI(self.dipole)
        self.data.values['I_predict'] = self.Cmagnets.getSI(self.dipole)
        self.data.values['p_predict'] = self.func.I2mom(self.Cmagnets,self.dipole,self.data.values['I_predict'])
        self.view.doubleSpinBox_I_predict.setValue(self.data.values['I_predict'])
        #self.view.doubleSpinBox_p_predict.setValue(self.data.values['p_predict'])

    def useRF(self):
        print 'This simply checks the linac timing: if gun only => 5 MeV/c, gun+linac =>35.5MeV/c'
        if self.Linac01Timing.isLinacOn() == True:
            self.data.values['p_predict'] = 35.5
        else:
            self.data.values['p_predict'] = 5
        self.data.values['I_predict'] = self.func.mom2I(self.Cmagnets,self.dipole,self.data.values['p_predict'])
        self.view.doubleSpinBox_p_predict.setValue(self.data.values['p_predict'])

    def changeBox_p_predict(self, y):
        self.data.values['I_predict'] = y
        try:
            self.view.doubleSpinBox_p_predict.valueChanged[float].disconnect(self.changeBox_I_predict)
        except:
            pass
        self.data.values['p_predict'] = self.func.I2mom(self.Cmagnets, self.dipole, y)
        self.view.doubleSpinBox_p_predict.setValue(self.data.values['p_predict'])
        self.view.doubleSpinBox_p_predict.valueChanged[float].connect(self.changeBox_I_predict)
        print str(datetime.datetime.now())[:-7], ', Prediction: I =', self.data.values['I_predict'], 'A, p =', self.data.values['p_predict'], 'MeV/c'

    def changeBox_I_predict(self, y):
        self.data.values['p_predict'] = y
        try:
            self.view.doubleSpinBox_I_predict.valueChanged[float].disconnect(self.changeBox_p_predict)
        except:
            pass
        self.data.values['I_predict'] = self.func.mom2I(self.Cmagnets, self.dipole, y)
        self.view.doubleSpinBox_I_predict.setValue(self.data.values['I_predict'])
        self.view.doubleSpinBox_I_predict.valueChanged[float].connect(self.changeBox_p_predict)
        print str(datetime.datetime.now())[:-7], ', Prediction: I =', self.data.values['I_predict'], 'A, p =', self.data.values['p_predict'], 'MeV/c'

################################################################################
# Rough measure functions

    def setRoughStep(self, y):
        self.data.values['rough_step'] = y
        print 'Rough dipole step size = ', self.data.values['rough_step']

    def get_p_rough(self):
        self.data.values['I_rough'] = self.Cmagnets.getSI(self.dipole)
        self.data.values['p_rough'] = self.func.I2mom(self.Cmagnets,self.dipole,self.data.values['I_rough'])
        self.view.label_p_rough.setText(str(self.data.values['p_rough']))
        print str(datetime.datetime.now())[:-7], ', Rough measurement: I =', self.data.values['I_rough'], 'A, p =', self.data.values['p_rough'], 'MeV/c'

    def roughGetCurrentRange(self):
        #self.roughMinI = 0.8*self.predictedI
        #self.roughMaxI = 1.2*self.predictedI
        try:
            #print 'Predicted momentum = ', self.data.values['p_predict']
            self.data.values['roughIMin'] = 0.8*self.data.values['I_predict']
            self.data.values['roughIMax'] = 1.1*self.data.values['I_predict']
            self.data.values['roughIStep'] = 0.01*self.data.values['I_predict']
            #self.view.lineEdit_roughCurrentMin.setText("%.2f" % self.data.values['roughMinI'])
            #self.view.lineEdit_roughCurrentMax.setText("%.2f" % self.data.values['roughMaxI'])
            #self.view.lineEdit_roughCurrentStep.setText("%.2f" % self.data.values['roughStepI'])
            self.view.doubleSpinBox_roughIMin.setValue(self.data.values['roughIMin'])
            self.view.doubleSpinBox_roughIMax.setValue(self.data.values['roughIMax'])
            self.view.doubleSpinBox_roughIStep.setValue(self.data.values['roughIStep'])
        except:
            print 'Needs a predicted momentum'

    def roughIMin(self, y):
        self.data.values['roughIMin'] = y
        print 'Rough scan minimum current = ', self.data.values['roughIMin']

    def roughIMax(self, y):
        self.data.values['roughIMax'] = y
        print 'Rough scan maximum current = ', self.data.values['roughIMax']

    def roughIStep(self, y):
        self.data.values['roughIStep'] = y
        print 'Rough scan step size = ', self.data.values['roughIStep']

    def dipole_current_up(self):
        self.func.stepCurrent(self.Cmagnets,self.dipole,self.data.values['rough_step'])

    def dipole_current_down(self):
        self.func.stepCurrent(self.Cmagnets,self.dipole,-self.data.values['rough_step'])

    def measureMomentumCentreC2VApprox(self):
        '''3. Centre in Spec. Line'''
        self.data.values['I_scan_centre'] = self.findDipoleCurrent()
        self.data.values['p_scan_centre'] = self.func.I2mom(self.Cmagnets,self.dipole, self.data.values['I_scan_centre'])
        print str(datetime.datetime.now())[:-7], ', Rough scan centre: I =', self.data.values['I_scan_centre'], 'A, p =', self.data.values['p_scan_centre'], 'MeV/c'

        #######################################################################
        # based on AutoPhaseCalibv2 model 22/8/18
    def findDipoleCurrent(self):
        # initialise variables for the plots
        # scan 1 - rough scan c2v dipole
        self.dipCurrent = []
        self.BPMPosition = []

        self.sleepTimeDipole = 0.1
        self.sleepTime = 0.05

        # if self.view.comboBox_selectRF.currentIndex() == 0: # gun
        #     self.dipoleIStep = 0.1
        #     self.nSamples = 10
        #     self.getDataFunction = partial(self.func.getBPMPosition, self.Cbpms,'C2V-BPM01')
        # elif self.view.comboBox_selectRF.currentIndex() == 1: # linac
        #     self.dipoleIStep = 1
        #     self.nSamples = 3
        #     self.getDataFunction = partial(self.func.getBPMPosition, self.Cbpms,'C2V-BPM01')
        self.nSamples = 5
        self.getDataFunction = partial(self.func.getBPMPosition, self.Cbpms, self.C2Vbpm)
        self.roughMinI = self.data.values['roughIMin']
        self.roughMaxI = self.data.values['roughIMax']
        self.dipoleIStep = self.data.values['roughIStep']

        range = np.arange(self.roughMinI, self.roughMaxI, self.dipoleIStep)
        for i,I in enumerate(range):
            print 'I = ', I
            self.Cmagnets.setSI(self.dipole, I)
            while abs(self.Cmagnets.getSI(self.dipole) - I) > 0.05:
                print 'Waiting for dipole, set=', I, 'read=', self.Cmagnets.getSI(self.dipole), 'diff=', abs(self.Cmagnets.getSI(self.dipole) - I)
                QApplication.processEvents()
                time.sleep(self.sleepTimeDipole)
            data, stddata = self.getData() # could replace getData->func.getBPMPosition with func.getXBPM
            #print 'data stddata', data, stddata
            if data != 20:
                self.dipCurrent.append(I)
                self.BPMPosition.append(data)
            QApplication.processEvents()

        if len(self.BPMPosition) > 1:
            arg_min = np.argmin(self.BPMPosition)
            arg_max = np.argmax(self.BPMPosition)
            self.fineMinI = self.dipCurrent[arg_min]
            self.fineMaxI = self.dipCurrent[arg_max]
            approxI =  (self.dipCurrent[arg_min]+self.dipCurrent[arg_max])/2
            #self.fineGetCurrentRange_2() # set range for fine scan
            self.Cmagnets.setSI(self.dipole, approxI)
            while abs(self.Cmagnets.getSI(self.dipole) - approxI) > 0.2:
                time.sleep(self.sleepTimeDipole)
            #print 'approxI', approxI
            return approxI
        else:
            print 'No signal found'
            return 0

    def getData(self):
        time.sleep(self.sleepTime)
        self.dat = []
        while len(self.dat) < self.nSamples:
            self.dat.append(self.getDataFunction())
            time.sleep(self.sleepTime)
        return [np.mean(self.dat), np.std(self.dat)] if np.std(self.dat) > 0.001 else [20,0]

################################################################################
# Rough set functions
    def p_rough_set(self, y):
        self.data.values['p_rough_set'] = y
        self.data.values['I_rough_set'] = self.func.mom2I(self.Cmagnets,self.dipole,self.data.values['p_rough_set'])
        #self.view.label_p_rough.setText(str(self.data.values['p_rough']))
        self.view.doubleSpinBox_I_2.setValue(self.data.values['I_rough_set'])
        print str(datetime.datetime.now())[:-7], ', Rough set: I =', self.data.values['I_rough_set'], 'A, p =', self.data.values['p_rough_set'], 'MeV/c'

    def set_I_rough(self):
        self.func.setCurrent(self.Cmagnets, self.dipole, self.data.values['I_rough_set'])

    def setRoughSetStep(self, y):
        self.data.values['rough_set_step'] = y
        print 'Rough set step size = ', self.data.values['rough_set_step']

    def select_gun(self):
        self.data.values['RFmode_rough'] = 'Gun'
        self.view.lineEdit_RFmode_rough.setText(self.data.values['RFmode_rough'])

    def select_linac(self):
        self.data.values['RFmode_rough'] = 'Linac'
        self.view.lineEdit_RFmode_rough.setText(self.data.values['RFmode_rough'])

    def RF_amplitude_up(self):
        if self.data.values['RFmode_rough'] == 'Gun':
            rfmode = self.gun
        elif self.data.values['RFmode_rough'] == 'Linac':
            rfmode = self.linac1
        else:
            print 'RF mode not selected'
        self.func.stepRF(rfmode,self.data.values['rough_set_step'])

    def RF_amplitude_down(self):
        if self.data.values['RFmode_rough'] == 'Gun':
            rfmode = self.gun
        elif self.data.values['RFmode_rough'] == 'Linac':
            rfmode = self.linac1
        else:
            print 'RF mode not selected'
        self.func.stepRF(rfmode,-self.data.values['rough_set_step'])


################################################################################
# Alignment functions
    def degauss(self):
        #self.view.checkBox.setCheckable(False)
        #self.view.checkBox_2.setCheckable(False)
        print 'Close the laser shutters'
        #self.shut.close('SHUT01')
        self.shut.close(self.shut1)
        self.shut.close(self.shut2)
        #do degaussing
        print 'Degaussing...'
        #QApplication.processEvents()
        self.Cmagnets.degauss(self.dipole,True)
        self.Cmagnets.degauss(self.s02_quad3,True)
        self.Cmagnets.degauss(self.s02_quad4,True)
        self.Cmagnets.degauss(self.s02_quad5,True)
        # while True:
        #     print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing(self.s02_quad3), \
        #     self.Cmagnets.isDegaussing('S02-QUAD4'), self.Cmagnets.isDegaussing('S02-QUAD5')
        #     time.sleep(0.2)
        while (self.Cmagnets.isDegaussing(self.dipole)==False) and (self.Cmagnets.isDegaussing(self.s02_quad3)==False)\
        and (self.Cmagnets.isDegaussing(self.s02_quad4)==False) and (self.Cmagnets.isDegaussing(self.s02_quad5)==False):
            print 'Waiting to start degaussing...'
            #print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing(self.s02_quad3), \
            #self.Cmagnets.isDegaussing(self.s02_quad4), self.Cmagnets.isDegaussing(self.s02_quad5)
            time.sleep(0.2)
            #QApplication.processEvents()
        while (self.Cmagnets.isDegaussing(self.dipole)==True) or (self.Cmagnets.isDegaussing(self.s02_quad3)==True)\
        or (self.Cmagnets.isDegaussing(self.s02_quad4)==True) or (self.Cmagnets.isDegaussing(self.s02_quad5)==True):
            print 'still degaussing...'
            #print self.Cmagnets.isDegaussing(self.dipole), self.Cmagnets.isDegaussing(self.s02_quad3), \
            #self.Cmagnets.isDegaussing(self.s02_quad4), self.Cmagnets.isDegaussing(self.s02_quad5)
            time.sleep(0.2)
            #QApplication.processEvents()
        print 'Degaussing finished'
        print 'Open the laser shutters'
        #self.shut.close('SHUT01')
        self.shut.open(self.shut1)
        self.shut.open(self.shut2)

    def measureMomentumAlign_1(self):
        #self.view.checkBox.setCheckable(False)
        #self.view.checkBox_2.setCheckable(False)
        #'''2. Align Beam through Dipole'''
        #if self.view.checkBox_2.isChecked()==True:
        self.target1 = self.data.values['target1']
        self.tol1 = self.data.values['tol1']
        print 'Aligning on S02-BPM-02 with S02-HCOR-02'
        #print 'Delta x = ', self.Cbpms.getXFromPV('S02-BPM02')-self.view.doubleSpinBox_x_1.value()
        #print 'Tolerance = ', self.view.doubleSpinBox_tol_1.value()
        print 'offset', (self.Cbpms.getXFromPV(self.S02bpm) - self.target1)
        print 'tolerance', self.tol1
        self.initialCurrentStep = 0.1 # MAKE THIS MOMEMTUM-DEPENDENT
        if abs((self.Cbpms.getXFromPV(self.S02bpm) - self.target1)) > self.tol1:
            self.func.align(self.Cmagnets, self.cor2, self.Cbpms, self.S02bpm, self.target1, self.tol1, self.initialCurrentStep)
        else:
            print 'Already aligned'


    def setFineStep1(self, y):
        self.data.values['fine_step1'] = y
        print 'S02-HCOR01 step size = ', self.data.values['fine_step1']

    def setFineStep2(self, y):
        self.data.values['fine_step2'] = y
        print 'S02-HCOR02 step size = ', self.data.values['fine_step2']

    def cor2_current_up(self):
        self.func.stepCurrent(self.Cmagnets,self.cor2,self.data.values['fine_step2'])

    def cor2_current_down(self):
        self.func.stepCurrent(self.Cmagnets,self.cor2,-self.data.values['fine_step2'])

    def insertYAG(self):
        print 'Switch to S02-YAG-02'
        self.measureMomentumAlign_2_A()
        print 'Insert S02-YAG-02 (screen controls not reliable yet, use control system if necessary)'
        screen = self.S02screen
        #print 'insert YAG'
        #self.scrn.insertYAG(screen)
        print 'Screen state is: ', self.scrn.getScreenState(screen)#self.scrn.isYAGIn(screen)
        print 'Is YAG in? ', self.scrn.isYAGIn(screen)
        print 'ACTPOS = ', self.scrn.getACTPOS(self.S02screen)
        print 'YAG pos = ', self.scrn.getDevicePosition(self.S02screen, scrn.SCREEN_STATE.V_YAG)
        #self.scrn.moveScreenOut(screen)
        #if self.scrn.isYAGIn(screen) is False:
        if str(self.scrn.getScreenState(screen)) != 'V_YAG':
            self.scrn.moveScreenTo(screen,scrn.SCREEN_STATE.V_YAG)
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

    def measureMomentumAlign_2_A(self):
        self.camNames = list(self.cam.getCameraNames())
        self.camNames.remove('VIRTUAL_CATHODE')

        for name in self.camNames:
            if self.cam.isAcquiring(name):
                self.cam.stopAcquiring(name)
                time.sleep(1)
        #print name
        self.chosen_camera = self.S02cam
        #self.cam.setCamera(self.chosen_camera)
        print 'Start acquiring', self.chosen_camera
        self.cam.startAcquiring(self.chosen_camera)
        #self.camerasIA.setCamera(self.chosen_camera)
        time.sleep(1)


    def measureMomentumAlign_3(self):
        #self.view.checkBox.setCheckable(False)
        #self.view.checkBox_2.setCheckable(False)
        print 'Aligning on S02-YAG-02 with S02-HCOR-02'
        self.target2 = self.data.values['target2']
        self.tol2 = self.data.values['tol2']
        #print 'testing...'
        #print self.target2
        #print self.tol2
        #print self.initialCurrentStep
        self.initialCurrentStep = 0.1 # MAKE THIS MOMEMTUM-DEPENDENT
        if abs(self.cam.getX(self.S02cam) - self.target2) > self.tol2:
            self.func.alignOnScreen(self.Cmagnets, self.cor1, self.cam, self.S02cam, self.target2, self.tol2, self.initialCurrentStep) #was 0.000001
        else:
            print 'Already aligned'

    def retractYAG(self):
        #if (self.cam.getX(self.S02cam)- self.target2 < self.tol2:
        #    self.view.checkBox.setCheckable(True)
        #    self.view.checkBox.setChecked(True)
            #self.view.checkBox.setCheckable(False)

        print 'Retract S02-YAG-02 (screen controls not reliable yet, use control system if necessary)'# **change back to -02**'
        screen = self.S02screen
        #self.scrn.moveScreenTo(screen,scrn.SCREEN_STATE.V_RETRACTED)

        #time.sleep(5)
        #if self.scrn.isYAGIn(screen) is True:
        print 'is screen in?', self.scrn.getScreenState(screen)
        if str(self.scrn.getScreenState(screen)) == 'V_YAG':
            print 'YAG is in'
            self.scrn.moveScreenTo(screen,scrn.SCREEN_STATE.V_RF)
            while True:
                isscreenmoving1 = self.scrn.isScreenMoving(screen)
                print 'Is screen moving?', isscreenmoving1
                QApplication.processEvents()
                time.sleep(1)
                isscreenmoving2 = self.scrn.isScreenMoving(screen)
                if isscreenmoving2 is False and isscreenmoving1 is True:
                    print 'Finished Moving!'
                    break
        elif str(self.scrn.getScreenState(screen)) == 'V_RF':
            print 'YAG already out, RF cage is in'
        #else:
        #    print 'Error moving screen'

        #if (self.Cbpms.getXFromPV('S02-BPM02')-self.view.doubleSpinBox_x_1.value()) < self.view.doubleSpinBox_tol_1.value():
        #    self.view.checkBox_2.setCheckable(True)
        #    self.view.checkBox_2.setChecked(True)


    def cor1_current_up(self):
        self.func.stepCurrent(self.Cmagnets,self.cor1,self.data.values['fine_step1'])

    def cor1_current_down(self):
        self.func.stepCurrent(self.Cmagnets,self.cor1,-self.data.values['fine_step1'])

    def fineGetCurrentRange_2(self):
        try:
            self.data.values['fineIMin'] = 0.98*self.data.values['I_rough']
            self.data.values['fineIMax'] = 1.02*self.data.values['I_rough']
            self.data.values['fineIStep'] = 0.005*self.data.values['I_rough']
            self.view.lineEdit_fineCurrentMin.setText("%.2f" % self.data.values['fineIMin'])
            self.view.lineEdit_fineCurrentMax.setText("%.2f" % self.data.values['fineIMax'])
        except:
            print 'Needs a rough momentum measurement'
        #self.fineMinI = 0.95*self.approxI
        #self.fineMaxI = 1.05*self.approxI


    def measureMomentumCentreC2V(self):
        '''3. Centre in Spec. Line'''
        #if self.view.checkBox_3.isChecked()==True:
        self.data.values['I_fine'] = self.func.bendBeam(self.Cmagnets,self.dipole,
                                    self.Cbpms,self.C2Vbpm,
                                     self.data.values['fineIMin'], self.data.values['fineIMax'], self.data.values['fineIStep'])#0.00001                 # tol=0.0001 (metres)
        self.data.values['p_fine'] = self.func.I2mom(self.Cmagnets,self.dipole,self.data.values['I_fine'])
        #print self.p
        print str(datetime.datetime.now())[:-7], ', Fine measurement: I =', self.data.values['I_fine'], 'A, p =', self.data.values['p_fine'], 'MeV/c'


################################################################################
# Fine set functions
    def p_fine_set(self, y):
        self.data.values['p_fine_set'] = y
        self.data.values['I_fine_set'] = self.func.mom2I(self.Cmagnets,self.dipole,self.data.values['p_fine_set'])
        #self.view.label_p_rough.setText(str(self.data.values['p_rough']))
        self.view.doubleSpinBox_I_3.setValue(self.data.values['I_fine_set'])
        print str(datetime.datetime.now())[:-7], ', Fine set: I =', self.data.values['I_fine_set'], 'A, p =', self.data.values['p_fine_set'], 'MeV/c'

    def set_I_fine(self):
        self.func.setCurrent(self.Cmagnets, self.dipole, self.data.values['I_fine_set'])

    def setFineSetStep(self, y):
        self.data.values['fine_set_step'] = y
        print 'Fine set step size = ', self.data.values['fine_set_step']

    def select_gun_fine(self):
        self.data.values['RFmode_fine'] = 'Gun'
        self.view.lineEdit_RFmode_fine.setText(self.data.values['RFmode_fine'])

    def select_linac_fine(self):
        self.data.values['RFmode_fine'] = 'Linac'
        self.view.lineEdit_RFmode_fine.setText(self.data.values['RFmode_fine'])

    def RF_amplitude_up_fine(self):
        if self.data.values['RFmode_fine'] == 'Gun':
            rfmode = self.gun
        elif self.data.values['RFmode_fine'] == 'Linac':
            rfmode = self.linac1
        else:
            print 'RF mode not selected'
        self.func.stepRF(rfmode,self.data.values['fine_set_step'])

    def RF_amplitude_down_fine(self):
        if self.data.values['RFmode_fine'] == 'Gun':
            rfmode = self.gun
        elif self.data.values['RFmode_fine'] == 'Linac':
            rfmode = self.linac1
        else:
            print 'RF mode not selected'
        self.func.stepRF(rfmode,-self.data.values['fine_set_step'])

# Momentum spread
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
                                                self.C2Vcam,
                                                self.data.values['I_rough'],10,0.1)
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
        self.beamSigma = self.cam.getSigX(self.C2Vcam)
        self.Is = self.beamSigma/self.Dispersion
        self.pSpread = self.func.calcMomSpread(self.Cmagnets,self.dipole,self.Is,self.data.values['I_rough'])
        print str(datetime.datetime.now())[:-7], ', Momentum spread =', self.pSpread, 'MeV/c, =>', 100*self.pSpread/self.data.values['I_rough'], '%'

        #a = self.func.calcMomSpread(self.Cmagnets,'DIP01',self.Is,self.I)
        #print a
        #else:
        #    print 'Not confirmed momentum measurement'

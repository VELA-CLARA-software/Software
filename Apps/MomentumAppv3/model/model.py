#from PyQt4.QtCore import QThread, QObject, pyqtSignal, QTimer
#from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QObject
import datetime
import momentumFunctions

import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_Screen_Control as scrn

import sys
sys.path.append("../../../")
import Software.Procedures.linacTiming as linacTiming



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

        self.bpmInit = bpm.init()
        self.Cbpms = self.bpmInit.physical_C2B_BPM_Controller()
        self.C2Vbpm = 'C2V-BPM01'

        self.llrfInit = llrf.init()
        self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
        self.linac1 = self.llrfInit.physical_L01_LLRF_Controller()
        self.Linac01Timing = linacTiming.Linac01Timing()

        self.scrnInit = scrn.init()
        self.scrn = self.scrnInit.physical_C2B_Screen_Controller()
        self.S02screen = 'S02-SCR-02'


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
        print 'Rough step size = ', self.data.values['rough_step']

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

################################################################################
# Rough set functions
    def p_rough_set(self, y):
        self.data.values['p_rough_set'] = y
        self.data.values['I_rough_set'] = self.func.mom2I(self.Cmagnets,self.dipole,self.data.values['p_rough_set'])
        #self.view.label_p_rough.setText(str(self.data.values['p_rough']))
        self.view.doubleSpinBox_I_2.setValue(self.data.values['I_rough_set'])
        print str(datetime.datetime.now())[:-7], ', Rough set: I =', self.data.values['I_rough_set'], 'A, p =', self.data.values['p_rough_set'], 'MeV/c'

    def setRoughSetStep(self, y):
        self.data.values['rough_set_step'] = y
        print 'Rough set step size = ', self.data.values['rough_set_step']


    def select_gun(self):
        self.data.values['RFmode_rough'] = 'Gun'
        self.view.lineEdit_RFmode_rough.setText(self.data.values['RFmode_rough'])

    def select_linac(self):
        self.data.values['RFmode_rough'] = 'Linac'
        self.view.lineEdit_RFmode_rough.setText(self.data.values['RFmode_rough'])

################################################################################
# Alignment functions

    def measureMomentumAlign_2(self):
        print 'Insert S02-YAG-02'
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

################################################################################
# Fine set functions
    def p_fine_set(self, y):
        self.data.values['p_fine_set'] = y
        self.data.values['I_fine_set'] = self.func.mom2I(self.Cmagnets,self.dipole,self.data.values['p_fine_set'])
        #self.view.label_p_rough.setText(str(self.data.values['p_rough']))
        self.view.doubleSpinBox_I_3.setValue(self.data.values['I_fine_set'])
        print str(datetime.datetime.now())[:-7], ', Fine set: I =', self.data.values['I_fine_set'], 'A, p =', self.data.values['p_fine_set'], 'MeV/c'

    def setFineSetStep(self, y):
        self.data.values['fine_set_step'] = y
        print 'Fine set step size = ', self.data.values['fine_set_step']

    def select_gun_fine(self):
        self.data.values['RFmode_fine'] = 'Gun'
        self.view.lineEdit_RFmode_fine.setText(self.data.values['RFmode_fine'])

    def select_linac_fine(self):
        self.data.values['RFmode_fine'] = 'Linac'
        self.view.lineEdit_RFmode_fine.setText(self.data.values['RFmode_fine'])

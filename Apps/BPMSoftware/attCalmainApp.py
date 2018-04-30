import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\View')

from PyQt4 import QtGui, QtCore
import VELA_CLARA_BPM_Control as vbpmc
import VELA_CLARA_Scope_Control as vcsc
import attCalmainModel
import attCalmainController
import attCalmainView
# import loggerWidget as lw
# import logging

class attCalApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        #App is launched here based on inputs from the Master app. Cumbersome, I know...
        super(attCalApp, self).__init__(sys_argv)
        self.bpm = vbpmc.init()
        self.scope = vcsc.init()
        # self.logger = logging.getLogger(__name__)
        if sys_argv[2] == "VELA_INJ":
            self.contType = "VELA_INJ"
            if sys_argv[1] == "Virtual":
                self.bpmCont = self.bpm.virtual_VELA_INJ_BPM_Controller()
                self.scopeCont = self.scope.virtual_VELA_INJ_Scope_Controller()
            elif sys_argv[1] == "Offline":
                self.bpmCont = self.bpm.offline_VELA_INJ_BPM_Controller()
                self.scopeCont = self.scope.offline_VELA_INJ_Scope_Controller()
            elif sys_argv[1] == "Physical":
                self.bpmCont = self.bpm.physical_VELA_INJ_BPM_Controller()
                self.scopeCont = self.scope.physical_VELA_INJ_Scope_Controller()
        elif sys_argv[2] == "VELA_BA1":
            self.contType = "VELA_BA1"
            if sys_argv[1] == "Virtual":
                self.bpmCont = self.bpm.virtual_VELA_BA1_BPM_Controller()
                self.scopeCont = self.scope.virtual_VELA_BA1_Scope_Controller()
            elif sys_argv[1] == "Offline":
                self.bpmCont = self.bpm.offline_VELA_BA1_BPM_Controller()
                self.scopeCont = self.scope.offline_VELA_BA1_Scope_Controller()
            elif sys_argv[1] == "Physical":
                self.bpmCont = self.bpm.physical_VELA_BA1_BPM_Controller()
                self.scopeCont = self.scope.physical_VELA_BA1_Scope_Controller()
        elif sys_argv[2] == "VELA_BA2":
            self.contType = "VELA_BA2"
            if sys_argv[1] == "Virtual":
                self.bpmCont = self.bpm.virtual_VELA_BA2_BPM_Controller()
                self.scopeCont = self.scope.virtual_VELA_BA2_Scope_Controller()
            elif sys_argv[1] == "Offline":
                self.bpmCont = self.bpm.offline_VELA_BA2_BPM_Controller()
                self.scopeCont = self.scope.offline_VELA_BA2_Scope_Controller()
            elif sys_argv[1] == "Physical":
                self.bpmCont = self.bpm.physical_VELA_BA2_BPM_Controller()
                self.scopeCont = self.scope.physical_VELA_BA2_Scope_Controller()
        elif sys_argv[2] == "CLARA_PH1":
            self.contType = "CLARA_PH1"
            if sys_argv[1] == "Virtual":
                self.bpmCont = self.bpm.virtual_CLARA_PH1_BPM_Controller()
                self.scopeCont = self.scope.virtual_VELA_INJ_Scope_Controller()
            elif sys_argv[1] == "Offline":
                self.bpmCont = self.bpm.offline_CLARA_PH1_BPM_Controller()
                self.scopeCont = self.scope.offline_VELA_INJ_Scope_Controller()
            elif sys_argv[1] == "Physical":
                self.bpmCont = self.bpm.physical_CLARA_PH1_BPM_Controller()
                self.scopeCont = self.scope.physical_VELA_INJ_Scope_Controller()
        elif sys_argv[2] == "CLARA_2_VELA":
            self.contType = "CLARA_2_VELA"
            if sys_argv[1] == "Virtual":
                self.bpmCont = self.bpm.virtual_CLARA_2_VELA_BPM_Controller()
                self.scopeCont = self.scope.virtual_C2V_Scope_Controller()
            elif sys_argv[1] == "Offline":
                self.bpmCont = self.bpm.offline_CLARA_2_VELA_BPM_Controller()
                self.scopeCont = self.scope.offline_C2V_Scope_Controller()
            elif sys_argv[1] == "Physical":
                self.bpmCont = self.bpm.physical_CLARA_2_VELA_BPM_Controller()
                self.scopeCont = self.scope.physical_C2V_Scope_Controller()
        self.view = attCalmainView.attCalUi_TabWidget()
        self.MainWindow = QtGui.QTabWidget()
        self.view.setupUi(self.MainWindow, self.bpmCont, sys_argv[1], sys_argv[2])
        self.model = attCalmainModel.attCalModel(self.bpmCont, self.scopeCont)
        self.controller = attCalmainController.attCalController(self.view, self.model, self.bpmCont, self.scopeCont)
        # self.logwidget1 = lw.loggerWidget([self.logger, attCalmainController.logger])
        # self.MainWindow.addTab(self.logwidget1,"Log")
        self.MainWindow.show()

if __name__ == '__main__':
    app = attCalApp(sys.argv)
    sys.exit(app.exec_())

import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.chdir("..\BPMAttenuationCalibration")
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\View')

from PyQt4 import QtGui, QtCore
import VELA_CLARA_BPM_Control as vbpmc
import VELA_CLARA_Scope_Control as vcsc
import attCalmainModel
import attCalmainController
import attCalmainView
import loggerWidget as lw
import logging

class attCalApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        #App is launched here based on inputs from the Master app. Cumbersome, I know...
        super(attCalApp, self).__init__(sys_argv)
        self.bpm = vbpmc.init()
        self.scope = vcsc.init()
        self.logger = logging.getLogger(__name__)
        if sys_argv[1] == "Virtual":
            self.machineMode = vbpmc.MACHINE_MODE.VIRTUAL
        elif sys_argv[1] == "Offline":
            self.machineMode = vbpmc.MACHINE_MODE.OFFLINE
        elif sys_argv[1] == "Physical":
            self.machineMode = vbpmc.MACHINE_MODE.PHYSICAL
        if sys_argv[2] == "VELA_INJ":
            self.machineArea = vbpmc.MACHINE_AREA.VELA_INJ
        elif sys_argv[2] == "VELA_BA1":
            self.machineArea = vbpmc.MACHINE_AREA.VELA_BA1
        elif sys_argv[2] == "VELA_BA2":
            self.machineArea = vbpmc.MACHINE_AREA.VELA_BA2
        elif sys_argv[2] == "CLARA_INJ":
            self.machineArea = vbpmc.MACHINE_AREA.CLARA_INJ
        elif sys_argv[2] == "C2V":
            self.machineArea = vbpmc.MACHINE_AREA.CLARA_2_VELA
        self.scopeCont = self.scope.getScopeController(self.machineMode, self.machineArea)
        self.bpmCont = self.bpm.getBPMController(self.machineMode, self.machineArea)
        #self.scopeCont = self.scope.virtual_VELA_INJ_Scope_Controller()
        #self.scopeCont = self.scope.getScopeController(self.machineMode, self.machineArea)
        self.view = attCalmainView.attCalUi_TabWidget()
        self.MainWindow = QtGui.QTabWidget()
        self.view.setupUi(self.MainWindow, self.bpmCont, sys_argv[1], sys_argv[2])
        self.model = attCalmainModel.attCalModel(self.bpmCont, self.scopeCont)
        self.controller = attCalmainController.attCalController(self.view, self.model, self.bpmCont, self.scopeCont)
        self.logwidget1 = lw.loggerWidget([self.logger, attCalmainController.logger])
        self.MainWindow.addTab(self.logwidget1,"Log")
        self.MainWindow.show()

if __name__ == '__main__':
    app = attCalApp(sys.argv)
    sys.exit(app.exec_())

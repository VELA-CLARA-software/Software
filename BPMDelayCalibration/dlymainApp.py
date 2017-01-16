import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.chdir("..\BPMDelayCalibration")
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\View')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'..\..\loggerWidget')
sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\CONTROLLERS\\VELA-CLARA-Controllers\\bin\\Release')

from PyQt4 import QtGui, QtCore
import VELA_CLARA_BPM_Control as vbpmc
import dlymainModel
import dlymainController
import dlymainView
import loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

class dlyApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(dlyApp, self).__init__(sys_argv)
        self.bpm = vbpmc.init()
        if sys_argv[1] == "VELA_INJ":
            self.contType = "VELA_INJ"
            if sys_argv[2] == "Virtual":
                self.bpmCont = self.bpm.virtual_VELA_INJ_BPM_Controller()
            elif sys_argv[2] == "Offline":
                self.bpmCont = self.bpm.offline_VELA_INJ_BPM_Controller()
            elif sys_argv[2] == "Physical":
                self.bpmCont = self.bpm.physical_VELA_INJ_BPM_Controller()
        elif sys_argv[1] == "VELA_BA1":
            self.contType = "VELA_BA1"
            if sys_argv[2] == "Virtual":
                self.bpmCont = self.bpm.virtual_VELA_BA1_BPM_Controller()
            elif sys_argv[2] == "Offline":
                self.bpmCont = self.bpm.offline_VELA_BA1_BPM_Controller()
            elif sys_argv[2] == "Physical":
                self.bpmCont = self.bpm.physical_VELA_BA1_BPM_Controller()
        elif sys_argv[1] == "VELA_BA2":
            self.contType = "VELA_BA2"
            if sys_argv[2] == "Virtual":
                self.bpmCont = self.bpm.virtual_VELA_BA2_BPM_Controller()
            elif sys_argv[2] == "Offline":
                self.bpmCont = self.bpm.offline_VELA_BA2_BPM_Controller()
            elif sys_argv[2] == "Physical":
                self.bpmCont = self.bpm.physical_VELA_BA2_BPM_Controller()
        elif sys_argv[1] == "CLARA":
            self.contType = "CLARA"
            if sys_argv[2] == "Virtual":
                self.bpmCont = self.bpm.virtual_CLARA_BPM_Controller()
            elif sys_argv[2] == "Offline":
                self.bpmCont = self.bpm.offline_CLARA_BPM_Controller()
            elif sys_argv[2] == "Physical":
                self.bpmCont = self.bpm.physical_CLARA_BPM_Controller()
        elif sys_argv[1] == "C2V":
            self.contType = "C2V"
            if sys_argv[2] == "Virtual":
                self.bpmCont = self.bpm.virtual_C2V_BPM_Controller()
            elif sys_argv[2] == "Offline":
                self.bpmCont = self.bpm.offline_C2V_BPM_Controller()
            elif sys_argv[2] == "Physical":
                self.bpmCont = self.bpm.physical_C2V_BPM_Controller()
        self.view = dlymainView.dlyUi_TabWidget()
        self.MainWindow = QtGui.QTabWidget()
        self.view.setupUi(self.MainWindow, self.bpmCont, sys_argv[1], sys_argv[2])
        self.model = dlymainModel.dlyModel(self.bpmCont)
        self.controller = dlymainController.dlyController(self.view, self.model, self.bpmCont)
        self.logwidget1 = lw.loggerWidget([logger,dlymainController.logger])
        self.MainWindow.addTab(self.logwidget1,"Log")
        self.MainWindow.show()

if __name__ == '__main__':
    app = dlyApp(sys.argv)
    sys.exit(app.exec_())

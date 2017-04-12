import sys,os
#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
from PyQt4 import QtGui, QtCore
import VELA_CLARA_Scope_Control as vcsc
import scope_writer_model
import scope_writer_controller
import scope_writer_view
import loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

class scopeWriterApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        #App is launched here based on inputs from the Master app. Cumbersome, I know...
        super(scopeWriterApp, self).__init__(sys_argv)
        self.scope = vcsc.init()
        if sys_argv[1] == "VELA_INJ":
            self.contType = "VELA_INJ"
            if sys_argv[2] == "Virtual":
                self.scopeCont = self.scope.virtual_VELA_INJ_Scope_Controller()
            elif sys_argv[2] == "Offline":
                self.scopeCont = self.scope.offline_VELA_INJ_Scope_Controller()
            elif sys_argv[2] == "Physical":
                self.scopeCont = self.scope.physical_VELA_INJ_Scope_Controller()
        elif sys_argv[1] == "VELA_BA1":
            self.contType = "VELA_BA1"
            if sys_argv[2] == "Virtual":
                self.scopeCont = self.scope.virtual_VELA_BA1_Scope_Controller()
            elif sys_argv[2] == "Offline":
                self.scopeCont = self.scope.offline_VELA_BA1_Scope_Controller()
            elif sys_argv[2] == "Physical":
                self.scopeCont = self.scope.physical_VELA_BA1_Scope_Controller()
        elif sys_argv[1] == "VELA_BA2":
            self.contType = "VELA_BA2"
            if sys_argv[2] == "Virtual":
                self.scopeCont = self.scope.virtual_VELA_BA2_Scope_Controller()
            elif sys_argv[2] == "Offline":
                self.scopeCont = self.scope.offline_VELA_BA2_Scope_Controller()
            elif sys_argv[2] == "Physical":
                self.scopeCont = self.scope.physical_VELA_BA2_Scope_Controller()
        elif sys_argv[1] == "CLARA_S01":
            self.contType = "CLARA_S01"
            if sys_argv[2] == "Virtual":
                self.scopeCont = self.scope.virtual_CLARA_S01_Scope_Controller()
            elif sys_argv[2] == "Offline":
                self.scopeCont = self.scope.offline_CLARA_S01_Scope_Controller()
            elif sys_argv[2] == "Physical":
                self.scopeCont = self.scope.physical_VELA_INJ_Scope_Controller()
        elif sys_argv[1] == "CLARA_2_VELA":
            self.contType = "C2V"
            if sys_argv[2] == "Virtual":
                self.scopeCont = self.scope.virtual_CLARA_2_VELA_Scope_Controller()
            elif sys_argv[2] == "Offline":
                self.scopeCont = self.scope.offline_CLARA_2_VELA_Scope_Controller()
            elif sys_argv[2] == "Physical":
                self.scopeCont = self.scope.physical_CLARA_2_VELA_Scope_Controller()
        self.view = scope_writer_view.scopeWriterUi_TabWidget()
        self.MainWindow = QtGui.QTabWidget()
        self.view.setupUi(self.MainWindow, self.scopeCont)
        self.model = scope_writer_model.scopeWriterModel(self.scopeCont)
        self.controller = scope_writer_controller.scopeWriterController(self.view, self.model, self.scopeCont)
        #self.logwidget1 = lw.loggerWidget([logger,scopeWriterController.logger])
        #self.MainWindow.addTab(self.logwidget1,"Log")
        self.MainWindow.show()

if __name__ == '__main__':
    app = scopeWriterApp(sys.argv)
    sys.exit(app.exec_())

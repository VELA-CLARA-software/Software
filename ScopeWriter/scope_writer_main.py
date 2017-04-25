import sys,os
from PyQt4 import QtGui, QtCore
import VELA_CLARA_Scope_Control as vcsc
import scope_writer_model
import scope_writer_controller
import scope_writer_view

class scopeWriterApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        #App is launched here based on inputs from the Master app. Cumbersome, I know...
        super(scopeWriterApp, self).__init__(sys_argv)
        self.scope = vcsc.init()
        self.beamlines = {"VELA_INJ":  vcsc.MACHINE_AREA.VELA_INJ,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA1,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA2,
                          "CLARA_S01": vcsc.MACHINE_AREA.CLARA_S01}
        self.modes = {"Physical": vcsc.MACHINE_MODE.PHYSICAL,
                      "Virtual":  vcsc.MACHINE_MODE.VIRTUAL,
                      "Offline":  vcsc.MACHINE_MODE.OFFLINE}
        self.controllerType = self.searchInDict(self.modes, sys_argv[1])
        self.beamline = self.searchInDict(self.beamlines, sys_argv[2])
        self.scopeCont = self.scope.getScopeController( self.controllerType, self.beamline )
        self.view = scope_writer_view.scopeWriterUi_TabWidget()
        self.MainWindow = QtGui.QTabWidget()
        self.view.setupUi(self.MainWindow, self.scopeCont)
        self.model = scope_writer_model.scopeWriterModel(self.scopeCont)
        self.controller = scope_writer_controller.scopeWriterController(self.view, self.model, self.scopeCont)
        #self.logwidget1 = lw.loggerWidget([logger,scopeWriterController.logger])
        #self.MainWindow.addTab(self.logwidget1,"Log")
        self.MainWindow.show()

    def searchInDict(self, myDict, lookup):
        self.myDict = myDict
        self.lookup = lookup
        for key, value in self.myDict.items():
            if self.lookup == key:
                print type(value)
                return value

if __name__ == '__main__':
    app = scopeWriterApp(sys.argv)
    sys.exit(app.exec_())

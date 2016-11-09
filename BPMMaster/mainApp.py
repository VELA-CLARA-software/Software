import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\View')
sys.path.append('D:\\VELA-CLARA_software\\VELA-CLARA-Controllers-New-Structure-With-Magnets\\bin\\Release')
from PyQt4 import QtGui, QtCore

import mainController
import mainView

class masterApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(masterApp, self).__init__(sys_argv)
        #os.chdir("D:\VELA-CLARA_software\Software\BPMMaster")
        self.view = mainView.Ui_TabWidget()
        self.MainWindow = QtGui.QTabWidget()
        self.view.setupUi(self.MainWindow)
        self.controller = mainController.Controller(self.view)
        self.MainWindow.show()

if __name__ == '__main__':
    app = masterApp(sys.argv)
    sys.exit(app.exec_())

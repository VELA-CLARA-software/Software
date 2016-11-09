import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\View')
from PyQt4 import QtGui, QtCore

class masterApp(QtGui.QApplication):
    def __init__(self, sys_argv):
        super(masterApp, self).__init__(sys_argv)
        os.system("python ..\BPMDelayCalibration\mainApp.py")

if __name__ == '__main__':
    app = masterApp(sys.argv)
    sys.exit(app.exec_())

from PyQt4 import QtGui, QtCore
import sys,os
print os.getcwd()
from control.matlabImageViewerMasterController import matlabImageViewerMasterController

class matlabImageViewerLauncher(QtGui.QApplication):
    def __init__(self,argv):
        # you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the magnetAppController
        self.controller = matlabImageViewerMasterController()

if __name__ == '__main__':
    print "starting matlab writer"
    app = matlabImageViewerLauncher(sys.argv)
    sys.exit(app.exec_())

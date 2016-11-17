from PyQt4 import QtGui, QtCore
import sys,os

#sys.path.append('D:\\VELA\\GIT Projects\\VELA-CLARA-Controllers\\bin\\Release')
sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release\\')
import magnetAppController


class magnetApp(QtGui.QApplication):
    def __init__(self,argv):
        # seems you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the controller
        self.controller = magnetAppController.magnetAppController(argv)

if __name__ == '__main__':
    app = magnetApp(sys.argv)
    sys.exit(app.exec_())
from PyQt4 import QtGui, QtCore
import sys,os

sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')

from aligncontroller import alignAppController
from draftgui import draftappgui


class alignApp(QtGui.QApplication):
    def __init__(self,argv):
        # seems you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the controller
        self.controller = alignAppController(argv)

		
if __name__ == '__main__':
    app = alignApp(sys.argv)
    sys.exit(app.exec_())

from PyQt4 import QtCore, QtGui

from design import Ui_MainWindow

class GUI(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self):
        print 'create startup window'
        super(self.__class__, self).__init__()
        #QtGui.QWidget.__init__(self)
        self.setupUi(self)
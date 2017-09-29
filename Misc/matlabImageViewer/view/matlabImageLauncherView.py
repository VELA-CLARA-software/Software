from PyQt4 import QtGui, QtCore
import matlabImageLauncherViewUI

class matlabImageLauncherView(QtGui.QMainWindow, matlabImageLauncherViewUI.matlabImageLauncherViewUI):
    # static signals to emit when radioButtons are pressed
    # this lets the master controller know which type of processing is requested
    measurementTypeSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.measurementTypesComboBox.currentIndexChanged['QString'].connect(self.handle_measurementTypeRadio)
        self.setWindowTitle("Matlab image viewer launcher")

    def handle_measurementTypeRadio(self):
        self.measurementTypeSignal.emit(str(self.measurementTypesComboBox.currentText()))

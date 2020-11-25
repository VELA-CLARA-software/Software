from PyQt4 import QtGui, QtCore
import energySpreadViewUI

class energySpreadView(QtGui.QMainWindow, energySpreadViewUI.energySpreadViewUI):
    filekeychanged = QtCore.pyqtSignal(str)
    subfilekeychanged = QtCore.pyqtSignal(str)
    subsubfilekeychanged = QtCore.pyqtSignal(str)
    isfilechanged = QtCore.pyqtSignal(bool)
    closing = QtCore.pyqtSignal()

    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.isfilechanged = False
        self.measuretype = "energyspread"
        self.keysComboBox.currentIndexChanged['QString'].connect(self.fileKeyChangedEvent)
        self.subKeysComboBox.currentIndexChanged['QString'].connect(self.subFileKeyChangedEvent)
        self.subSubKeysComboBox.currentIndexChanged['QString'].connect(self.subSubFileKeyChangedEvent)
        self.allFilesComboBox.currentIndexChanged['QString'].connect(self.fileKeyChangedEvent)

    def fileKeyChangedEvent(self):
        self.filekeychanged.emit(str(self.keysComboBox.currentText()))

    def subFileKeyChangedEvent(self):
        self.subfilekeychanged.emit(str(self.subKeysComboBox.currentText()))

    def subSubFileKeyChangedEvent(self):
        self.subsubfilekeychanged.emit(str(self.subSubKeysComboBox.currentText()))

    def closeEvent(self,event):
        self.closing.emit()
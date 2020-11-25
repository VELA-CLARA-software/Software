from PyQt4 import QtGui, QtCore
import snapshot_guiUI
import os

class snapshotGUI(QtGui.QMainWindow, snapshot_guiUI.snapshotUI):
    filekeychanged = QtCore.pyqtSignal(str)
    subfilekeychanged = QtCore.pyqtSignal(str)
    subsubfilekeychanged = QtCore.pyqtSignal(str)
    isfilechanged = QtCore.pyqtSignal(bool)
    closing = QtCore.pyqtSignal()

    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
    #     self.getDirectoryButton.clicked.connect(self.setDirOrFile1)
    #
    # @QtCore.pyqtSlot()
    # def setDirOrFile1(self):
    #     if self.setDirectory.isChecked():
    #         path = QtGui.QFileDialog.getExistingDirectory(None, 'Pick a Folder', os.getcwd())
    #         if path:
    #             self.getDirectoryLineEdit.setText(path)
    #             self.isDirectorySet = True
    #             self.isFileSet = True
    #     elif self.setFile.isChecked():
    #         file = QtGui.QFileDialog.getOpenFileName(None, "Pick a file", os.getcwd())
    #         if file:
    #             self.getDirectoryLineEdit.setText(file)
    #             self.isDirectorySet = False
    #             self.isFileSet = True
    #     return

    def closeEvent(self,event):
        self.closing.emit()

# uncompyle6 version 2.10.0
# Python bytecode 2.7 (62211)
# Decompiled from: Python 2.7.10 (default, May 23 2015, 09:40:32) [MSC v.1500 32 bit (Intel)]
# Embedded file name: D:\VELA-CLARA_software\Software\matlabImageViewer\view\matlabImageView.py
# Compiled at: 2017-06-01 15:50:43
from PyQt4 import QtGui, QtCore
import matlabImageViewUI

class matlabImageView(QtGui.QMainWindow, matlabImageViewUI.matlabImageViewUI):
    filekeychanged = QtCore.pyqtSignal(str)
    subfilekeychanged = QtCore.pyqtSignal(str)
    subsubfilekeychanged = QtCore.pyqtSignal(str)
    isfilechanged = QtCore.pyqtSignal(bool)

    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.isfilechanged = False
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
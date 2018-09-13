from PyQt4 import QtCore, QtGui, Qt
import numpy
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:

    def _fromUtf8(s):
        return s


try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)


except AttributeError:

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class snapshotUI(object):

    def setupUi(self, mainWindow):
        mainWindow.resize(310, 210)
        mainWindow.setObjectName(_fromUtf8('Machine snapshot button'))
        self.mainWidget = QtGui.QWidget(mainWindow)
        self.mainWidget.resize(300, 200)
        self.mainWidget.setObjectName(_fromUtf8('mainWidget'))
        self.mainBox = QtGui.QHBoxLayout(self.mainWidget)

        # loading files and config, etc.
        self.snapshotVBox = QtGui.QVBoxLayout()
        # self.setDirOrFileLayout = QtGui.QHBoxLayout()
        # self.setDirOrFile = QtGui.QGroupBox()
        # self.setDirOrFile.setAlignment(QtCore.Qt.AlignCenter)
        # self.setDirOrFile.setGeometry(QtCore.QRect(360, 140, 193, 211))
        # self.setDirectory = QtGui.QRadioButton()
        # self.setDirectory.setObjectName(_fromUtf8('setDirectory'))
        # self.setDirectory.setMinimumSize(QtCore.QSize(100,20))
        # self.setFile = QtGui.QRadioButton()
        # self.setFile.setObjectName(_fromUtf8('setFile'))
        # self.setFile.setMinimumSize(QtCore.QSize(100, 20))
        # self.setDirOrFileLayout.addWidget(self.setDirectory)
        # self.setDirOrFileLayout.addWidget(self.setFile)
        # self.setDirOrFile.setLayout(self.setDirOrFileLayout)
        self.getDirectoryLayout = QtGui.QHBoxLayout()
        self.setLayout(self.getDirectoryLayout)
        self.getDirectoryLineEdit = QtGui.QLineEdit(self)
        self.getDirectoryLayout.addWidget(self.getDirectoryLineEdit)
        # self.getDirectoryButton = QtGui.QPushButton('...', self)
        # self.getDirectoryLayout.addWidget(self.getDirectoryButton)
        self.setFileTypeLayout = QtGui.QHBoxLayout()
        self.setFileType = QtGui.QGroupBox()
        self.setFileType.setAlignment(QtCore.Qt.AlignCenter)
        # self.setFileType.setGeometry(QtCore.QRect(560, 340, 393, 411))
        # self.setJSON = QtGui.QRadioButton()
        # self.setJSON.setObjectName(_fromUtf8('setJSON'))
        # self.setJSON.setMinimumSize(QtCore.QSize(100, 20))
        self.setHDF5 = QtGui.QRadioButton()
        self.setHDF5.setObjectName(_fromUtf8('setHDF5'))
        self.setHDF5.setMinimumSize(QtCore.QSize(100, 20))
        self.setAll = QtGui.QRadioButton()
        self.setAll.setObjectName(_fromUtf8('setAll'))
        self.setAll.setMinimumSize(QtCore.QSize(100, 20))
        # self.setFileTypeLayout.addWidget(self.setJSON)
        self.setFileTypeLayout.addWidget(self.setHDF5)
        self.setFileTypeLayout.addWidget(self.setAll)
        self.setFileType.setLayout(self.setFileTypeLayout)
        self.saveSnapshotButton = QtGui.QPushButton('Save snapshot', self)
        self.saveSnapshotButton.setObjectName(_fromUtf8('saveSnapshotButton'))
        self.saveSnapshotButton.setMaximumSize(QtCore.QSize(300, 300))
        self.saveSnapshotButton.setMaximumSize(QtCore.QSize(300, 300))

        # self.snapshotVBox.addWidget(self.setDirOrFile)
        self.snapshotVBox.addLayout(self.getDirectoryLayout)
        self.snapshotVBox.addWidget(self.setFileType)
        self.snapshotVBox.addWidget(self.saveSnapshotButton)
        self.snapshotVBox.addStretch()

        # add all layouts and make main panel
        self.mainBox.addLayout(self.snapshotVBox)
        self.retranslateUi(mainWindow)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(_translate('mainWindow', 'Machine snapshot example', None))
        # self.setDirectory.setText(_translate('mainWindow', 'Set Directory', None))
        # self.setFile.setText(_translate('mainWindow', 'Set File', None))
        self.saveSnapshotButton.setText(_translate('mainWindow', 'save snapshot', None))
        # self.setJSON.setText(_translate('mainWindow', 'Set .json', None))
        self.setHDF5.setText(_translate('mainWindow', 'Set .hdf5', None))
        self.setAll.setText(_translate('mainWindow', 'Set all', None))
        return

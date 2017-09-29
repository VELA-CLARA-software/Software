# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_FileLoad.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_FileLoad(object):
    def setupUi(self, FileLoad):
        FileLoad.setObjectName(_fromUtf8("FileLoad"))
        FileLoad.resize(978, 582)
        self.verticalLayout = QtGui.QVBoxLayout(FileLoad)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(FileLoad)
        self.groupBox.setMinimumSize(QtCore.QSize(400, 50))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.allMagnets = QtGui.QRadioButton(self.groupBox)
        self.allMagnets.setChecked(True)
        self.allMagnets.setObjectName(_fromUtf8("allMagnets"))
        self.horizontalLayout.addWidget(self.allMagnets)
        self.quadMagnets = QtGui.QRadioButton(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.quadMagnets.setFont(font)
        self.quadMagnets.setObjectName(_fromUtf8("quadMagnets"))
        self.horizontalLayout.addWidget(self.quadMagnets)
        self.corrMagnets = QtGui.QRadioButton(self.groupBox)
        self.corrMagnets.setObjectName(_fromUtf8("corrMagnets"))
        self.horizontalLayout.addWidget(self.corrMagnets)
        self.verticalLayout.addWidget(self.groupBox)
        self.label = QtGui.QLabel(FileLoad)
        self.label.setMinimumSize(QtCore.QSize(400, 30))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.frame_2 = QtGui.QFrame(FileLoad)
        self.frame_2.setMinimumSize(QtCore.QSize(400, 300))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.treeView = QtGui.QTreeView(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.treeView.setFont(font)
        self.treeView.setObjectName(_fromUtf8("treeView"))
        self.horizontalLayout_3.addWidget(self.treeView)
        self.listView = QtGui.QListView(self.frame_2)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listView.setFont(font)
        self.listView.setObjectName(_fromUtf8("listView"))
        self.horizontalLayout_3.addWidget(self.listView)
        self.horizontalLayout_3.setStretch(0, 5)
        self.horizontalLayout_3.setStretch(1, 4)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(FileLoad)
        self.frame.setMinimumSize(QtCore.QSize(400, 30))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.selectButton = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.selectButton.setFont(font)
        self.selectButton.setObjectName(_fromUtf8("selectButton"))
        self.horizontalLayout_2.addWidget(self.selectButton)
        self.cancelButton = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancelButton.setFont(font)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.horizontalLayout_2.addWidget(self.cancelButton)
        self.viewButton = QtGui.QPushButton(self.frame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.viewButton.setFont(font)
        self.viewButton.setObjectName(_fromUtf8("viewButton"))
        self.horizontalLayout_2.addWidget(self.viewButton)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(FileLoad)
        QtCore.QMetaObject.connectSlotsByName(FileLoad)

    def retranslateUi(self, FileLoad):
        FileLoad.setWindowTitle(_translate("FileLoad", "Dialog", None))
        self.groupBox.setTitle(_translate("FileLoad", "Which Magnets To Apply File To?", None))
        self.allMagnets.setText(_translate("FileLoad", "All", None))
        self.quadMagnets.setText(_translate("FileLoad", "Quads", None))
        self.corrMagnets.setText(_translate("FileLoad", "Correctors", None))
        self.label.setText(_translate("FileLoad", "Choose File To Load Magnet Settings", None))
        self.selectButton.setText(_translate("FileLoad", "Select", None))
        self.cancelButton.setText(_translate("FileLoad", "Cancel", None))
        self.viewButton.setText(_translate("FileLoad", "View File", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_FileSave.ui'
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

class scopeWriterSaveUI(object):
    def setupUi(self, FileSave):
        FileSave.setObjectName(_fromUtf8("FileSave"))
        FileSave.resize(300, 300)
        self.centralwidget = QtGui.QWidget(FileSave)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.keywordFrame = QtGui.QFrame(self.centralwidget)
        self.keywordFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.keywordFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.keywordFrame.setObjectName(_fromUtf8("keywordFrame"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout(self.keywordFrame)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.label_6 = QtGui.QLabel(self.keywordFrame)
        self.label_6.setMinimumSize(QtCore.QSize(90, 0))
        self.label_6.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_8.addWidget(self.label_6)
        self.areaCombo = QtGui.QComboBox(self.keywordFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.areaCombo.setFont(font)
        self.areaCombo.setObjectName(_fromUtf8("areaCombo"))
        self.horizontalLayout_8.addWidget(self.areaCombo)
        self.verticalLayout.addWidget(self.keywordFrame)
        self.filenameFrame = QtGui.QFrame(self.centralwidget)
        self.filenameFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.filenameFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.filenameFrame.setObjectName(_fromUtf8("filenameFrame"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.filenameFrame)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_4 = QtGui.QLabel(self.filenameFrame)
        self.label_4.setMinimumSize(QtCore.QSize(90, 0))
        self.label_4.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_6.addWidget(self.label_4)
        self.file_name_entry = QtGui.QLineEdit(self.filenameFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_name_entry.setFont(font)
        self.file_name_entry.setObjectName(_fromUtf8("file_name_entry"))
        self.horizontalLayout_6.addWidget(self.file_name_entry)
        self.verticalLayout.addWidget(self.filenameFrame)
        self.burronFrame = QtGui.QFrame(self.centralwidget)
        self.burronFrame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.burronFrame.setFrameShadow(QtGui.QFrame.Raised)
        self.burronFrame.setObjectName(_fromUtf8("burronFrame"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.burronFrame)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.saveNowButton_2 = QtGui.QPushButton(self.burronFrame)
        self.saveNowButton_2.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.saveNowButton_2.setFont(font)
        self.saveNowButton_2.setObjectName(_fromUtf8("saveNowButton_2"))
        self.horizontalLayout_5.addWidget(self.saveNowButton_2)
        self.cancelButton_2 = QtGui.QPushButton(self.burronFrame)
        self.cancelButton_2.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancelButton_2.setFont(font)
        self.cancelButton_2.setObjectName(_fromUtf8("cancelButton_2"))
        self.horizontalLayout_5.addWidget(self.cancelButton_2)
        self.verticalLayout.addWidget(self.burronFrame)
        FileSave.setCentralWidget(self.centralwidget)

        self.retranslateUi(FileSave)
        QtCore.QMetaObject.connectSlotsByName(FileSave)

    def retranslateUi(self, FileSave):
        FileSave.setWindowTitle(_translate("FileSave", "MainWindow", None))
        self.label_6.setText(_translate("FileSave", "KEYWORDS:", None))
        self.label_4.setText(_translate("FileSave", "FILENAME:", None))
        self.saveNowButton_2.setText(_translate("FileSave", "SAVE NOW", None))
        self.cancelButton_2.setText(_translate("FileSave", "CANCEL", None))


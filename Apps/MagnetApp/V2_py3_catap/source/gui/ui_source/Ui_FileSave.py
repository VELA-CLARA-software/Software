# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_FileSave.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FileSave(object):
    def setupUi(self, FileSave):
        FileSave.setObjectName("FileSave")
        FileSave.resize(706, 454)
        self.centralwidget = QtWidgets.QWidget(FileSave)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.commentFrame = QtWidgets.QFrame(self.centralwidget)
        self.commentFrame.setMinimumSize(QtCore.QSize(0, 200))
        self.commentFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.commentFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.commentFrame.setObjectName("commentFrame")
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout(self.commentFrame)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_5 = QtWidgets.QLabel(self.commentFrame)
        self.label_5.setMinimumSize(QtCore.QSize(90, 0))
        self.label_5.setMaximumSize(QtCore.QSize(90, 16777215))
        self.label_5.setBaseSize(QtCore.QSize(0, 200))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_7.addWidget(self.label_5)
        self.commentsSection = QtWidgets.QPlainTextEdit(self.commentFrame)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.commentsSection.setFont(font)
        self.commentsSection.setObjectName("commentsSection")
        self.horizontalLayout_7.addWidget(self.commentsSection)
        self.verticalLayout.addWidget(self.commentFrame)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setMinimumSize(QtCore.QSize(90, 0))
        self.label_6.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 0, 0, 1, 1)
        self.path_name_entry = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.path_name_entry.setFont(font)
        self.path_name_entry.setObjectName("path_name_entry")
        self.gridLayout.addWidget(self.path_name_entry, 0, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setMinimumSize(QtCore.QSize(90, 0))
        self.label_4.setMaximumSize(QtCore.QSize(90, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 1, 0, 1, 1)
        self.file_name_entry = QtWidgets.QLineEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.file_name_entry.setFont(font)
        self.file_name_entry.setObjectName("file_name_entry")
        self.gridLayout.addWidget(self.file_name_entry, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.burronFrame = QtWidgets.QFrame(self.centralwidget)
        self.burronFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.burronFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.burronFrame.setObjectName("burronFrame")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.burronFrame)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.saveNowButton_2 = QtWidgets.QPushButton(self.burronFrame)
        self.saveNowButton_2.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.saveNowButton_2.setFont(font)
        self.saveNowButton_2.setObjectName("saveNowButton_2")
        self.horizontalLayout_5.addWidget(self.saveNowButton_2)
        self.cancelButton_2 = QtWidgets.QPushButton(self.burronFrame)
        self.cancelButton_2.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.cancelButton_2.setFont(font)
        self.cancelButton_2.setObjectName("cancelButton_2")
        self.horizontalLayout_5.addWidget(self.cancelButton_2)
        self.verticalLayout.addWidget(self.burronFrame)
        FileSave.setCentralWidget(self.centralwidget)

        self.retranslateUi(FileSave)
        QtCore.QMetaObject.connectSlotsByName(FileSave)

    def retranslateUi(self, FileSave):
        _translate = QtCore.QCoreApplication.translate
        FileSave.setWindowTitle(_translate("FileSave", "MainWindow"))
        self.label_5.setText(_translate("FileSave", "COMMENTS:"))
        self.label_6.setText(_translate("FileSave", "PATH"))
        self.label_4.setText(_translate("FileSave", "FILENAME:"))
        self.saveNowButton_2.setText(_translate("FileSave", "SAVE NOW"))
        self.cancelButton_2.setText(_translate("FileSave", "CANCEL"))

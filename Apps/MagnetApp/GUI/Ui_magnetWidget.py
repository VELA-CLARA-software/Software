# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_magnetWidget.ui'
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

class Ui_magnetWidget(object):
    def setupUi(self, magnetWidget):
        magnetWidget.setObjectName(_fromUtf8("magnetWidget"))
        magnetWidget.resize(94, 120)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(magnetWidget.sizePolicy().hasHeightForWidth())
        magnetWidget.setSizePolicy(sizePolicy)
        magnetWidget.setMinimumSize(QtCore.QSize(80, 120))
        magnetWidget.setMaximumSize(QtCore.QSize(94, 120))
        self.PSU_R_State_Button = QtGui.QPushButton(magnetWidget)
        self.PSU_R_State_Button.setGeometry(QtCore.QRect(54, 72, 20, 15))
        self.PSU_R_State_Button.setMinimumSize(QtCore.QSize(20, 15))
        self.PSU_R_State_Button.setMaximumSize(QtCore.QSize(20, 15))
        self.PSU_R_State_Button.setObjectName(_fromUtf8("PSU_R_State_Button"))
        self.SIValue = QtGui.QDoubleSpinBox(magnetWidget)
        self.SIValue.setGeometry(QtCore.QRect(34, 91, 41, 20))
        self.SIValue.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.SIValue.setDecimals(3)
        self.SIValue.setMinimum(-1000.0)
        self.SIValue.setMaximum(1000.0)
        self.SIValue.setSingleStep(0.001)
        self.SIValue.setObjectName(_fromUtf8("SIValue"))
        self.RIMeter = QtGui.QSlider(magnetWidget)
        self.RIMeter.setGeometry(QtCore.QRect(14, 11, 15, 80))
        self.RIMeter.setOrientation(QtCore.Qt.Vertical)
        self.RIMeter.setObjectName(_fromUtf8("RIMeter"))
        self.PSU_N_State_Button = QtGui.QPushButton(magnetWidget)
        self.PSU_N_State_Button.setGeometry(QtCore.QRect(32, 72, 20, 15))
        self.PSU_N_State_Button.setMinimumSize(QtCore.QSize(20, 15))
        self.PSU_N_State_Button.setMaximumSize(QtCore.QSize(20, 15))
        self.PSU_N_State_Button.setObjectName(_fromUtf8("PSU_N_State_Button"))
        self.Mag_PSU_State_Button = QtGui.QPushButton(magnetWidget)
        self.Mag_PSU_State_Button.setGeometry(QtCore.QRect(32, 30, 43, 41))
        self.Mag_PSU_State_Button.setMinimumSize(QtCore.QSize(43, 0))
        self.Mag_PSU_State_Button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Mag_PSU_State_Button.setAutoDefault(False)
        self.Mag_PSU_State_Button.setDefault(False)
        self.Mag_PSU_State_Button.setObjectName(_fromUtf8("Mag_PSU_State_Button"))
        self.mag_Active = QtGui.QCheckBox(magnetWidget)
        self.mag_Active.setGeometry(QtCore.QRect(15, 91, 20, 20))
        self.mag_Active.setMinimumSize(QtCore.QSize(20, 20))
        self.mag_Active.setMaximumSize(QtCore.QSize(20, 19))
        self.mag_Active.setText(_fromUtf8(""))
        self.mag_Active.setIconSize(QtCore.QSize(20, 20))
        self.mag_Active.setTristate(False)
        self.mag_Active.setObjectName(_fromUtf8("mag_Active"))
        self.name = QtGui.QLabel(magnetWidget)
        self.name.setGeometry(QtCore.QRect(33, 10, 41, 20))
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setObjectName(_fromUtf8("name"))

        self.retranslateUi(magnetWidget)
        QtCore.QMetaObject.connectSlotsByName(magnetWidget)

    def retranslateUi(self, magnetWidget):
        magnetWidget.setWindowTitle(_translate("magnetWidget", "Form", None))
        self.PSU_R_State_Button.setText(_translate("magnetWidget", "R", None))
        self.PSU_N_State_Button.setText(_translate("magnetWidget", "N", None))
        self.Mag_PSU_State_Button.setText(_translate("magnetWidget", "ERR", None))
        self.name.setText(_translate("magnetWidget", "Name", None))


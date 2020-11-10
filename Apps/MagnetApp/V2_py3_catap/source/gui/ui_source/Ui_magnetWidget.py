# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_magnetWidget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_magnetWidget(object):
    def setupUi(self, magnetWidget):
        magnetWidget.setObjectName("magnetWidget")
        magnetWidget.resize(100, 120)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(magnetWidget.sizePolicy().hasHeightForWidth())
        magnetWidget.setSizePolicy(sizePolicy)
        magnetWidget.setMinimumSize(QtCore.QSize(100, 120))
        magnetWidget.setMaximumSize(QtCore.QSize(100, 120))
        self.SIValue = QtWidgets.QDoubleSpinBox(magnetWidget)
        self.SIValue.setGeometry(QtCore.QRect(25, 91, 71, 20))
        self.SIValue.setMinimumSize(QtCore.QSize(10, 10))
        self.SIValue.setButtonSymbols(QtWidgets.QAbstractSpinBox.PlusMinus)
        self.SIValue.setDecimals(3)
        self.SIValue.setMinimum(-1000.0)
        self.SIValue.setMaximum(1000.0)
        self.SIValue.setSingleStep(0.001)
        self.SIValue.setObjectName("SIValue")
        self.RIMeter = QtWidgets.QSlider(magnetWidget)
        self.RIMeter.setGeometry(QtCore.QRect(5, 11, 15, 80))
        self.RIMeter.setOrientation(QtCore.Qt.Vertical)
        self.RIMeter.setObjectName("RIMeter")
        self.Mag_PSU_State_Button = QtWidgets.QPushButton(magnetWidget)
        self.Mag_PSU_State_Button.setGeometry(QtCore.QRect(33, 40, 43, 41))
        self.Mag_PSU_State_Button.setMinimumSize(QtCore.QSize(43, 0))
        self.Mag_PSU_State_Button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Mag_PSU_State_Button.setAutoDefault(False)
        self.Mag_PSU_State_Button.setDefault(False)
        self.Mag_PSU_State_Button.setObjectName("Mag_PSU_State_Button")
        self.mag_Active = QtWidgets.QRadioButton(magnetWidget)
        self.mag_Active.setGeometry(QtCore.QRect(7, 91, 20, 20))
        self.mag_Active.setMinimumSize(QtCore.QSize(20, 20))
        self.mag_Active.setMaximumSize(QtCore.QSize(20, 19))
        self.mag_Active.setText("")
        self.mag_Active.setIconSize(QtCore.QSize(20, 20))
        self.mag_Active.setObjectName("mag_Active")
        self.name = QtWidgets.QLabel(magnetWidget)
        self.name.setGeometry(QtCore.QRect(23, 10, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(7)
        self.name.setFont(font)
        self.name.setAlignment(QtCore.Qt.AlignCenter)
        self.name.setWordWrap(True)
        self.name.setObjectName("name")

        self.retranslateUi(magnetWidget)
        QtCore.QMetaObject.connectSlotsByName(magnetWidget)

    def retranslateUi(self, magnetWidget):
        _translate = QtCore.QCoreApplication.translate
        magnetWidget.setWindowTitle(_translate("magnetWidget", "Form"))
        self.Mag_PSU_State_Button.setText(_translate("magnetWidget", "ERR"))
        self.name.setText(_translate("magnetWidget", "Name"))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vc_image_auto_save_gui.ui'
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

class Ui_VC_IMAGE_AUTO_SAVE(object):
    def setupUi(self, VC_IMAGE_AUTO_SAVE):
        VC_IMAGE_AUTO_SAVE.setObjectName(_fromUtf8("VC_IMAGE_AUTO_SAVE"))
        VC_IMAGE_AUTO_SAVE.resize(336, 395)
        self.centralwidget = QtGui.QWidget(VC_IMAGE_AUTO_SAVE)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.minutes_to_next_save = QtGui.QDoubleSpinBox(self.centralwidget)
        self.minutes_to_next_save.setMinimumSize(QtCore.QSize(75, 0))
        self.minutes_to_next_save.setMaximumSize(QtCore.QSize(75, 16777215))
        self.minutes_to_next_save.setMinimum(0.1)
        self.minutes_to_next_save.setMaximum(999.0)
        self.minutes_to_next_save.setProperty("value", 30.0)
        self.minutes_to_next_save.setObjectName(_fromUtf8("minutes_to_next_save"))
        self.horizontalLayout.addWidget(self.minutes_to_next_save)
        self.label = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout.addWidget(self.label)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pix_int_threshold = QtGui.QDoubleSpinBox(self.centralwidget)
        self.pix_int_threshold.setMinimumSize(QtCore.QSize(75, 0))
        self.pix_int_threshold.setMaximumSize(QtCore.QSize(75, 16777215))
        self.pix_int_threshold.setMinimum(0.1)
        self.pix_int_threshold.setMaximum(500.0)
        self.pix_int_threshold.setProperty("value", 50.0)
        self.pix_int_threshold.setObjectName(_fromUtf8("pix_int_threshold"))
        self.horizontalLayout_2.addWidget(self.pix_int_threshold)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_2.addWidget(self.label_7)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_1 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_1.setFont(font)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.verticalLayout.addWidget(self.label_1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout.addWidget(self.label_6)
        VC_IMAGE_AUTO_SAVE.setCentralWidget(self.centralwidget)

        self.retranslateUi(VC_IMAGE_AUTO_SAVE)
        QtCore.QMetaObject.connectSlotsByName(VC_IMAGE_AUTO_SAVE)

    def retranslateUi(self, VC_IMAGE_AUTO_SAVE):
        VC_IMAGE_AUTO_SAVE.setWindowTitle(_translate("VC_IMAGE_AUTO_SAVE", "MainWindow", None))
        self.checkBox.setText(_translate("VC_IMAGE_AUTO_SAVE", "Autosave Virtual Cathode Images", None))
        self.label.setText(_translate("VC_IMAGE_AUTO_SAVE", "Mins Between Saves", None))
        self.label_7.setText(_translate("VC_IMAGE_AUTO_SAVE", "Average Pixel Intensity threshold", None))
        self.label_1.setText(_translate("VC_IMAGE_AUTO_SAVE", "TextLabel 1", None))
        self.label_2.setText(_translate("VC_IMAGE_AUTO_SAVE", "TextLabel 1", None))
        self.label_3.setText(_translate("VC_IMAGE_AUTO_SAVE", "TextLabel 1", None))
        self.label_4.setText(_translate("VC_IMAGE_AUTO_SAVE", "TextLabel 1", None))
        self.label_5.setText(_translate("VC_IMAGE_AUTO_SAVE", "TextLabel 1", None))
        self.label_6.setText(_translate("VC_IMAGE_AUTO_SAVE", "TextLabel 1", None))


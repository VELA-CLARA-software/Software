# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
<<<<<<< HEAD
        MainWindow.resize(954, 699)
=======
        MainWindow.resize(643, 679)
>>>>>>> efec22cf5e952f3d87d75e4a21930c12008c3145
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
<<<<<<< HEAD
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 17, 0, 1, 1)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 5, 0, 1, 2)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 10, 0, 1, 2)
        self.spinBox_maxLevel = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_maxLevel.setMaximum(65536)
        self.spinBox_maxLevel.setSingleStep(100)
        self.spinBox_maxLevel.setProperty("value", 65536)
        self.spinBox_maxLevel.setObjectName(_fromUtf8("spinBox_maxLevel"))
        self.gridLayout.addWidget(self.spinBox_maxLevel, 4, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 14, 0, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.liveStream_pushButton = QtGui.QPushButton(self.centralwidget)
        self.liveStream_pushButton.setObjectName(_fromUtf8("liveStream_pushButton"))
        self.gridLayout.addWidget(self.liveStream_pushButton, 2, 0, 1, 2)
        self.maskYRadius_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskYRadius_spinBox.setMaximum(9999)
        self.maskYRadius_spinBox.setObjectName(_fromUtf8("maskYRadius_spinBox"))
        self.gridLayout.addWidget(self.maskYRadius_spinBox, 18, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 7, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 13, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 16, 0, 1, 1)
        self.spinBox_minLevel = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_minLevel.setMaximum(65536)
        self.spinBox_minLevel.setSingleStep(100)
        self.spinBox_minLevel.setObjectName(_fromUtf8("spinBox_minLevel"))
        self.gridLayout.addWidget(self.spinBox_minLevel, 4, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 18, 0, 1, 1)
        self.getImages_pushButton = QtGui.QPushButton(self.centralwidget)
        self.getImages_pushButton.setObjectName(_fromUtf8("getImages_pushButton"))
        self.gridLayout.addWidget(self.getImages_pushButton, 9, 0, 1, 2)
        self.setMask_pushButton = QtGui.QPushButton(self.centralwidget)
        self.setMask_pushButton.setObjectName(_fromUtf8("setMask_pushButton"))
        self.gridLayout.addWidget(self.setMask_pushButton, 19, 0, 1, 2)
        self.acquire_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.acquire_pushButton.sizePolicy().hasHeightForWidth())
        self.acquire_pushButton.setSizePolicy(sizePolicy)
        self.acquire_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.acquire_pushButton.setObjectName(_fromUtf8("acquire_pushButton"))
        self.gridLayout.addWidget(self.acquire_pushButton, 6, 0, 1, 2)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.analyse_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.analyse_pushButton.sizePolicy().hasHeightForWidth())
        self.analyse_pushButton.setSizePolicy(sizePolicy)
        self.analyse_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.analyse_pushButton.setObjectName(_fromUtf8("analyse_pushButton"))
        self.gridLayout.addWidget(self.analyse_pushButton, 11, 0, 1, 2)
        self.cameraName_comboBox = QtGui.QComboBox(self.centralwidget)
        self.cameraName_comboBox.setObjectName(_fromUtf8("cameraName_comboBox"))
        self.gridLayout.addWidget(self.cameraName_comboBox, 1, 0, 1, 2)
        self.maskXRadius_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskXRadius_spinBox.setMaximum(9999)
        self.maskXRadius_spinBox.setObjectName(_fromUtf8("maskXRadius_spinBox"))
        self.gridLayout.addWidget(self.maskXRadius_spinBox, 17, 1, 1, 1)
        self.numImages_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.numImages_spinBox.setMinimum(1)
        self.numImages_spinBox.setObjectName(_fromUtf8("numImages_spinBox"))
        self.gridLayout.addWidget(self.numImages_spinBox, 7, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 15, 0, 1, 1)
=======
>>>>>>> efec22cf5e952f3d87d75e4a21930c12008c3145
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.avPixIntensity_label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.avPixIntensity_label.setFont(font)
        self.avPixIntensity_label.setObjectName(_fromUtf8("avPixIntensity_label"))
        self.gridLayout_3.addWidget(self.avPixIntensity_label, 0, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_3.addWidget(self.label_11, 3, 0, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_3.addWidget(self.label_12, 4, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 5, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 2, 0, 1, 1)
        self.label_14 = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_3.addWidget(self.label_14, 1, 0, 1, 1)
        self.sxMM_label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.sxMM_label.setFont(font)
        self.sxMM_label.setObjectName(_fromUtf8("sxMM_label"))
        self.gridLayout_3.addWidget(self.sxMM_label, 3, 1, 1, 1)
        self.yMM_label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.yMM_label.setFont(font)
        self.yMM_label.setObjectName(_fromUtf8("yMM_label"))
        self.gridLayout_3.addWidget(self.yMM_label, 2, 1, 1, 1)
        self.syMM_label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.syMM_label.setFont(font)
        self.syMM_label.setObjectName(_fromUtf8("syMM_label"))
        self.gridLayout_3.addWidget(self.syMM_label, 4, 1, 1, 1)
        self.xMM_label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.xMM_label.setFont(font)
        self.xMM_label.setObjectName(_fromUtf8("xMM_label"))
        self.gridLayout_3.addWidget(self.xMM_label, 1, 1, 1, 1)
        self.apI_label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.apI_label.setFont(font)
        self.apI_label.setObjectName(_fromUtf8("apI_label"))
        self.gridLayout_3.addWidget(self.apI_label, 0, 1, 1, 1)
        self.covXY_label = QtGui.QLabel(self.groupBox)
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.covXY_label.setFont(font)
        self.covXY_label.setObjectName(_fromUtf8("covXY_label"))
        self.gridLayout_3.addWidget(self.covXY_label, 5, 1, 1, 1)
<<<<<<< HEAD
        self.gridLayout.addWidget(self.groupBox, 20, 0, 1, 2)
        self.maskY_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskY_spinBox.setMaximum(9999)
        self.maskY_spinBox.setObjectName(_fromUtf8("maskY_spinBox"))
        self.gridLayout.addWidget(self.maskY_spinBox, 16, 1, 1, 1)
        self.useBackground_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.useBackground_checkBox.setObjectName(_fromUtf8("useBackground_checkBox"))
        self.gridLayout.addWidget(self.useBackground_checkBox, 12, 1, 1, 1)
=======
        self.gridLayout.addWidget(self.groupBox, 22, 0, 7, 2)
        self.useNPoint_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.useNPoint_checkBox.setObjectName(_fromUtf8("useNPoint_checkBox"))
        self.gridLayout.addWidget(self.useNPoint_checkBox, 15, 0, 1, 1)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 11, 0, 1, 2)
        self.maskXRadius_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskXRadius_spinBox.setMaximum(9999)
        self.maskXRadius_spinBox.setObjectName(_fromUtf8("maskXRadius_spinBox"))
        self.gridLayout.addWidget(self.maskXRadius_spinBox, 19, 1, 1, 1)
        self.getImages_pushButton = QtGui.QPushButton(self.centralwidget)
        self.getImages_pushButton.setObjectName(_fromUtf8("getImages_pushButton"))
        self.gridLayout.addWidget(self.getImages_pushButton, 10, 0, 1, 2)
        self.spinBox_maxLevel = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_maxLevel.setMaximum(65536)
        self.spinBox_maxLevel.setProperty("value", 65536)
        self.spinBox_maxLevel.setObjectName(_fromUtf8("spinBox_maxLevel"))
        self.gridLayout.addWidget(self.spinBox_maxLevel, 5, 1, 1, 1)
        self.resetBackground_pushButton = QtGui.QPushButton(self.centralwidget)
        self.resetBackground_pushButton.setObjectName(_fromUtf8("resetBackground_pushButton"))
        self.gridLayout.addWidget(self.resetBackground_pushButton, 13, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.liveStream_pushButton = QtGui.QPushButton(self.centralwidget)
        self.liveStream_pushButton.setObjectName(_fromUtf8("liveStream_pushButton"))
        self.gridLayout.addWidget(self.liveStream_pushButton, 2, 0, 1, 2)
>>>>>>> efec22cf5e952f3d87d75e4a21930c12008c3145
        self.stepSize_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.stepSize_spinBox.setMinimum(1)
        self.stepSize_spinBox.setMaximum(10)
        self.stepSize_spinBox.setSingleStep(1)
        self.stepSize_spinBox.setProperty("value", 1)
        self.stepSize_spinBox.setObjectName(_fromUtf8("stepSize_spinBox"))
<<<<<<< HEAD
        self.gridLayout.addWidget(self.stepSize_spinBox, 14, 1, 1, 1)
        self.useNPoint_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.useNPoint_checkBox.setObjectName(_fromUtf8("useNPoint_checkBox"))
        self.gridLayout.addWidget(self.useNPoint_checkBox, 13, 0, 1, 1)
        self.maskX_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskX_spinBox.setMaximum(9999)
        self.maskX_spinBox.setObjectName(_fromUtf8("maskX_spinBox"))
        self.gridLayout.addWidget(self.maskX_spinBox, 15, 1, 1, 1)
        self.resetBackground_pushButton = QtGui.QPushButton(self.centralwidget)
        self.resetBackground_pushButton.setObjectName(_fromUtf8("resetBackground_pushButton"))
        self.gridLayout.addWidget(self.resetBackground_pushButton, 12, 0, 1, 1)
        self.save_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_pushButton.sizePolicy().hasHeightForWidth())
        self.save_pushButton.setSizePolicy(sizePolicy)
        self.save_pushButton.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.save_pushButton.setObjectName(_fromUtf8("save_pushButton"))
        self.gridLayout.addWidget(self.save_pushButton, 8, 0, 1, 2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout.addLayout(self.gridLayout_2, 0, 2, 21, 1)
        self.gridLayout.setColumnStretch(1, 1)
        self.gridLayout.setColumnStretch(2, 20)
        self.label_3.raise_()
        self.liveStream_pushButton.raise_()
        self.label.raise_()
        self.label_4.raise_()
        self.cameraName_comboBox.raise_()
        self.spinBox_minLevel.raise_()
        self.spinBox_maxLevel.raise_()
        self.line.raise_()
        self.acquire_pushButton.raise_()
        self.label_2.raise_()
        self.numImages_spinBox.raise_()
        self.save_pushButton.raise_()
        self.getImages_pushButton.raise_()
        self.line_2.raise_()
        self.analyse_pushButton.raise_()
        self.resetBackground_pushButton.raise_()
        self.useBackground_checkBox.raise_()
        self.useNPoint_checkBox.raise_()
        self.checkBox.raise_()
        self.label_5.raise_()
        self.stepSize_spinBox.raise_()
        self.label_6.raise_()
        self.maskX_spinBox.raise_()
        self.label_7.raise_()
        self.maskY_spinBox.raise_()
        self.label_8.raise_()
        self.maskXRadius_spinBox.raise_()
        self.label_9.raise_()
        self.maskYRadius_spinBox.raise_()
        self.setMask_pushButton.raise_()
        self.groupBox.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 954, 21))
=======
        self.gridLayout.addWidget(self.stepSize_spinBox, 16, 1, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setScaledContents(False)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.maskY_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskY_spinBox.setMaximum(9999)
        self.maskY_spinBox.setObjectName(_fromUtf8("maskY_spinBox"))
        self.gridLayout.addWidget(self.maskY_spinBox, 18, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 8, 0, 1, 1)
        self.spinBox_minLevel = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_minLevel.setMaximum(65536)
        self.spinBox_minLevel.setObjectName(_fromUtf8("spinBox_minLevel"))
        self.gridLayout.addWidget(self.spinBox_minLevel, 5, 0, 1, 1)
        self.numImages_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.numImages_spinBox.setMinimum(1)
        self.numImages_spinBox.setObjectName(_fromUtf8("numImages_spinBox"))
        self.gridLayout.addWidget(self.numImages_spinBox, 8, 1, 1, 1)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 6, 0, 1, 2)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 16, 0, 1, 1)
        self.useBackground_checkBox = QtGui.QCheckBox(self.centralwidget)
        self.useBackground_checkBox.setObjectName(_fromUtf8("useBackground_checkBox"))
        self.gridLayout.addWidget(self.useBackground_checkBox, 13, 1, 1, 1)
        self.maskX_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskX_spinBox.setMaximum(9999)
        self.maskX_spinBox.setObjectName(_fromUtf8("maskX_spinBox"))
        self.gridLayout.addWidget(self.maskX_spinBox, 17, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.centralwidget)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 18, 0, 1, 1)
        self.acquire_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.acquire_pushButton.sizePolicy().hasHeightForWidth())
        self.acquire_pushButton.setSizePolicy(sizePolicy)
        self.acquire_pushButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.acquire_pushButton.setObjectName(_fromUtf8("acquire_pushButton"))
        self.gridLayout.addWidget(self.acquire_pushButton, 7, 0, 1, 2)
        self.label_8 = QtGui.QLabel(self.centralwidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 19, 0, 1, 1)
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout.addWidget(self.checkBox, 15, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 17, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.centralwidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 20, 0, 1, 1)
        self.cameraName_comboBox = QtGui.QComboBox(self.centralwidget)
        self.cameraName_comboBox.setObjectName(_fromUtf8("cameraName_comboBox"))
        self.gridLayout.addWidget(self.cameraName_comboBox, 1, 0, 1, 2)
        self.save_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.save_pushButton.sizePolicy().hasHeightForWidth())
        self.save_pushButton.setSizePolicy(sizePolicy)
        self.save_pushButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.save_pushButton.setObjectName(_fromUtf8("save_pushButton"))
        self.gridLayout.addWidget(self.save_pushButton, 9, 0, 1, 2)
        self.maskYRadius_spinBox = QtGui.QSpinBox(self.centralwidget)
        self.maskYRadius_spinBox.setMaximum(9999)
        self.maskYRadius_spinBox.setObjectName(_fromUtf8("maskYRadius_spinBox"))
        self.gridLayout.addWidget(self.maskYRadius_spinBox, 20, 1, 1, 1)
        self.analyse_pushButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(20)
        sizePolicy.setHeightForWidth(self.analyse_pushButton.sizePolicy().hasHeightForWidth())
        self.analyse_pushButton.setSizePolicy(sizePolicy)
        self.analyse_pushButton.setMaximumSize(QtCore.QSize(16777215, 100))
        self.analyse_pushButton.setObjectName(_fromUtf8("analyse_pushButton"))
        self.gridLayout.addWidget(self.analyse_pushButton, 12, 0, 1, 2)
        self.setMask_pushButton = QtGui.QPushButton(self.centralwidget)
        self.setMask_pushButton.setObjectName(_fromUtf8("setMask_pushButton"))
        self.gridLayout.addWidget(self.setMask_pushButton, 21, 0, 1, 2)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout.addLayout(self.gridLayout_2, 0, 2, 22, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 643, 18))
>>>>>>> efec22cf5e952f3d87d75e4a21930c12008c3145
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
<<<<<<< HEAD
        MainWindow.setTabOrder(self.cameraName_comboBox, self.liveStream_pushButton)
        MainWindow.setTabOrder(self.liveStream_pushButton, self.spinBox_minLevel)
        MainWindow.setTabOrder(self.spinBox_minLevel, self.spinBox_maxLevel)
        MainWindow.setTabOrder(self.spinBox_maxLevel, self.acquire_pushButton)
        MainWindow.setTabOrder(self.acquire_pushButton, self.numImages_spinBox)
        MainWindow.setTabOrder(self.numImages_spinBox, self.save_pushButton)
        MainWindow.setTabOrder(self.save_pushButton, self.getImages_pushButton)
        MainWindow.setTabOrder(self.getImages_pushButton, self.analyse_pushButton)
        MainWindow.setTabOrder(self.analyse_pushButton, self.resetBackground_pushButton)
        MainWindow.setTabOrder(self.resetBackground_pushButton, self.useBackground_checkBox)
        MainWindow.setTabOrder(self.useBackground_checkBox, self.useNPoint_checkBox)
        MainWindow.setTabOrder(self.useNPoint_checkBox, self.checkBox)
        MainWindow.setTabOrder(self.checkBox, self.stepSize_spinBox)
        MainWindow.setTabOrder(self.stepSize_spinBox, self.maskX_spinBox)
        MainWindow.setTabOrder(self.maskX_spinBox, self.maskY_spinBox)
        MainWindow.setTabOrder(self.maskY_spinBox, self.maskXRadius_spinBox)
        MainWindow.setTabOrder(self.maskXRadius_spinBox, self.maskYRadius_spinBox)
        MainWindow.setTabOrder(self.maskYRadius_spinBox, self.setMask_pushButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Collector", None))
        self.label_8.setText(_translate("MainWindow", "Mask X Radius Pixel:", None))
        self.label_5.setText(_translate("MainWindow", "Step Size:", None))
        self.label.setText(_translate("MainWindow", "Selected Camera:", None))
        self.label_3.setText(_translate("MainWindow", "Min. Level:", None))
        self.liveStream_pushButton.setText(_translate("MainWindow", "Live Stream", None))
        self.label_2.setText(_translate("MainWindow", "Number of Images:", None))
        self.checkBox.setText(_translate("MainWindow", "Feedback", None))
        self.label_7.setText(_translate("MainWindow", "Mask Center Y Pixel:", None))
        self.label_9.setText(_translate("MainWindow", "Mask Y Radius Pixel:", None))
        self.getImages_pushButton.setText(_translate("MainWindow", "Open Image Directory", None))
        self.setMask_pushButton.setText(_translate("MainWindow", "Set Mask", None))
        self.acquire_pushButton.setText(_translate("MainWindow", "Acquire", None))
        self.label_4.setText(_translate("MainWindow", "Max. Level:", None))
        self.analyse_pushButton.setText(_translate("MainWindow", "Analyse", None))
        self.label_6.setText(_translate("MainWindow", "Mask Center X Pixel:", None))
        self.groupBox.setTitle(_translate("MainWindow", "Results (mm)", None))
        self.avPixIntensity_label.setText(_translate("MainWindow", "Average Pixel Intensity:", None))
        self.label_11.setText(_translate("MainWindow", "Sigma X:", None))
        self.label_12.setText(_translate("MainWindow", "Sigma Y:", None))
        self.label_13.setText(_translate("MainWindow", "Covariance XY (mm²): ", None))
=======

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Image Collector", None))
        self.groupBox.setTitle(_translate("MainWindow", "Results (mm)", None))
        self.avPixIntensity_label.setText(_translate("MainWindow", "Average Pixel Intesity:", None))
        self.label_11.setText(_translate("MainWindow", "Sigma X:", None))
        self.label_12.setText(_translate("MainWindow", "Sigma Y:", None))
        self.label_13.setText(_translate("MainWindow", "Covariance XY (mm^2): ", None))
>>>>>>> efec22cf5e952f3d87d75e4a21930c12008c3145
        self.label_10.setText(_translate("MainWindow", "Y:", None))
        self.label_14.setText(_translate("MainWindow", "X:", None))
        self.sxMM_label.setText(_translate("MainWindow", "-", None))
        self.yMM_label.setText(_translate("MainWindow", "-", None))
        self.syMM_label.setText(_translate("MainWindow", "-", None))
        self.xMM_label.setText(_translate("MainWindow", "-", None))
        self.apI_label.setText(_translate("MainWindow", "-", None))
        self.covXY_label.setText(_translate("MainWindow", "-", None))
<<<<<<< HEAD
        self.useBackground_checkBox.setText(_translate("MainWindow", "Use Background", None))
        self.useNPoint_checkBox.setText(_translate("MainWindow", "Use N-Point Scaling", None))
        self.resetBackground_pushButton.setText(_translate("MainWindow", "Reset Background Image", None))
        self.save_pushButton.setText(_translate("MainWindow", "Collect and Save", None))
=======
        self.useNPoint_checkBox.setText(_translate("MainWindow", "Use N-Point Scaling", None))
        self.getImages_pushButton.setText(_translate("MainWindow", "Open Image Directory", None))
        self.resetBackground_pushButton.setText(_translate("MainWindow", "Reset Background Image", None))
        self.label_3.setText(_translate("MainWindow", "Min. Level:", None))
        self.liveStream_pushButton.setText(_translate("MainWindow", "Live Steam", None))
        self.label.setText(_translate("MainWindow", "Selected Camera:", None))
        self.label_2.setText(_translate("MainWindow", "Number of Images:", None))
        self.label_5.setText(_translate("MainWindow", "Step Size:", None))
        self.useBackground_checkBox.setText(_translate("MainWindow", "Use Background", None))
        self.label_7.setText(_translate("MainWindow", "Mask Center Y Pixel:", None))
        self.acquire_pushButton.setText(_translate("MainWindow", "Acquire", None))
        self.label_8.setText(_translate("MainWindow", "Mask X Radius Pixel:", None))
        self.checkBox.setText(_translate("MainWindow", "Feedback", None))
        self.label_4.setText(_translate("MainWindow", "Max. Level:", None))
        self.label_6.setText(_translate("MainWindow", "Mask Center X Pixel:", None))
        self.label_9.setText(_translate("MainWindow", "Mask Y Radius Pixel:", None))
        self.save_pushButton.setText(_translate("MainWindow", "Collect and Save", None))
        self.analyse_pushButton.setText(_translate("MainWindow", "Analyse", None))
        self.setMask_pushButton.setText(_translate("MainWindow", "Set Mask", None))
>>>>>>> efec22cf5e952f3d87d75e4a21930c12008c3145


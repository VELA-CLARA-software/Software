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
        MainWindow.resize(1313, 856)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("resources/byscitv2/icon.ico")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.checkBox_showBVNFit = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_showBVNFit.setObjectName(_fromUtf8("checkBox_showBVNFit"))
        self.gridLayout.addWidget(self.checkBox_showBVNFit, 3, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.centralwidget)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 7, 2, 1, 1)
        self.label = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 7, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 7, 1, 1, 1)
        self.checkBox_show3DLens = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_show3DLens.setObjectName(_fromUtf8("checkBox_show3DLens"))
        self.gridLayout.addWidget(self.checkBox_show3DLens, 6, 0, 1, 1)
        self.checkBox_showSaturatedPixels = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_showSaturatedPixels.setObjectName(_fromUtf8("checkBox_showSaturatedPixels"))
        self.gridLayout.addWidget(self.checkBox_showSaturatedPixels, 5, 0, 1, 1)
        self.checkBox_showMLEFit = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_showMLEFit.setObjectName(_fromUtf8("checkBox_showMLEFit"))
        self.gridLayout.addWidget(self.checkBox_showMLEFit, 4, 0, 1, 1)
        self.spinBox_min = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_min.setMaximum(65535)
        self.spinBox_min.setObjectName(_fromUtf8("spinBox_min"))
        self.gridLayout.addWidget(self.spinBox_min, 8, 0, 1, 1)
        self.spinBox_max = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_max.setMaximum(65535)
        self.spinBox_max.setProperty("value", 65535)
        self.spinBox_max.setObjectName(_fromUtf8("spinBox_max"))
        self.gridLayout.addWidget(self.spinBox_max, 8, 1, 1, 1)
        self.spinBox_satLevel = QtGui.QSpinBox(self.centralwidget)
        self.spinBox_satLevel.setMaximum(65535)
        self.spinBox_satLevel.setProperty("value", 30000)
        self.spinBox_satLevel.setObjectName(_fromUtf8("spinBox_satLevel"))
        self.gridLayout.addWidget(self.spinBox_satLevel, 8, 2, 1, 1)
        self.line = QtGui.QFrame(self.centralwidget)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 21, 0, 1, 3)
        self.label_syBVN = QtGui.QLabel(self.centralwidget)
        self.label_syBVN.setAlignment(QtCore.Qt.AlignCenter)
        self.label_syBVN.setObjectName(_fromUtf8("label_syBVN"))
        self.gridLayout.addWidget(self.label_syBVN, 18, 1, 1, 1)
        self.label_19 = QtGui.QLabel(self.centralwidget)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout.addWidget(self.label_19, 18, 0, 1, 1)
        self.label_sxMLE = QtGui.QLabel(self.centralwidget)
        self.label_sxMLE.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sxMLE.setObjectName(_fromUtf8("label_sxMLE"))
        self.gridLayout.addWidget(self.label_sxMLE, 17, 2, 1, 1)
        self.label_sxBVN = QtGui.QLabel(self.centralwidget)
        self.label_sxBVN.setAlignment(QtCore.Qt.AlignCenter)
        self.label_sxBVN.setObjectName(_fromUtf8("label_sxBVN"))
        self.gridLayout.addWidget(self.label_sxBVN, 17, 1, 1, 1)
        self.label_cxyMLE = QtGui.QLabel(self.centralwidget)
        self.label_cxyMLE.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cxyMLE.setObjectName(_fromUtf8("label_cxyMLE"))
        self.gridLayout.addWidget(self.label_cxyMLE, 19, 2, 1, 1)
        self.label_cxyBVN = QtGui.QLabel(self.centralwidget)
        self.label_cxyBVN.setAlignment(QtCore.Qt.AlignCenter)
        self.label_cxyBVN.setObjectName(_fromUtf8("label_cxyBVN"))
        self.gridLayout.addWidget(self.label_cxyBVN, 19, 1, 1, 1)
        self.label_20 = QtGui.QLabel(self.centralwidget)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout.addWidget(self.label_20, 19, 0, 1, 1)
        self.label_syMLE = QtGui.QLabel(self.centralwidget)
        self.label_syMLE.setAlignment(QtCore.Qt.AlignCenter)
        self.label_syMLE.setObjectName(_fromUtf8("label_syMLE"))
        self.gridLayout.addWidget(self.label_syMLE, 18, 2, 1, 1)
        self.label_18 = QtGui.QLabel(self.centralwidget)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout.addWidget(self.label_18, 17, 0, 1, 1)
        self.label_yMLE = QtGui.QLabel(self.centralwidget)
        self.label_yMLE.setAlignment(QtCore.Qt.AlignCenter)
        self.label_yMLE.setObjectName(_fromUtf8("label_yMLE"))
        self.gridLayout.addWidget(self.label_yMLE, 16, 2, 1, 1)
        self.label_yBVN = QtGui.QLabel(self.centralwidget)
        self.label_yBVN.setAlignment(QtCore.Qt.AlignCenter)
        self.label_yBVN.setObjectName(_fromUtf8("label_yBVN"))
        self.gridLayout.addWidget(self.label_yBVN, 16, 1, 1, 1)
        self.label_17 = QtGui.QLabel(self.centralwidget)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout.addWidget(self.label_17, 16, 0, 1, 1)
        self.label_xMLE = QtGui.QLabel(self.centralwidget)
        self.label_xMLE.setAlignment(QtCore.Qt.AlignCenter)
        self.label_xMLE.setObjectName(_fromUtf8("label_xMLE"))
        self.gridLayout.addWidget(self.label_xMLE, 15, 2, 1, 1)
        self.label_xBVN = QtGui.QLabel(self.centralwidget)
        self.label_xBVN.setAlignment(QtCore.Qt.AlignCenter)
        self.label_xBVN.setObjectName(_fromUtf8("label_xBVN"))
        self.gridLayout.addWidget(self.label_xBVN, 15, 1, 1, 1)
        self.label_16 = QtGui.QLabel(self.centralwidget)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout.addWidget(self.label_16, 15, 0, 1, 1)
        self.label_5 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 14, 2, 1, 1)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 14, 1, 1, 1)
        self.line_2 = QtGui.QFrame(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout.addWidget(self.line_2, 12, 0, 1, 3)
        self.comboBox_colourMap = QtGui.QComboBox(self.centralwidget)
        self.comboBox_colourMap.setObjectName(_fromUtf8("comboBox_colourMap"))
        self.comboBox_colourMap.addItem(_fromUtf8(""))
        self.comboBox_colourMap.addItem(_fromUtf8(""))
        self.comboBox_colourMap.addItem(_fromUtf8(""))
        self.comboBox_colourMap.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_colourMap, 9, 2, 1, 1)
        self.label_ColourMap = QtGui.QLabel(self.centralwidget)
        self.label_ColourMap.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_ColourMap.setObjectName(_fromUtf8("label_ColourMap"))
        self.gridLayout.addWidget(self.label_ColourMap, 9, 1, 1, 1)
        self.checkBox_autoScale = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_autoScale.setChecked(True)
        self.checkBox_autoScale.setObjectName(_fromUtf8("checkBox_autoScale"))
        self.gridLayout.addWidget(self.checkBox_autoScale, 9, 0, 1, 1)
        self.checkBox_useBackground = QtGui.QCheckBox(self.centralwidget)
        self.checkBox_useBackground.setObjectName(_fromUtf8("checkBox_useBackground"))
        self.gridLayout.addWidget(self.checkBox_useBackground, 1, 2, 1, 1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout.addLayout(self.gridLayout_4, 0, 3, 23, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.checkBox_useCustomMask = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useCustomMask.setObjectName(_fromUtf8("checkBox_useCustomMask"))
        self.gridLayout_2.addWidget(self.checkBox_useCustomMask, 0, 0, 1, 1)
        self.lineEdit_lowestPixelValue = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_lowestPixelValue.setObjectName(_fromUtf8("lineEdit_lowestPixelValue"))
        self.gridLayout_2.addWidget(self.lineEdit_lowestPixelValue, 5, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_2.addWidget(self.label_7, 5, 3, 1, 1)
        self.checkBox_lowestPixValue = QtGui.QCheckBox(self.groupBox)
        self.checkBox_lowestPixValue.setObjectName(_fromUtf8("checkBox_lowestPixValue"))
        self.gridLayout_2.addWidget(self.checkBox_lowestPixValue, 5, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_2.addWidget(self.label_8, 4, 3, 1, 1)
        self.lineEdit_rollingAverage = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_rollingAverage.setObjectName(_fromUtf8("lineEdit_rollingAverage"))
        self.gridLayout_2.addWidget(self.lineEdit_rollingAverage, 4, 2, 1, 1)
        self.checkBox_rollingAverage = QtGui.QCheckBox(self.groupBox)
        self.checkBox_rollingAverage.setObjectName(_fromUtf8("checkBox_rollingAverage"))
        self.gridLayout_2.addWidget(self.checkBox_rollingAverage, 4, 0, 1, 2)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_2.addWidget(self.label_9, 3, 3, 1, 1)
        self.lineEdit_rSquared = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_rSquared.setObjectName(_fromUtf8("lineEdit_rSquared"))
        self.gridLayout_2.addWidget(self.lineEdit_rSquared, 3, 2, 1, 1)
        self.checkBox_rSquared = QtGui.QCheckBox(self.groupBox)
        self.checkBox_rSquared.setObjectName(_fromUtf8("checkBox_rSquared"))
        self.gridLayout_2.addWidget(self.checkBox_rSquared, 3, 0, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_2.addWidget(self.label_10, 1, 3, 1, 1)
        self.frame = QtGui.QFrame(self.groupBox)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_customRX = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_customRX.sizePolicy().hasHeightForWidth())
        self.label_customRX.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_customRX.setFont(font)
        self.label_customRX.setObjectName(_fromUtf8("label_customRX"))
        self.gridLayout_3.addWidget(self.label_customRX, 0, 2, 1, 1)
        self.label_customY = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_customY.sizePolicy().hasHeightForWidth())
        self.label_customY.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_customY.setFont(font)
        self.label_customY.setObjectName(_fromUtf8("label_customY"))
        self.gridLayout_3.addWidget(self.label_customY, 0, 1, 1, 1)
        self.label_customX = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_customX.sizePolicy().hasHeightForWidth())
        self.label_customX.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_customX.setFont(font)
        self.label_customX.setObjectName(_fromUtf8("label_customX"))
        self.gridLayout_3.addWidget(self.label_customX, 0, 0, 1, 1)
        self.label_customRY = QtGui.QLabel(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_customRY.sizePolicy().hasHeightForWidth())
        self.label_customRY.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_customRY.setFont(font)
        self.label_customRY.setObjectName(_fromUtf8("label_customRY"))
        self.gridLayout_3.addWidget(self.label_customRY, 0, 3, 1, 1)
        self.gridLayout_2.addWidget(self.frame, 1, 0, 1, 3)
        self.gridLayout.addWidget(self.groupBox, 22, 0, 1, 3)
        self.label_3 = QtGui.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 13, 1, 1, 1)
        self.line_4 = QtGui.QFrame(self.centralwidget)
        self.line_4.setFrameShape(QtGui.QFrame.HLine)
        self.line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_4.setObjectName(_fromUtf8("line_4"))
        self.gridLayout.addWidget(self.line_4, 10, 0, 1, 3)
        self.groupBox_2 = QtGui.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.pushButton_loadImagesBatch = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_loadImagesBatch.setCheckable(False)
        self.pushButton_loadImagesBatch.setObjectName(_fromUtf8("pushButton_loadImagesBatch"))
        self.gridLayout_5.addWidget(self.pushButton_loadImagesBatch, 0, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_2)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_5.addWidget(self.label_11, 2, 0, 1, 1)
        self.progressBar_batchMode = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar_batchMode.setProperty("value", 0)
        self.progressBar_batchMode.setObjectName(_fromUtf8("progressBar_batchMode"))
        self.gridLayout_5.addWidget(self.progressBar_batchMode, 4, 0, 1, 2)
        self.lineEdit_dataFileNameBatch = QtGui.QLineEdit(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_dataFileNameBatch.sizePolicy().hasHeightForWidth())
        self.lineEdit_dataFileNameBatch.setSizePolicy(sizePolicy)
        self.lineEdit_dataFileNameBatch.setObjectName(_fromUtf8("lineEdit_dataFileNameBatch"))
        self.gridLayout_5.addWidget(self.lineEdit_dataFileNameBatch, 2, 1, 1, 1)
        self.pushButton_loadBkgrndImagesBatch = QtGui.QPushButton(self.groupBox_2)
        self.pushButton_loadBkgrndImagesBatch.setObjectName(_fromUtf8("pushButton_loadBkgrndImagesBatch"))
        self.gridLayout_5.addWidget(self.pushButton_loadBkgrndImagesBatch, 0, 1, 1, 1)
        self.pushButton_analyseBatch = QtGui.QPushButton(self.groupBox_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_analyseBatch.setFont(font)
        self.pushButton_analyseBatch.setObjectName(_fromUtf8("pushButton_analyseBatch"))
        self.gridLayout_5.addWidget(self.pushButton_analyseBatch, 3, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox_2, 11, 0, 1, 3)
        self.pushButton_analyse = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_analyse.sizePolicy().hasHeightForWidth())
        self.pushButton_analyse.setSizePolicy(sizePolicy)
        self.pushButton_analyse.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_analyse.setFont(font)
        self.pushButton_analyse.setCheckable(False)
        self.pushButton_analyse.setChecked(False)
        self.pushButton_analyse.setAutoExclusive(False)
        self.pushButton_analyse.setObjectName(_fromUtf8("pushButton_analyse"))
        self.gridLayout.addWidget(self.pushButton_analyse, 2, 0, 1, 3)
        self.pushButton_loadBkgrnd = QtGui.QPushButton(self.centralwidget)
        self.pushButton_loadBkgrnd.setObjectName(_fromUtf8("pushButton_loadBkgrnd"))
        self.gridLayout.addWidget(self.pushButton_loadBkgrnd, 1, 0, 1, 2)
        self.pushButton_loadImage = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_loadImage.sizePolicy().hasHeightForWidth())
        self.pushButton_loadImage.setSizePolicy(sizePolicy)
        self.pushButton_loadImage.setMinimumSize(QtCore.QSize(0, 40))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_loadImage.setFont(font)
        self.pushButton_loadImage.setObjectName(_fromUtf8("pushButton_loadImage"))
        self.gridLayout.addWidget(self.pushButton_loadImage, 0, 0, 1, 3)
        self.pushButton_saveCurrentData = QtGui.QPushButton(self.centralwidget)
        self.pushButton_saveCurrentData.setObjectName(_fromUtf8("pushButton_saveCurrentData"))
        self.gridLayout.addWidget(self.pushButton_saveCurrentData, 20, 2, 1, 1)
        self.lineEdit_dataFileName = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_dataFileName.sizePolicy().hasHeightForWidth())
        self.lineEdit_dataFileName.setSizePolicy(sizePolicy)
        self.lineEdit_dataFileName.setObjectName(_fromUtf8("lineEdit_dataFileName"))
        self.gridLayout.addWidget(self.lineEdit_dataFileName, 20, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSingle = QtGui.QAction(MainWindow)
        self.actionSingle.setObjectName(_fromUtf8("actionSingle"))
        self.actionBatch = QtGui.QAction(MainWindow)
        self.actionBatch.setObjectName(_fromUtf8("actionBatch"))

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Jammy Dodger", None))
        self.checkBox_showBVNFit.setText(_translate("MainWindow", "Show Bivariant Normal Fit", None))
        self.label_6.setText(_translate("MainWindow", "Saturation Level:", None))
        self.label.setText(_translate("MainWindow", "Min. Level:", None))
        self.label_2.setText(_translate("MainWindow", "Max.Level:", None))
        self.checkBox_show3DLens.setText(_translate("MainWindow", "Show 3D Lens", None))
        self.checkBox_showSaturatedPixels.setText(_translate("MainWindow", "Show Saturated Pixels", None))
        self.checkBox_showMLEFit.setText(_translate("MainWindow", "Show MLE Fit", None))
        self.label_syBVN.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_19.setText(_translate("MainWindow", "SigmaY:", None))
        self.label_sxMLE.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_sxBVN.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_cxyMLE.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_cxyBVN.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_20.setText(_translate("MainWindow", "Covariance XY:", None))
        self.label_syMLE.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_18.setText(_translate("MainWindow", "Sigma X:", None))
        self.label_yMLE.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_yBVN.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_17.setText(_translate("MainWindow", "Y Position:", None))
        self.label_xMLE.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_xBVN.setText(_translate("MainWindow", "-- +/- --", None))
        self.label_16.setText(_translate("MainWindow", "X Position:", None))
        self.label_5.setText(_translate("MainWindow", "MLE", None))
        self.label_4.setText(_translate("MainWindow", "BVN", None))
        self.comboBox_colourMap.setItemText(0, _translate("MainWindow", "Grayscale", None))
        self.comboBox_colourMap.setItemText(1, _translate("MainWindow", "Inverted Grayscale", None))
        self.comboBox_colourMap.setItemText(2, _translate("MainWindow", "Fire", None))
        self.comboBox_colourMap.setItemText(3, _translate("MainWindow", "Rainbow", None))
        self.label_ColourMap.setText(_translate("MainWindow", "Colour Map: ", None))
        self.checkBox_autoScale.setText(_translate("MainWindow", "Auto Scale Loaded Image", None))
        self.checkBox_useBackground.setText(_translate("MainWindow", "Use Background Image", None))
        self.groupBox.setTitle(_translate("MainWindow", "Expert Settings", None))
        self.checkBox_useCustomMask.setText(_translate("MainWindow", "Use Custom Mask", None))
        self.label_7.setText(_translate("MainWindow", "%", None))
        self.checkBox_lowestPixValue.setText(_translate("MainWindow", "Lowest percentage cut on data for MLE Method", None))
        self.label_8.setText(_translate("MainWindow", "(integer)", None))
        self.checkBox_rollingAverage.setText(_translate("MainWindow", "Number of points for rolling average on projections", None))
        self.label_9.setText(_translate("MainWindow", "(decimal number <1)", None))
        self.checkBox_rSquared.setText(_translate("MainWindow", "Use R-Squared Threshold", None))
        self.label_10.setText(_translate("MainWindow", "(pixels)", None))
        self.label_customRX.setText(_translate("MainWindow", "X Radius:", None))
        self.label_customY.setText(_translate("MainWindow", "Y:", None))
        self.label_customX.setText(_translate("MainWindow", "X:", None))
        self.label_customRY.setText(_translate("MainWindow", "Y Radius:", None))
        self.label_3.setText(_translate("MainWindow", "Results", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Batch Mode", None))
        self.pushButton_loadImagesBatch.setText(_translate("MainWindow", "Load Images", None))
        self.label_11.setText(_translate("MainWindow", "Name of Output File:", None))
        self.lineEdit_dataFileNameBatch.setText(_translate("MainWindow", "batchData.csv", None))
        self.pushButton_loadBkgrndImagesBatch.setText(_translate("MainWindow", "Load Background Images", None))
        self.pushButton_analyseBatch.setText(_translate("MainWindow", "Batch Analyse", None))
        self.pushButton_analyse.setText(_translate("MainWindow", "Analyse", None))
        self.pushButton_loadBkgrnd.setText(_translate("MainWindow", "Load Background", None))
        self.pushButton_loadImage.setText(_translate("MainWindow", "Load Image", None))
        self.pushButton_saveCurrentData.setText(_translate("MainWindow", "Save Current Results", None))
        self.lineEdit_dataFileName.setText(_translate("MainWindow", "data.csv", None))
        self.actionSingle.setText(_translate("MainWindow", "Single", None))
        self.actionBatch.setText(_translate("MainWindow", "Batch", None))

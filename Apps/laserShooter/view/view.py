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
        MainWindow.resize(672, 481)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.centralWidgetLayout = QtGui.QGridLayout(self.centralwidget)
        self.centralWidgetLayout.setObjectName(_fromUtf8("centralWidgetLayout"))
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.centralWidgetLayout.addWidget(self.frame, 2, 0, 2, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_MODE = QtGui.QLabel(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_MODE.sizePolicy().hasHeightForWidth())
        self.label_MODE.setSizePolicy(sizePolicy)
        self.label_MODE.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_MODE.setObjectName(_fromUtf8("label_MODE"))
        self.horizontalLayout.addWidget(self.label_MODE)
        self.abortButton = QtGui.QPushButton(self.groupBox_3)
        self.abortButton.setObjectName(_fromUtf8("abortButton"))
        self.horizontalLayout.addWidget(self.abortButton)
        self.centralWidgetLayout.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.laserTab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.laserTab.sizePolicy().hasHeightForWidth())
        self.laserTab.setSizePolicy(sizePolicy)
        self.laserTab.setObjectName(_fromUtf8("laserTab"))
        self.linacTabLayout = QtGui.QGridLayout(self.laserTab)
        self.linacTabLayout.setObjectName(_fromUtf8("linacTabLayout"))
        self.groupBox = QtGui.QGroupBox(self.laserTab)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.laserNormalButton = QtGui.QPushButton(self.groupBox)
        self.laserNormalButton.setMinimumSize(QtCore.QSize(170, 0))
        self.laserNormalButton.setObjectName(_fromUtf8("laserNormalButton"))
        self.gridLayout.addWidget(self.laserNormalButton, 0, 0, 1, 1)
        self.laserBurstButton = QtGui.QPushButton(self.groupBox)
        self.laserBurstButton.setObjectName(_fromUtf8("laserBurstButton"))
        self.gridLayout.addWidget(self.laserBurstButton, 1, 0, 1, 1)
        self.laserNormalStatus = QtGui.QPushButton(self.groupBox)
        self.laserNormalStatus.setMaximumSize(QtCore.QSize(50, 16777215))
        self.laserNormalStatus.setText(_fromUtf8(""))
        self.laserNormalStatus.setFlat(False)
        self.laserNormalStatus.setObjectName(_fromUtf8("laserNormalStatus"))
        self.gridLayout.addWidget(self.laserNormalStatus, 0, 1, 1, 1)
        self.laserBurstStatus = QtGui.QPushButton(self.groupBox)
        self.laserBurstStatus.setMaximumSize(QtCore.QSize(50, 16777215))
        self.laserBurstStatus.setText(_fromUtf8(""))
        self.laserBurstStatus.setFlat(False)
        self.laserBurstStatus.setObjectName(_fromUtf8("laserBurstStatus"))
        self.gridLayout.addWidget(self.laserBurstStatus, 1, 1, 1, 1)
        self.linacTabLayout.addWidget(self.groupBox, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.linacTabLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.tabWidget_2 = QtGui.QTabWidget(self.laserTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy)
        self.tabWidget_2.setMinimumSize(QtCore.QSize(400, 0))
        self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox_2 = QtGui.QGroupBox(self.tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label = QtGui.QLabel(self.groupBox_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(200, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_4.addWidget(self.label, 0, 0, 1, 1)
        self.qIntegratedChargeSpinBox = QtGui.QSpinBox(self.groupBox_2)
        self.qIntegratedChargeSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.qIntegratedChargeSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.qIntegratedChargeSpinBox.setMaximum(1000000000)
        self.qIntegratedChargeSpinBox.setSingleStep(10)
        self.qIntegratedChargeSpinBox.setProperty("value", 0)
        self.qIntegratedChargeSpinBox.setObjectName(_fromUtf8("qIntegratedChargeSpinBox"))
        self.gridLayout_4.addWidget(self.qIntegratedChargeSpinBox, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setMinimumSize(QtCore.QSize(200, 0))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 3, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 2, 0, 1, 1)
        self.qEnergySpinbox = QtGui.QSpinBox(self.groupBox_2)
        self.qEnergySpinbox.setMinimumSize(QtCore.QSize(80, 0))
        self.qEnergySpinbox.setProperty("value", 40)
        self.qEnergySpinbox.setObjectName(_fromUtf8("qEnergySpinbox"))
        self.gridLayout_4.addWidget(self.qEnergySpinbox, 1, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem1, 0, 2, 1, 1)
        self.qCommentTextBox = QtGui.QLineEdit(self.groupBox_2)
        self.qCommentTextBox.setMinimumSize(QtCore.QSize(300, 0))
        self.qCommentTextBox.setObjectName(_fromUtf8("qCommentTextBox"))
        self.gridLayout_4.addWidget(self.qCommentTextBox, 3, 1, 1, 2)
        self.qMotorPositionSpinBox = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.qMotorPositionSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.qMotorPositionSpinBox.setDecimals(1)
        self.qMotorPositionSpinBox.setMaximum(300.0)
        self.qMotorPositionSpinBox.setSingleStep(10.0)
        self.qMotorPositionSpinBox.setObjectName(_fromUtf8("qMotorPositionSpinBox"))
        self.gridLayout_4.addWidget(self.qMotorPositionSpinBox, 2, 1, 1, 1)
        self.gridLayout_2.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.qFireButton = QtGui.QPushButton(self.tab)
        self.qFireButton.setObjectName(_fromUtf8("qFireButton"))
        self.gridLayout_2.addWidget(self.qFireButton, 1, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setMinimumSize(QtCore.QSize(200, 0))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 0, 0, 1, 1)
        self.nShotsSpinBox = QtGui.QSpinBox(self.groupBox_4)
        self.nShotsSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.nShotsSpinBox.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.nShotsSpinBox.setSuffix(_fromUtf8(""))
        self.nShotsSpinBox.setMaximum(1000000)
        self.nShotsSpinBox.setProperty("value", 0)
        self.nShotsSpinBox.setObjectName(_fromUtf8("nShotsSpinBox"))
        self.gridLayout_5.addWidget(self.nShotsSpinBox, 0, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setMinimumSize(QtCore.QSize(200, 0))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_5.addWidget(self.label_6, 1, 0, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_4)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_5.addWidget(self.label_7, 3, 0, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_4)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_5.addWidget(self.label_8, 2, 0, 1, 1)
        self.nEnergySpinbox = QtGui.QSpinBox(self.groupBox_4)
        self.nEnergySpinbox.setMinimumSize(QtCore.QSize(80, 0))
        self.nEnergySpinbox.setProperty("value", 40)
        self.nEnergySpinbox.setObjectName(_fromUtf8("nEnergySpinbox"))
        self.gridLayout_5.addWidget(self.nEnergySpinbox, 1, 1, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem2, 0, 2, 1, 1)
        self.nCommentTextBox = QtGui.QLineEdit(self.groupBox_4)
        self.nCommentTextBox.setMinimumSize(QtCore.QSize(300, 0))
        self.nCommentTextBox.setObjectName(_fromUtf8("nCommentTextBox"))
        self.gridLayout_5.addWidget(self.nCommentTextBox, 3, 1, 1, 2)
        self.nMotorPositionSpinBox = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.nMotorPositionSpinBox.setMinimumSize(QtCore.QSize(80, 0))
        self.nMotorPositionSpinBox.setDecimals(1)
        self.nMotorPositionSpinBox.setMaximum(300.0)
        self.nMotorPositionSpinBox.setSingleStep(10.0)
        self.nMotorPositionSpinBox.setObjectName(_fromUtf8("nMotorPositionSpinBox"))
        self.gridLayout_5.addWidget(self.nMotorPositionSpinBox, 2, 1, 1, 1)
        self.gridLayout_6.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.nFireButton = QtGui.QPushButton(self.tab_2)
        self.nFireButton.setObjectName(_fromUtf8("nFireButton"))
        self.gridLayout_6.addWidget(self.nFireButton, 1, 0, 1, 1)
        self.tabWidget_2.addTab(self.tab_2, _fromUtf8(""))
        self.linacTabLayout.addWidget(self.tabWidget_2, 1, 0, 1, 2)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.linacTabLayout.addItem(spacerItem3, 2, 0, 1, 2)
        self.tabWidget.addTab(self.laserTab, _fromUtf8(""))
        self.logTab = QtGui.QWidget()
        self.logTab.setObjectName(_fromUtf8("logTab"))
        self.logTabLayout = QtGui.QVBoxLayout(self.logTab)
        self.logTabLayout.setObjectName(_fromUtf8("logTabLayout"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../Resources/Icons/log.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.logTab, icon, _fromUtf8(""))
        self.centralWidgetLayout.addWidget(self.tabWidget, 4, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 672, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.actionSave_Calibation_Data = QtGui.QAction(MainWindow)
        self.actionSave_Calibation_Data.setObjectName(_fromUtf8("actionSave_Calibation_Data"))
        self.menuFile.addAction(self.actionSave_Calibation_Data)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "laserShooter", None))
        self.label_MODE.setText(_translate("MainWindow", "Mode", None))
        self.abortButton.setText(_translate("MainWindow", "Abort", None))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox", None))
        self.laserNormalButton.setText(_translate("MainWindow", "Set Normal Laser Operation", None))
        self.laserBurstButton.setText(_translate("MainWindow", "Set Burst Mode Operation", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Settings", None))
        self.label.setText(_translate("MainWindow", "Total Integrated Charge", None))
        self.qIntegratedChargeSpinBox.setSuffix(_translate("MainWindow", " pC", None))
        self.label_2.setText(_translate("MainWindow", "Beam Energy", None))
        self.label_4.setText(_translate("MainWindow", "Comment", None))
        self.label_3.setText(_translate("MainWindow", "Motor Stage Position", None))
        self.qEnergySpinbox.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.qMotorPositionSpinBox.setSuffix(_translate("MainWindow", " mm", None))
        self.qFireButton.setText(_translate("MainWindow", "Fire!", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab), _translate("MainWindow", "Integrated Charge", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Settings", None))
        self.label_5.setText(_translate("MainWindow", "Total Number of Shots", None))
        self.label_6.setText(_translate("MainWindow", "Beam Energy", None))
        self.label_7.setText(_translate("MainWindow", "Comment", None))
        self.label_8.setText(_translate("MainWindow", "Motor Stage Position", None))
        self.nEnergySpinbox.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.nFireButton.setText(_translate("MainWindow", "Fire!", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_2), _translate("MainWindow", "Number Of Shots", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.laserTab), _translate("MainWindow", "Laser Shooting", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logTab), _translate("MainWindow", "Log", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSave_Calibation_Data.setText(_translate("MainWindow", "Save Calibation Data", None))


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
        MainWindow.resize(1040, 818)
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
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.linac1Tab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linac1Tab.sizePolicy().hasHeightForWidth())
        self.linac1Tab.setSizePolicy(sizePolicy)
        self.linac1Tab.setObjectName(_fromUtf8("linac1Tab"))
        self.linacTabLayout = QtGui.QGridLayout(self.linac1Tab)
        self.linacTabLayout.setObjectName(_fromUtf8("linacTabLayout"))
        self.groupBox_4 = QtGui.QGroupBox(self.linac1Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4.sizePolicy().hasHeightForWidth())
        self.groupBox_4.setSizePolicy(sizePolicy)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.formLayout_4 = QtGui.QFormLayout(self.groupBox_4)
        self.formLayout_4.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4.setObjectName(_fromUtf8("formLayout_4"))
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6.sizePolicy().hasHeightForWidth())
        self.label_6.setSizePolicy(sizePolicy)
        self.label_6.setMinimumSize(QtCore.QSize(150, 0))
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_6)
        self.linac1LowerSet = QtGui.QSpinBox(self.groupBox_4)
        self.linac1LowerSet.setMinimumSize(QtCore.QSize(100, 0))
        self.linac1LowerSet.setMaximum(17500)
        self.linac1LowerSet.setSingleStep(100)
        self.linac1LowerSet.setProperty("value", 8000)
        self.linac1LowerSet.setObjectName(_fromUtf8("linac1LowerSet"))
        self.formLayout_4.setWidget(0, QtGui.QFormLayout.FieldRole, self.linac1LowerSet)
        self.label = QtGui.QLabel(self.groupBox_4)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.LabelRole, self.label)
        self.linac1UpperSet = QtGui.QSpinBox(self.groupBox_4)
        self.linac1UpperSet.setMinimumSize(QtCore.QSize(100, 0))
        self.linac1UpperSet.setMaximum(17500)
        self.linac1UpperSet.setSingleStep(100)
        self.linac1UpperSet.setProperty("value", 16000)
        self.linac1UpperSet.setObjectName(_fromUtf8("linac1UpperSet"))
        self.formLayout_4.setWidget(1, QtGui.QFormLayout.FieldRole, self.linac1UpperSet)
        self.linacTabLayout.addWidget(self.groupBox_4, 0, 0, 1, 1)
        self.groupBox_methodLinac1 = QtGui.QGroupBox(self.linac1Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_methodLinac1.sizePolicy().hasHeightForWidth())
        self.groupBox_methodLinac1.setSizePolicy(sizePolicy)
        self.groupBox_methodLinac1.setObjectName(_fromUtf8("groupBox_methodLinac1"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.groupBox_methodLinac1)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.linac1StartRoughScanButton = QtGui.QPushButton(self.groupBox_methodLinac1)
        self.linac1StartRoughScanButton.setObjectName(_fromUtf8("linac1StartRoughScanButton"))
        self.verticalLayout_4.addWidget(self.linac1StartRoughScanButton)
        self.linac1StartFineScanButton = QtGui.QPushButton(self.groupBox_methodLinac1)
        self.linac1StartFineScanButton.setObjectName(_fromUtf8("linac1StartFineScanButton"))
        self.verticalLayout_4.addWidget(self.linac1StartFineScanButton)
        self.linac1SetRFCentreButton = QtGui.QPushButton(self.groupBox_methodLinac1)
        self.linac1SetRFCentreButton.setObjectName(_fromUtf8("linac1SetRFCentreButton"))
        self.verticalLayout_4.addWidget(self.linac1SetRFCentreButton)
        self.linacTabLayout.addWidget(self.groupBox_methodLinac1, 1, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.linacTabLayout.addItem(spacerItem, 2, 0, 2, 1)
        self.tabWidget_plotsLinac1 = QtGui.QTabWidget(self.linac1Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_plotsLinac1.sizePolicy().hasHeightForWidth())
        self.tabWidget_plotsLinac1.setSizePolicy(sizePolicy)
        self.tabWidget_plotsLinac1.setMinimumSize(QtCore.QSize(0, 500))
        self.tabWidget_plotsLinac1.setObjectName(_fromUtf8("tabWidget_plotsLinac1"))
        self.linacTabLayout.addWidget(self.tabWidget_plotsLinac1, 0, 1, 4, 1)
        self.tabWidget.addTab(self.linac1Tab, _fromUtf8(""))
        self.linac1BLMTab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.linac1BLMTab.sizePolicy().hasHeightForWidth())
        self.linac1BLMTab.setSizePolicy(sizePolicy)
        self.linac1BLMTab.setObjectName(_fromUtf8("linac1BLMTab"))
        self.linac1BLMTabLayout = QtGui.QGridLayout(self.linac1BLMTab)
        self.linac1BLMTabLayout.setObjectName(_fromUtf8("linac1BLMTabLayout"))
        self.groupBox_4BLM = QtGui.QGroupBox(self.linac1BLMTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_4BLM.sizePolicy().hasHeightForWidth())
        self.groupBox_4BLM.setSizePolicy(sizePolicy)
        self.groupBox_4BLM.setObjectName(_fromUtf8("groupBox_4BLM"))
        self.formLayout_4BLM = QtGui.QFormLayout(self.groupBox_4BLM)
        self.formLayout_4BLM.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_4BLM.setObjectName(_fromUtf8("formLayout_4BLM"))
        self.label_6BLM = QtGui.QLabel(self.groupBox_4BLM)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_6BLM.sizePolicy().hasHeightForWidth())
        self.label_6BLM.setSizePolicy(sizePolicy)
        self.label_6BLM.setMinimumSize(QtCore.QSize(150, 0))
        self.label_6BLM.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6BLM.setObjectName(_fromUtf8("label_6BLM"))
        self.formLayout_4BLM.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_6BLM)
        self.linac1BLMLowerSet = QtGui.QSpinBox(self.groupBox_4BLM)
        self.linac1BLMLowerSet.setMinimumSize(QtCore.QSize(100, 0))
        self.linac1BLMLowerSet.setMaximum(17500)
        self.linac1BLMLowerSet.setSingleStep(100)
        self.linac1BLMLowerSet.setProperty("value", 10000)
        self.linac1BLMLowerSet.setObjectName(_fromUtf8("linac1BLMLowerSet"))
        self.formLayout_4BLM.setWidget(0, QtGui.QFormLayout.FieldRole, self.linac1BLMLowerSet)
        self.label1 = QtGui.QLabel(self.groupBox_4BLM)
        self.label1.setObjectName(_fromUtf8("label1"))
        self.formLayout_4BLM.setWidget(1, QtGui.QFormLayout.LabelRole, self.label1)
        self.linac1BLMUpperSet = QtGui.QSpinBox(self.groupBox_4BLM)
        self.linac1BLMUpperSet.setMinimumSize(QtCore.QSize(100, 0))
        self.linac1BLMUpperSet.setMaximum(17500)
        self.linac1BLMUpperSet.setSingleStep(100)
        self.linac1BLMUpperSet.setProperty("value", 17000)
        self.linac1BLMUpperSet.setObjectName(_fromUtf8("linac1BLMUpperSet"))
        self.formLayout_4BLM.setWidget(1, QtGui.QFormLayout.FieldRole, self.linac1BLMUpperSet)
        self.linac1BLMTabLayout.addWidget(self.groupBox_4BLM, 0, 0, 1, 1)
        self.groupBox_methodLinac1BLM = QtGui.QGroupBox(self.linac1BLMTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_methodLinac1BLM.sizePolicy().hasHeightForWidth())
        self.groupBox_methodLinac1BLM.setSizePolicy(sizePolicy)
        self.groupBox_methodLinac1BLM.setObjectName(_fromUtf8("groupBox_methodLinac1BLM"))
        self.verticalLayout_4BLM = QtGui.QVBoxLayout(self.groupBox_methodLinac1BLM)
        self.verticalLayout_4BLM.setObjectName(_fromUtf8("verticalLayout_4BLM"))
        self.linac1BLMStartRoughScanButton = QtGui.QPushButton(self.groupBox_methodLinac1BLM)
        self.linac1BLMStartRoughScanButton.setObjectName(_fromUtf8("linac1BLMStartRoughScanButton"))
        self.verticalLayout_4BLM.addWidget(self.linac1BLMStartRoughScanButton)
        self.linac1BLMStartFineScanButton = QtGui.QPushButton(self.groupBox_methodLinac1BLM)
        self.linac1BLMStartFineScanButton.setObjectName(_fromUtf8("linac1BLMStartFineScanButton"))
        self.verticalLayout_4BLM.addWidget(self.linac1BLMStartFineScanButton)
        self.linac1BLMTabLayout.addWidget(self.groupBox_methodLinac1BLM, 1, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.linac1BLMTabLayout.addItem(spacerItem1, 2, 0, 2, 1)
        self.tabWidget_plotsLinac1BLM = QtGui.QTabWidget(self.linac1BLMTab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_plotsLinac1BLM.sizePolicy().hasHeightForWidth())
        self.tabWidget_plotsLinac1BLM.setSizePolicy(sizePolicy)
        self.tabWidget_plotsLinac1BLM.setObjectName(_fromUtf8("tabWidget_plotsLinac1BLM"))
        self.linac1BLMTabLayout.addWidget(self.tabWidget_plotsLinac1BLM, 0, 1, 4, 1)
        self.tabWidget.addTab(self.linac1BLMTab, _fromUtf8(""))
        self.SOL1Tab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SOL1Tab.sizePolicy().hasHeightForWidth())
        self.SOL1Tab.setSizePolicy(sizePolicy)
        self.SOL1Tab.setObjectName(_fromUtf8("SOL1Tab"))
        self.gridLayout = QtGui.QGridLayout(self.SOL1Tab)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.SOL1Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_2.sizePolicy().hasHeightForWidth())
        self.groupBox_2.setSizePolicy(sizePolicy)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.label_4 = QtGui.QLabel(self.groupBox_2)
        self.label_4.setMinimumSize(QtCore.QSize(150, 0))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_4)
        self.sol1LowerSet = QtGui.QSpinBox(self.groupBox_2)
        self.sol1LowerSet.setMinimumSize(QtCore.QSize(100, 0))
        self.sol1LowerSet.setMinimum(-250)
        self.sol1LowerSet.setMaximum(250)
        self.sol1LowerSet.setSingleStep(10)
        self.sol1LowerSet.setProperty("value", -50)
        self.sol1LowerSet.setObjectName(_fromUtf8("sol1LowerSet"))
        self.formLayout_2.setWidget(0, QtGui.QFormLayout.FieldRole, self.sol1LowerSet)
        self.label_5 = QtGui.QLabel(self.groupBox_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_5)
        self.sol1UpperSet = QtGui.QSpinBox(self.groupBox_2)
        self.sol1UpperSet.setMinimumSize(QtCore.QSize(100, 0))
        self.sol1UpperSet.setMinimum(-250)
        self.sol1UpperSet.setMaximum(250)
        self.sol1UpperSet.setSingleStep(10)
        self.sol1UpperSet.setProperty("value", 50)
        self.sol1UpperSet.setObjectName(_fromUtf8("sol1UpperSet"))
        self.formLayout_2.setWidget(1, QtGui.QFormLayout.FieldRole, self.sol1UpperSet)
        self.gridLayout.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox_6 = QtGui.QGroupBox(self.SOL1Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_6.sizePolicy().hasHeightForWidth())
        self.groupBox_6.setSizePolicy(sizePolicy)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_6)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.sol1StartRoughScanButton = QtGui.QPushButton(self.groupBox_6)
        self.sol1StartRoughScanButton.setObjectName(_fromUtf8("sol1StartRoughScanButton"))
        self.verticalLayout.addWidget(self.sol1StartRoughScanButton)
        self.sol1StartFineScanButton = QtGui.QPushButton(self.groupBox_6)
        self.sol1StartFineScanButton.setObjectName(_fromUtf8("sol1StartFineScanButton"))
        self.verticalLayout.addWidget(self.sol1StartFineScanButton)
        self.gridLayout.addWidget(self.groupBox_6, 1, 0, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem2, 2, 0, 1, 1)
        self.tabWidget_plotsSol1 = QtGui.QTabWidget(self.SOL1Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_plotsSol1.sizePolicy().hasHeightForWidth())
        self.tabWidget_plotsSol1.setSizePolicy(sizePolicy)
        self.tabWidget_plotsSol1.setObjectName(_fromUtf8("tabWidget_plotsSol1"))
        self.gridLayout.addWidget(self.tabWidget_plotsSol1, 0, 1, 3, 1)
        self.tabWidget.addTab(self.SOL1Tab, _fromUtf8(""))
        self.SOL2Tab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SOL2Tab.sizePolicy().hasHeightForWidth())
        self.SOL2Tab.setSizePolicy(sizePolicy)
        self.SOL2Tab.setObjectName(_fromUtf8("SOL2Tab"))
        self.gridLayout_2 = QtGui.QGridLayout(self.SOL2Tab)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.SOL2Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.formLayout_5 = QtGui.QFormLayout(self.groupBox_3)
        self.formLayout_5.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_5.setObjectName(_fromUtf8("formLayout_5"))
        self.label_7 = QtGui.QLabel(self.groupBox_3)
        self.label_7.setMinimumSize(QtCore.QSize(150, 0))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_7)
        self.sol2LowerSet = QtGui.QSpinBox(self.groupBox_3)
        self.sol2LowerSet.setMinimumSize(QtCore.QSize(100, 0))
        self.sol2LowerSet.setMinimum(-250)
        self.sol2LowerSet.setMaximum(250)
        self.sol2LowerSet.setSingleStep(10)
        self.sol2LowerSet.setProperty("value", -50)
        self.sol2LowerSet.setObjectName(_fromUtf8("sol2LowerSet"))
        self.formLayout_5.setWidget(0, QtGui.QFormLayout.FieldRole, self.sol2LowerSet)
        self.label_10 = QtGui.QLabel(self.groupBox_3)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_10)
        self.sol2UpperSet = QtGui.QSpinBox(self.groupBox_3)
        self.sol2UpperSet.setMinimumSize(QtCore.QSize(100, 0))
        self.sol2UpperSet.setMinimum(-250)
        self.sol2UpperSet.setMaximum(250)
        self.sol2UpperSet.setSingleStep(10)
        self.sol2UpperSet.setProperty("value", 50)
        self.sol2UpperSet.setObjectName(_fromUtf8("sol2UpperSet"))
        self.formLayout_5.setWidget(1, QtGui.QFormLayout.FieldRole, self.sol2UpperSet)
        self.gridLayout_2.addWidget(self.groupBox_3, 0, 0, 1, 1)
        self.groupBox_7 = QtGui.QGroupBox(self.SOL2Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_7.sizePolicy().hasHeightForWidth())
        self.groupBox_7.setSizePolicy(sizePolicy)
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.sol2StartRoughScanButton = QtGui.QPushButton(self.groupBox_7)
        self.sol2StartRoughScanButton.setObjectName(_fromUtf8("sol2StartRoughScanButton"))
        self.verticalLayout_2.addWidget(self.sol2StartRoughScanButton)
        self.sol2StartFineScanButton = QtGui.QPushButton(self.groupBox_7)
        self.sol2StartFineScanButton.setObjectName(_fromUtf8("sol2StartFineScanButton"))
        self.verticalLayout_2.addWidget(self.sol2StartFineScanButton)
        self.gridLayout_2.addWidget(self.groupBox_7, 1, 0, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem3, 2, 0, 1, 1)
        self.tabWidget_plotsSol2 = QtGui.QTabWidget(self.SOL2Tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(1)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget_plotsSol2.sizePolicy().hasHeightForWidth())
        self.tabWidget_plotsSol2.setSizePolicy(sizePolicy)
        self.tabWidget_plotsSol2.setObjectName(_fromUtf8("tabWidget_plotsSol2"))
        self.gridLayout_2.addWidget(self.tabWidget_plotsSol2, 0, 1, 3, 1)
        self.tabWidget.addTab(self.SOL2Tab, _fromUtf8(""))
        self.logTab = QtGui.QWidget()
        self.logTab.setObjectName(_fromUtf8("logTab"))
        self.logTabLayout = QtGui.QVBoxLayout(self.logTab)
        self.logTabLayout.setObjectName(_fromUtf8("logTabLayout"))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../Resources/Icons/log.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.tabWidget.addTab(self.logTab, icon, _fromUtf8(""))
        self.centralWidgetLayout.addWidget(self.tabWidget, 4, 0, 1, 1)
        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_3 = QtGui.QGridLayout(self.frame)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        spacerItem4 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 0, 3, 4, 1)
        self.groupBox_8 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_8.sizePolicy().hasHeightForWidth())
        self.groupBox_8.setSizePolicy(sizePolicy)
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.formLayout_3 = QtGui.QFormLayout(self.groupBox_8)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        self.saveDataCheckbox = QtGui.QCheckBox(self.groupBox_8)
        self.saveDataCheckbox.setChecked(True)
        self.saveDataCheckbox.setObjectName(_fromUtf8("saveDataCheckbox"))
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.SpanningRole, self.saveDataCheckbox)
        self.gridLayout_3.addWidget(self.groupBox_8, 1, 2, 1, 1)
        self.groupBox_5 = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_5.sizePolicy().hasHeightForWidth())
        self.groupBox_5.setSizePolicy(sizePolicy)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.gridLayout_4 = QtGui.QGridLayout(self.groupBox_5)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_14 = QtGui.QLabel(self.groupBox_5)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_4.addWidget(self.label_14, 5, 0, 1, 1)
        self.Corr2_Max = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.Corr2_Max.setDecimals(2)
        self.Corr2_Max.setMinimum(-5.0)
        self.Corr2_Max.setMaximum(5.0)
        self.Corr2_Max.setSingleStep(0.1)
        self.Corr2_Max.setProperty("value", 5.0)
        self.Corr2_Max.setObjectName(_fromUtf8("Corr2_Max"))
        self.gridLayout_4.addWidget(self.Corr2_Max, 5, 2, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_5)
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_4.addWidget(self.label_13, 3, 2, 1, 1)
        self.Corr1_Max = QtGui.QDoubleSpinBox(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Corr1_Max.sizePolicy().hasHeightForWidth())
        self.Corr1_Max.setSizePolicy(sizePolicy)
        self.Corr1_Max.setMinimumSize(QtCore.QSize(100, 0))
        self.Corr1_Max.setDecimals(2)
        self.Corr1_Max.setMinimum(-5.0)
        self.Corr1_Max.setMaximum(5.0)
        self.Corr1_Max.setSingleStep(0.1)
        self.Corr1_Max.setProperty("value", 5.0)
        self.Corr1_Max.setObjectName(_fromUtf8("Corr1_Max"))
        self.gridLayout_4.addWidget(self.Corr1_Max, 4, 2, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_5)
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_4.addWidget(self.label_12, 3, 1, 1, 1)
        self.Corr2_Min = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.Corr2_Min.setDecimals(2)
        self.Corr2_Min.setMinimum(-5.0)
        self.Corr2_Min.setMaximum(5.0)
        self.Corr2_Min.setSingleStep(0.1)
        self.Corr2_Min.setProperty("value", -5.0)
        self.Corr2_Min.setObjectName(_fromUtf8("Corr2_Min"))
        self.gridLayout_4.addWidget(self.Corr2_Min, 5, 1, 1, 1)
        self.Corr1_Min = QtGui.QDoubleSpinBox(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Corr1_Min.sizePolicy().hasHeightForWidth())
        self.Corr1_Min.setSizePolicy(sizePolicy)
        self.Corr1_Min.setMinimumSize(QtCore.QSize(100, 0))
        self.Corr1_Min.setDecimals(2)
        self.Corr1_Min.setMinimum(-5.0)
        self.Corr1_Min.setMaximum(5.0)
        self.Corr1_Min.setSingleStep(0.1)
        self.Corr1_Min.setProperty("value", -5.0)
        self.Corr1_Min.setObjectName(_fromUtf8("Corr1_Min"))
        self.gridLayout_4.addWidget(self.Corr1_Min, 4, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_5)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_4.addWidget(self.label_11, 4, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox_5)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_4.addWidget(self.label_2, 1, 0, 1, 1)
        self.roughStepSetCorrector = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.roughStepSetCorrector.setDecimals(2)
        self.roughStepSetCorrector.setMaximum(5.0)
        self.roughStepSetCorrector.setSingleStep(0.1)
        self.roughStepSetCorrector.setProperty("value", 1.0)
        self.roughStepSetCorrector.setObjectName(_fromUtf8("roughStepSetCorrector"))
        self.gridLayout_4.addWidget(self.roughStepSetCorrector, 1, 1, 1, 1)
        self.fineStepSetCorrector = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.fineStepSetCorrector.setDecimals(2)
        self.fineStepSetCorrector.setMaximum(5.0)
        self.fineStepSetCorrector.setSingleStep(0.1)
        self.fineStepSetCorrector.setProperty("value", 0.1)
        self.fineStepSetCorrector.setObjectName(_fromUtf8("fineStepSetCorrector"))
        self.gridLayout_4.addWidget(self.fineStepSetCorrector, 1, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_5)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_4.addWidget(self.label_8, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_5)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_4.addWidget(self.label_9, 0, 2, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_5, 1, 0, 2, 1)
        self.groupBox = QtGui.QGroupBox(self.frame)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_3)
        self.nSamples = QtGui.QSpinBox(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.nSamples.sizePolicy().hasHeightForWidth())
        self.nSamples.setSizePolicy(sizePolicy)
        self.nSamples.setMinimum(2)
        self.nSamples.setProperty("value", 10)
        self.nSamples.setObjectName(_fromUtf8("nSamples"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.nSamples)
        self.gridLayout_3.addWidget(self.groupBox, 1, 1, 1, 1)
        self.groupBox_9 = QtGui.QGroupBox(self.frame)
        self.groupBox_9.setEnabled(True)
        self.groupBox_9.setFlat(False)
        self.groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_9)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.horizontalRadio = QtGui.QRadioButton(self.groupBox_9)
        self.horizontalRadio.setChecked(True)
        self.horizontalRadio.setObjectName(_fromUtf8("horizontalRadio"))
        self.horizontalLayout_3.addWidget(self.horizontalRadio)
        self.verticalRadio = QtGui.QRadioButton(self.groupBox_9)
        self.verticalRadio.setChecked(False)
        self.verticalRadio.setObjectName(_fromUtf8("verticalRadio"))
        self.horizontalLayout_3.addWidget(self.verticalRadio)
        self.gridLayout_3.addWidget(self.groupBox_9, 2, 1, 1, 2)
        self.centralWidgetLayout.addWidget(self.frame, 2, 0, 2, 1)
        self.groupBox_31 = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_31.sizePolicy().hasHeightForWidth())
        self.groupBox_31.setSizePolicy(sizePolicy)
        self.groupBox_31.setObjectName(_fromUtf8("groupBox_31"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_31)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_MODE = QtGui.QLabel(self.groupBox_31)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_MODE.sizePolicy().hasHeightForWidth())
        self.label_MODE.setSizePolicy(sizePolicy)
        self.label_MODE.setMaximumSize(QtCore.QSize(16777215, 100))
        self.label_MODE.setObjectName(_fromUtf8("label_MODE"))
        self.horizontalLayout.addWidget(self.label_MODE)
        self.finishButton = QtGui.QPushButton(self.groupBox_31)
        self.finishButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.finishButton.setObjectName(_fromUtf8("finishButton"))
        self.horizontalLayout.addWidget(self.finishButton)
        self.abortButton = QtGui.QPushButton(self.groupBox_31)
        self.abortButton.setMaximumSize(QtCore.QSize(200, 16777215))
        self.abortButton.setAutoFillBackground(False)
        self.abortButton.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8("../../Resources/Icons/off.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.abortButton.setIcon(icon1)
        self.abortButton.setObjectName(_fromUtf8("abortButton"))
        self.horizontalLayout.addWidget(self.abortButton)
        self.centralWidgetLayout.addWidget(self.groupBox_31, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1040, 21))
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
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Linac Kick Steering", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Linac Settings", None))
        self.label_6.setText(_translate("MainWindow", "Lower Amplitude", None))
        self.label.setText(_translate("MainWindow", "Upper Amplitude", None))
        self.groupBox_methodLinac1.setTitle(_translate("MainWindow", "Method", None))
        self.linac1StartRoughScanButton.setText(_translate("MainWindow", "Scan RF centre (Approx)", None))
        self.linac1StartFineScanButton.setText(_translate("MainWindow", "Scan RF centre (Fine)", None))
        self.linac1SetRFCentreButton.setText(_translate("MainWindow", "Set RF centre", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.linac1Tab), _translate("MainWindow", "Linac 1", None))
        self.groupBox_4BLM.setTitle(_translate("MainWindow", "Linac Settings", None))
        self.label_6BLM.setText(_translate("MainWindow", "Lower Amplitude", None))
        self.label1.setText(_translate("MainWindow", "Upper Amplitude", None))
        self.groupBox_methodLinac1BLM.setTitle(_translate("MainWindow", "Method", None))
        self.linac1BLMStartRoughScanButton.setText(_translate("MainWindow", "Scan RF centre (Approx)", None))
        self.linac1BLMStartFineScanButton.setText(_translate("MainWindow", "Scan RF centre (Fine)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.linac1BLMTab), _translate("MainWindow", "Linac 1 Alt", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Solenoid Settings", None))
        self.label_4.setText(_translate("MainWindow", "Lower", None))
        self.label_5.setText(_translate("MainWindow", "Upper", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Method", None))
        self.sol1StartRoughScanButton.setText(_translate("MainWindow", "Scan Sol-01 centre (Approx)", None))
        self.sol1StartFineScanButton.setText(_translate("MainWindow", "Scan Sol-01 centre (Fine)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SOL1Tab), _translate("MainWindow", "SOL1", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Solenoid Settings", None))
        self.label_7.setText(_translate("MainWindow", "Lower", None))
        self.label_10.setText(_translate("MainWindow", "Upper", None))
        self.groupBox_7.setTitle(_translate("MainWindow", "Method", None))
        self.sol2StartRoughScanButton.setText(_translate("MainWindow", "Scan Sol-02 centre (Approx)", None))
        self.sol2StartFineScanButton.setText(_translate("MainWindow", "Scan Sol-02 centre (Fine)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.SOL2Tab), _translate("MainWindow", "SOL2", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.logTab), _translate("MainWindow", "Log", None))
        self.groupBox_8.setTitle(_translate("MainWindow", "Verbosity", None))
        self.saveDataCheckbox.setText(_translate("MainWindow", "Save Data", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Corrector Settings", None))
        self.label_14.setText(_translate("MainWindow", "S01-COR-02", None))
        self.Corr2_Max.setSuffix(_translate("MainWindow", " A", None))
        self.label_13.setText(_translate("MainWindow", "Max", None))
        self.Corr1_Max.setSuffix(_translate("MainWindow", " A", None))
        self.label_12.setText(_translate("MainWindow", "Min", None))
        self.Corr2_Min.setSuffix(_translate("MainWindow", " A", None))
        self.Corr1_Min.setSuffix(_translate("MainWindow", " A", None))
        self.label_11.setText(_translate("MainWindow", "S01-COR-01", None))
        self.label_2.setText(_translate("MainWindow", "StepSize", None))
        self.roughStepSetCorrector.setSuffix(_translate("MainWindow", " A", None))
        self.fineStepSetCorrector.setSuffix(_translate("MainWindow", " A", None))
        self.label_8.setText(_translate("MainWindow", "Approximate", None))
        self.label_9.setText(_translate("MainWindow", "Fine", None))
        self.groupBox.setTitle(_translate("MainWindow", "BPM Settings", None))
        self.label_3.setText(_translate("MainWindow", "BPM Samples", None))
        self.groupBox_9.setTitle(_translate("MainWindow", "Plane", None))
        self.horizontalRadio.setText(_translate("MainWindow", "Horizontal", None))
        self.verticalRadio.setText(_translate("MainWindow", "Vertical", None))
        self.label_MODE.setText(_translate("MainWindow", "Mode", None))
        self.finishButton.setText(_translate("MainWindow", "Finish Scan", None))
        self.abortButton.setText(_translate("MainWindow", "Abort", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.actionSave_Calibation_Data.setText(_translate("MainWindow", "Save Calibation Data", None))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view_v4.ui'
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
        MainWindow.resize(691, 864)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.textEdit = QtGui.QTextEdit(self.centralwidget)
        self.textEdit.setMaximumSize(QtCore.QSize(16777215, 70))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.gridLayout.addWidget(self.textEdit, 2, 0, 1, 1)
        self.groupBox_10 = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_10.setMinimumSize(QtCore.QSize(0, 71))
        self.groupBox_10.setObjectName(_fromUtf8("groupBox_10"))
        self.gridLayout_19 = QtGui.QGridLayout(self.groupBox_10)
        self.gridLayout_19.setObjectName(_fromUtf8("gridLayout_19"))
        self.label_14 = QtGui.QLabel(self.groupBox_10)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_19.addWidget(self.label_14, 0, 0, 1, 1)
        self.doubleSpinBox_I = QtGui.QDoubleSpinBox(self.groupBox_10)
        self.doubleSpinBox_I.setObjectName(_fromUtf8("doubleSpinBox_I"))
        self.gridLayout_19.addWidget(self.doubleSpinBox_I, 1, 0, 1, 1)
        self.label_13 = QtGui.QLabel(self.groupBox_10)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_19.addWidget(self.label_13, 0, 1, 1, 1)
        self.doubleSpinBox_p = QtGui.QDoubleSpinBox(self.groupBox_10)
        self.doubleSpinBox_p.setObjectName(_fromUtf8("doubleSpinBox_p"))
        self.gridLayout_19.addWidget(self.doubleSpinBox_p, 1, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_10, 0, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralwidget)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 71))
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.toolBox = QtGui.QToolBox(self.groupBox)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.toolBox.setFont(font)
        self.toolBox.setAutoFillBackground(False)
        self.toolBox.setStyleSheet(_fromUtf8(""))
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.page_7 = QtGui.QWidget()
        self.page_7.setGeometry(QtCore.QRect(0, 0, 645, 469))
        self.page_7.setObjectName(_fromUtf8("page_7"))
        self.gridLayout_20 = QtGui.QGridLayout(self.page_7)
        self.gridLayout_20.setObjectName(_fromUtf8("gridLayout_20"))
        self.label = QtGui.QLabel(self.page_7)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_20.addWidget(self.label, 0, 0, 1, 1, QtCore.Qt.AlignTop)
        self.toolBox.addItem(self.page_7, _fromUtf8(""))
        self.page = QtGui.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 645, 469))
        self.page.setObjectName(_fromUtf8("page"))
        self.gridLayout_11 = QtGui.QGridLayout(self.page)
        self.gridLayout_11.setObjectName(_fromUtf8("gridLayout_11"))
        self.line = QtGui.QFrame(self.page)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout_11.addWidget(self.line, 1, 0, 1, 1)
        self.label_2 = QtGui.QLabel(self.page)
        self.label_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_11.addWidget(self.label_2, 0, 0, 1, 1)
        self.line_2 = QtGui.QFrame(self.page)
        self.line_2.setFrameShape(QtGui.QFrame.HLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridLayout_11.addWidget(self.line_2, 3, 0, 1, 1)
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.doubleSpinBox_I_predict = QtGui.QDoubleSpinBox(self.page)
        self.doubleSpinBox_I_predict.setObjectName(_fromUtf8("doubleSpinBox_I_predict"))
        self.gridLayout_4.addWidget(self.doubleSpinBox_I_predict, 1, 1, 1, 1)
        self.pushButton_useCurrent = QtGui.QPushButton(self.page)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_useCurrent.sizePolicy().hasHeightForWidth())
        self.pushButton_useCurrent.setSizePolicy(sizePolicy)
        self.pushButton_useCurrent.setMinimumSize(QtCore.QSize(140, 22))
        self.pushButton_useCurrent.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_useCurrent.setChecked(False)
        self.pushButton_useCurrent.setObjectName(_fromUtf8("pushButton_useCurrent"))
        self.gridLayout_4.addWidget(self.pushButton_useCurrent, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(self.page)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_4.addWidget(self.label_3, 0, 2, 1, 1)
        self.doubleSpinBox_p_predict = QtGui.QDoubleSpinBox(self.page)
        self.doubleSpinBox_p_predict.setObjectName(_fromUtf8("doubleSpinBox_p_predict"))
        self.gridLayout_4.addWidget(self.doubleSpinBox_p_predict, 1, 2, 1, 1)
        self.pushButton_useRF = QtGui.QPushButton(self.page)
        self.pushButton_useRF.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_useRF.sizePolicy().hasHeightForWidth())
        self.pushButton_useRF.setSizePolicy(sizePolicy)
        self.pushButton_useRF.setMinimumSize(QtCore.QSize(140, 22))
        self.pushButton_useRF.setMaximumSize(QtCore.QSize(371, 16777215))
        font = QtGui.QFont()
        self.pushButton_useRF.setFont(font)
        self.pushButton_useRF.setChecked(False)
        self.pushButton_useRF.setObjectName(_fromUtf8("pushButton_useRF"))
        self.gridLayout_4.addWidget(self.pushButton_useRF, 1, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.page)
        self.label_4.setMaximumSize(QtCore.QSize(16777215, 10))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_4.addWidget(self.label_4, 0, 1, 1, 1)
        self.gridLayout_11.addLayout(self.gridLayout_4, 2, 0, 1, 1)
        self.label_I = QtGui.QLabel(self.page)
        self.label_I.setMinimumSize(QtCore.QSize(120, 0))
        self.label_I.setObjectName(_fromUtf8("label_I"))
        self.gridLayout_11.addWidget(self.label_I, 4, 0, 1, 1)
        self.label_6 = QtGui.QLabel(self.page)
        self.label_6.setMinimumSize(QtCore.QSize(0, 270))
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_11.addWidget(self.label_6, 5, 0, 1, 1)
        self.toolBox.addItem(self.page, _fromUtf8(""))
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 645, 469))
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.page_2)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.page_2)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_6 = QtGui.QGridLayout(self.tab)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.label_5 = QtGui.QLabel(self.tab)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_6.addWidget(self.label_5, 0, 0, 1, 1)
        self.toolBox_2 = QtGui.QToolBox(self.tab)
        self.toolBox_2.setObjectName(_fromUtf8("toolBox_2"))
        self.page_5 = QtGui.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 595, 295))
        self.page_5.setObjectName(_fromUtf8("page_5"))
        self.gridLayout_13 = QtGui.QGridLayout(self.page_5)
        self.gridLayout_13.setObjectName(_fromUtf8("gridLayout_13"))
        self.gridLayout_7 = QtGui.QGridLayout()
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.label_16 = QtGui.QLabel(self.page_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout_7.addWidget(self.label_16, 0, 0, 1, 4)
        self.label_15 = QtGui.QLabel(self.page_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_7.addWidget(self.label_15, 1, 0, 1, 1)
        self.doubleSpinBox_step_1 = QtGui.QDoubleSpinBox(self.page_5)
        self.doubleSpinBox_step_1.setDecimals(3)
        self.doubleSpinBox_step_1.setSingleStep(0.1)
        self.doubleSpinBox_step_1.setProperty("value", 0.2)
        self.doubleSpinBox_step_1.setObjectName(_fromUtf8("doubleSpinBox_step_1"))
        self.gridLayout_7.addWidget(self.doubleSpinBox_step_1, 1, 1, 1, 1)
        self.label_17 = QtGui.QLabel(self.page_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.gridLayout_7.addWidget(self.label_17, 2, 0, 1, 1)
        self.label_dipole_set = QtGui.QLabel(self.page_5)
        self.label_dipole_set.setMinimumSize(QtCore.QSize(100, 0))
        self.label_dipole_set.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_dipole_set.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_dipole_set.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_dipole_set.setText(_fromUtf8(""))
        self.label_dipole_set.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_dipole_set.setObjectName(_fromUtf8("label_dipole_set"))
        self.gridLayout_7.addWidget(self.label_dipole_set, 2, 1, 1, 1)
        self.pushButton_x_up_1 = QtGui.QPushButton(self.page_5)
        self.pushButton_x_up_1.setMinimumSize(QtCore.QSize(20, 12))
        self.pushButton_x_up_1.setMaximumSize(QtCore.QSize(20, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.pushButton_x_up_1.setFont(font)
        self.pushButton_x_up_1.setStyleSheet(_fromUtf8("QPushButton{ color: rgb(0, 0, 0);font: 75 5pt \"MS Shell Dlg 2\";}\n"
""))
        self.pushButton_x_up_1.setAutoDefault(False)
        self.pushButton_x_up_1.setObjectName(_fromUtf8("pushButton_x_up_1"))
        self.gridLayout_7.addWidget(self.pushButton_x_up_1, 2, 2, 1, 1)
        self.pushButton_x_down_1 = QtGui.QPushButton(self.page_5)
        self.pushButton_x_down_1.setMinimumSize(QtCore.QSize(20, 12))
        self.pushButton_x_down_1.setMaximumSize(QtCore.QSize(20, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.pushButton_x_down_1.setFont(font)
        self.pushButton_x_down_1.setStyleSheet(_fromUtf8("QPushButton{ color: rgb(0, 0, 0);font: 75 5pt \"MS Shell Dlg 2\";}"))
        self.pushButton_x_down_1.setObjectName(_fromUtf8("pushButton_x_down_1"))
        self.gridLayout_7.addWidget(self.pushButton_x_down_1, 2, 3, 1, 1)
        self.pushButton_get_p_rough = QtGui.QPushButton(self.page_5)
        self.pushButton_get_p_rough.setObjectName(_fromUtf8("pushButton_get_p_rough"))
        self.gridLayout_7.addWidget(self.pushButton_get_p_rough, 3, 0, 1, 1)
        self.label_p_rough = QtGui.QLabel(self.page_5)
        self.label_p_rough.setMinimumSize(QtCore.QSize(100, 0))
        self.label_p_rough.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_p_rough.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_p_rough.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_p_rough.setText(_fromUtf8(""))
        self.label_p_rough.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_p_rough.setObjectName(_fromUtf8("label_p_rough"))
        self.gridLayout_7.addWidget(self.label_p_rough, 3, 1, 1, 1)
        self.gridLayout_13.addLayout(self.gridLayout_7, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 146, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_13.addItem(spacerItem, 1, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.page_5)
        self.groupBox_3.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout_13.addWidget(self.groupBox_3, 0, 1, 2, 1)
        self.toolBox_2.addItem(self.page_5, _fromUtf8(""))
        self.page_6 = QtGui.QWidget()
        self.page_6.setGeometry(QtCore.QRect(0, 0, 595, 295))
        self.page_6.setObjectName(_fromUtf8("page_6"))
        self.gridLayout_14 = QtGui.QGridLayout(self.page_6)
        self.gridLayout_14.setObjectName(_fromUtf8("gridLayout_14"))
        self.gridLayout_12 = QtGui.QGridLayout()
        self.gridLayout_12.setObjectName(_fromUtf8("gridLayout_12"))
        self.pushButton_roughGetCurrentRange = QtGui.QPushButton(self.page_6)
        self.pushButton_roughGetCurrentRange.setChecked(False)
        self.pushButton_roughGetCurrentRange.setObjectName(_fromUtf8("pushButton_roughGetCurrentRange"))
        self.gridLayout_12.addWidget(self.pushButton_roughGetCurrentRange, 0, 0, 1, 1)
        self.doubleSpinBox_roughIMin = QtGui.QDoubleSpinBox(self.page_6)
        self.doubleSpinBox_roughIMin.setObjectName(_fromUtf8("doubleSpinBox_roughIMin"))
        self.gridLayout_12.addWidget(self.doubleSpinBox_roughIMin, 0, 1, 1, 1)
        self.pushButton_roughCentreC2VCurrent = QtGui.QPushButton(self.page_6)
        self.pushButton_roughCentreC2VCurrent.setChecked(False)
        self.pushButton_roughCentreC2VCurrent.setObjectName(_fromUtf8("pushButton_roughCentreC2VCurrent"))
        self.gridLayout_12.addWidget(self.pushButton_roughCentreC2VCurrent, 1, 0, 1, 4)
        self.doubleSpinBox_roughIMax = QtGui.QDoubleSpinBox(self.page_6)
        self.doubleSpinBox_roughIMax.setObjectName(_fromUtf8("doubleSpinBox_roughIMax"))
        self.gridLayout_12.addWidget(self.doubleSpinBox_roughIMax, 0, 2, 1, 1)
        self.doubleSpinBox_roughIStep = QtGui.QDoubleSpinBox(self.page_6)
        self.doubleSpinBox_roughIStep.setObjectName(_fromUtf8("doubleSpinBox_roughIStep"))
        self.gridLayout_12.addWidget(self.doubleSpinBox_roughIStep, 0, 3, 1, 1)
        self.groupBox_2 = QtGui.QGroupBox(self.page_6)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.gridLayout_12.addWidget(self.groupBox_2, 2, 0, 1, 4)
        self.gridLayout_14.addLayout(self.gridLayout_12, 0, 0, 1, 1)
        self.toolBox_2.addItem(self.page_6, _fromUtf8(""))
        self.gridLayout_6.addWidget(self.toolBox_2, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.gridLayout_16 = QtGui.QGridLayout(self.tab_2)
        self.gridLayout_16.setObjectName(_fromUtf8("gridLayout_16"))
        self.pushButton_set_I_rough = QtGui.QPushButton(self.tab_2)
        self.pushButton_set_I_rough.setObjectName(_fromUtf8("pushButton_set_I_rough"))
        self.gridLayout_16.addWidget(self.pushButton_set_I_rough, 4, 0, 1, 1)
        self.label_I_rough = QtGui.QLabel(self.tab_2)
        self.label_I_rough.setMinimumSize(QtCore.QSize(100, 0))
        self.label_I_rough.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_I_rough.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_I_rough.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_I_rough.setText(_fromUtf8(""))
        self.label_I_rough.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_I_rough.setObjectName(_fromUtf8("label_I_rough"))
        self.gridLayout_16.addWidget(self.label_I_rough, 4, 1, 1, 2)
        self.doubleSpinBox_p_rough_set = QtGui.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_p_rough_set.setObjectName(_fromUtf8("doubleSpinBox_p_rough_set"))
        self.gridLayout_16.addWidget(self.doubleSpinBox_p_rough_set, 3, 0, 1, 3)
        self.pushButton_get_p_rough_3 = QtGui.QPushButton(self.tab_2)
        self.pushButton_get_p_rough_3.setAutoFillBackground(False)
        self.pushButton_get_p_rough_3.setObjectName(_fromUtf8("pushButton_get_p_rough_3"))
        self.gridLayout_16.addWidget(self.pushButton_get_p_rough_3, 1, 0, 1, 2)
        self.pushButton_get_p_rough_4 = QtGui.QPushButton(self.tab_2)
        self.pushButton_get_p_rough_4.setObjectName(_fromUtf8("pushButton_get_p_rough_4"))
        self.gridLayout_16.addWidget(self.pushButton_get_p_rough_4, 1, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.tab_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout_16.addWidget(self.label_7, 0, 0, 1, 4)
        spacerItem1 = QtGui.QSpacerItem(20, 143, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_16.addItem(spacerItem1, 6, 1, 1, 2)
        self.label_18 = QtGui.QLabel(self.tab_2)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.gridLayout_16.addWidget(self.label_18, 2, 0, 1, 3)
        self.groupBox_4 = QtGui.QGroupBox(self.tab_2)
        self.groupBox_4.setMinimumSize(QtCore.QSize(300, 0))
        self.groupBox_4.setAutoFillBackground(False)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.gridLayout_16.addWidget(self.groupBox_4, 1, 3, 6, 1)
        self.gridLayout_15 = QtGui.QGridLayout()
        self.gridLayout_15.setObjectName(_fromUtf8("gridLayout_15"))
        self.label_dipole_set_2 = QtGui.QLabel(self.tab_2)
        self.label_dipole_set_2.setMinimumSize(QtCore.QSize(100, 0))
        self.label_dipole_set_2.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.label_dipole_set_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_dipole_set_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_dipole_set_2.setText(_fromUtf8(""))
        self.label_dipole_set_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_dipole_set_2.setObjectName(_fromUtf8("label_dipole_set_2"))
        self.gridLayout_15.addWidget(self.label_dipole_set_2, 2, 1, 1, 1)
        self.pushButton_x_up_2 = QtGui.QPushButton(self.tab_2)
        self.pushButton_x_up_2.setMinimumSize(QtCore.QSize(20, 12))
        self.pushButton_x_up_2.setMaximumSize(QtCore.QSize(20, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.pushButton_x_up_2.setFont(font)
        self.pushButton_x_up_2.setStyleSheet(_fromUtf8("QPushButton{ color: rgb(0, 0, 0);font: 75 5pt \"MS Shell Dlg 2\";}\n"
""))
        self.pushButton_x_up_2.setAutoDefault(False)
        self.pushButton_x_up_2.setObjectName(_fromUtf8("pushButton_x_up_2"))
        self.gridLayout_15.addWidget(self.pushButton_x_up_2, 2, 2, 1, 1)
        self.pushButton_x_down_2 = QtGui.QPushButton(self.tab_2)
        self.pushButton_x_down_2.setMinimumSize(QtCore.QSize(20, 12))
        self.pushButton_x_down_2.setMaximumSize(QtCore.QSize(20, 16777215))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(5)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.pushButton_x_down_2.setFont(font)
        self.pushButton_x_down_2.setStyleSheet(_fromUtf8("QPushButton{ color: rgb(0, 0, 0);font: 75 5pt \"MS Shell Dlg 2\";}"))
        self.pushButton_x_down_2.setObjectName(_fromUtf8("pushButton_x_down_2"))
        self.gridLayout_15.addWidget(self.pushButton_x_down_2, 2, 3, 1, 1)
        self.label_19 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_15.addWidget(self.label_19, 0, 0, 1, 4)
        self.label_21 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setAlignment(QtCore.Qt.AlignCenter)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.gridLayout_15.addWidget(self.label_21, 2, 0, 1, 1)
        self.label_20 = QtGui.QLabel(self.tab_2)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setAlignment(QtCore.Qt.AlignCenter)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.gridLayout_15.addWidget(self.label_20, 1, 0, 1, 1)
        self.doubleSpinBox_step_2 = QtGui.QDoubleSpinBox(self.tab_2)
        self.doubleSpinBox_step_2.setSuffix(_fromUtf8(""))
        self.doubleSpinBox_step_2.setDecimals(3)
        self.doubleSpinBox_step_2.setSingleStep(10.0)
        self.doubleSpinBox_step_2.setProperty("value", 10.0)
        self.doubleSpinBox_step_2.setObjectName(_fromUtf8("doubleSpinBox_step_2"))
        self.gridLayout_15.addWidget(self.doubleSpinBox_step_2, 1, 1, 1, 1)
        self.gridLayout_16.addLayout(self.gridLayout_15, 5, 0, 1, 3)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.gridLayout_2.addWidget(self.tabWidget, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_2, _fromUtf8(""))
        self.page_3 = QtGui.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 645, 469))
        self.page_3.setObjectName(_fromUtf8("page_3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.page_3)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.tabWidget_2 = QtGui.QTabWidget(self.page_3)
        self.tabWidget_2.setObjectName(_fromUtf8("tabWidget_2"))
        self.tab_3 = QtGui.QWidget()
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.tabWidget_2.addTab(self.tab_3, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.tabWidget_2.addTab(self.tab_4, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.tabWidget_2, 2, 0, 1, 1)
        self.groupBox_6 = QtGui.QGroupBox(self.page_3)
        self.groupBox_6.setMinimumSize(QtCore.QSize(0, 70))
        self.groupBox_6.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.gridLayout_8 = QtGui.QGridLayout(self.groupBox_6)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.label_9 = QtGui.QLabel(self.groupBox_6)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_8.addWidget(self.label_9, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox_6, 0, 0, 1, 1)
        self.tabWidget_3 = QtGui.QTabWidget(self.page_3)
        self.tabWidget_3.setObjectName(_fromUtf8("tabWidget_3"))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.tabWidget_3.addTab(self.tab_5, _fromUtf8(""))
        self.gridLayout_3.addWidget(self.tabWidget_3, 1, 0, 1, 1)
        self.toolBox.addItem(self.page_3, _fromUtf8(""))
        self.page_4 = QtGui.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 645, 469))
        self.page_4.setObjectName(_fromUtf8("page_4"))
        self.gridLayout_10 = QtGui.QGridLayout(self.page_4)
        self.gridLayout_10.setObjectName(_fromUtf8("gridLayout_10"))
        self.groupBox_9 = QtGui.QGroupBox(self.page_4)
        self.groupBox_9.setMinimumSize(QtCore.QSize(0, 70))
        self.groupBox_9.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
        self.gridLayout_9 = QtGui.QGridLayout(self.groupBox_9)
        self.gridLayout_9.setObjectName(_fromUtf8("gridLayout_9"))
        self.label_10 = QtGui.QLabel(self.groupBox_9)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_9.addWidget(self.label_10, 0, 0, 1, 1)
        self.gridLayout_10.addWidget(self.groupBox_9, 0, 0, 1, 1)
        self.tabWidget_4 = QtGui.QTabWidget(self.page_4)
        self.tabWidget_4.setObjectName(_fromUtf8("tabWidget_4"))
        self.tab_6 = QtGui.QWidget()
        self.tab_6.setObjectName(_fromUtf8("tab_6"))
        self.tabWidget_4.addTab(self.tab_6, _fromUtf8(""))
        self.gridLayout_10.addWidget(self.tabWidget_4, 1, 0, 1, 1)
        self.tabWidget_5 = QtGui.QTabWidget(self.page_4)
        self.tabWidget_5.setObjectName(_fromUtf8("tabWidget_5"))
        self.tab_7 = QtGui.QWidget()
        self.tab_7.setObjectName(_fromUtf8("tab_7"))
        self.tabWidget_5.addTab(self.tab_7, _fromUtf8(""))
        self.gridLayout_10.addWidget(self.tabWidget_5, 2, 0, 1, 1)
        self.tabWidget_6 = QtGui.QTabWidget(self.page_4)
        self.tabWidget_6.setObjectName(_fromUtf8("tabWidget_6"))
        self.tab_8 = QtGui.QWidget()
        self.tab_8.setObjectName(_fromUtf8("tab_8"))
        self.tabWidget_6.addTab(self.tab_8, _fromUtf8(""))
        self.gridLayout_10.addWidget(self.tabWidget_6, 3, 0, 1, 1)
        self.tabWidget_7 = QtGui.QTabWidget(self.page_4)
        self.tabWidget_7.setObjectName(_fromUtf8("tabWidget_7"))
        self.tab_10 = QtGui.QWidget()
        self.tab_10.setObjectName(_fromUtf8("tab_10"))
        self.tabWidget_7.addTab(self.tab_10, _fromUtf8(""))
        self.gridLayout_10.addWidget(self.tabWidget_7, 4, 0, 1, 1)
        self.toolBox.addItem(self.page_4, _fromUtf8(""))
        self.gridLayout_5.addWidget(self.toolBox, 0, 0, 1, 2)
        self.gridLayout.addWidget(self.groupBox, 1, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.toolBox.setCurrentIndex(2)
        self.tabWidget.setCurrentIndex(0)
        self.toolBox_2.setCurrentIndex(1)
        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget_3.setCurrentIndex(0)
        self.tabWidget_4.setCurrentIndex(0)
        self.tabWidget_5.setCurrentIndex(0)
        self.tabWidget_6.setCurrentIndex(0)
        self.tabWidget_7.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox_10.setTitle(_translate("MainWindow", "Quick converter", None))
        self.label_14.setText(_translate("MainWindow", "Dipole current", None))
        self.doubleSpinBox_I.setSuffix(_translate("MainWindow", " A", None))
        self.label_13.setText(_translate("MainWindow", "Momentum", None))
        self.doubleSpinBox_p.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.label.setText(_translate("MainWindow", "Work from top to bottom through the steps below to measure momentum and momentum spread.", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_7), _translate("MainWindow", "Introduction", None))
        self.label_2.setText(_translate("MainWindow", "Skip this step if beam already on C2V BPM\n"
"Otherwise use either magnet or RF settings to predict the momentum", None))
        self.doubleSpinBox_I_predict.setSuffix(_translate("MainWindow", " A", None))
        self.pushButton_useCurrent.setText(_translate("MainWindow", "Use current from dipole", None))
        self.label_3.setText(_translate("MainWindow", "Predicted Momentum", None))
        self.doubleSpinBox_p_predict.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.pushButton_useRF.setText(_translate("MainWindow", "Predict momentum from RF", None))
        self.label_4.setText(_translate("MainWindow", "Dipole current", None))
        self.label_I.setText(_translate("MainWindow", "...", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("MainWindow", "Predicted Momentum", None))
        self.label_5.setText(_translate("MainWindow", "If beam is already on C2V BPM then centre it to get a rough momentum measurement\n"
"Otherwise scan dipole to find C2V BPM signal, then do centering", None))
        self.label_16.setText(_translate("MainWindow", "S02-DIP-01 adjustment", None))
        self.label_15.setText(_translate("MainWindow", "Step size [A]", None))
        self.doubleSpinBox_step_1.setSuffix(_translate("MainWindow", " A", None))
        self.label_17.setText(_translate("MainWindow", "Set value [A]", None))
        self.pushButton_x_up_1.setText(_translate("MainWindow", "▲", None))
        self.pushButton_x_down_1.setText(_translate("MainWindow", "▼", None))
        self.pushButton_get_p_rough.setText(_translate("MainWindow", "Get Momentum", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "C2V BPM", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_5), _translate("MainWindow", "Centre beam on C2V BPM", None))
        self.pushButton_roughGetCurrentRange.setText(_translate("MainWindow", "Get scan range from predicted mom. (min/max/step):", None))
        self.doubleSpinBox_roughIMin.setSuffix(_translate("MainWindow", " A", None))
        self.pushButton_roughCentreC2VCurrent.setText(_translate("MainWindow", "Scan dipole", None))
        self.doubleSpinBox_roughIMax.setSuffix(_translate("MainWindow", " A", None))
        self.doubleSpinBox_roughIStep.setSuffix(_translate("MainWindow", " A", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "C2V BPM x-pos vs dipole setting", None))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_6), _translate("MainWindow", "Scan dipole to find beam on C2V BPM", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Measure", None))
        self.pushButton_set_I_rough.setText(_translate("MainWindow", "Set Current", None))
        self.doubleSpinBox_p_rough_set.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.pushButton_get_p_rough_3.setText(_translate("MainWindow", "Vary gun amplitude", None))
        self.pushButton_get_p_rough_4.setText(_translate("MainWindow", "Vary linac amplitude", None))
        self.label_7.setText(_translate("MainWindow", "Confirm whether gun only or gun + linac. Select momentum then set current.\n"
"Set RF amplitude to centre on C2V", None))
        self.label_18.setText(_translate("MainWindow", "Set target momentum:", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "C2V BPM", None))
        self.pushButton_x_up_2.setText(_translate("MainWindow", "▲", None))
        self.pushButton_x_down_2.setText(_translate("MainWindow", "▼", None))
        self.label_19.setText(_translate("MainWindow", "RF adjustment", None))
        self.label_21.setText(_translate("MainWindow", "Set value", None))
        self.label_20.setText(_translate("MainWindow", "Step size", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Set", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("MainWindow", "Rough Momentum Measure/Set", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_3), _translate("MainWindow", "Measure", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "Set", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Instructions", None))
        self.label_9.setText(_translate("MainWindow", "Need to have completed rough measurement to continue\n"
"Need to align beam through dipole for both fine measure and fine set", None))
        self.tabWidget_3.setTabText(self.tabWidget_3.indexOf(self.tab_5), _translate("MainWindow", "Align beam through dipole", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("MainWindow", "Fine Momentum Measure/Set", None))
        self.groupBox_9.setTitle(_translate("MainWindow", "Show relevant information", None))
        self.label_10.setText(_translate("MainWindow", "Need to have done fine momentum measurement to continue", None))
        self.tabWidget_4.setTabText(self.tabWidget_4.indexOf(self.tab_6), _translate("MainWindow", "Beta minimisation", None))
        self.tabWidget_5.setTabText(self.tabWidget_5.indexOf(self.tab_7), _translate("MainWindow", "Set dispersion size", None))
        self.tabWidget_6.setTabText(self.tabWidget_6.indexOf(self.tab_8), _translate("MainWindow", "Calculate dispersion", None))
        self.tabWidget_7.setTabText(self.tabWidget_7.indexOf(self.tab_10), _translate("MainWindow", "Calculate Momentum Spread", None))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("MainWindow", "Momentum Spread Measure", None))

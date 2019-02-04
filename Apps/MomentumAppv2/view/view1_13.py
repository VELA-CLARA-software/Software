# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view1_13.ui'
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
        MainWindow.resize(1539, 960)
        MainWindow.setStyleSheet(_fromUtf8("QToolTip\n"
"{\n"
"     border: 1px solid black;\n"
"     background-color: #ffa02f;\n"
"     padding: 1px;\n"
"     border-radius: 3px;\n"
"     opacity: 100;\n"
"}\n"
"\n"
"QWidget\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QWidget:item:hover\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #ca0619);\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:item:selected\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QMenuBar::item\n"
"{\n"
"    background: transparent;\n"
"}\n"
"\n"
"QMenuBar::item:selected\n"
"{\n"
"    background: transparent;\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QMenuBar::item:pressed\n"
"{\n"
"    background: #444;\n"
"    border: 1px solid #000;\n"
"    background-color: QLinearGradient(\n"
"        x1:0, y1:0,\n"
"        x2:0, y2:1,\n"
"        stop:1 #212121,\n"
"        stop:0.4 #343434/*,\n"
"        stop:0.2 #343434,\n"
"        stop:0.1 #ffaa00*/\n"
"    );\n"
"    margin-bottom:-1px;\n"
"    padding-bottom:1px;\n"
"}\n"
"\n"
"QMenu\n"
"{\n"
"    border: 1px solid #000;\n"
"}\n"
"\n"
"QMenu::item\n"
"{\n"
"    padding: 2px 20px 2px 20px;\n"
"}\n"
"\n"
"QMenu::item:selected\n"
"{\n"
"    color: #000000;\n"
"}\n"
"\n"
"QWidget:disabled\n"
"{\n"
"    color: #404040;\n"
"    background-color: #323232;\n"
"}\n"
"\n"
"QAbstractItemView\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0.1 #646464, stop: 1 #5d5d5d);\n"
"}\n"
"\n"
"QWidget:focus\n"
"{\n"
"    /*border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);*/\n"
"}\n"
"\n"
"QLineEdit\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #4d4d4d, stop: 0 #646464, stop: 1 #5d5d5d);\n"
"    padding: 1px;\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QPushButton\n"
"{\n"
"    color: #b1b1b1;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-width: 1px;\n"
"    border-color: #1e1e1e;\n"
"    border-style: solid;\n"
"    border-radius: 6;\n"
"    padding: 3px;\n"
"    font-size: 12px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"}\n"
"\n"
"QPushButton:pressed\n"
"{\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"}\n"
"\n"
"QComboBox\n"
"{\n"
"    selection-background-color: #ffaa00;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #565656, stop: 0.1 #525252, stop: 0.5 #4e4e4e, stop: 0.9 #4a4a4a, stop: 1 #464646);\n"
"    border-style: solid;\n"
"    border: 1px solid #1e1e1e;\n"
"    border-radius: 5;\n"
"}\n"
"\n"
"QComboBox:hover,QPushButton:hover\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"\n"
"QComboBox:on\n"
"{\n"
"    padding-top: 3px;\n"
"    padding-left: 4px;\n"
"    background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #2d2d2d, stop: 0.1 #2b2b2b, stop: 0.5 #292929, stop: 0.9 #282828, stop: 1 #252525);\n"
"    selection-background-color: #ffaa00;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView\n"
"{\n"
"    border: 2px solid darkgray;\n"
"    selection-background-color: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QComboBox::drop-down\n"
"{\n"
"     subcontrol-origin: padding;\n"
"     subcontrol-position: top right;\n"
"     width: 15px;\n"
"\n"
"     border-left-width: 0px;\n"
"     border-left-color: darkgray;\n"
"     border-left-style: solid; /* just a single line */\n"
"     border-top-right-radius: 3px; /* same radius as the QComboBox */\n"
"     border-bottom-right-radius: 3px;\n"
" }\n"
"\n"
"QComboBox::down-arrow\n"
"{\n"
"     image: url(:/down_arrow.png);\n"
"}\n"
"\n"
"QGroupBox:focus\n"
"{\n"
"border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QTextEdit:focus\n"
"{\n"
"    border: 2px solid QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"}\n"
"\n"
"QScrollBar:horizontal {\n"
"     border: 1px solid #222222;\n"
"     background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"     height: 7px;\n"
"     margin: 0px 16px 0 16px;\n"
"}\n"
"\n"
"QScrollBar::handle:horizontal\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"      subcontrol-position: right;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal {\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      width: 14px;\n"
"     subcontrol-position: left;\n"
"     subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::right-arrow:horizontal, QScrollBar::left-arrow:horizontal\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QScrollBar:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 1, y2: 0, stop: 0.0 #121212, stop: 0.2 #282828, stop: 1 #484848);\n"
"      width: 7px;\n"
"      margin: 16px 0 16px 0;\n"
"      border: 1px solid #222222;\n"
"}\n"
"\n"
"QScrollBar::handle:vertical\n"
"{\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 0.5 #d7801a, stop: 1 #ffa02f);\n"
"      min-height: 20px;\n"
"      border-radius: 2px;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #ffa02f, stop: 1 #d7801a);\n"
"      height: 14px;\n"
"      subcontrol-position: bottom;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical\n"
"{\n"
"      border: 1px solid #1b1b19;\n"
"      border-radius: 2px;\n"
"      background: QLinearGradient( x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 #d7801a, stop: 1 #ffa02f);\n"
"      height: 14px;\n"
"      subcontrol-position: top;\n"
"      subcontrol-origin: margin;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical\n"
"{\n"
"      border: 1px solid black;\n"
"      width: 1px;\n"
"      height: 1px;\n"
"      background: white;\n"
"}\n"
"\n"
"\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical\n"
"{\n"
"      background: none;\n"
"}\n"
"\n"
"QTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QPlainTextEdit\n"
"{\n"
"    background-color: #242424;\n"
"}\n"
"\n"
"QHeaderView::section\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #616161, stop: 0.5 #505050, stop: 0.6 #434343, stop:1 #656565);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"}\n"
"\n"
"QCheckBox:disabled\n"
"{\n"
"color: #414141;\n"
"}\n"
"\n"
"QDockWidget::title\n"
"{\n"
"    text-align: center;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button, QDockWidget::float-button\n"
"{\n"
"    text-align: center;\n"
"    spacing: 1px; /* spacing between items in the tool bar */\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #323232, stop: 0.5 #242424, stop:1 #323232);\n"
"}\n"
"\n"
"QDockWidget::close-button:hover, QDockWidget::float-button:hover\n"
"{\n"
"    background: #242424;\n"
"}\n"
"\n"
"QDockWidget::close-button:pressed, QDockWidget::float-button:pressed\n"
"{\n"
"    padding: 1px -1px -1px 1px;\n"
"}\n"
"\n"
"QMainWindow::separator\n"
"{\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #4c4c4c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QMainWindow::separator:hover\n"
"{\n"
"\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #d7801a, stop:0.5 #b56c17 stop:1 #ffa02f);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    border: 1px solid #6c6c6c;\n"
"    spacing: 3px; /* spacing between items in the tool bar */\n"
"}\n"
"\n"
"QToolBar::handle\n"
"{\n"
"     spacing: 3px; /* spacing between items in the tool bar */\n"
"     background: url(:/images/handle.png);\n"
"}\n"
"\n"
"QMenu::separator\n"
"{\n"
"    height: 2px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:0 #161616, stop: 0.5 #151515, stop: 0.6 #212121, stop:1 #343434);\n"
"    color: white;\n"
"    padding-left: 4px;\n"
"    margin-left: 10px;\n"
"    margin-right: 5px;\n"
"}\n"
"\n"
"QProgressBar\n"
"{\n"
"    border: 2px solid grey;\n"
"    border-radius: 5px;\n"
"    text-align: center;\n"
"}\n"
"\n"
"QProgressBar::chunk\n"
"{\n"
"    background-color: #d7801a;\n"
"    width: 2.15px;\n"
"    margin: 0.5px;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    color: #b1b1b1;\n"
"    border: 1px solid #444;\n"
"    border-bottom-style: none;\n"
"    background-color: #323232;\n"
"    padding-left: 10px;\n"
"    padding-right: 10px;\n"
"    padding-top: 3px;\n"
"    padding-bottom: 2px;\n"
"    margin-right: -1px;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    border: 1px solid #444;\n"
"    top: 1px;\n"
"}\n"
"\n"
"QTabBar::tab:last\n"
"{\n"
"    margin-right: 0; /* the last selected tab has nothing to overlap with on the right */\n"
"    border-top-right-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:first:!selected\n"
"{\n"
" margin-left: 0px; /* the last selected tab has nothing to overlap with on the right */\n"
"\n"
"\n"
"    border-top-left-radius: 3px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected\n"
"{\n"
"    color: #b1b1b1;\n"
"    border-bottom-style: solid;\n"
"    margin-top: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:.4 #343434);\n"
"}\n"
"\n"
"QTabBar::tab:selected\n"
"{\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    margin-bottom: 0px;\n"
"}\n"
"\n"
"QTabBar::tab:!selected:hover\n"
"{\n"
"    /*border-top: 2px solid #ffaa00;\n"
"    padding-bottom: 3px;*/\n"
"    border-top-left-radius: 3px;\n"
"    border-top-right-radius: 3px;\n"
"    background-color: QLinearGradient(x1:0, y1:0, x2:0, y2:1, stop:1 #212121, stop:0.4 #343434, stop:0.2 #343434, stop:0.1 #ffaa00);\n"
"}\n"
"\n"
"QRadioButton::indicator:checked, QRadioButton::indicator:unchecked{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"}\n"
"\n"
"QCheckBox::indicator{\n"
"    color: #b1b1b1;\n"
"    background-color: #323232;\n"
"    border: 1px solid #b1b1b1;\n"
"    width: 9px;\n"
"    height: 9px;\n"
"}\n"
"\n"
"QRadioButton::indicator\n"
"{\n"
"    border-radius: 6px;\n"
"}\n"
"\n"
"QRadioButton::indicator:hover, QCheckBox::indicator:hover\n"
"{\n"
"    border: 1px solid #ffaa00;\n"
"}\n"
"\n"
"QCheckBox::indicator:checked\n"
"{\n"
"    background-color: qradialgradient(\n"
"        cx: 0.5, cy: 0.5,\n"
"        fx: 0.5, fy: 0.5,\n"
"        radius: 1.0,\n"
"        stop: 0.25 #ffaa00,\n"
"        stop: 0.3 #323232\n"
"    );\n"
"    image:url(:/images/checkbox.png);\n"
"}\n"
"\n"
"QCheckBox::indicator:disabled, QRadioButton::indicator:disabled\n"
"{\n"
"    border: 1px solid #444;\n"
"}"))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridLayout_4 = QtGui.QGridLayout(self.tab)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox_run = QtGui.QGroupBox(self.tab)
        self.groupBox_run.setMinimumSize(QtCore.QSize(700, 0))
        self.groupBox_run.setMaximumSize(QtCore.QSize(770, 16777215))
        self.groupBox_run.setObjectName(_fromUtf8("groupBox_run"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox_run)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_2.setTitle(_fromUtf8(""))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_I_4 = QtGui.QLabel(self.groupBox_2)
        self.label_I_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_I_4.setObjectName(_fromUtf8("label_I_4"))
        self.horizontalLayout.addWidget(self.label_I_4)
        self.comboBox_selectRF = QtGui.QComboBox(self.groupBox_2)
        self.comboBox_selectRF.setObjectName(_fromUtf8("comboBox_selectRF"))
        self.comboBox_selectRF.addItem(_fromUtf8(""))
        self.comboBox_selectRF.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_selectRF)
        self.label_I_3 = QtGui.QLabel(self.groupBox_2)
        self.label_I_3.setEnabled(False)
        self.label_I_3.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.label_I_3.setFont(font)
        self.label_I_3.setObjectName(_fromUtf8("label_I_3"))
        self.horizontalLayout.addWidget(self.label_I_3)
        self.comboBox_dipole = QtGui.QComboBox(self.groupBox_2)
        self.comboBox_dipole.setEnabled(False)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.comboBox_dipole.setFont(font)
        self.comboBox_dipole.setObjectName(_fromUtf8("comboBox_dipole"))
        self.comboBox_dipole.addItem(_fromUtf8(""))
        self.horizontalLayout.addWidget(self.comboBox_dipole)
        self.verticalLayout.addWidget(self.groupBox_2)
        self.groupBox = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 71))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(110, 0, 0);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}"))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_I = QtGui.QLabel(self.groupBox)
        self.label_I.setMinimumSize(QtCore.QSize(120, 0))
        self.label_I.setObjectName(_fromUtf8("label_I"))
        self.gridLayout.addWidget(self.label_I, 0, 0, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 2, 1, 1)
        self.label_RF = QtGui.QLabel(self.groupBox)
        self.label_RF.setEnabled(False)
        self.label_RF.setMinimumSize(QtCore.QSize(120, 0))
        self.label_RF.setObjectName(_fromUtf8("label_RF"))
        self.gridLayout.addWidget(self.label_RF, 0, 3, 1, 1)
        self.pushButton_useCurrent = QtGui.QPushButton(self.groupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_useCurrent.sizePolicy().hasHeightForWidth())
        self.pushButton_useCurrent.setSizePolicy(sizePolicy)
        self.pushButton_useCurrent.setMinimumSize(QtCore.QSize(140, 22))
        self.pushButton_useCurrent.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_useCurrent.setChecked(False)
        self.pushButton_useCurrent.setObjectName(_fromUtf8("pushButton_useCurrent"))
        self.gridLayout.addWidget(self.pushButton_useCurrent, 1, 0, 1, 1)
        self.doubleSpinBox_I = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_I.setObjectName(_fromUtf8("doubleSpinBox_I"))
        self.gridLayout.addWidget(self.doubleSpinBox_I, 1, 1, 1, 1)
        self.doubleSpinBox_p = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_p.setObjectName(_fromUtf8("doubleSpinBox_p"))
        self.gridLayout.addWidget(self.doubleSpinBox_p, 1, 2, 1, 1)
        self.pushButton_useRF = QtGui.QPushButton(self.groupBox)
        self.pushButton_useRF.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_useRF.sizePolicy().hasHeightForWidth())
        self.pushButton_useRF.setSizePolicy(sizePolicy)
        self.pushButton_useRF.setMinimumSize(QtCore.QSize(140, 22))
        self.pushButton_useRF.setMaximumSize(QtCore.QSize(371, 16777215))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_useRF.setFont(font)
        self.pushButton_useRF.setChecked(False)
        self.pushButton_useRF.setObjectName(_fromUtf8("pushButton_useRF"))
        self.gridLayout.addWidget(self.pushButton_useRF, 1, 3, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout.addWidget(self.groupBox)
        self.groupBox_10 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_10.setMinimumSize(QtCore.QSize(0, 137))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_10.setFont(font)
        self.groupBox_10.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(75, 0, 75);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_10.setObjectName(_fromUtf8("groupBox_10"))
        self.horizontalLayout_7 = QtGui.QHBoxLayout(self.groupBox_10)
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.groupBox_8 = QtGui.QGroupBox(self.groupBox_10)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(75, 0, 75);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.gridLayout_7 = QtGui.QGridLayout(self.groupBox_8)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.pushButton_roughGetCurrentRange = QtGui.QPushButton(self.groupBox_8)
        self.pushButton_roughGetCurrentRange.setChecked(False)
        self.pushButton_roughGetCurrentRange.setObjectName(_fromUtf8("pushButton_roughGetCurrentRange"))
        self.gridLayout_7.addWidget(self.pushButton_roughGetCurrentRange, 0, 0, 1, 3)
        self.label_3 = QtGui.QLabel(self.groupBox_8)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_7.addWidget(self.label_3, 1, 0, 1, 1)
        self.lineEdit_roughCurrentMin = QtGui.QLineEdit(self.groupBox_8)
        self.lineEdit_roughCurrentMin.setObjectName(_fromUtf8("lineEdit_roughCurrentMin"))
        self.gridLayout_7.addWidget(self.lineEdit_roughCurrentMin, 1, 1, 1, 1)
        self.lineEdit_roughCurrentMax = QtGui.QLineEdit(self.groupBox_8)
        self.lineEdit_roughCurrentMax.setObjectName(_fromUtf8("lineEdit_roughCurrentMax"))
        self.gridLayout_7.addWidget(self.lineEdit_roughCurrentMax, 1, 2, 1, 1)
        self.pushButton_roughCentreC2VCurrent = QtGui.QPushButton(self.groupBox_8)
        self.pushButton_roughCentreC2VCurrent.setChecked(False)
        self.pushButton_roughCentreC2VCurrent.setObjectName(_fromUtf8("pushButton_roughCentreC2VCurrent"))
        self.gridLayout_7.addWidget(self.pushButton_roughCentreC2VCurrent, 2, 0, 1, 3)
        self.horizontalLayout_7.addWidget(self.groupBox_8)
        self.groupBox_11 = QtGui.QGroupBox(self.groupBox_10)
        self.groupBox_11.setEnabled(False)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.groupBox_11.setFont(font)
        self.groupBox_11.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(55, 0, 55);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_11.setObjectName(_fromUtf8("groupBox_11"))
        self.gridLayout_6 = QtGui.QGridLayout(self.groupBox_11)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.pushButton_roughGetRFRange = QtGui.QPushButton(self.groupBox_11)
        self.pushButton_roughGetRFRange.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_roughGetRFRange.setFont(font)
        self.pushButton_roughGetRFRange.setChecked(False)
        self.pushButton_roughGetRFRange.setObjectName(_fromUtf8("pushButton_roughGetRFRange"))
        self.gridLayout_6.addWidget(self.pushButton_roughGetRFRange, 0, 0, 1, 3)
        self.label_8 = QtGui.QLabel(self.groupBox_11)
        self.label_8.setEnabled(False)
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_6.addWidget(self.label_8, 1, 0, 1, 1)
        self.lineEdit_roughRFMin = QtGui.QLineEdit(self.groupBox_11)
        self.lineEdit_roughRFMin.setEnabled(False)
        self.lineEdit_roughRFMin.setObjectName(_fromUtf8("lineEdit_roughRFMin"))
        self.gridLayout_6.addWidget(self.lineEdit_roughRFMin, 1, 1, 1, 1)
        self.lineEdit_roughRFMax = QtGui.QLineEdit(self.groupBox_11)
        self.lineEdit_roughRFMax.setEnabled(False)
        self.lineEdit_roughRFMax.setObjectName(_fromUtf8("lineEdit_roughRFMax"))
        self.gridLayout_6.addWidget(self.lineEdit_roughRFMax, 1, 2, 1, 1)
        self.pushButton_roughCentreC2VRF = QtGui.QPushButton(self.groupBox_11)
        self.pushButton_roughCentreC2VRF.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_roughCentreC2VRF.setFont(font)
        self.pushButton_roughCentreC2VRF.setChecked(False)
        self.pushButton_roughCentreC2VRF.setObjectName(_fromUtf8("pushButton_roughCentreC2VRF"))
        self.gridLayout_6.addWidget(self.pushButton_roughCentreC2VRF, 2, 0, 1, 3)
        self.horizontalLayout_7.addWidget(self.groupBox_11)
        self.verticalLayout.addWidget(self.groupBox_10)
        self.groupBox_9 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_9.setMinimumSize(QtCore.QSize(0, 471))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_9.setFont(font)
        self.groupBox_9.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(0, 0, 100);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_9)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout_15 = QtGui.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.pushButton_Prelim_1 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_Prelim_1.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Prelim_1.sizePolicy().hasHeightForWidth())
        self.pushButton_Prelim_1.setSizePolicy(sizePolicy)
        self.pushButton_Prelim_1.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Prelim_1.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_Prelim_1.setChecked(False)
        self.pushButton_Prelim_1.setObjectName(_fromUtf8("pushButton_Prelim_1"))
        self.horizontalLayout_15.addWidget(self.pushButton_Prelim_1)
        self.pushButton_Prelim_3 = QtGui.QPushButton(self.groupBox_3)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Prelim_3.sizePolicy().hasHeightForWidth())
        self.pushButton_Prelim_3.setSizePolicy(sizePolicy)
        self.pushButton_Prelim_3.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Prelim_3.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_Prelim_3.setChecked(False)
        self.pushButton_Prelim_3.setObjectName(_fromUtf8("pushButton_Prelim_3"))
        self.horizontalLayout_15.addWidget(self.pushButton_Prelim_3)
        self.verticalLayout_3.addWidget(self.groupBox_3)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.gridLayout_5 = QtGui.QGridLayout(self.groupBox_4)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.horizontalLayout_18 = QtGui.QHBoxLayout()
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.label_11 = QtGui.QLabel(self.groupBox_4)
        self.label_11.setMinimumSize(QtCore.QSize(210, 0))
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.horizontalLayout_18.addWidget(self.label_11)
        self.lineEdit_maskX = QtGui.QLineEdit(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskX.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskX.setSizePolicy(sizePolicy)
        self.lineEdit_maskX.setObjectName(_fromUtf8("lineEdit_maskX"))
        self.horizontalLayout_18.addWidget(self.lineEdit_maskX)
        self.lineEdit_maskY = QtGui.QLineEdit(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskY.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskY.setSizePolicy(sizePolicy)
        self.lineEdit_maskY.setObjectName(_fromUtf8("lineEdit_maskY"))
        self.horizontalLayout_18.addWidget(self.lineEdit_maskY)
        self.lineEdit_maskXRad = QtGui.QLineEdit(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskXRad.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskXRad.setSizePolicy(sizePolicy)
        self.lineEdit_maskXRad.setObjectName(_fromUtf8("lineEdit_maskXRad"))
        self.horizontalLayout_18.addWidget(self.lineEdit_maskXRad)
        self.lineEdit_maskYRad = QtGui.QLineEdit(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskYRad.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskYRad.setSizePolicy(sizePolicy)
        self.lineEdit_maskYRad.setObjectName(_fromUtf8("lineEdit_maskYRad"))
        self.horizontalLayout_18.addWidget(self.lineEdit_maskYRad)
        self.gridLayout_5.addLayout(self.horizontalLayout_18, 3, 1, 1, 3)
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.horizontalLayout_10.addWidget(self.label_13)
        self.doubleSpinBox_x_1 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_x_1.setMinimum(-100.0)
        self.doubleSpinBox_x_1.setMaximum(100.0)
        self.doubleSpinBox_x_1.setSingleStep(0.1)
        self.doubleSpinBox_x_1.setObjectName(_fromUtf8("doubleSpinBox_x_1"))
        self.horizontalLayout_10.addWidget(self.doubleSpinBox_x_1)
        self.label_12 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_10.addWidget(self.label_12)
        self.doubleSpinBox_tol_1 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_tol_1.setSingleStep(0.1)
        self.doubleSpinBox_tol_1.setProperty("value", 0.5)
        self.doubleSpinBox_tol_1.setObjectName(_fromUtf8("doubleSpinBox_tol_1"))
        self.horizontalLayout_10.addWidget(self.doubleSpinBox_tol_1)
        self.label_16 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.horizontalLayout_10.addWidget(self.label_16)
        self.label_H_1 = QtGui.QLabel(self.groupBox_4)
        self.label_H_1.setMinimumSize(QtCore.QSize(70, 0))
        self.label_H_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_1.setText(_fromUtf8(""))
        self.label_H_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_1.setObjectName(_fromUtf8("label_H_1"))
        self.horizontalLayout_10.addWidget(self.label_H_1)
        self.gridLayout_5.addLayout(self.horizontalLayout_10, 1, 1, 1, 3)
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        self.pushButton_Align_2_A = QtGui.QPushButton(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Align_2_A.sizePolicy().hasHeightForWidth())
        self.pushButton_Align_2_A.setSizePolicy(sizePolicy)
        self.pushButton_Align_2_A.setMinimumSize(QtCore.QSize(160, 0))
        self.pushButton_Align_2_A.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Align_2_A.setChecked(False)
        self.pushButton_Align_2_A.setObjectName(_fromUtf8("pushButton_Align_2_A"))
        self.horizontalLayout_19.addWidget(self.pushButton_Align_2_A)
        self.pushButton_Align_2_B = QtGui.QPushButton(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Align_2_B.sizePolicy().hasHeightForWidth())
        self.pushButton_Align_2_B.setSizePolicy(sizePolicy)
        self.pushButton_Align_2_B.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_Align_2_B.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Align_2_B.setChecked(False)
        self.pushButton_Align_2_B.setObjectName(_fromUtf8("pushButton_Align_2_B"))
        self.horizontalLayout_19.addWidget(self.pushButton_Align_2_B)
        self.gridLayout_5.addLayout(self.horizontalLayout_19, 2, 1, 1, 3)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.label_14 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.horizontalLayout_9.addWidget(self.label_14)
        self.doubleSpinBox_x_2 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_x_2.setMinimum(-100.0)
        self.doubleSpinBox_x_2.setMaximum(100.0)
        self.doubleSpinBox_x_2.setSingleStep(0.1)
        self.doubleSpinBox_x_2.setProperty("value", 6.4)
        self.doubleSpinBox_x_2.setObjectName(_fromUtf8("doubleSpinBox_x_2"))
        self.horizontalLayout_9.addWidget(self.doubleSpinBox_x_2)
        self.label_15 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_9.addWidget(self.label_15)
        self.doubleSpinBox_tol_2 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_tol_2.setSingleStep(0.1)
        self.doubleSpinBox_tol_2.setProperty("value", 0.5)
        self.doubleSpinBox_tol_2.setObjectName(_fromUtf8("doubleSpinBox_tol_2"))
        self.horizontalLayout_9.addWidget(self.doubleSpinBox_tol_2)
        self.label_17 = QtGui.QLabel(self.groupBox_4)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.horizontalLayout_9.addWidget(self.label_17)
        self.label_H_2 = QtGui.QLabel(self.groupBox_4)
        self.label_H_2.setMinimumSize(QtCore.QSize(70, 0))
        self.label_H_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_2.setText(_fromUtf8(""))
        self.label_H_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_2.setObjectName(_fromUtf8("label_H_2"))
        self.horizontalLayout_9.addWidget(self.label_H_2)
        self.gridLayout_5.addLayout(self.horizontalLayout_9, 4, 1, 2, 3)
        self.label_6 = QtGui.QLabel(self.groupBox_4)
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_5.addWidget(self.label_6, 9, 1, 1, 2)
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.pushButton_Align_1a = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_1a.setChecked(False)
        self.pushButton_Align_1a.setObjectName(_fromUtf8("pushButton_Align_1a"))
        self.verticalLayout_4.addWidget(self.pushButton_Align_1a)
        self.pushButton_Align_1 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_1.setChecked(False)
        self.pushButton_Align_1.setObjectName(_fromUtf8("pushButton_Align_1"))
        self.verticalLayout_4.addWidget(self.pushButton_Align_1)
        self.pushButton_Align_2 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_2.setChecked(False)
        self.pushButton_Align_2.setObjectName(_fromUtf8("pushButton_Align_2"))
        self.verticalLayout_4.addWidget(self.pushButton_Align_2)
        self.label_24 = QtGui.QLabel(self.groupBox_4)
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.verticalLayout_4.addWidget(self.label_24)
        self.pushButton_Align_3 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_3.setChecked(False)
        self.pushButton_Align_3.setObjectName(_fromUtf8("pushButton_Align_3"))
        self.verticalLayout_4.addWidget(self.pushButton_Align_3)
        self.pushButton_Align_4 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_4.setChecked(False)
        self.pushButton_Align_4.setObjectName(_fromUtf8("pushButton_Align_4"))
        self.verticalLayout_4.addWidget(self.pushButton_Align_4)
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_4.addWidget(self.label_4)
        self.gridLayout_5.addLayout(self.verticalLayout_4, 0, 0, 10, 1)
        self.checkBox = QtGui.QCheckBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox.sizePolicy().hasHeightForWidth())
        self.checkBox.setSizePolicy(sizePolicy)
        self.checkBox.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkBox.setFont(font)
        self.checkBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox.setStyleSheet(_fromUtf8("QCheckBox{ background-color: rgb(0, 0, 0);}"))
        self.checkBox.setCheckable(False)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.gridLayout_5.addWidget(self.checkBox, 6, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_5.addWidget(self.label_5, 0, 1, 1, 3)
        self.checkBox_2 = QtGui.QCheckBox(self.groupBox_4)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.checkBox_2.sizePolicy().hasHeightForWidth())
        self.checkBox_2.setSizePolicy(sizePolicy)
        self.checkBox_2.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_2.setStyleSheet(_fromUtf8("QCheckBox{ background-color: rgb(0, 0, 0);}"))
        self.checkBox_2.setCheckable(False)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.gridLayout_5.addWidget(self.checkBox_2, 6, 2, 1, 1)
        self.verticalLayout_3.addWidget(self.groupBox_4)
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox_9)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(0, 0, 100);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.pushButton_fineGetCurrentRange_2 = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_fineGetCurrentRange_2.setChecked(False)
        self.pushButton_fineGetCurrentRange_2.setObjectName(_fromUtf8("pushButton_fineGetCurrentRange_2"))
        self.verticalLayout_5.addWidget(self.pushButton_fineGetCurrentRange_2)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.label_9 = QtGui.QLabel(self.groupBox_5)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_12.addWidget(self.label_9)
        self.lineEdit_fineCurrentMin = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_fineCurrentMin.setObjectName(_fromUtf8("lineEdit_fineCurrentMin"))
        self.horizontalLayout_12.addWidget(self.lineEdit_fineCurrentMin)
        self.lineEdit_fineCurrentMax = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_fineCurrentMax.setObjectName(_fromUtf8("lineEdit_fineCurrentMax"))
        self.horizontalLayout_12.addWidget(self.lineEdit_fineCurrentMax)
        self.verticalLayout_5.addLayout(self.horizontalLayout_12)
        self.pushButton_fineCentreC2VCurrent = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_fineCentreC2VCurrent.setChecked(False)
        self.pushButton_fineCentreC2VCurrent.setObjectName(_fromUtf8("pushButton_fineCentreC2VCurrent"))
        self.verticalLayout_5.addWidget(self.pushButton_fineCentreC2VCurrent)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.label_19 = QtGui.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.horizontalLayout_14.addWidget(self.label_19)
        self.doubleSpinBox_x_3 = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_x_3.setMaximumSize(QtCore.QSize(75, 16777215))
        self.doubleSpinBox_x_3.setReadOnly(True)
        self.doubleSpinBox_x_3.setMinimum(-100.0)
        self.doubleSpinBox_x_3.setMaximum(100.0)
        self.doubleSpinBox_x_3.setSingleStep(0.1)
        self.doubleSpinBox_x_3.setProperty("value", 0.0)
        self.doubleSpinBox_x_3.setObjectName(_fromUtf8("doubleSpinBox_x_3"))
        self.horizontalLayout_14.addWidget(self.doubleSpinBox_x_3)
        self.label_18 = QtGui.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.horizontalLayout_14.addWidget(self.label_18)
        self.doubleSpinBox_tol_3 = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_tol_3.setMaximumSize(QtCore.QSize(75, 16777215))
        self.doubleSpinBox_tol_3.setSingleStep(0.1)
        self.doubleSpinBox_tol_3.setProperty("value", 0.1)
        self.doubleSpinBox_tol_3.setObjectName(_fromUtf8("doubleSpinBox_tol_3"))
        self.horizontalLayout_14.addWidget(self.doubleSpinBox_tol_3)
        self.label_22 = QtGui.QLabel(self.groupBox_5)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.horizontalLayout_14.addWidget(self.label_22)
        self.label_H_3 = QtGui.QLabel(self.groupBox_5)
        self.label_H_3.setMinimumSize(QtCore.QSize(70, 0))
        self.label_H_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_3.setText(_fromUtf8(""))
        self.label_H_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_3.setObjectName(_fromUtf8("label_H_3"))
        self.horizontalLayout_14.addWidget(self.label_H_3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_8.addWidget(self.groupBox_5)
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox_9)
        self.groupBox_6.setEnabled(True)
        self.groupBox_6.setMinimumSize(QtCore.QSize(300, 0))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(0, 0, 100);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.label_7 = QtGui.QLabel(self.groupBox_6)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_17.addWidget(self.label_7)
        self.doubleSpinBox_p_2 = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_p_2.setObjectName(_fromUtf8("doubleSpinBox_p_2"))
        self.horizontalLayout_17.addWidget(self.doubleSpinBox_p_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.pushButton_fineGetRFRange_2 = QtGui.QPushButton(self.groupBox_6)
        self.pushButton_fineGetRFRange_2.setMinimumSize(QtCore.QSize(200, 0))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_fineGetRFRange_2.setFont(font)
        self.pushButton_fineGetRFRange_2.setChecked(False)
        self.pushButton_fineGetRFRange_2.setObjectName(_fromUtf8("pushButton_fineGetRFRange_2"))
        self.horizontalLayout_16.addWidget(self.pushButton_fineGetRFRange_2)
        self.label_I_2 = QtGui.QLabel(self.groupBox_6)
        self.label_I_2.setMinimumSize(QtCore.QSize(50, 0))
        self.label_I_2.setObjectName(_fromUtf8("label_I_2"))
        self.horizontalLayout_16.addWidget(self.label_I_2)
        self.verticalLayout_6.addLayout(self.horizontalLayout_16)
        self.label_10 = QtGui.QLabel(self.groupBox_6)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.verticalLayout_6.addWidget(self.label_10)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.label_20 = QtGui.QLabel(self.groupBox_6)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.horizontalLayout_13.addWidget(self.label_20)
        self.doubleSpinBox_x_4 = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_x_4.setMaximumSize(QtCore.QSize(80, 16777215))
        self.doubleSpinBox_x_4.setReadOnly(True)
        self.doubleSpinBox_x_4.setMinimum(-100.0)
        self.doubleSpinBox_x_4.setMaximum(100.0)
        self.doubleSpinBox_x_4.setSingleStep(0.1)
        self.doubleSpinBox_x_4.setProperty("value", 0.0)
        self.doubleSpinBox_x_4.setObjectName(_fromUtf8("doubleSpinBox_x_4"))
        self.horizontalLayout_13.addWidget(self.doubleSpinBox_x_4)
        self.label_21 = QtGui.QLabel(self.groupBox_6)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.horizontalLayout_13.addWidget(self.label_21)
        self.doubleSpinBox_tol_4 = QtGui.QDoubleSpinBox(self.groupBox_6)
        self.doubleSpinBox_tol_4.setSingleStep(0.1)
        self.doubleSpinBox_tol_4.setProperty("value", 0.1)
        self.doubleSpinBox_tol_4.setObjectName(_fromUtf8("doubleSpinBox_tol_4"))
        self.horizontalLayout_13.addWidget(self.doubleSpinBox_tol_4)
        self.label_23 = QtGui.QLabel(self.groupBox_6)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_23.setFont(font)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.horizontalLayout_13.addWidget(self.label_23)
        self.label_H_4 = QtGui.QLabel(self.groupBox_6)
        self.label_H_4.setMinimumSize(QtCore.QSize(70, 0))
        self.label_H_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_4.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_4.setText(_fromUtf8(""))
        self.label_H_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_4.setObjectName(_fromUtf8("label_H_4"))
        self.horizontalLayout_13.addWidget(self.label_H_4)
        self.verticalLayout_6.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_8.addWidget(self.groupBox_6)
        self.verticalLayout_3.addLayout(self.horizontalLayout_8)
        self.verticalLayout.addWidget(self.groupBox_9)
        self.gridLayout_4.addWidget(self.groupBox_run, 0, 0, 1, 1)
        self.groupBox_monitor = QtGui.QGroupBox(self.tab)
        self.groupBox_monitor.setMinimumSize(QtCore.QSize(500, 0))
        self.groupBox_monitor.setObjectName(_fromUtf8("groupBox_monitor"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_monitor)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.gridLayout_4.addWidget(self.groupBox_monitor, 0, 1, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.tab_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.groupBox_s_run = QtGui.QGroupBox(self.tab_2)
        self.groupBox_s_run.setMinimumSize(QtCore.QSize(500, 0))
        self.groupBox_s_run.setMaximumSize(QtCore.QSize(500, 16777215))
        self.groupBox_s_run.setObjectName(_fromUtf8("groupBox_s_run"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_s_run)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.pushButton_CalcDisp = QtGui.QPushButton(self.groupBox_s_run)
        self.pushButton_CalcDisp.setChecked(False)
        self.pushButton_CalcDisp.setObjectName(_fromUtf8("pushButton_CalcDisp"))
        self.gridLayout_2.addWidget(self.pushButton_CalcDisp, 4, 0, 1, 1)
        self.pushButton_Calc = QtGui.QPushButton(self.groupBox_s_run)
        self.pushButton_Calc.setChecked(False)
        self.pushButton_Calc.setObjectName(_fromUtf8("pushButton_Calc"))
        self.gridLayout_2.addWidget(self.pushButton_Calc, 6, 0, 1, 1)
        self.checkBox_done_mom = QtGui.QCheckBox(self.groupBox_s_run)
        self.checkBox_done_mom.setObjectName(_fromUtf8("checkBox_done_mom"))
        self.gridLayout_2.addWidget(self.checkBox_done_mom, 0, 0, 1, 1)
        self.pushButton_refreshProfile = QtGui.QPushButton(self.groupBox_s_run)
        self.pushButton_refreshProfile.setObjectName(_fromUtf8("pushButton_refreshProfile"))
        self.gridLayout_2.addWidget(self.pushButton_refreshProfile, 7, 0, 1, 2)
        self.pushButton_Checks = QtGui.QPushButton(self.groupBox_s_run)
        self.pushButton_Checks.setChecked(False)
        self.pushButton_Checks.setObjectName(_fromUtf8("pushButton_Checks"))
        self.gridLayout_2.addWidget(self.pushButton_Checks, 1, 0, 1, 1)
        self.pushButton_MinBeta = QtGui.QPushButton(self.groupBox_s_run)
        self.pushButton_MinBeta.setChecked(False)
        self.pushButton_MinBeta.setObjectName(_fromUtf8("pushButton_MinBeta"))
        self.gridLayout_2.addWidget(self.pushButton_MinBeta, 2, 0, 1, 1)
        self.pushButton_SetDispSize = QtGui.QPushButton(self.groupBox_s_run)
        self.pushButton_SetDispSize.setObjectName(_fromUtf8("pushButton_SetDispSize"))
        self.gridLayout_2.addWidget(self.pushButton_SetDispSize, 3, 0, 1, 1)
        self.horizontalLayout_3.addWidget(self.groupBox_s_run)
        self.groupBox_s_monitor = QtGui.QGroupBox(self.tab_2)
        self.groupBox_s_monitor.setMinimumSize(QtCore.QSize(600, 0))
        self.groupBox_s_monitor.setObjectName(_fromUtf8("groupBox_s_monitor"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.groupBox_s_monitor)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.horizontalLayout_3.addWidget(self.groupBox_s_monitor)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tabLog = QtGui.QWidget()
        self.tabLog.setObjectName(_fromUtf8("tabLog"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.tabLog)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_6.addLayout(self.gridLayout_3)
        self.tabWidget.addTab(self.tabLog, _fromUtf8(""))
        self.horizontalLayout_2.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1539, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox_run.setTitle(_translate("MainWindow", "Run", None))
        self.label_I_4.setText(_translate("MainWindow", "Select RF:", None))
        self.comboBox_selectRF.setItemText(0, _translate("MainWindow", "Gun only", None))
        self.comboBox_selectRF.setItemText(1, _translate("MainWindow", "Gun + Linac (gun fixed)", None))
        self.label_I_3.setText(_translate("MainWindow", "Select dipole:", None))
        self.comboBox_dipole.setItemText(0, _translate("MainWindow", "S02-DIP01", None))
        self.groupBox.setTitle(_translate("MainWindow", "Initial estimate (sets scan range for rough measurements):", None))
        self.label_I.setText(_translate("MainWindow", "...", None))
        self.label.setText(_translate("MainWindow", "Dipole current", None))
        self.label_2.setText(_translate("MainWindow", "Momentum", None))
        self.label_RF.setText(_translate("MainWindow", "...", None))
        self.pushButton_useCurrent.setText(_translate("MainWindow", "Use current from dipole", None))
        self.doubleSpinBox_I.setSuffix(_translate("MainWindow", " A", None))
        self.doubleSpinBox_p.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.pushButton_useRF.setText(_translate("MainWindow", "Estimate momentum from RF", None))
        self.groupBox_10.setTitle(_translate("MainWindow", "Rough measure/set (finds BPM range to use for fine measurements):", None))
        self.groupBox_8.setTitle(_translate("MainWindow", "Measure momentum:", None))
        self.pushButton_roughGetCurrentRange.setText(_translate("MainWindow", "1. Get scan range from initial estimate", None))
        self.label_3.setText(_translate("MainWindow", "Dipole min/max (editable):", None))
        self.pushButton_roughCentreC2VCurrent.setText(_translate("MainWindow", "2. Scan dipole", None))
        self.groupBox_11.setTitle(_translate("MainWindow", "Set momentum:", None))
        self.pushButton_roughGetRFRange.setText(_translate("MainWindow", "1. Get scan range from initial estimate", None))
        self.label_8.setText(_translate("MainWindow", "RF amp min/max (editable):", None))
        self.pushButton_roughCentreC2VRF.setText(_translate("MainWindow", "2. Scan RF", None))
        self.groupBox_9.setTitle(_translate("MainWindow", "Fine measure/set:", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Preliminaries:", None))
        self.pushButton_Prelim_1.setText(_translate("MainWindow", "1. Recalibrate BPMs", None))
        self.pushButton_Prelim_3.setText(_translate("MainWindow", "2. Degauss to zero: S02-DIP01, Q-03,04,05 (Closes laser shutters while degaussing)", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Align through dipole:", None))
        self.label_11.setText(_translate("MainWindow", "↑ Run 2a. and 2b. on first iteration", None))
        self.lineEdit_maskX.setText(_translate("MainWindow", "590", None))
        self.lineEdit_maskY.setText(_translate("MainWindow", "650", None))
        self.lineEdit_maskXRad.setText(_translate("MainWindow", "500", None))
        self.lineEdit_maskYRad.setText(_translate("MainWindow", "500", None))
        self.label_13.setText(_translate("MainWindow", "x target", None))
        self.doubleSpinBox_x_1.setSuffix(_translate("MainWindow", " mm", None))
        self.label_12.setText(_translate("MainWindow", "Tolerance", None))
        self.doubleSpinBox_tol_1.setSuffix(_translate("MainWindow", " mm", None))
        self.label_16.setText(_translate("MainWindow", "Δx", None))
        self.pushButton_Align_2_A.setText(_translate("MainWindow", "2a. Switch to S02-CAM02", None))
        self.pushButton_Align_2_B.setText(_translate("MainWindow", "2b. Set mask x/y/xradius/yradius ↓", None))
        self.label_14.setText(_translate("MainWindow", "x target", None))
        self.doubleSpinBox_x_2.setSuffix(_translate("MainWindow", " mm", None))
        self.label_15.setText(_translate("MainWindow", "Tolerance", None))
        self.doubleSpinBox_tol_2.setSuffix(_translate("MainWindow", " mm", None))
        self.label_17.setText(_translate("MainWindow", "Δx", None))
        self.pushButton_Align_1a.setText(_translate("MainWindow", "1a. Find beam on S02-BPM02 (if needed)", None))
        self.pushButton_Align_1.setText(_translate("MainWindow", "1. Align on S02-BPM02 using S02-HCOR02", None))
        self.pushButton_Align_2.setText(_translate("MainWindow", "2. Insert S02-YAG02", None))
        self.label_24.setText(_translate("MainWindow", "Check ImageCollector cross-hair is tracking", None))
        self.pushButton_Align_3.setText(_translate("MainWindow", "3. Align on S02-YAG02 using S02-HCOR01", None))
        self.pushButton_Align_4.setText(_translate("MainWindow", "4. Retract S02-YAG02 and test alignment", None))
        self.label_4.setText(_translate("MainWindow", "↑ Repeat above steps until aligned on both ↑", None))
        self.checkBox.setText(_translate("MainWindow", "Aligned on S02-YAG02", None))
        self.label_5.setText(_translate("MainWindow", "↓ Default targets are expected centres", None))
        self.checkBox_2.setText(_translate("MainWindow", "Aligned on S02-BPM02", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Measure momentum:", None))
        self.pushButton_fineGetCurrentRange_2.setText(_translate("MainWindow", "1. Get scan range from rough measurement", None))
        self.label_9.setText(_translate("MainWindow", "Dipole min/max:", None))
        self.pushButton_fineCentreC2VCurrent.setText(_translate("MainWindow", "2. Start scan", None))
        self.label_19.setText(_translate("MainWindow", "Target", None))
        self.doubleSpinBox_x_3.setSuffix(_translate("MainWindow", " mm", None))
        self.label_18.setText(_translate("MainWindow", "Tol.", None))
        self.doubleSpinBox_tol_3.setSuffix(_translate("MainWindow", " mm", None))
        self.label_22.setText(_translate("MainWindow", "Δx", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Set momentum:", None))
        self.label_7.setText(_translate("MainWindow", "1. Enter target momentum", None))
        self.doubleSpinBox_p_2.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.pushButton_fineGetRFRange_2.setText(_translate("MainWindow", "2. Set corresponding dipole current", None))
        self.label_I_2.setText(_translate("MainWindow", "...", None))
        self.label_10.setText(_translate("MainWindow", "3. Set gun or linac amp. from RF panel to centre on C2V", None))
        self.label_20.setText(_translate("MainWindow", "Target", None))
        self.doubleSpinBox_x_4.setSuffix(_translate("MainWindow", " mm", None))
        self.label_21.setText(_translate("MainWindow", "Tol.", None))
        self.doubleSpinBox_tol_4.setSuffix(_translate("MainWindow", " mm", None))
        self.label_23.setText(_translate("MainWindow", "Δx", None))
        self.groupBox_monitor.setTitle(_translate("MainWindow", "Monitor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Momentum", None))
        self.groupBox_s_run.setTitle(_translate("MainWindow", "Run", None))
        self.pushButton_CalcDisp.setText(_translate("MainWindow", "3. Calculate Dispersion", None))
        self.pushButton_Calc.setText(_translate("MainWindow", "4. Calculate Momentum Spread", None))
        self.checkBox_done_mom.setText(_translate("MainWindow", "Momentum Measurement Done", None))
        self.pushButton_refreshProfile.setText(_translate("MainWindow", "Refresh Profile", None))
        self.pushButton_Checks.setText(_translate("MainWindow", "1. Checks", None))
        self.pushButton_MinBeta.setText(_translate("MainWindow", "2. Minimise Beta", None))
        self.pushButton_SetDispSize.setText(_translate("MainWindow", "3. Set Dispersion Size", None))
        self.groupBox_s_monitor.setTitle(_translate("MainWindow", "Monitor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Momentum Spread", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLog), _translate("MainWindow", "Log", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


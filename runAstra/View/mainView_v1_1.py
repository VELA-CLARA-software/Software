# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUI_v1.1.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import pyqtgraph as pg
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
        MainWindow.resize(963, 572)
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
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(6, -1, 951, 531))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.setTab = QtGui.QWidget()
        self.setTab.setObjectName(_fromUtf8("setTab"))
        self.setVirtualMachine_Btn = QtGui.QPushButton(self.setTab)
        self.setVirtualMachine_Btn.setGeometry(QtCore.QRect(10, 370, 211, 91))
        self.setVirtualMachine_Btn.setObjectName(_fromUtf8("setVirtualMachine_Btn"))
        self.runASTRA_Btn = QtGui.QPushButton(self.setTab)
        self.runASTRA_Btn.setGeometry(QtCore.QRect(230, 370, 211, 91))
        self.runASTRA_Btn.setObjectName(_fromUtf8("runASTRA_Btn"))
        self.groupBox = QtGui.QGroupBox(self.setTab)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 431, 341))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 30, 101, 21))
        self.label.setObjectName(_fromUtf8("label"))
        self.lineEdit_RFGA = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_RFGA.setGeometry(QtCore.QRect(100, 30, 113, 20))
        self.lineEdit_RFGA.setObjectName(_fromUtf8("lineEdit_RFGA"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 50, 101, 21))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lineEdit_RFGP = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_RFGP.setGeometry(QtCore.QRect(100, 50, 113, 20))
        self.lineEdit_RFGP.setObjectName(_fromUtf8("lineEdit_RFGP"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 101, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.lineEdit_Q1C = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Q1C.setGeometry(QtCore.QRect(100, 70, 113, 20))
        self.lineEdit_Q1C.setObjectName(_fromUtf8("lineEdit_Q1C"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(10, 90, 101, 21))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.lineEdit_Q2C = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Q2C.setGeometry(QtCore.QRect(100, 90, 113, 20))
        self.lineEdit_Q2C.setObjectName(_fromUtf8("lineEdit_Q2C"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(10, 110, 101, 21))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.lineEdit_Q3C = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Q3C.setGeometry(QtCore.QRect(100, 110, 113, 20))
        self.lineEdit_Q3C.setObjectName(_fromUtf8("lineEdit_Q3C"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(10, 130, 101, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.lineEdit_Q4C = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Q4C.setGeometry(QtCore.QRect(100, 130, 113, 20))
        self.lineEdit_Q4C.setObjectName(_fromUtf8("lineEdit_Q4C"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(10, 150, 101, 21))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.lineEdit_Q7C = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Q7C.setGeometry(QtCore.QRect(100, 150, 113, 20))
        self.lineEdit_Q7C.setObjectName(_fromUtf8("lineEdit_Q7C"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(10, 170, 101, 21))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.lineEdit_Q8C = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Q8C.setGeometry(QtCore.QRect(100, 170, 113, 20))
        self.lineEdit_Q8C.setObjectName(_fromUtf8("lineEdit_Q8C"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setGeometry(QtCore.QRect(10, 190, 101, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.lineEdit_Q9C = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_Q9C.setGeometry(QtCore.QRect(100, 190, 113, 20))
        self.lineEdit_Q9C.setObjectName(_fromUtf8("lineEdit_Q9C"))
        self.checkBox_useQuad_1 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_1.setEnabled(True)
        self.checkBox_useQuad_1.setGeometry(QtCore.QRect(220, 70, 70, 17))
        self.checkBox_useQuad_1.setText(_fromUtf8(""))
        self.checkBox_useQuad_1.setChecked(True)
        self.checkBox_useQuad_1.setObjectName(_fromUtf8("checkBox_useQuad_1"))
        self.checkBox_useQuad_2 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_2.setGeometry(QtCore.QRect(220, 90, 70, 17))
        self.checkBox_useQuad_2.setText(_fromUtf8(""))
        self.checkBox_useQuad_2.setChecked(True)
        self.checkBox_useQuad_2.setObjectName(_fromUtf8("checkBox_useQuad_2"))
        self.checkBox_useQuad_3 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_3.setGeometry(QtCore.QRect(220, 110, 70, 17))
        self.checkBox_useQuad_3.setText(_fromUtf8(""))
        self.checkBox_useQuad_3.setChecked(True)
        self.checkBox_useQuad_3.setObjectName(_fromUtf8("checkBox_useQuad_3"))
        self.checkBox_useQuad_4 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_4.setGeometry(QtCore.QRect(220, 130, 70, 17))
        self.checkBox_useQuad_4.setText(_fromUtf8(""))
        self.checkBox_useQuad_4.setChecked(True)
        self.checkBox_useQuad_4.setObjectName(_fromUtf8("checkBox_useQuad_4"))
        self.checkBox_useQuad_5 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_5.setGeometry(QtCore.QRect(300, 50, 70, 17))
        self.checkBox_useQuad_5.setText(_fromUtf8(""))
        self.checkBox_useQuad_5.setObjectName(_fromUtf8("checkBox_useQuad_5"))
        self.checkBox_useQuad_6 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_6.setGeometry(QtCore.QRect(310, 80, 70, 17))
        self.checkBox_useQuad_6.setText(_fromUtf8(""))
        self.checkBox_useQuad_6.setObjectName(_fromUtf8("checkBox_useQuad_6"))
        self.checkBox_useQuad_7 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_7.setGeometry(QtCore.QRect(220, 150, 70, 17))
        self.checkBox_useQuad_7.setText(_fromUtf8(""))
        self.checkBox_useQuad_7.setChecked(True)
        self.checkBox_useQuad_7.setObjectName(_fromUtf8("checkBox_useQuad_7"))
        self.checkBox_useQuad_8 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_8.setGeometry(QtCore.QRect(220, 170, 70, 17))
        self.checkBox_useQuad_8.setText(_fromUtf8(""))
        self.checkBox_useQuad_8.setChecked(True)
        self.checkBox_useQuad_8.setObjectName(_fromUtf8("checkBox_useQuad_8"))
        self.checkBox_useQuad_9 = QtGui.QCheckBox(self.groupBox)
        self.checkBox_useQuad_9.setGeometry(QtCore.QRect(220, 190, 70, 17))
        self.checkBox_useQuad_9.setText(_fromUtf8(""))
        self.checkBox_useQuad_9.setChecked(True)
        self.checkBox_useQuad_9.setObjectName(_fromUtf8("checkBox_useQuad_9"))
        self.groupBox_2 = QtGui.QGroupBox(self.setTab)
        self.groupBox_2.setGeometry(QtCore.QRect(450, 10, 431, 341))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.lineEdit_SAB = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_SAB.setGeometry(QtCore.QRect(120, 240, 113, 20))
        self.lineEdit_SAB.setObjectName(_fromUtf8("lineEdit_SAB"))
        self.lineEdit_RN = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_RN.setGeometry(QtCore.QRect(120, 120, 113, 20))
        self.lineEdit_RN.setObjectName(_fromUtf8("lineEdit_RN"))
        self.label_21 = QtGui.QLabel(self.groupBox_2)
        self.label_21.setGeometry(QtCore.QRect(10, 200, 91, 21))
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.label_20 = QtGui.QLabel(self.groupBox_2)
        self.label_20.setGeometry(QtCore.QRect(10, 160, 91, 21))
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.lineEdit_SC = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_SC.setGeometry(QtCore.QRect(120, 220, 113, 20))
        self.lineEdit_SC.setObjectName(_fromUtf8("lineEdit_SC"))
        self.label_18 = QtGui.QLabel(self.groupBox_2)
        self.label_18.setGeometry(QtCore.QRect(10, 120, 101, 21))
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_24 = QtGui.QLabel(self.groupBox_2)
        self.label_24.setGeometry(QtCore.QRect(10, 260, 101, 21))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.lineEdit_PL = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_PL.setGeometry(QtCore.QRect(120, 160, 113, 20))
        self.lineEdit_PL.setObjectName(_fromUtf8("lineEdit_PL"))
        self.lineEdit_C = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_C.setGeometry(QtCore.QRect(120, 200, 113, 20))
        self.lineEdit_C.setObjectName(_fromUtf8("lineEdit_C"))
        self.lineEdit_EOL = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_EOL.setGeometry(QtCore.QRect(120, 260, 113, 20))
        self.lineEdit_EOL.setObjectName(_fromUtf8("lineEdit_EOL"))
        self.label_23 = QtGui.QLabel(self.groupBox_2)
        self.label_23.setGeometry(QtCore.QRect(10, 240, 101, 21))
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.label_17 = QtGui.QLabel(self.groupBox_2)
        self.label_17.setGeometry(QtCore.QRect(10, 140, 111, 21))
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.lineEdit_SS = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_SS.setGeometry(QtCore.QRect(120, 180, 113, 20))
        self.lineEdit_SS.setObjectName(_fromUtf8("lineEdit_SS"))
        self.label_22 = QtGui.QLabel(self.groupBox_2)
        self.label_22.setGeometry(QtCore.QRect(10, 220, 101, 21))
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_19 = QtGui.QLabel(self.groupBox_2)
        self.label_19.setGeometry(QtCore.QRect(10, 180, 91, 21))
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.lineEdit_NOP = QtGui.QLineEdit(self.groupBox_2)
        self.lineEdit_NOP.setGeometry(QtCore.QRect(120, 140, 113, 20))
        self.lineEdit_NOP.setObjectName(_fromUtf8("lineEdit_NOP"))
        self.comboBoxDistribs = QtGui.QComboBox(self.groupBox_2)
        self.comboBoxDistribs.setGeometry(QtCore.QRect(10, 30, 121, 22))
        self.comboBoxDistribs.setObjectName(_fromUtf8("comboBoxDistribs"))
        self.comboBoxDistribs.addItem(_fromUtf8(""))
        self.comboBoxDistribs.addItem(_fromUtf8(""))
        self.comboBoxDistribs.addItem(_fromUtf8(""))
        self.checkBox_useDistribs = QtGui.QCheckBox(self.groupBox_2)
        self.checkBox_useDistribs.setGeometry(QtCore.QRect(140, 30, 181, 17))
        self.checkBox_useDistribs.setObjectName(_fromUtf8("checkBox_useDistribs"))
        self.tabWidget.addTab(self.setTab, _fromUtf8(""))
        self.tab = QtGui.QWidget()

        self.tab.setObjectName(_fromUtf8("tab"))
        self.outputGraphs = pg.GraphicsView(self.tab)
        self.outputGraphs.setGeometry(QtCore.QRect(0, 10, 941, 491))
        self.outputGraphs.setObjectName(_fromUtf8("outputGraphs"))
        self.glayoutOutput = pg.GraphicsLayout(border=(200,200,200))
        self.outputGraphs.setCentralItem(self.glayoutOutput)
        self.outputGraphs.show()
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.monitorTab = QtGui.QWidget()

        self.monitorTab.setObjectName(_fromUtf8("monitorTab"))
        self.monitorGraphs =pg.GraphicsView(self.monitorTab)
        self.monitorGraphs.setGeometry(QtCore.QRect(10, 11, 921, 481))
        self.monitorGraphs.setObjectName(_fromUtf8("monitorGraphs"))
        self.glayoutMonitor = pg.GraphicsLayout(border=(200,200,200))
        self.monitorGraphs.setCentralItem(self.glayoutMonitor)
        self.monitorGraphs.show()
        self.tabWidget.addTab(self.monitorTab, _fromUtf8(""))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 963, 21))
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
        self.setVirtualMachine_Btn.setText(_translate("MainWindow", "Set Machine", None))
        self.runASTRA_Btn.setText(_translate("MainWindow", "Run Machine", None))
        self.groupBox.setTitle(_translate("MainWindow", "Machine Quantities", None))
        self.label.setText(_translate("MainWindow", "RF Gun Amplitude:", None))
        self.lineEdit_RFGA.setText(_translate("MainWindow", "1800", None))
        self.label_2.setText(_translate("MainWindow", "RF Gun Phase:", None))
        self.lineEdit_RFGP.setText(_translate("MainWindow", "0", None))
        self.label_3.setText(_translate("MainWindow", "QUAD-01 Current:", None))
        self.lineEdit_Q1C.setText(_translate("MainWindow", "0.228", None))
        self.label_4.setText(_translate("MainWindow", "QUAD-02 Current:", None))
        self.lineEdit_Q2C.setText(_translate("MainWindow", "-0.14", None))
        self.label_5.setText(_translate("MainWindow", "QUAD-03 Current:", None))
        self.lineEdit_Q3C.setText(_translate("MainWindow", "0.138", None))
        self.label_6.setText(_translate("MainWindow", "QUAD-04 Current:", None))
        self.lineEdit_Q4C.setText(_translate("MainWindow", "-0.230", None))
        self.label_7.setText(_translate("MainWindow", "QUAD-07 Current:", None))
        self.lineEdit_Q7C.setText(_translate("MainWindow", "0.012", None))
        self.label_8.setText(_translate("MainWindow", "QUAD-08 Current:", None))
        self.lineEdit_Q8C.setText(_translate("MainWindow", "0.011", None))
        self.label_9.setText(_translate("MainWindow", "QUAD-09 Current:", None))
        self.lineEdit_Q9C.setText(_translate("MainWindow", "0.031", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "ASTRA Specific Quantities", None))
        self.lineEdit_SAB.setText(_translate("MainWindow", "0.0", None))
        self.label_21.setText(_translate("MainWindow", "Charge (nC):", None))
        self.label_20.setText(_translate("MainWindow", "Pulse Length (ps):", None))
        self.lineEdit_SC.setText(_translate("MainWindow", "F", None))
        self.label_18.setText(_translate("MainWindow", "Run Number:", None))
        self.label_24.setText(_translate("MainWindow", "End of Line (cm):", None))
        self.lineEdit_PL.setText(_translate("MainWindow", "0.076", None))
        self.lineEdit_C.setText(_translate("MainWindow", "0.25", None))
        self.lineEdit_EOL.setText(_translate("MainWindow", "1320", None))
        self.label_23.setText(_translate("MainWindow", "SOL & BSOL  (T):", None))
        self.label_17.setText(_translate("MainWindow", "# of particles (1000s):", None))
        self.lineEdit_SS.setText(_translate("MainWindow", "0.25", None))
        self.label_22.setText(_translate("MainWindow", "Space Charge (T/F):", None))
        self.label_19.setText(_translate("MainWindow", "Spot Size:", None))
        self.lineEdit_NOP.setText(_translate("MainWindow", "1", None))
        self.comboBoxDistribs.setItemText(0, _translate("MainWindow", "Distrib 1", None))
        self.comboBoxDistribs.setItemText(1, _translate("MainWindow", "Distrib 2", None))
        self.comboBoxDistribs.setItemText(2, _translate("MainWindow", "Distrib 3", None))
        self.checkBox_useDistribs.setText(_translate("MainWindow", "Use A Pre-defined distribution", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.setTab), _translate("MainWindow", "Set Values", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.monitorTab), _translate("MainWindow", "Monitor Machine Values", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Output form ASTRA Run", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

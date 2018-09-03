# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view1_12.ui'
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
        MainWindow.resize(1669, 903)
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
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setMinimumSize(QtCore.QSize(0, 594))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.verticalLayout = QtGui.QVBoxLayout(self.tab)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox_run = QtGui.QGroupBox(self.tab)
        self.groupBox_run.setMinimumSize(QtCore.QSize(50, 0))
        self.groupBox_run.setMaximumSize(QtCore.QSize(10000, 16777215))
        self.groupBox_run.setObjectName(_fromUtf8("groupBox_run"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_run)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1)
        self.label_11 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 1, 1, 1)
        self.label_12 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 0, 2, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 3, 1, 1)
        self.label_4 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 4, 1, 1)
        self.label_5 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 0, 5, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 0, 6, 1, 1)
        self.label_7 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 0, 7, 1, 1)
        self.label_10 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 0, 8, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 0, 12, 1, 1)
        self.label_15 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout.addWidget(self.label_15, 0, 13, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_9.setFont(font)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 0, 14, 1, 1)
        self.label_16 = QtGui.QLabel(self.groupBox_run)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.gridLayout.addWidget(self.label_16, 0, 15, 1, 1)
        self.comboBox_1 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_1.setEditable(False)
        self.comboBox_1.setMaxVisibleItems(10)
        self.comboBox_1.setObjectName(_fromUtf8("comboBox_1"))
        self.comboBox_1.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_1, 1, 0, 1, 1)
        self.label_H_1 = QtGui.QLabel(self.groupBox_run)
        self.label_H_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_1.setObjectName(_fromUtf8("label_H_1"))
        self.gridLayout.addWidget(self.label_H_1, 1, 1, 1, 1)
        self.label_V_1 = QtGui.QLabel(self.groupBox_run)
        self.label_V_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_V_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_V_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_V_1.setObjectName(_fromUtf8("label_V_1"))
        self.gridLayout.addWidget(self.label_V_1, 1, 2, 1, 1)
        self.comboBox_H_1 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_H_1.setEditable(False)
        self.comboBox_H_1.setMaxVisibleItems(10)
        self.comboBox_H_1.setObjectName(_fromUtf8("comboBox_H_1"))
        self.comboBox_H_1.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_H_1, 1, 3, 1, 1)
        self.comboBox_V_1 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_V_1.setEditable(False)
        self.comboBox_V_1.setMaxVisibleItems(10)
        self.comboBox_V_1.setObjectName(_fromUtf8("comboBox_V_1"))
        self.comboBox_V_1.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_V_1, 1, 4, 1, 1)
        self.doubleSpinBox_x_1 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_x_1.setMinimum(-100.0)
        self.doubleSpinBox_x_1.setMaximum(100.0)
        self.doubleSpinBox_x_1.setSingleStep(0.1)
        self.doubleSpinBox_x_1.setObjectName(_fromUtf8("doubleSpinBox_x_1"))
        self.gridLayout.addWidget(self.doubleSpinBox_x_1, 1, 5, 1, 1)
        self.doubleSpinBox_y_1 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_y_1.setMinimum(-100.0)
        self.doubleSpinBox_y_1.setMaximum(100.0)
        self.doubleSpinBox_y_1.setSingleStep(0.1)
        self.doubleSpinBox_y_1.setObjectName(_fromUtf8("doubleSpinBox_y_1"))
        self.gridLayout.addWidget(self.doubleSpinBox_y_1, 1, 6, 1, 1)
        self.doubleSpinBox_tol_1 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_tol_1.setSingleStep(0.01)
        self.doubleSpinBox_tol_1.setProperty("value", 0.1)
        self.doubleSpinBox_tol_1.setObjectName(_fromUtf8("doubleSpinBox_tol_1"))
        self.gridLayout.addWidget(self.doubleSpinBox_tol_1, 1, 7, 1, 1)
        self.doubleSpinBox_step_1 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_step_1.setDecimals(3)
        self.doubleSpinBox_step_1.setSingleStep(0.1)
        self.doubleSpinBox_step_1.setProperty("value", 0.5)
        self.doubleSpinBox_step_1.setObjectName(_fromUtf8("doubleSpinBox_step_1"))
        self.gridLayout.addWidget(self.doubleSpinBox_step_1, 1, 8, 1, 1)
        self.pushButton_Align_x_1 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_x_1.setChecked(False)
        self.pushButton_Align_x_1.setObjectName(_fromUtf8("pushButton_Align_x_1"))
        self.gridLayout.addWidget(self.pushButton_Align_x_1, 1, 9, 1, 1)
        self.pushButton_Align_y_1 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_y_1.setChecked(False)
        self.pushButton_Align_y_1.setObjectName(_fromUtf8("pushButton_Align_y_1"))
        self.gridLayout.addWidget(self.pushButton_Align_y_1, 1, 10, 1, 1)
        self.pushButton_Align_both_1 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_both_1.setChecked(False)
        self.pushButton_Align_both_1.setObjectName(_fromUtf8("pushButton_Align_both_1"))
        self.gridLayout.addWidget(self.pushButton_Align_both_1, 1, 11, 1, 1)
        self.label_HC_1 = QtGui.QLabel(self.groupBox_run)
        self.label_HC_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_HC_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_HC_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_HC_1.setObjectName(_fromUtf8("label_HC_1"))
        self.gridLayout.addWidget(self.label_HC_1, 1, 12, 1, 1)
        self.lineEdit_HC_1 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_HC_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_HC_1.setSizePolicy(sizePolicy)
        self.lineEdit_HC_1.setObjectName(_fromUtf8("lineEdit_HC_1"))
        self.gridLayout.addWidget(self.lineEdit_HC_1, 1, 13, 1, 1)
        self.label_VC_1 = QtGui.QLabel(self.groupBox_run)
        self.label_VC_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_VC_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_VC_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_VC_1.setObjectName(_fromUtf8("label_VC_1"))
        self.gridLayout.addWidget(self.label_VC_1, 1, 14, 1, 1)
        self.lineEdit_VC_1 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VC_1.sizePolicy().hasHeightForWidth())
        self.lineEdit_VC_1.setSizePolicy(sizePolicy)
        self.lineEdit_VC_1.setObjectName(_fromUtf8("lineEdit_VC_1"))
        self.gridLayout.addWidget(self.lineEdit_VC_1, 1, 15, 1, 1)
        self.comboBox_2 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setMaxVisibleItems(10)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_2, 2, 0, 1, 1)
        self.label_H_2 = QtGui.QLabel(self.groupBox_run)
        self.label_H_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_2.setObjectName(_fromUtf8("label_H_2"))
        self.gridLayout.addWidget(self.label_H_2, 2, 1, 1, 1)
        self.label_V_2 = QtGui.QLabel(self.groupBox_run)
        self.label_V_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_V_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_V_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_V_2.setObjectName(_fromUtf8("label_V_2"))
        self.gridLayout.addWidget(self.label_V_2, 2, 2, 1, 1)
        self.comboBox_H_2 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_H_2.setEditable(False)
        self.comboBox_H_2.setMaxVisibleItems(10)
        self.comboBox_H_2.setObjectName(_fromUtf8("comboBox_H_2"))
        self.comboBox_H_2.addItem(_fromUtf8(""))
        self.comboBox_H_2.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_H_2, 2, 3, 1, 1)
        self.comboBox_V_2 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_V_2.setEditable(False)
        self.comboBox_V_2.setMaxVisibleItems(10)
        self.comboBox_V_2.setObjectName(_fromUtf8("comboBox_V_2"))
        self.comboBox_V_2.addItem(_fromUtf8(""))
        self.comboBox_V_2.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_V_2, 2, 4, 1, 1)
        self.doubleSpinBox_x_2 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_x_2.setMinimum(-100.0)
        self.doubleSpinBox_x_2.setMaximum(100.0)
        self.doubleSpinBox_x_2.setSingleStep(0.1)
        self.doubleSpinBox_x_2.setObjectName(_fromUtf8("doubleSpinBox_x_2"))
        self.gridLayout.addWidget(self.doubleSpinBox_x_2, 2, 5, 1, 1)
        self.doubleSpinBox_y_2 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_y_2.setMinimum(-100.0)
        self.doubleSpinBox_y_2.setMaximum(100.0)
        self.doubleSpinBox_y_2.setSingleStep(0.1)
        self.doubleSpinBox_y_2.setObjectName(_fromUtf8("doubleSpinBox_y_2"))
        self.gridLayout.addWidget(self.doubleSpinBox_y_2, 2, 6, 1, 1)
        self.doubleSpinBox_tol_2 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_tol_2.setSingleStep(0.01)
        self.doubleSpinBox_tol_2.setProperty("value", 0.1)
        self.doubleSpinBox_tol_2.setObjectName(_fromUtf8("doubleSpinBox_tol_2"))
        self.gridLayout.addWidget(self.doubleSpinBox_tol_2, 2, 7, 1, 1)
        self.doubleSpinBox_step_2 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_step_2.setDecimals(3)
        self.doubleSpinBox_step_2.setSingleStep(0.1)
        self.doubleSpinBox_step_2.setProperty("value", 0.5)
        self.doubleSpinBox_step_2.setObjectName(_fromUtf8("doubleSpinBox_step_2"))
        self.gridLayout.addWidget(self.doubleSpinBox_step_2, 2, 8, 1, 1)
        self.pushButton_Align_x_2 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_x_2.setChecked(False)
        self.pushButton_Align_x_2.setObjectName(_fromUtf8("pushButton_Align_x_2"))
        self.gridLayout.addWidget(self.pushButton_Align_x_2, 2, 9, 1, 1)
        self.pushButton_Align_y_2 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_y_2.setChecked(False)
        self.pushButton_Align_y_2.setObjectName(_fromUtf8("pushButton_Align_y_2"))
        self.gridLayout.addWidget(self.pushButton_Align_y_2, 2, 10, 1, 1)
        self.pushButton_Align_both_2 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_both_2.setChecked(False)
        self.pushButton_Align_both_2.setObjectName(_fromUtf8("pushButton_Align_both_2"))
        self.gridLayout.addWidget(self.pushButton_Align_both_2, 2, 11, 1, 1)
        self.label_HC_2 = QtGui.QLabel(self.groupBox_run)
        self.label_HC_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_HC_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_HC_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_HC_2.setObjectName(_fromUtf8("label_HC_2"))
        self.gridLayout.addWidget(self.label_HC_2, 2, 12, 1, 1)
        self.lineEdit_HC_2 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_HC_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_HC_2.setSizePolicy(sizePolicy)
        self.lineEdit_HC_2.setObjectName(_fromUtf8("lineEdit_HC_2"))
        self.gridLayout.addWidget(self.lineEdit_HC_2, 2, 13, 1, 1)
        self.label_VC_2 = QtGui.QLabel(self.groupBox_run)
        self.label_VC_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_VC_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_VC_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_VC_2.setObjectName(_fromUtf8("label_VC_2"))
        self.gridLayout.addWidget(self.label_VC_2, 2, 14, 1, 1)
        self.lineEdit_VC_2 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VC_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_VC_2.setSizePolicy(sizePolicy)
        self.lineEdit_VC_2.setObjectName(_fromUtf8("lineEdit_VC_2"))
        self.gridLayout.addWidget(self.lineEdit_VC_2, 2, 15, 1, 1)
        self.comboBox_3 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setMaxVisibleItems(10)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_3, 3, 0, 1, 1)
        self.label_H_3 = QtGui.QLabel(self.groupBox_run)
        self.label_H_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_3.setObjectName(_fromUtf8("label_H_3"))
        self.gridLayout.addWidget(self.label_H_3, 3, 1, 1, 1)
        self.label_V_3 = QtGui.QLabel(self.groupBox_run)
        self.label_V_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_V_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_V_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_V_3.setObjectName(_fromUtf8("label_V_3"))
        self.gridLayout.addWidget(self.label_V_3, 3, 2, 1, 1)
        self.comboBox_H_3 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_H_3.setEditable(False)
        self.comboBox_H_3.setMaxVisibleItems(10)
        self.comboBox_H_3.setObjectName(_fromUtf8("comboBox_H_3"))
        self.comboBox_H_3.addItem(_fromUtf8(""))
        self.comboBox_H_3.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_H_3, 3, 3, 1, 1)
        self.comboBox_V_3 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_V_3.setEditable(False)
        self.comboBox_V_3.setMaxVisibleItems(10)
        self.comboBox_V_3.setObjectName(_fromUtf8("comboBox_V_3"))
        self.comboBox_V_3.addItem(_fromUtf8(""))
        self.comboBox_V_3.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_V_3, 3, 4, 1, 1)
        self.doubleSpinBox_x_3 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_x_3.setMinimum(-100.0)
        self.doubleSpinBox_x_3.setMaximum(100.0)
        self.doubleSpinBox_x_3.setSingleStep(0.1)
        self.doubleSpinBox_x_3.setObjectName(_fromUtf8("doubleSpinBox_x_3"))
        self.gridLayout.addWidget(self.doubleSpinBox_x_3, 3, 5, 1, 1)
        self.doubleSpinBox_y_3 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_y_3.setMinimum(-100.0)
        self.doubleSpinBox_y_3.setMaximum(100.0)
        self.doubleSpinBox_y_3.setSingleStep(0.1)
        self.doubleSpinBox_y_3.setObjectName(_fromUtf8("doubleSpinBox_y_3"))
        self.gridLayout.addWidget(self.doubleSpinBox_y_3, 3, 6, 1, 1)
        self.doubleSpinBox_tol_3 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_tol_3.setSingleStep(0.01)
        self.doubleSpinBox_tol_3.setProperty("value", 0.1)
        self.doubleSpinBox_tol_3.setObjectName(_fromUtf8("doubleSpinBox_tol_3"))
        self.gridLayout.addWidget(self.doubleSpinBox_tol_3, 3, 7, 1, 1)
        self.doubleSpinBox_step_3 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_step_3.setDecimals(3)
        self.doubleSpinBox_step_3.setSingleStep(0.1)
        self.doubleSpinBox_step_3.setProperty("value", 0.5)
        self.doubleSpinBox_step_3.setObjectName(_fromUtf8("doubleSpinBox_step_3"))
        self.gridLayout.addWidget(self.doubleSpinBox_step_3, 3, 8, 1, 1)
        self.pushButton_Align_x_3 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_x_3.setChecked(False)
        self.pushButton_Align_x_3.setObjectName(_fromUtf8("pushButton_Align_x_3"))
        self.gridLayout.addWidget(self.pushButton_Align_x_3, 3, 9, 1, 1)
        self.pushButton_Align_y_3 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_y_3.setChecked(False)
        self.pushButton_Align_y_3.setObjectName(_fromUtf8("pushButton_Align_y_3"))
        self.gridLayout.addWidget(self.pushButton_Align_y_3, 3, 10, 1, 1)
        self.pushButton_Align_both_3 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_both_3.setChecked(False)
        self.pushButton_Align_both_3.setObjectName(_fromUtf8("pushButton_Align_both_3"))
        self.gridLayout.addWidget(self.pushButton_Align_both_3, 3, 11, 1, 1)
        self.label_HC_3 = QtGui.QLabel(self.groupBox_run)
        self.label_HC_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_HC_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_HC_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_HC_3.setObjectName(_fromUtf8("label_HC_3"))
        self.gridLayout.addWidget(self.label_HC_3, 3, 12, 1, 1)
        self.lineEdit_HC_3 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_HC_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_HC_3.setSizePolicy(sizePolicy)
        self.lineEdit_HC_3.setObjectName(_fromUtf8("lineEdit_HC_3"))
        self.gridLayout.addWidget(self.lineEdit_HC_3, 3, 13, 1, 1)
        self.label_VC_3 = QtGui.QLabel(self.groupBox_run)
        self.label_VC_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_VC_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_VC_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_VC_3.setObjectName(_fromUtf8("label_VC_3"))
        self.gridLayout.addWidget(self.label_VC_3, 3, 14, 1, 1)
        self.lineEdit_VC_3 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VC_3.sizePolicy().hasHeightForWidth())
        self.lineEdit_VC_3.setSizePolicy(sizePolicy)
        self.lineEdit_VC_3.setObjectName(_fromUtf8("lineEdit_VC_3"))
        self.gridLayout.addWidget(self.lineEdit_VC_3, 3, 15, 1, 1)
        self.comboBox_4 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_4.setEditable(False)
        self.comboBox_4.setMaxVisibleItems(10)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_4, 4, 0, 1, 1)
        self.label_H_4 = QtGui.QLabel(self.groupBox_run)
        self.label_H_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_4.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_4.setObjectName(_fromUtf8("label_H_4"))
        self.gridLayout.addWidget(self.label_H_4, 4, 1, 1, 1)
        self.label_V_4 = QtGui.QLabel(self.groupBox_run)
        self.label_V_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_V_4.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_V_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_V_4.setObjectName(_fromUtf8("label_V_4"))
        self.gridLayout.addWidget(self.label_V_4, 4, 2, 1, 1)
        self.comboBox_H_4 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_H_4.setEditable(False)
        self.comboBox_H_4.setMaxVisibleItems(10)
        self.comboBox_H_4.setObjectName(_fromUtf8("comboBox_H_4"))
        self.comboBox_H_4.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_H_4, 4, 3, 1, 1)
        self.comboBox_V_4 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_V_4.setEditable(False)
        self.comboBox_V_4.setMaxVisibleItems(10)
        self.comboBox_V_4.setObjectName(_fromUtf8("comboBox_V_4"))
        self.comboBox_V_4.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_V_4, 4, 4, 1, 1)
        self.doubleSpinBox_x_4 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_x_4.setMinimum(-100.0)
        self.doubleSpinBox_x_4.setMaximum(100.0)
        self.doubleSpinBox_x_4.setSingleStep(0.1)
        self.doubleSpinBox_x_4.setObjectName(_fromUtf8("doubleSpinBox_x_4"))
        self.gridLayout.addWidget(self.doubleSpinBox_x_4, 4, 5, 1, 1)
        self.doubleSpinBox_y_4 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_y_4.setMinimum(-100.0)
        self.doubleSpinBox_y_4.setMaximum(100.0)
        self.doubleSpinBox_y_4.setSingleStep(0.1)
        self.doubleSpinBox_y_4.setObjectName(_fromUtf8("doubleSpinBox_y_4"))
        self.gridLayout.addWidget(self.doubleSpinBox_y_4, 4, 6, 1, 1)
        self.doubleSpinBox_tol_4 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_tol_4.setSingleStep(0.01)
        self.doubleSpinBox_tol_4.setProperty("value", 0.1)
        self.doubleSpinBox_tol_4.setObjectName(_fromUtf8("doubleSpinBox_tol_4"))
        self.gridLayout.addWidget(self.doubleSpinBox_tol_4, 4, 7, 1, 1)
        self.doubleSpinBox_step_4 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_step_4.setDecimals(3)
        self.doubleSpinBox_step_4.setSingleStep(0.1)
        self.doubleSpinBox_step_4.setProperty("value", 0.5)
        self.doubleSpinBox_step_4.setObjectName(_fromUtf8("doubleSpinBox_step_4"))
        self.gridLayout.addWidget(self.doubleSpinBox_step_4, 4, 8, 1, 1)
        self.pushButton_Align_x_4 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_x_4.setChecked(False)
        self.pushButton_Align_x_4.setObjectName(_fromUtf8("pushButton_Align_x_4"))
        self.gridLayout.addWidget(self.pushButton_Align_x_4, 4, 9, 1, 1)
        self.pushButton_Align_y_4 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_y_4.setChecked(False)
        self.pushButton_Align_y_4.setObjectName(_fromUtf8("pushButton_Align_y_4"))
        self.gridLayout.addWidget(self.pushButton_Align_y_4, 4, 10, 1, 1)
        self.pushButton_Align_both_4 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_both_4.setChecked(False)
        self.pushButton_Align_both_4.setObjectName(_fromUtf8("pushButton_Align_both_4"))
        self.gridLayout.addWidget(self.pushButton_Align_both_4, 4, 11, 1, 1)
        self.label_HC_4 = QtGui.QLabel(self.groupBox_run)
        self.label_HC_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_HC_4.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_HC_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_HC_4.setObjectName(_fromUtf8("label_HC_4"))
        self.gridLayout.addWidget(self.label_HC_4, 4, 12, 1, 1)
        self.lineEdit_HC_4 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_HC_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_HC_4.setSizePolicy(sizePolicy)
        self.lineEdit_HC_4.setObjectName(_fromUtf8("lineEdit_HC_4"))
        self.gridLayout.addWidget(self.lineEdit_HC_4, 4, 13, 1, 1)
        self.label_VC_4 = QtGui.QLabel(self.groupBox_run)
        self.label_VC_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_VC_4.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_VC_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_VC_4.setObjectName(_fromUtf8("label_VC_4"))
        self.gridLayout.addWidget(self.label_VC_4, 4, 14, 1, 1)
        self.lineEdit_VC_4 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VC_4.sizePolicy().hasHeightForWidth())
        self.lineEdit_VC_4.setSizePolicy(sizePolicy)
        self.lineEdit_VC_4.setObjectName(_fromUtf8("lineEdit_VC_4"))
        self.gridLayout.addWidget(self.lineEdit_VC_4, 4, 15, 1, 1)
        self.comboBox_5 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_5.setEditable(False)
        self.comboBox_5.setMaxVisibleItems(10)
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_5, 5, 0, 1, 1)
        self.label_H_5 = QtGui.QLabel(self.groupBox_run)
        self.label_H_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_5.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_5.setObjectName(_fromUtf8("label_H_5"))
        self.gridLayout.addWidget(self.label_H_5, 5, 1, 1, 1)
        self.label_V_5 = QtGui.QLabel(self.groupBox_run)
        self.label_V_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_V_5.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_V_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_V_5.setObjectName(_fromUtf8("label_V_5"))
        self.gridLayout.addWidget(self.label_V_5, 5, 2, 1, 1)
        self.comboBox_H_5 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_H_5.setEditable(False)
        self.comboBox_H_5.setMaxVisibleItems(10)
        self.comboBox_H_5.setObjectName(_fromUtf8("comboBox_H_5"))
        self.comboBox_H_5.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_H_5, 5, 3, 1, 1)
        self.comboBox_V_5 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_V_5.setEditable(False)
        self.comboBox_V_5.setMaxVisibleItems(10)
        self.comboBox_V_5.setObjectName(_fromUtf8("comboBox_V_5"))
        self.comboBox_V_5.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_V_5, 5, 4, 1, 1)
        self.doubleSpinBox_x_5 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_x_5.setMinimum(-100.0)
        self.doubleSpinBox_x_5.setMaximum(100.0)
        self.doubleSpinBox_x_5.setSingleStep(0.1)
        self.doubleSpinBox_x_5.setObjectName(_fromUtf8("doubleSpinBox_x_5"))
        self.gridLayout.addWidget(self.doubleSpinBox_x_5, 5, 5, 1, 1)
        self.doubleSpinBox_y_5 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_y_5.setMinimum(-100.0)
        self.doubleSpinBox_y_5.setMaximum(100.0)
        self.doubleSpinBox_y_5.setSingleStep(0.1)
        self.doubleSpinBox_y_5.setObjectName(_fromUtf8("doubleSpinBox_y_5"))
        self.gridLayout.addWidget(self.doubleSpinBox_y_5, 5, 6, 1, 1)
        self.doubleSpinBox_tol_5 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_tol_5.setSingleStep(0.01)
        self.doubleSpinBox_tol_5.setProperty("value", 0.1)
        self.doubleSpinBox_tol_5.setObjectName(_fromUtf8("doubleSpinBox_tol_5"))
        self.gridLayout.addWidget(self.doubleSpinBox_tol_5, 5, 7, 1, 1)
        self.doubleSpinBox_step_5 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_step_5.setDecimals(3)
        self.doubleSpinBox_step_5.setSingleStep(0.1)
        self.doubleSpinBox_step_5.setProperty("value", 0.5)
        self.doubleSpinBox_step_5.setObjectName(_fromUtf8("doubleSpinBox_step_5"))
        self.gridLayout.addWidget(self.doubleSpinBox_step_5, 5, 8, 1, 1)
        self.pushButton_Align_x_5 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_x_5.setChecked(False)
        self.pushButton_Align_x_5.setObjectName(_fromUtf8("pushButton_Align_x_5"))
        self.gridLayout.addWidget(self.pushButton_Align_x_5, 5, 9, 1, 1)
        self.pushButton_Align_y_5 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_y_5.setChecked(False)
        self.pushButton_Align_y_5.setObjectName(_fromUtf8("pushButton_Align_y_5"))
        self.gridLayout.addWidget(self.pushButton_Align_y_5, 5, 10, 1, 1)
        self.pushButton_Align_both_5 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_both_5.setChecked(False)
        self.pushButton_Align_both_5.setObjectName(_fromUtf8("pushButton_Align_both_5"))
        self.gridLayout.addWidget(self.pushButton_Align_both_5, 5, 11, 1, 1)
        self.label_HC_5 = QtGui.QLabel(self.groupBox_run)
        self.label_HC_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_HC_5.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_HC_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_HC_5.setObjectName(_fromUtf8("label_HC_5"))
        self.gridLayout.addWidget(self.label_HC_5, 5, 12, 1, 1)
        self.lineEdit_HC_5 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_HC_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_HC_5.setSizePolicy(sizePolicy)
        self.lineEdit_HC_5.setObjectName(_fromUtf8("lineEdit_HC_5"))
        self.gridLayout.addWidget(self.lineEdit_HC_5, 5, 13, 1, 1)
        self.label_VC_5 = QtGui.QLabel(self.groupBox_run)
        self.label_VC_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_VC_5.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_VC_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_VC_5.setObjectName(_fromUtf8("label_VC_5"))
        self.gridLayout.addWidget(self.label_VC_5, 5, 14, 1, 1)
        self.lineEdit_VC_5 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VC_5.sizePolicy().hasHeightForWidth())
        self.lineEdit_VC_5.setSizePolicy(sizePolicy)
        self.lineEdit_VC_5.setObjectName(_fromUtf8("lineEdit_VC_5"))
        self.gridLayout.addWidget(self.lineEdit_VC_5, 5, 15, 1, 1)
        self.comboBox_6 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_6.setEditable(False)
        self.comboBox_6.setMaxVisibleItems(10)
        self.comboBox_6.setObjectName(_fromUtf8("comboBox_6"))
        self.comboBox_6.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_6, 6, 0, 1, 1)
        self.label_H_6 = QtGui.QLabel(self.groupBox_run)
        self.label_H_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_6.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_6.setObjectName(_fromUtf8("label_H_6"))
        self.gridLayout.addWidget(self.label_H_6, 6, 1, 1, 1)
        self.label_V_6 = QtGui.QLabel(self.groupBox_run)
        self.label_V_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_V_6.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_V_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_V_6.setObjectName(_fromUtf8("label_V_6"))
        self.gridLayout.addWidget(self.label_V_6, 6, 2, 1, 1)
        self.comboBox_H_6 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_H_6.setEditable(False)
        self.comboBox_H_6.setMaxVisibleItems(10)
        self.comboBox_H_6.setObjectName(_fromUtf8("comboBox_H_6"))
        self.comboBox_H_6.addItem(_fromUtf8(""))
        self.comboBox_H_6.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_H_6, 6, 3, 1, 1)
        self.comboBox_V_6 = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_V_6.setEditable(False)
        self.comboBox_V_6.setMaxVisibleItems(10)
        self.comboBox_V_6.setObjectName(_fromUtf8("comboBox_V_6"))
        self.comboBox_V_6.addItem(_fromUtf8(""))
        self.comboBox_V_6.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.comboBox_V_6, 6, 4, 1, 1)
        self.doubleSpinBox_x_6 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_x_6.setMinimum(-100.0)
        self.doubleSpinBox_x_6.setMaximum(100.0)
        self.doubleSpinBox_x_6.setSingleStep(0.1)
        self.doubleSpinBox_x_6.setObjectName(_fromUtf8("doubleSpinBox_x_6"))
        self.gridLayout.addWidget(self.doubleSpinBox_x_6, 6, 5, 1, 1)
        self.doubleSpinBox_y_6 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_y_6.setMinimum(-100.0)
        self.doubleSpinBox_y_6.setMaximum(100.0)
        self.doubleSpinBox_y_6.setSingleStep(0.1)
        self.doubleSpinBox_y_6.setObjectName(_fromUtf8("doubleSpinBox_y_6"))
        self.gridLayout.addWidget(self.doubleSpinBox_y_6, 6, 6, 1, 1)
        self.doubleSpinBox_tol_6 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_tol_6.setSingleStep(0.01)
        self.doubleSpinBox_tol_6.setProperty("value", 0.1)
        self.doubleSpinBox_tol_6.setObjectName(_fromUtf8("doubleSpinBox_tol_6"))
        self.gridLayout.addWidget(self.doubleSpinBox_tol_6, 6, 7, 1, 1)
        self.doubleSpinBox_step_6 = QtGui.QDoubleSpinBox(self.groupBox_run)
        self.doubleSpinBox_step_6.setDecimals(3)
        self.doubleSpinBox_step_6.setSingleStep(0.1)
        self.doubleSpinBox_step_6.setProperty("value", 0.5)
        self.doubleSpinBox_step_6.setObjectName(_fromUtf8("doubleSpinBox_step_6"))
        self.gridLayout.addWidget(self.doubleSpinBox_step_6, 6, 8, 1, 1)
        self.pushButton_Align_x_6 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_x_6.setChecked(False)
        self.pushButton_Align_x_6.setObjectName(_fromUtf8("pushButton_Align_x_6"))
        self.gridLayout.addWidget(self.pushButton_Align_x_6, 6, 9, 1, 1)
        self.pushButton_Align_y_6 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_y_6.setChecked(False)
        self.pushButton_Align_y_6.setObjectName(_fromUtf8("pushButton_Align_y_6"))
        self.gridLayout.addWidget(self.pushButton_Align_y_6, 6, 10, 1, 1)
        self.pushButton_Align_both_6 = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_Align_both_6.setChecked(False)
        self.pushButton_Align_both_6.setObjectName(_fromUtf8("pushButton_Align_both_6"))
        self.gridLayout.addWidget(self.pushButton_Align_both_6, 6, 11, 1, 1)
        self.label_HC_6 = QtGui.QLabel(self.groupBox_run)
        self.label_HC_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_HC_6.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_HC_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_HC_6.setObjectName(_fromUtf8("label_HC_6"))
        self.gridLayout.addWidget(self.label_HC_6, 6, 12, 1, 1)
        self.lineEdit_HC_6 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_HC_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_HC_6.setSizePolicy(sizePolicy)
        self.lineEdit_HC_6.setObjectName(_fromUtf8("lineEdit_HC_6"))
        self.gridLayout.addWidget(self.lineEdit_HC_6, 6, 13, 1, 1)
        self.label_VC_6 = QtGui.QLabel(self.groupBox_run)
        self.label_VC_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_VC_6.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_VC_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_VC_6.setObjectName(_fromUtf8("label_VC_6"))
        self.gridLayout.addWidget(self.label_VC_6, 6, 14, 1, 1)
        self.lineEdit_VC_6 = QtGui.QLineEdit(self.groupBox_run)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_VC_6.sizePolicy().hasHeightForWidth())
        self.lineEdit_VC_6.setSizePolicy(sizePolicy)
        self.lineEdit_VC_6.setObjectName(_fromUtf8("lineEdit_VC_6"))
        self.gridLayout.addWidget(self.lineEdit_VC_6, 6, 15, 1, 1)
        self.label = QtGui.QLabel(self.groupBox_run)
        self.label.setText(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 7, 7, 1, 1)
        self.pushButton_set = QtGui.QPushButton(self.groupBox_run)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_set.setFont(font)
        self.pushButton_set.setStyleSheet(_fromUtf8("QPushButton{ background-color: rgb(0, 0, 0);}"))
        self.pushButton_set.setObjectName(_fromUtf8("pushButton_set"))
        self.gridLayout.addWidget(self.pushButton_set, 8, 8, 1, 2)
        self.pushButton_set_0 = QtGui.QPushButton(self.groupBox_run)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_set_0.setFont(font)
        self.pushButton_set_0.setStyleSheet(_fromUtf8("QPushButton{ background-color: rgb(0, 0, 0);}"))
        self.pushButton_set_0.setObjectName(_fromUtf8("pushButton_set_0"))
        self.gridLayout.addWidget(self.pushButton_set_0, 8, 10, 1, 2)
        self.pushButton_save_2 = QtGui.QPushButton(self.groupBox_run)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_save_2.setFont(font)
        self.pushButton_save_2.setStyleSheet(_fromUtf8("QPushButton{ background-color: rgb(0, 0, 0);}"))
        self.pushButton_save_2.setObjectName(_fromUtf8("pushButton_save_2"))
        self.gridLayout.addWidget(self.pushButton_save_2, 8, 12, 1, 2)
        self.pushButton_load = QtGui.QPushButton(self.groupBox_run)
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_load.setFont(font)
        self.pushButton_load.setStyleSheet(_fromUtf8("QPushButton{ background-color: rgb(0, 0, 0);}"))
        self.pushButton_load.setObjectName(_fromUtf8("pushButton_load"))
        self.gridLayout.addWidget(self.pushButton_load, 8, 14, 1, 2)
        self.verticalLayout.addWidget(self.groupBox_run)
        self.groupBox_monitor = QtGui.QGroupBox(self.tab)
        self.groupBox_monitor.setMinimumSize(QtCore.QSize(600, 0))
        self.groupBox_monitor.setObjectName(_fromUtf8("groupBox_monitor"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_monitor)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.verticalLayout.addWidget(self.groupBox_monitor)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tabLog = QtGui.QWidget()
        self.tabLog.setObjectName(_fromUtf8("tabLog"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout(self.tabLog)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.horizontalLayout_6.addLayout(self.gridLayout_3)
        self.tabWidget.addTab(self.tabLog, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1669, 26))
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
        self.label_2.setText(_translate("MainWindow", "BPM", None))
        self.label_11.setText(_translate("MainWindow", "H readout", None))
        self.label_12.setText(_translate("MainWindow", "V readout", None))
        self.label_3.setText(_translate("MainWindow", "H corrector", None))
        self.label_4.setText(_translate("MainWindow", "V corrector", None))
        self.label_5.setText(_translate("MainWindow", "H target", None))
        self.label_6.setText(_translate("MainWindow", "V target", None))
        self.label_7.setText(_translate("MainWindow", "Tolerance", None))
        self.label_10.setText(_translate("MainWindow", "Initial step [A]", None))
        self.label_8.setText(_translate("MainWindow", "HCOR [A]", None))
        self.label_15.setText(_translate("MainWindow", "Set HCOR", None))
        self.label_9.setText(_translate("MainWindow", "VCOR [A]", None))
        self.label_16.setText(_translate("MainWindow", "Set VCOR", None))
        self.comboBox_1.setItemText(0, _translate("MainWindow", "S01-BPM01", None))
        self.label_H_1.setText(_translate("MainWindow", "TextLabel", None))
        self.label_V_1.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_H_1.setItemText(0, _translate("MainWindow", "S01-HCOR1", None))
        self.comboBox_V_1.setItemText(0, _translate("MainWindow", "S01-VCOR1", None))
        self.pushButton_Align_x_1.setText(_translate("MainWindow", "Align x", None))
        self.pushButton_Align_y_1.setText(_translate("MainWindow", "Align y", None))
        self.pushButton_Align_both_1.setText(_translate("MainWindow", "Align both", None))
        self.label_HC_1.setText(_translate("MainWindow", "TextLabel", None))
        self.label_VC_1.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "S02-BPM01", None))
        self.label_H_2.setText(_translate("MainWindow", "TextLabel", None))
        self.label_V_2.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_H_2.setItemText(0, _translate("MainWindow", "S01-HCOR2", None))
        self.comboBox_H_2.setItemText(1, _translate("MainWindow", "S01-HC0R1", None))
        self.comboBox_V_2.setItemText(0, _translate("MainWindow", "S01-VCOR2", None))
        self.comboBox_V_2.setItemText(1, _translate("MainWindow", "S01-VCOR1", None))
        self.pushButton_Align_x_2.setText(_translate("MainWindow", "Align x", None))
        self.pushButton_Align_y_2.setText(_translate("MainWindow", "Align y", None))
        self.pushButton_Align_both_2.setText(_translate("MainWindow", "Align both", None))
        self.label_HC_2.setText(_translate("MainWindow", "TextLabel", None))
        self.label_VC_2.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "S02-BPM02", None))
        self.label_H_3.setText(_translate("MainWindow", "TextLabel", None))
        self.label_V_3.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_H_3.setItemText(0, _translate("MainWindow", "S02-HCOR2", None))
        self.comboBox_H_3.setItemText(1, _translate("MainWindow", "S02-HCOR1", None))
        self.comboBox_V_3.setItemText(0, _translate("MainWindow", "S02-VCOR2", None))
        self.comboBox_V_3.setItemText(1, _translate("MainWindow", "S02-VCOR1", None))
        self.pushButton_Align_x_3.setText(_translate("MainWindow", "Align x", None))
        self.pushButton_Align_y_3.setText(_translate("MainWindow", "Align y", None))
        self.pushButton_Align_both_3.setText(_translate("MainWindow", "Align both", None))
        self.label_HC_3.setText(_translate("MainWindow", "TextLabel", None))
        self.label_VC_3.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "C2V-BPM01", None))
        self.label_H_4.setText(_translate("MainWindow", "TextLabel", None))
        self.label_V_4.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_H_4.setItemText(0, _translate("MainWindow", "S02-DIP01", None))
        self.comboBox_V_4.setItemText(0, _translate("MainWindow", "S02-VCOR2", None))
        self.pushButton_Align_x_4.setText(_translate("MainWindow", "Align x", None))
        self.pushButton_Align_y_4.setText(_translate("MainWindow", "Align y", None))
        self.pushButton_Align_both_4.setText(_translate("MainWindow", "Align both", None))
        self.label_HC_4.setText(_translate("MainWindow", "TextLabel", None))
        self.label_VC_4.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "INJ-BPM04", None))
        self.label_H_5.setText(_translate("MainWindow", "TextLabel", None))
        self.label_V_5.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_H_5.setItemText(0, _translate("MainWindow", "INJ-HCOR06", None))
        self.comboBox_V_5.setItemText(0, _translate("MainWindow", "INJ-VCOR06", None))
        self.pushButton_Align_x_5.setText(_translate("MainWindow", "Align x", None))
        self.pushButton_Align_y_5.setText(_translate("MainWindow", "Align y", None))
        self.pushButton_Align_both_5.setText(_translate("MainWindow", "Align both", None))
        self.label_HC_5.setText(_translate("MainWindow", "TextLabel", None))
        self.label_VC_5.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "INJ-BPM05", None))
        self.label_H_6.setText(_translate("MainWindow", "TextLabel", None))
        self.label_V_6.setText(_translate("MainWindow", "TextLabel", None))
        self.comboBox_H_6.setItemText(0, _translate("MainWindow", "INJ-HCOR08", None))
        self.comboBox_H_6.setItemText(1, _translate("MainWindow", "INJ-HCOR07", None))
        self.comboBox_V_6.setItemText(0, _translate("MainWindow", "INJ-VCOR08", None))
        self.comboBox_V_6.setItemText(1, _translate("MainWindow", "INJ-VCOR07", None))
        self.pushButton_Align_x_6.setText(_translate("MainWindow", "Align x", None))
        self.pushButton_Align_y_6.setText(_translate("MainWindow", "Align y", None))
        self.pushButton_Align_both_6.setText(_translate("MainWindow", "Align both", None))
        self.label_HC_6.setText(_translate("MainWindow", "TextLabel", None))
        self.label_VC_6.setText(_translate("MainWindow", "TextLabel", None))
        self.pushButton_set.setText(_translate("MainWindow", "Set targets to present positions", None))
        self.pushButton_set_0.setText(_translate("MainWindow", "Set targets to zero", None))
        self.pushButton_save_2.setText(_translate("MainWindow", "Save positions", None))
        self.pushButton_load.setText(_translate("MainWindow", "Load saved positions as targets", None))
        self.groupBox_monitor.setTitle(_translate("MainWindow", "Monitor", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Aligment", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tabLog), _translate("MainWindow", "Log", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


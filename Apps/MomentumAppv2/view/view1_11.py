# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view1_11.ui'
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
        MainWindow.resize(1413, 946)
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
        self.gridLayout_5 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox_run = QtGui.QGroupBox(self.tab)
        self.groupBox_run.setMinimumSize(QtCore.QSize(680, 0))
        self.groupBox_run.setMaximumSize(QtCore.QSize(700, 16777215))
        self.groupBox_run.setObjectName(_fromUtf8("groupBox_run"))
        self.groupBox = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox.setGeometry(QtCore.QRect(10, 50, 661, 91))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(105, 0, 0);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}"))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(190, 20, 85, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(330, 20, 71, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.pushButton_useCurrent = QtGui.QPushButton(self.groupBox)
        self.pushButton_useCurrent.setGeometry(QtCore.QRect(30, 40, 141, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_useCurrent.sizePolicy().hasHeightForWidth())
        self.pushButton_useCurrent.setSizePolicy(sizePolicy)
        self.pushButton_useCurrent.setMinimumSize(QtCore.QSize(140, 22))
        self.pushButton_useCurrent.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_useCurrent.setChecked(False)
        self.pushButton_useCurrent.setObjectName(_fromUtf8("pushButton_useCurrent"))
        self.pushButton_useRF = QtGui.QPushButton(self.groupBox)
        self.pushButton_useRF.setEnabled(False)
        self.pushButton_useRF.setGeometry(QtCore.QRect(430, 40, 172, 22))
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
        self.label_I = QtGui.QLabel(self.groupBox)
        self.label_I.setGeometry(QtCore.QRect(30, 60, 251, 16))
        self.label_I.setMinimumSize(QtCore.QSize(120, 0))
        self.label_I.setObjectName(_fromUtf8("label_I"))
        self.label_RF = QtGui.QLabel(self.groupBox)
        self.label_RF.setEnabled(False)
        self.label_RF.setGeometry(QtCore.QRect(430, 60, 211, 20))
        self.label_RF.setMinimumSize(QtCore.QSize(120, 0))
        self.label_RF.setObjectName(_fromUtf8("label_RF"))
        self.doubleSpinBox_I = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_I.setGeometry(QtCore.QRect(180, 40, 111, 22))
        self.doubleSpinBox_I.setObjectName(_fromUtf8("doubleSpinBox_I"))
        self.doubleSpinBox_p = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_p.setGeometry(QtCore.QRect(310, 40, 111, 22))
        self.doubleSpinBox_p.setObjectName(_fromUtf8("doubleSpinBox_p"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(50, 20, 85, 16))
        self.label_6.setText(_fromUtf8(""))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(440, 20, 85, 16))
        self.label_7.setText(_fromUtf8(""))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.groupBox_9 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_9.setGeometry(QtCore.QRect(10, 300, 661, 521))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_9.setFont(font)
        self.groupBox_9.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(0, 0, 75);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_9.setObjectName(_fromUtf8("groupBox_9"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_9)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 20, 641, 91))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
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
        self.gridLayout.addWidget(self.pushButton_Prelim_3, 1, 0, 1, 1)
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
        self.gridLayout.addWidget(self.pushButton_Prelim_1, 0, 0, 1, 1)
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_9)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 120, 641, 201))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.pushButton_Align_1 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_1.setGeometry(QtCore.QRect(10, 28, 251, 22))
        self.pushButton_Align_1.setChecked(False)
        self.pushButton_Align_1.setObjectName(_fromUtf8("pushButton_Align_1"))
        self.pushButton_Align_4 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_4.setGeometry(QtCore.QRect(12, 145, 251, 21))
        self.pushButton_Align_4.setChecked(False)
        self.pushButton_Align_4.setObjectName(_fromUtf8("pushButton_Align_4"))
        self.pushButton_Align_2 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_2.setGeometry(QtCore.QRect(12, 70, 251, 22))
        self.pushButton_Align_2.setChecked(False)
        self.pushButton_Align_2.setObjectName(_fromUtf8("pushButton_Align_2"))
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(40, 173, 201, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.pushButton_Align_3 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_3.setGeometry(QtCore.QRect(10, 116, 251, 22))
        self.pushButton_Align_3.setChecked(False)
        self.pushButton_Align_3.setObjectName(_fromUtf8("pushButton_Align_3"))
        self.pushButton_Align_2_A = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_2_A.setGeometry(QtCore.QRect(270, 57, 171, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Align_2_A.sizePolicy().hasHeightForWidth())
        self.pushButton_Align_2_A.setSizePolicy(sizePolicy)
        self.pushButton_Align_2_A.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Align_2_A.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Align_2_A.setChecked(False)
        self.pushButton_Align_2_A.setObjectName(_fromUtf8("pushButton_Align_2_A"))
        self.pushButton_Align_2_B = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_2_B.setGeometry(QtCore.QRect(270, 87, 171, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Align_2_B.sizePolicy().hasHeightForWidth())
        self.pushButton_Align_2_B.setSizePolicy(sizePolicy)
        self.pushButton_Align_2_B.setMinimumSize(QtCore.QSize(0, 0))
        self.pushButton_Align_2_B.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Align_2_B.setChecked(False)
        self.pushButton_Align_2_B.setObjectName(_fromUtf8("pushButton_Align_2_B"))
        self.doubleSpinBox_x_1 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_x_1.setGeometry(QtCore.QRect(340, 30, 61, 20))
        self.doubleSpinBox_x_1.setMinimum(-100.0)
        self.doubleSpinBox_x_1.setMaximum(100.0)
        self.doubleSpinBox_x_1.setSingleStep(0.1)
        self.doubleSpinBox_x_1.setObjectName(_fromUtf8("doubleSpinBox_x_1"))
        self.label_12 = QtGui.QLabel(self.groupBox_4)
        self.label_12.setGeometry(QtCore.QRect(410, 30, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_12.setFont(font)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.label_13 = QtGui.QLabel(self.groupBox_4)
        self.label_13.setGeometry(QtCore.QRect(270, 30, 61, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_13.setFont(font)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.doubleSpinBox_tol_1 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_tol_1.setGeometry(QtCore.QRect(440, 30, 51, 20))
        self.doubleSpinBox_tol_1.setSingleStep(0.1)
        self.doubleSpinBox_tol_1.setProperty("value", 0.25)
        self.doubleSpinBox_tol_1.setObjectName(_fromUtf8("doubleSpinBox_tol_1"))
        self.doubleSpinBox_x_2 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_x_2.setGeometry(QtCore.QRect(340, 120, 61, 20))
        self.doubleSpinBox_x_2.setMinimum(-100.0)
        self.doubleSpinBox_x_2.setMaximum(100.0)
        self.doubleSpinBox_x_2.setSingleStep(0.1)
        self.doubleSpinBox_x_2.setProperty("value", 13.0)
        self.doubleSpinBox_x_2.setObjectName(_fromUtf8("doubleSpinBox_x_2"))
        self.label_14 = QtGui.QLabel(self.groupBox_4)
        self.label_14.setGeometry(QtCore.QRect(270, 120, 61, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.doubleSpinBox_tol_2 = QtGui.QDoubleSpinBox(self.groupBox_4)
        self.doubleSpinBox_tol_2.setGeometry(QtCore.QRect(440, 120, 51, 20))
        self.doubleSpinBox_tol_2.setSingleStep(0.1)
        self.doubleSpinBox_tol_2.setProperty("value", 0.25)
        self.doubleSpinBox_tol_2.setObjectName(_fromUtf8("doubleSpinBox_tol_2"))
        self.label_15 = QtGui.QLabel(self.groupBox_4)
        self.label_15.setGeometry(QtCore.QRect(410, 120, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_15.setFont(font)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.label_16 = QtGui.QLabel(self.groupBox_4)
        self.label_16.setGeometry(QtCore.QRect(500, 30, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_16.setFont(font)
        self.label_16.setObjectName(_fromUtf8("label_16"))
        self.label_H_1 = QtGui.QLabel(self.groupBox_4)
        self.label_H_1.setGeometry(QtCore.QRect(570, 30, 61, 22))
        self.label_H_1.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_1.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_1.setText(_fromUtf8(""))
        self.label_H_1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_1.setObjectName(_fromUtf8("label_H_1"))
        self.label_H_2 = QtGui.QLabel(self.groupBox_4)
        self.label_H_2.setGeometry(QtCore.QRect(570, 120, 61, 22))
        self.label_H_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_2.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_2.setText(_fromUtf8(""))
        self.label_H_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_2.setObjectName(_fromUtf8("label_H_2"))
        self.lineEdit_maskX = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_maskX.setGeometry(QtCore.QRect(440, 90, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskX.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskX.setSizePolicy(sizePolicy)
        self.lineEdit_maskX.setObjectName(_fromUtf8("lineEdit_maskX"))
        self.lineEdit_maskY = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_maskY.setGeometry(QtCore.QRect(490, 90, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskY.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskY.setSizePolicy(sizePolicy)
        self.lineEdit_maskY.setObjectName(_fromUtf8("lineEdit_maskY"))
        self.lineEdit_maskXRad = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_maskXRad.setGeometry(QtCore.QRect(540, 90, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskXRad.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskXRad.setSizePolicy(sizePolicy)
        self.lineEdit_maskXRad.setObjectName(_fromUtf8("lineEdit_maskXRad"))
        self.lineEdit_maskYRad = QtGui.QLineEdit(self.groupBox_4)
        self.lineEdit_maskYRad.setGeometry(QtCore.QRect(590, 90, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskYRad.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskYRad.setSizePolicy(sizePolicy)
        self.lineEdit_maskYRad.setObjectName(_fromUtf8("lineEdit_maskYRad"))
        self.label_17 = QtGui.QLabel(self.groupBox_4)
        self.label_17.setGeometry(QtCore.QRect(500, 120, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_17.setFont(font)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.label_5 = QtGui.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(350, 150, 231, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.label_24 = QtGui.QLabel(self.groupBox_4)
        self.label_24.setGeometry(QtCore.QRect(10, 100, 261, 16))
        self.label_24.setObjectName(_fromUtf8("label_24"))
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox_9)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 330, 321, 181))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_5.setFont(font)
        self.groupBox_5.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(0, 0, 75);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.lineEdit_fineCurrentMax = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_fineCurrentMax.setGeometry(QtCore.QRect(250, 50, 61, 22))
        self.lineEdit_fineCurrentMax.setObjectName(_fromUtf8("lineEdit_fineCurrentMax"))
        self.label_9 = QtGui.QLabel(self.groupBox_5)
        self.label_9.setGeometry(QtCore.QRect(10, 50, 151, 21))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.pushButton_fineCentreC2VCurrent = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_fineCentreC2VCurrent.setGeometry(QtCore.QRect(12, 80, 201, 22))
        self.pushButton_fineCentreC2VCurrent.setChecked(False)
        self.pushButton_fineCentreC2VCurrent.setObjectName(_fromUtf8("pushButton_fineCentreC2VCurrent"))
        self.lineEdit_fineCurrentMin = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_fineCurrentMin.setGeometry(QtCore.QRect(180, 50, 61, 22))
        self.lineEdit_fineCurrentMin.setObjectName(_fromUtf8("lineEdit_fineCurrentMin"))
        self.pushButton_fineGetCurrentRange_2 = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_fineGetCurrentRange_2.setGeometry(QtCore.QRect(10, 20, 301, 22))
        self.pushButton_fineGetCurrentRange_2.setChecked(False)
        self.pushButton_fineGetCurrentRange_2.setObjectName(_fromUtf8("pushButton_fineGetCurrentRange_2"))
        self.pushButton_fineCentreC2VCurrent_2 = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_fineCentreC2VCurrent_2.setGeometry(QtCore.QRect(10, 270, 201, 22))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_fineCentreC2VCurrent_2.setFont(font)
        self.pushButton_fineCentreC2VCurrent_2.setChecked(False)
        self.pushButton_fineCentreC2VCurrent_2.setObjectName(_fromUtf8("pushButton_fineCentreC2VCurrent_2"))
        self.pushButton_degaussC2V = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_degaussC2V.setGeometry(QtCore.QRect(10, 200, 131, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_degaussC2V.sizePolicy().hasHeightForWidth())
        self.pushButton_degaussC2V.setSizePolicy(sizePolicy)
        self.pushButton_degaussC2V.setMinimumSize(QtCore.QSize(1, 0))
        self.pushButton_degaussC2V.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.pushButton_degaussC2V.setChecked(False)
        self.pushButton_degaussC2V.setObjectName(_fromUtf8("pushButton_degaussC2V"))
        self.pushButton_camState2C2V = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_camState2C2V.setGeometry(QtCore.QRect(150, 200, 140, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_camState2C2V.sizePolicy().hasHeightForWidth())
        self.pushButton_camState2C2V.setSizePolicy(sizePolicy)
        self.pushButton_camState2C2V.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_camState2C2V.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_camState2C2V.setChecked(False)
        self.pushButton_camState2C2V.setObjectName(_fromUtf8("pushButton_camState2C2V"))
        self.pushButton_insertC2VScreen = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_insertC2VScreen.setGeometry(QtCore.QRect(10, 220, 131, 22))
        self.pushButton_insertC2VScreen.setChecked(False)
        self.pushButton_insertC2VScreen.setObjectName(_fromUtf8("pushButton_insertC2VScreen"))
        self.pushButton_retractC2VScreen = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_retractC2VScreen.setGeometry(QtCore.QRect(10, 300, 131, 22))
        self.pushButton_retractC2VScreen.setChecked(False)
        self.pushButton_retractC2VScreen.setObjectName(_fromUtf8("pushButton_retractC2VScreen"))
        self.pushButton_Align_2_B_2 = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_Align_2_B_2.setGeometry(QtCore.QRect(150, 220, 141, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Align_2_B_2.sizePolicy().hasHeightForWidth())
        self.pushButton_Align_2_B_2.setSizePolicy(sizePolicy)
        self.pushButton_Align_2_B_2.setMinimumSize(QtCore.QSize(1, 0))
        self.pushButton_Align_2_B_2.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Align_2_B_2.setChecked(False)
        self.pushButton_Align_2_B_2.setObjectName(_fromUtf8("pushButton_Align_2_B_2"))
        self.label_11 = QtGui.QLabel(self.groupBox_5)
        self.label_11.setGeometry(QtCore.QRect(10, 180, 241, 16))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.lineEdit_maskY_2 = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_maskY_2.setGeometry(QtCore.QRect(170, 240, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskY_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskY_2.setSizePolicy(sizePolicy)
        self.lineEdit_maskY_2.setObjectName(_fromUtf8("lineEdit_maskY_2"))
        self.lineEdit_maskYRad_2 = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_maskYRad_2.setGeometry(QtCore.QRect(270, 240, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskYRad_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskYRad_2.setSizePolicy(sizePolicy)
        self.lineEdit_maskYRad_2.setObjectName(_fromUtf8("lineEdit_maskYRad_2"))
        self.lineEdit_maskX_2 = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_maskX_2.setGeometry(QtCore.QRect(120, 240, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskX_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskX_2.setSizePolicy(sizePolicy)
        self.lineEdit_maskX_2.setObjectName(_fromUtf8("lineEdit_maskX_2"))
        self.lineEdit_maskXRad_2 = QtGui.QLineEdit(self.groupBox_5)
        self.lineEdit_maskXRad_2.setGeometry(QtCore.QRect(220, 240, 41, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lineEdit_maskXRad_2.sizePolicy().hasHeightForWidth())
        self.lineEdit_maskXRad_2.setSizePolicy(sizePolicy)
        self.lineEdit_maskXRad_2.setObjectName(_fromUtf8("lineEdit_maskXRad_2"))
        self.doubleSpinBox_tol_3 = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_tol_3.setGeometry(QtCore.QRect(270, 100, 51, 20))
        self.doubleSpinBox_tol_3.setSingleStep(0.1)
        self.doubleSpinBox_tol_3.setProperty("value", 0.1)
        self.doubleSpinBox_tol_3.setObjectName(_fromUtf8("doubleSpinBox_tol_3"))
        self.label_18 = QtGui.QLabel(self.groupBox_5)
        self.label_18.setGeometry(QtCore.QRect(220, 100, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_18.setFont(font)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.label_19 = QtGui.QLabel(self.groupBox_5)
        self.label_19.setGeometry(QtCore.QRect(220, 80, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_19.setFont(font)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.doubleSpinBox_x_3 = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_x_3.setGeometry(QtCore.QRect(270, 80, 51, 20))
        self.doubleSpinBox_x_3.setMinimum(-100.0)
        self.doubleSpinBox_x_3.setMaximum(100.0)
        self.doubleSpinBox_x_3.setSingleStep(0.1)
        self.doubleSpinBox_x_3.setProperty("value", 0.0)
        self.doubleSpinBox_x_3.setObjectName(_fromUtf8("doubleSpinBox_x_3"))
        self.label_20 = QtGui.QLabel(self.groupBox_5)
        self.label_20.setGeometry(QtCore.QRect(210, 290, 31, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_20.setFont(font)
        self.label_20.setObjectName(_fromUtf8("label_20"))
        self.label_21 = QtGui.QLabel(self.groupBox_5)
        self.label_21.setGeometry(QtCore.QRect(210, 270, 41, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_21.setFont(font)
        self.label_21.setObjectName(_fromUtf8("label_21"))
        self.doubleSpinBox_x_4 = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_x_4.setGeometry(QtCore.QRect(260, 270, 61, 20))
        self.doubleSpinBox_x_4.setMinimum(-100.0)
        self.doubleSpinBox_x_4.setMaximum(100.0)
        self.doubleSpinBox_x_4.setSingleStep(0.1)
        self.doubleSpinBox_x_4.setProperty("value", 0.0)
        self.doubleSpinBox_x_4.setObjectName(_fromUtf8("doubleSpinBox_x_4"))
        self.doubleSpinBox_tol_4 = QtGui.QDoubleSpinBox(self.groupBox_5)
        self.doubleSpinBox_tol_4.setGeometry(QtCore.QRect(260, 290, 61, 20))
        self.doubleSpinBox_tol_4.setSingleStep(0.1)
        self.doubleSpinBox_tol_4.setProperty("value", 0.2)
        self.doubleSpinBox_tol_4.setObjectName(_fromUtf8("doubleSpinBox_tol_4"))
        self.label_H_3 = QtGui.QLabel(self.groupBox_5)
        self.label_H_3.setGeometry(QtCore.QRect(270, 120, 51, 22))
        self.label_H_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_H_3.setFrameShape(QtGui.QFrame.WinPanel)
        self.label_H_3.setText(_fromUtf8(""))
        self.label_H_3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_H_3.setObjectName(_fromUtf8("label_H_3"))
        self.label_22 = QtGui.QLabel(self.groupBox_5)
        self.label_22.setGeometry(QtCore.QRect(220, 120, 51, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_22.setFont(font)
        self.label_22.setObjectName(_fromUtf8("label_22"))
        self.label_23 = QtGui.QLabel(self.groupBox_5)
        self.label_23.setGeometry(QtCore.QRect(0, 100, 221, 81))
        self.label_23.setAlignment(QtCore.Qt.AlignCenter)
        self.label_23.setWordWrap(True)
        self.label_23.setObjectName(_fromUtf8("label_23"))
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox_9)
        self.groupBox_6.setEnabled(False)
        self.groupBox_6.setGeometry(QtCore.QRect(340, 330, 311, 141))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.groupBox_6.setFont(font)
        self.groupBox_6.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(0, 0, 75);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.lineEdit_fineRFMin = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_fineRFMin.setGeometry(QtCore.QRect(170, 50, 61, 22))
        self.lineEdit_fineRFMin.setObjectName(_fromUtf8("lineEdit_fineRFMin"))
        self.lineEdit_fineRFMax = QtGui.QLineEdit(self.groupBox_6)
        self.lineEdit_fineRFMax.setGeometry(QtCore.QRect(240, 50, 61, 22))
        self.lineEdit_fineRFMax.setObjectName(_fromUtf8("lineEdit_fineRFMax"))
        self.label_10 = QtGui.QLabel(self.groupBox_6)
        self.label_10.setGeometry(QtCore.QRect(8, 50, 161, 21))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.label_10.setFont(font)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.pushButton_fineCentreC2VRF = QtGui.QPushButton(self.groupBox_6)
        self.pushButton_fineCentreC2VRF.setGeometry(QtCore.QRect(10, 80, 291, 22))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_fineCentreC2VRF.setFont(font)
        self.pushButton_fineCentreC2VRF.setChecked(False)
        self.pushButton_fineCentreC2VRF.setObjectName(_fromUtf8("pushButton_fineCentreC2VRF"))
        self.pushButton_fineGetRFRange_2 = QtGui.QPushButton(self.groupBox_6)
        self.pushButton_fineGetRFRange_2.setGeometry(QtCore.QRect(10, 20, 291, 22))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_fineGetRFRange_2.setFont(font)
        self.pushButton_fineGetRFRange_2.setChecked(False)
        self.pushButton_fineGetRFRange_2.setObjectName(_fromUtf8("pushButton_fineGetRFRange_2"))
        self.comboBox_dipole = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_dipole.setEnabled(False)
        self.comboBox_dipole.setGeometry(QtCore.QRect(440, 20, 111, 22))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.comboBox_dipole.setFont(font)
        self.comboBox_dipole.setObjectName(_fromUtf8("comboBox_dipole"))
        self.comboBox_dipole.addItem(_fromUtf8(""))
        self.label_I_3 = QtGui.QLabel(self.groupBox_run)
        self.label_I_3.setEnabled(False)
        self.label_I_3.setGeometry(QtCore.QRect(348, 20, 81, 20))
        self.label_I_3.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.label_I_3.setFont(font)
        self.label_I_3.setObjectName(_fromUtf8("label_I_3"))
        self.groupBox_10 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_10.setGeometry(QtCore.QRect(10, 150, 661, 141))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_10.setFont(font)
        self.groupBox_10.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(55, 0, 55);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_10.setObjectName(_fromUtf8("groupBox_10"))
        self.groupBox_8 = QtGui.QGroupBox(self.groupBox_10)
        self.groupBox_8.setGeometry(QtCore.QRect(10, 20, 311, 111))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.groupBox_8.setFont(font)
        self.groupBox_8.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(55, 0, 55);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_8.setObjectName(_fromUtf8("groupBox_8"))
        self.pushButton_roughCentreC2VCurrent = QtGui.QPushButton(self.groupBox_8)
        self.pushButton_roughCentreC2VCurrent.setGeometry(QtCore.QRect(12, 80, 291, 22))
        self.pushButton_roughCentreC2VCurrent.setChecked(False)
        self.pushButton_roughCentreC2VCurrent.setObjectName(_fromUtf8("pushButton_roughCentreC2VCurrent"))
        self.lineEdit_roughCurrentMin = QtGui.QLineEdit(self.groupBox_8)
        self.lineEdit_roughCurrentMin.setGeometry(QtCore.QRect(170, 50, 61, 22))
        self.lineEdit_roughCurrentMin.setObjectName(_fromUtf8("lineEdit_roughCurrentMin"))
        self.lineEdit_roughCurrentMax = QtGui.QLineEdit(self.groupBox_8)
        self.lineEdit_roughCurrentMax.setGeometry(QtCore.QRect(240, 50, 61, 22))
        self.lineEdit_roughCurrentMax.setObjectName(_fromUtf8("lineEdit_roughCurrentMax"))
        self.label_3 = QtGui.QLabel(self.groupBox_8)
        self.label_3.setGeometry(QtCore.QRect(10, 50, 161, 21))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.pushButton_roughGetCurrentRange = QtGui.QPushButton(self.groupBox_8)
        self.pushButton_roughGetCurrentRange.setGeometry(QtCore.QRect(10, 20, 291, 22))
        self.pushButton_roughGetCurrentRange.setChecked(False)
        self.pushButton_roughGetCurrentRange.setObjectName(_fromUtf8("pushButton_roughGetCurrentRange"))
        self.groupBox_11 = QtGui.QGroupBox(self.groupBox_10)
        self.groupBox_11.setEnabled(False)
        self.groupBox_11.setGeometry(QtCore.QRect(330, 20, 321, 111))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.groupBox_11.setFont(font)
        self.groupBox_11.setStyleSheet(_fromUtf8("QGroupBox{ background-color: rgb(55, 0, 55);}\n"
"QLabel{ background-color: rgba(0,0,0,0%);}\n"
"#QPushButton{ background-color: rgb(255, 255, 255);}"))
        self.groupBox_11.setObjectName(_fromUtf8("groupBox_11"))
        self.lineEdit_roughRFMax = QtGui.QLineEdit(self.groupBox_11)
        self.lineEdit_roughRFMax.setEnabled(False)
        self.lineEdit_roughRFMax.setGeometry(QtCore.QRect(250, 50, 61, 22))
        self.lineEdit_roughRFMax.setObjectName(_fromUtf8("lineEdit_roughRFMax"))
        self.label_8 = QtGui.QLabel(self.groupBox_11)
        self.label_8.setEnabled(False)
        self.label_8.setGeometry(QtCore.QRect(10, 50, 161, 21))
        font = QtGui.QFont()
        font.setStrikeOut(False)
        self.label_8.setFont(font)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.pushButton_roughCentreC2VRF = QtGui.QPushButton(self.groupBox_11)
        self.pushButton_roughCentreC2VRF.setEnabled(False)
        self.pushButton_roughCentreC2VRF.setGeometry(QtCore.QRect(10, 80, 301, 22))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_roughCentreC2VRF.setFont(font)
        self.pushButton_roughCentreC2VRF.setChecked(False)
        self.pushButton_roughCentreC2VRF.setObjectName(_fromUtf8("pushButton_roughCentreC2VRF"))
        self.lineEdit_roughRFMin = QtGui.QLineEdit(self.groupBox_11)
        self.lineEdit_roughRFMin.setEnabled(False)
        self.lineEdit_roughRFMin.setGeometry(QtCore.QRect(182, 50, 61, 22))
        self.lineEdit_roughRFMin.setObjectName(_fromUtf8("lineEdit_roughRFMin"))
        self.pushButton_roughGetRFRange = QtGui.QPushButton(self.groupBox_11)
        self.pushButton_roughGetRFRange.setEnabled(False)
        self.pushButton_roughGetRFRange.setGeometry(QtCore.QRect(10, 20, 301, 22))
        font = QtGui.QFont()
        font.setPointSize(-1)
        self.pushButton_roughGetRFRange.setFont(font)
        self.pushButton_roughGetRFRange.setChecked(False)
        self.pushButton_roughGetRFRange.setObjectName(_fromUtf8("pushButton_roughGetRFRange"))
        self.comboBox_selectRF = QtGui.QComboBox(self.groupBox_run)
        self.comboBox_selectRF.setGeometry(QtCore.QRect(160, 20, 161, 22))
        self.comboBox_selectRF.setObjectName(_fromUtf8("comboBox_selectRF"))
        self.comboBox_selectRF.addItem(_fromUtf8(""))
        self.comboBox_selectRF.addItem(_fromUtf8(""))
        self.label_I_4 = QtGui.QLabel(self.groupBox_run)
        self.label_I_4.setGeometry(QtCore.QRect(78, 20, 81, 20))
        self.label_I_4.setMinimumSize(QtCore.QSize(80, 0))
        self.label_I_4.setObjectName(_fromUtf8("label_I_4"))
        self.horizontalLayout.addWidget(self.groupBox_run)
        self.groupBox_monitor = QtGui.QGroupBox(self.tab)
        self.groupBox_monitor.setMinimumSize(QtCore.QSize(500, 0))
        self.groupBox_monitor.setObjectName(_fromUtf8("groupBox_monitor"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_monitor)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout.addWidget(self.groupBox_monitor)
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
        self.gridLayout_5.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1413, 26))
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
        self.groupBox.setTitle(_translate("MainWindow", "Initial estimate (sets scan ranges for rough measurements):", None))
        self.label.setText(_translate("MainWindow", "Dipole current", None))
        self.label_2.setText(_translate("MainWindow", "Momentum", None))
        self.pushButton_useCurrent.setText(_translate("MainWindow", "Use current from dipole", None))
        self.pushButton_useRF.setText(_translate("MainWindow", "Estimate momentum from RF", None))
        self.label_I.setText(_translate("MainWindow", "...", None))
        self.label_RF.setText(_translate("MainWindow", "...", None))
        self.doubleSpinBox_I.setSuffix(_translate("MainWindow", " A", None))
        self.doubleSpinBox_p.setSuffix(_translate("MainWindow", " MeV/c", None))
        self.groupBox_9.setTitle(_translate("MainWindow", "Fine measure/set:", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Preliminaries:", None))
        self.pushButton_Prelim_3.setText(_translate("MainWindow", "2. Degauss to zero: S02-DIP01, QUAD-03,04,05 (Closes laser shutters while degaussing)", None))
        self.pushButton_Prelim_1.setText(_translate("MainWindow", "1. Recalibrate BPMs", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Align through dipole:", None))
        self.pushButton_Align_1.setText(_translate("MainWindow", "1. Align on S02-BPM-02 using S02-HCOR-02", None))
        self.pushButton_Align_4.setText(_translate("MainWindow", "4. Retract S02-YAG-02", None))
        self.pushButton_Align_2.setText(_translate("MainWindow", "2. Insert S02-YAG-02", None))
        self.label_4.setText(_translate("MainWindow", "^ Repeat until aligned on both ^", None))
        self.pushButton_Align_3.setText(_translate("MainWindow", "3. Align on S02-YAG-02 using S02-HCOR-01", None))
        self.pushButton_Align_2_A.setText(_translate("MainWindow", "2a. Switch to S02-CAM-02", None))
        self.pushButton_Align_2_B.setText(_translate("MainWindow", "2b. Set mask x/y/xrad/yrad:", None))
        self.label_12.setText(_translate("MainWindow", "Tol.", None))
        self.label_13.setText(_translate("MainWindow", "H target", None))
        self.label_14.setText(_translate("MainWindow", "H target", None))
        self.label_15.setText(_translate("MainWindow", "Tol.", None))
        self.label_16.setText(_translate("MainWindow", "H readout", None))
        self.lineEdit_maskX.setText(_translate("MainWindow", "1280", None))
        self.lineEdit_maskY.setText(_translate("MainWindow", "1080", None))
        self.lineEdit_maskXRad.setText(_translate("MainWindow", "1080", None))
        self.lineEdit_maskYRad.setText(_translate("MainWindow", "1080", None))
        self.label_17.setText(_translate("MainWindow", "H readout", None))
        self.label_5.setText(_translate("MainWindow", "^ Default targets are expected centres", None))
        self.label_24.setText(_translate("MainWindow", "Check ImageCollector cross-hair is tracking", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Measure momentum:", None))
        self.label_9.setText(_translate("MainWindow", "Dipole min/max (editable):", None))
        self.pushButton_fineCentreC2VCurrent.setText(_translate("MainWindow", "2. Start scan", None))
        self.pushButton_fineGetCurrentRange_2.setText(_translate("MainWindow", "1. Get scan range from rough measurement", None))
        self.pushButton_fineCentreC2VCurrent_2.setText(_translate("MainWindow", "Inc. DIP to centre on C2V screen", None))
        self.pushButton_degaussC2V.setText(_translate("MainWindow", "Degauss C2V Q1/2/3", None))
        self.pushButton_camState2C2V.setText(_translate("MainWindow", "Switch to C2V-CAM-01", None))
        self.pushButton_insertC2VScreen.setText(_translate("MainWindow", "Insert C2V-CAM-01", None))
        self.pushButton_retractC2VScreen.setText(_translate("MainWindow", "Retract C2V-CAM-01", None))
        self.pushButton_Align_2_B_2.setText(_translate("MainWindow", "Set mask x/y/xrad/yrad:", None))
        self.label_11.setText(_translate("MainWindow", "OR - use C2V screen for centering:", None))
        self.lineEdit_maskY_2.setText(_translate("MainWindow", "1200", None))
        self.lineEdit_maskYRad_2.setText(_translate("MainWindow", "1240", None))
        self.lineEdit_maskX_2.setText(_translate("MainWindow", "1050", None))
        self.lineEdit_maskXRad_2.setText(_translate("MainWindow", "1180", None))
        self.label_18.setText(_translate("MainWindow", "Tol.", None))
        self.label_19.setText(_translate("MainWindow", "Target", None))
        self.label_20.setText(_translate("MainWindow", "Tol.", None))
        self.label_21.setText(_translate("MainWindow", "Target", None))
        self.label_22.setText(_translate("MainWindow", "H read.", None))
        self.label_23.setText(_translate("MainWindow", "The dipole current is set to the minimum value that gives a good BPM reading, then increases to approach x=0 on the BPM without overshooting", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Set momentum:", None))
        self.label_10.setText(_translate("MainWindow", "RF amp min/max (editable):", None))
        self.pushButton_fineCentreC2VRF.setText(_translate("MainWindow", "3. Set RF to centre down spectometer line", None))
        self.pushButton_fineGetRFRange_2.setText(_translate("MainWindow", "1. Get scan range from rough measurement", None))
        self.comboBox_dipole.setItemText(0, _translate("MainWindow", "S02-DIP01", None))
        self.label_I_3.setText(_translate("MainWindow", "Select dipole:", None))
        self.groupBox_10.setTitle(_translate("MainWindow", "Rough measure/set (finds BPM ranges to use for fine measurements):", None))
        self.groupBox_8.setTitle(_translate("MainWindow", "Measure momentum:", None))
        self.pushButton_roughCentreC2VCurrent.setText(_translate("MainWindow", "2. Scan dipole", None))
        self.label_3.setText(_translate("MainWindow", "Dipole min/max (editable):", None))
        self.pushButton_roughGetCurrentRange.setText(_translate("MainWindow", "1. Get scan range from initial estimate", None))
        self.groupBox_11.setTitle(_translate("MainWindow", "Set momentum:", None))
        self.label_8.setText(_translate("MainWindow", "RF amp min/max (editable):", None))
        self.pushButton_roughCentreC2VRF.setText(_translate("MainWindow", "2. Scan RF", None))
        self.pushButton_roughGetRFRange.setText(_translate("MainWindow", "1. Get scan range from initial estimate", None))
        self.comboBox_selectRF.setItemText(0, _translate("MainWindow", "Gun only", None))
        self.comboBox_selectRF.setItemText(1, _translate("MainWindow", "Gun + Linac (gun fixed)", None))
        self.label_I_4.setText(_translate("MainWindow", "Select RF:", None))
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


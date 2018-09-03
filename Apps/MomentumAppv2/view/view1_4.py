# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'view1_4.ui'
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
        MainWindow.resize(1400, 782)
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
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.tab)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.groupBox_run = QtGui.QGroupBox(self.tab)
        self.groupBox_run.setMinimumSize(QtCore.QSize(600, 0))
        self.groupBox_run.setMaximumSize(QtCore.QSize(600, 16777215))
        self.groupBox_run.setObjectName(_fromUtf8("groupBox_run"))
        self.pushButton_refreshImage = QtGui.QPushButton(self.groupBox_run)
        self.pushButton_refreshImage.setGeometry(QtCore.QRect(10, 630, 91, 22))
        self.pushButton_refreshImage.setObjectName(_fromUtf8("pushButton_refreshImage"))
        self.groupBox = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 581, 121))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(12, 86, 22, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.pushButton_predictMom_2 = QtGui.QPushButton(self.groupBox)
        self.pushButton_predictMom_2.setGeometry(QtCore.QRect(60, 86, 234, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_predictMom_2.sizePolicy().hasHeightForWidth())
        self.pushButton_predictMom_2.setSizePolicy(sizePolicy)
        self.pushButton_predictMom_2.setMinimumSize(QtCore.QSize(140, 22))
        self.pushButton_predictMom_2.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_predictMom_2.setChecked(False)
        self.pushButton_predictMom_2.setObjectName(_fromUtf8("pushButton_predictMom_2"))
        self.pushButton_predictMom = QtGui.QPushButton(self.groupBox)
        self.pushButton_predictMom.setGeometry(QtCore.QRect(60, 57, 231, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_predictMom.sizePolicy().hasHeightForWidth())
        self.pushButton_predictMom.setSizePolicy(sizePolicy)
        self.pushButton_predictMom.setMinimumSize(QtCore.QSize(140, 22))
        self.pushButton_predictMom.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_predictMom.setChecked(False)
        self.pushButton_predictMom.setObjectName(_fromUtf8("pushButton_predictMom"))
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(12, 28, 113, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(12, 57, 22, 16))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_I = QtGui.QLabel(self.groupBox)
        self.label_I.setGeometry(QtCore.QRect(300, 57, 131, 20))
        self.label_I.setMinimumSize(QtCore.QSize(120, 0))
        self.label_I.setObjectName(_fromUtf8("label_I"))
        self.lineEdit_predictMom = QtGui.QLineEdit(self.groupBox)
        self.lineEdit_predictMom.setGeometry(QtCore.QRect(132, 28, 80, 22))
        self.lineEdit_predictMom.setMinimumSize(QtCore.QSize(0, 22))
        self.lineEdit_predictMom.setObjectName(_fromUtf8("lineEdit_predictMom"))
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(440, 10, 131, 51))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.label_predictMom = QtGui.QLabel(self.groupBox_2)
        self.label_predictMom.setGeometry(QtCore.QRect(10, 20, 111, 22))
        self.label_predictMom.setObjectName(_fromUtf8("label_predictMom"))
        self.groupBox_7 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_7.setGeometry(QtCore.QRect(439, 60, 131, 51))
        self.groupBox_7.setObjectName(_fromUtf8("groupBox_7"))
        self.label_predictI = QtGui.QLabel(self.groupBox_7)
        self.label_predictI.setGeometry(QtCore.QRect(10, 20, 111, 22))
        self.label_predictI.setObjectName(_fromUtf8("label_predictI"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 150, 581, 141))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.pushButton_Prelim_3 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_Prelim_3.setGeometry(QtCore.QRect(20, 70, 353, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Prelim_3.sizePolicy().hasHeightForWidth())
        self.pushButton_Prelim_3.setSizePolicy(sizePolicy)
        self.pushButton_Prelim_3.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Prelim_3.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Prelim_3.setChecked(False)
        self.pushButton_Prelim_3.setObjectName(_fromUtf8("pushButton_Prelim_3"))
        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setGeometry(QtCore.QRect(140, 20, 126, 16))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.pushButton_Prelim_2 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_Prelim_2.setGeometry(QtCore.QRect(20, 40, 353, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Prelim_2.sizePolicy().hasHeightForWidth())
        self.pushButton_Prelim_2.setSizePolicy(sizePolicy)
        self.pushButton_Prelim_2.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Prelim_2.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Prelim_2.setChecked(False)
        self.pushButton_Prelim_2.setObjectName(_fromUtf8("pushButton_Prelim_2"))
        self.pushButton_Prelim_4 = QtGui.QPushButton(self.groupBox_3)
        self.pushButton_Prelim_4.setGeometry(QtCore.QRect(20, 100, 353, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Prelim_4.sizePolicy().hasHeightForWidth())
        self.pushButton_Prelim_4.setSizePolicy(sizePolicy)
        self.pushButton_Prelim_4.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Prelim_4.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Prelim_4.setChecked(False)
        self.pushButton_Prelim_4.setObjectName(_fromUtf8("pushButton_Prelim_4"))
        self.groupBox_4 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 300, 581, 201))
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.pushButton_Align_2_A = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_2_A.setGeometry(QtCore.QRect(330, 60, 141, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Align_2_A.sizePolicy().hasHeightForWidth())
        self.pushButton_Align_2_A.setSizePolicy(sizePolicy)
        self.pushButton_Align_2_A.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Align_2_A.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Align_2_A.setChecked(False)
        self.pushButton_Align_2_A.setObjectName(_fromUtf8("pushButton_Align_2_A"))
        self.label_4 = QtGui.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(20, 180, 281, 16))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.pushButton_Align_2_B = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_2_B.setGeometry(QtCore.QRect(330, 100, 141, 22))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_Align_2_B.sizePolicy().hasHeightForWidth())
        self.pushButton_Align_2_B.setSizePolicy(sizePolicy)
        self.pushButton_Align_2_B.setMinimumSize(QtCore.QSize(140, 0))
        self.pushButton_Align_2_B.setMaximumSize(QtCore.QSize(371, 16777215))
        self.pushButton_Align_2_B.setChecked(False)
        self.pushButton_Align_2_B.setObjectName(_fromUtf8("pushButton_Align_2_B"))
        self.pushButton_Align_3 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_3.setGeometry(QtCore.QRect(10, 120, 301, 22))
        self.pushButton_Align_3.setChecked(False)
        self.pushButton_Align_3.setObjectName(_fromUtf8("pushButton_Align_3"))
        self.pushButton_Align_2 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_2.setGeometry(QtCore.QRect(10, 80, 301, 22))
        self.pushButton_Align_2.setChecked(False)
        self.pushButton_Align_2.setObjectName(_fromUtf8("pushButton_Align_2"))
        self.pushButton_Align_4 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_4.setGeometry(QtCore.QRect(10, 150, 301, 22))
        self.pushButton_Align_4.setChecked(False)
        self.pushButton_Align_4.setObjectName(_fromUtf8("pushButton_Align_4"))
        self.pushButton_Align_1 = QtGui.QPushButton(self.groupBox_4)
        self.pushButton_Align_1.setGeometry(QtCore.QRect(10, 30, 301, 22))
        self.pushButton_Align_1.setChecked(False)
        self.pushButton_Align_1.setObjectName(_fromUtf8("pushButton_Align_1"))
        self.groupBox_5 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_5.setGeometry(QtCore.QRect(10, 500, 291, 141))
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.pushButton_CentreC2V = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_CentreC2V.setGeometry(QtCore.QRect(30, 50, 198, 22))
        self.pushButton_CentreC2V.setChecked(False)
        self.pushButton_CentreC2V.setObjectName(_fromUtf8("pushButton_CentreC2V"))
        self.pushButton_CalcMom = QtGui.QPushButton(self.groupBox_5)
        self.pushButton_CalcMom.setGeometry(QtCore.QRect(70, 90, 137, 22))
        self.pushButton_CalcMom.setChecked(False)
        self.pushButton_CalcMom.setObjectName(_fromUtf8("pushButton_CalcMom"))
        self.groupBox_6 = QtGui.QGroupBox(self.groupBox_run)
        self.groupBox_6.setGeometry(QtCore.QRect(310, 500, 281, 141))
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.pushButton_refreshImage.raise_()
        self.groupBox.raise_()
        self.groupBox_3.raise_()
        self.groupBox_4.raise_()
        self.groupBox_5.raise_()
        self.groupBox_6.raise_()
        self.pushButton_Prelim_4.raise_()
        self.horizontalLayout_2.addWidget(self.groupBox_run)
        self.groupBox_monitor = QtGui.QGroupBox(self.tab)
        self.groupBox_monitor.setMinimumSize(QtCore.QSize(600, 0))
        self.groupBox_monitor.setObjectName(_fromUtf8("groupBox_monitor"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.groupBox_monitor)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.horizontalLayout_2.addWidget(self.groupBox_monitor)
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
        self.horizontalLayout.addWidget(self.tabWidget)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1400, 26))
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
        self.pushButton_refreshImage.setText(_translate("MainWindow", "Refresh Image", None))
        self.groupBox.setTitle(_translate("MainWindow", "Define approx. momentum (to within ~20%):", None))
        self.label_8.setText(_translate("MainWindow", "OR:", None))
        self.pushButton_predictMom_2.setText(_translate("MainWindow", "Scan S02-DIP-01 (not implemented yet)", None))
        self.pushButton_predictMom.setText(_translate("MainWindow", "Predict momentum from S02 DIP-01", None))
        self.label.setText(_translate("MainWindow", "Predict momentum:", None))
        self.label_6.setText(_translate("MainWindow", "OR:", None))
        self.label_I.setText(_translate("MainWindow", "TextLabel", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Approx. p [MeV/c]", None))
        self.label_predictMom.setText(_translate("MainWindow", "TextLabel", None))
        self.groupBox_7.setTitle(_translate("MainWindow", "Corresponding I [A]", None))
        self.label_predictI.setText(_translate("MainWindow", "TextLabel", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Preliminaries:", None))
        self.pushButton_Prelim_3.setText(_translate("MainWindow", "Degauss to zero: S02 DIP-01, QUAD-03,04,05", None))
        self.label_5.setText(_translate("MainWindow", "Calibrate BPMs!", None))
        self.pushButton_Prelim_2.setText(_translate("MainWindow", "Close laser shutters", None))
        self.pushButton_Prelim_4.setText(_translate("MainWindow", "Open laser shutters", None))
        self.groupBox_4.setTitle(_translate("MainWindow", "Align through S02-DIP-01:", None))
        self.pushButton_Align_2_A.setText(_translate("MainWindow", "Switch to S02-CAM-02", None))
        self.label_4.setText(_translate("MainWindow", "^Repeat until aligned on both (what tolerance?)^", None))
        self.pushButton_Align_2_B.setText(_translate("MainWindow", "Set mask", None))
        self.pushButton_Align_3.setText(_translate("MainWindow", "Align on S02-YAG-02 using S02-HVCOR-01", None))
        self.pushButton_Align_2.setText(_translate("MainWindow", "Insert S02-YAG-02", None))
        self.pushButton_Align_4.setText(_translate("MainWindow", "Retract S02-YAG-02", None))
        self.pushButton_Align_1.setText(_translate("MainWindow", "Align on S02-BPM-02 using S02-HVCOR-02", None))
        self.groupBox_5.setTitle(_translate("MainWindow", "Measure momentum:", None))
        self.pushButton_CentreC2V.setText(_translate("MainWindow", "3.Centre Down Spectometer Line", None))
        self.pushButton_CalcMom.setText(_translate("MainWindow", "4.Calculate Momentum", None))
        self.groupBox_6.setTitle(_translate("MainWindow", "Set momentum:", None))
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


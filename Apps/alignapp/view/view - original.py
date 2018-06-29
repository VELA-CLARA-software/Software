# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitlednew2.ui'
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
        MainWindow.resize(899, 610)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
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
        self.gridLayout_2 = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.autogroupBox = QtGui.QGroupBox(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autogroupBox.sizePolicy().hasHeightForWidth())
        self.autogroupBox.setSizePolicy(sizePolicy)
        self.autogroupBox.setMaximumSize(QtCore.QSize(200, 145))
        self.autogroupBox.setObjectName(_fromUtf8("autogroupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.autogroupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.autopushButton = QtGui.QPushButton(self.autogroupBox)
        self.autopushButton.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.autopushButton.sizePolicy().hasHeightForWidth())
        self.autopushButton.setSizePolicy(sizePolicy)
        self.autopushButton.setMinimumSize(QtCore.QSize(2, 2))
        self.autopushButton.setMaximumSize(QtCore.QSize(281, 150))
        self.autopushButton.setObjectName(_fromUtf8("autopushButton"))
        self.verticalLayout.addWidget(self.autopushButton)
        self.checkBox_2 = QtGui.QCheckBox(self.autogroupBox)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.verticalLayout.addWidget(self.checkBox_2)
        self.checkBox = QtGui.QCheckBox(self.autogroupBox)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout.addWidget(self.checkBox)
        self.gridLayout_2.addWidget(self.autogroupBox, 0, 0, 1, 1)
        self.manualgroupBox = QtGui.QGroupBox(self.centralwidget)
        self.manualgroupBox.setMaximumSize(QtCore.QSize(16777215, 145))
        self.manualgroupBox.setObjectName(_fromUtf8("manualgroupBox"))
        self.gridLayout = QtGui.QGridLayout(self.manualgroupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.SOLlabel = QtGui.QLabel(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SOLlabel.sizePolicy().hasHeightForWidth())
        self.SOLlabel.setSizePolicy(sizePolicy)
        self.SOLlabel.setAlignment(QtCore.Qt.AlignCenter)
        self.SOLlabel.setObjectName(_fromUtf8("SOLlabel"))
        self.gridLayout.addWidget(self.SOLlabel, 0, 0, 1, 1)
        self.name_5 = QtGui.QLabel(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_5.sizePolicy().hasHeightForWidth())
        self.name_5.setSizePolicy(sizePolicy)
        self.name_5.setAlignment(QtCore.Qt.AlignCenter)
        self.name_5.setObjectName(_fromUtf8("name_5"))
        self.gridLayout.addWidget(self.name_5, 0, 1, 1, 1)
        self.name_3 = QtGui.QLabel(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_3.sizePolicy().hasHeightForWidth())
        self.name_3.setSizePolicy(sizePolicy)
        self.name_3.setAlignment(QtCore.Qt.AlignCenter)
        self.name_3.setObjectName(_fromUtf8("name_3"))
        self.gridLayout.addWidget(self.name_3, 0, 2, 1, 1)
        self.name_6 = QtGui.QLabel(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.name_6.sizePolicy().hasHeightForWidth())
        self.name_6.setSizePolicy(sizePolicy)
        self.name_6.setAlignment(QtCore.Qt.AlignCenter)
        self.name_6.setObjectName(_fromUtf8("name_6"))
        self.gridLayout.addWidget(self.name_6, 0, 3, 1, 1)
        self.Mag_PSU_State_Button = QtGui.QPushButton(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mag_PSU_State_Button.sizePolicy().hasHeightForWidth())
        self.Mag_PSU_State_Button.setSizePolicy(sizePolicy)
        self.Mag_PSU_State_Button.setMinimumSize(QtCore.QSize(43, 41))
        self.Mag_PSU_State_Button.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Mag_PSU_State_Button.setAutoDefault(False)
        self.Mag_PSU_State_Button.setDefault(False)
        self.Mag_PSU_State_Button.setObjectName(_fromUtf8("Mag_PSU_State_Button"))
        self.gridLayout.addWidget(self.Mag_PSU_State_Button, 1, 0, 1, 1)
        self.Mag_PSU_State_Button_5 = QtGui.QPushButton(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mag_PSU_State_Button_5.sizePolicy().hasHeightForWidth())
        self.Mag_PSU_State_Button_5.setSizePolicy(sizePolicy)
        self.Mag_PSU_State_Button_5.setMinimumSize(QtCore.QSize(43, 61))
        self.Mag_PSU_State_Button_5.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Mag_PSU_State_Button_5.setAutoDefault(False)
        self.Mag_PSU_State_Button_5.setDefault(False)
        self.Mag_PSU_State_Button_5.setObjectName(_fromUtf8("Mag_PSU_State_Button_5"))
        self.gridLayout.addWidget(self.Mag_PSU_State_Button_5, 1, 1, 2, 1)
        self.Mag_PSU_State_Button_3 = QtGui.QPushButton(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mag_PSU_State_Button_3.sizePolicy().hasHeightForWidth())
        self.Mag_PSU_State_Button_3.setSizePolicy(sizePolicy)
        self.Mag_PSU_State_Button_3.setMinimumSize(QtCore.QSize(43, 61))
        self.Mag_PSU_State_Button_3.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Mag_PSU_State_Button_3.setAutoDefault(False)
        self.Mag_PSU_State_Button_3.setDefault(False)
        self.Mag_PSU_State_Button_3.setObjectName(_fromUtf8("Mag_PSU_State_Button_3"))
        self.gridLayout.addWidget(self.Mag_PSU_State_Button_3, 1, 2, 2, 1)
        self.Mag_PSU_State_Button_6 = QtGui.QPushButton(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Mag_PSU_State_Button_6.sizePolicy().hasHeightForWidth())
        self.Mag_PSU_State_Button_6.setSizePolicy(sizePolicy)
        self.Mag_PSU_State_Button_6.setMinimumSize(QtCore.QSize(43, 61))
        self.Mag_PSU_State_Button_6.setMaximumSize(QtCore.QSize(40, 16777215))
        self.Mag_PSU_State_Button_6.setAutoDefault(False)
        self.Mag_PSU_State_Button_6.setDefault(False)
        self.Mag_PSU_State_Button_6.setObjectName(_fromUtf8("Mag_PSU_State_Button_6"))
        self.gridLayout.addWidget(self.Mag_PSU_State_Button_6, 1, 3, 2, 1)
        self.checkBox_3 = QtGui.QCheckBox(self.manualgroupBox)
        self.checkBox_3.setMinimumSize(QtCore.QSize(41, 20))
        self.checkBox_3.setMaximumSize(QtCore.QSize(80, 20))
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.gridLayout.addWidget(self.checkBox_3, 2, 0, 1, 1)
        self.SIValue = QtGui.QDoubleSpinBox(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SIValue.sizePolicy().hasHeightForWidth())
        self.SIValue.setSizePolicy(sizePolicy)
        self.SIValue.setMinimumSize(QtCore.QSize(41, 20))
        self.SIValue.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.SIValue.setDecimals(3)
        self.SIValue.setMinimum(-1000.0)
        self.SIValue.setMaximum(1000.0)
        self.SIValue.setSingleStep(0.001)
        self.SIValue.setObjectName(_fromUtf8("SIValue"))
        self.gridLayout.addWidget(self.SIValue, 3, 0, 1, 1)
        self.SIValue_5 = QtGui.QDoubleSpinBox(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SIValue_5.sizePolicy().hasHeightForWidth())
        self.SIValue_5.setSizePolicy(sizePolicy)
        self.SIValue_5.setMinimumSize(QtCore.QSize(41, 20))
        self.SIValue_5.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.SIValue_5.setDecimals(3)
        self.SIValue_5.setMinimum(-1000.0)
        self.SIValue_5.setMaximum(1000.0)
        self.SIValue_5.setSingleStep(0.001)
        self.SIValue_5.setObjectName(_fromUtf8("SIValue_5"))
        self.gridLayout.addWidget(self.SIValue_5, 3, 1, 1, 1)
        self.SIValue_3 = QtGui.QDoubleSpinBox(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SIValue_3.sizePolicy().hasHeightForWidth())
        self.SIValue_3.setSizePolicy(sizePolicy)
        self.SIValue_3.setMinimumSize(QtCore.QSize(41, 20))
        self.SIValue_3.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.SIValue_3.setDecimals(3)
        self.SIValue_3.setMinimum(-1000.0)
        self.SIValue_3.setMaximum(1000.0)
        self.SIValue_3.setSingleStep(0.001)
        self.SIValue_3.setObjectName(_fromUtf8("SIValue_3"))
        self.gridLayout.addWidget(self.SIValue_3, 3, 2, 1, 1)
        self.SIValue_6 = QtGui.QDoubleSpinBox(self.manualgroupBox)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.SIValue_6.sizePolicy().hasHeightForWidth())
        self.SIValue_6.setSizePolicy(sizePolicy)
        self.SIValue_6.setMinimumSize(QtCore.QSize(41, 20))
        self.SIValue_6.setButtonSymbols(QtGui.QAbstractSpinBox.PlusMinus)
        self.SIValue_6.setDecimals(3)
        self.SIValue_6.setMinimum(-1000.0)
        self.SIValue_6.setMaximum(1000.0)
        self.SIValue_6.setSingleStep(0.001)
        self.SIValue_6.setObjectName(_fromUtf8("SIValue_6"))
        self.gridLayout.addWidget(self.SIValue_6, 3, 3, 1, 1)
        self.name_3.raise_()
        self.SIValue_3.raise_()
        self.Mag_PSU_State_Button_3.raise_()
        self.name_6.raise_()
        self.SIValue_6.raise_()
        self.Mag_PSU_State_Button_6.raise_()
        self.SOLlabel.raise_()
        self.SIValue.raise_()
        self.Mag_PSU_State_Button.raise_()
        self.name_5.raise_()
        self.SIValue_5.raise_()
        self.Mag_PSU_State_Button_5.raise_()
        self.checkBox_3.raise_()
        self.gridLayout_2.addWidget(self.manualgroupBox, 0, 1, 1, 1)
        self.monitorgroupBox = QtGui.QGroupBox(self.centralwidget)
        self.monitorgroupBox.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.monitorgroupBox.sizePolicy().hasHeightForWidth())
        self.monitorgroupBox.setSizePolicy(sizePolicy)
        self.monitorgroupBox.setMinimumSize(QtCore.QSize(0, 400))
        self.monitorgroupBox.setMaximumSize(QtCore.QSize(16777215, 1000))
        self.monitorgroupBox.setObjectName(_fromUtf8("monitorgroupBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.monitorgroupBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.groupBox = QtGui.QGroupBox(self.monitorgroupBox)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.horizontalLayout.addWidget(self.groupBox)
        self.groupBox_2 = QtGui.QGroupBox(self.monitorgroupBox)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.horizontalLayout.addWidget(self.groupBox_2)
        self.groupBox_3 = QtGui.QGroupBox(self.monitorgroupBox)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.horizontalLayout.addWidget(self.groupBox_3)
        self.gridLayout_2.addWidget(self.monitorgroupBox, 1, 0, 1, 2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 899, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.autogroupBox.setTitle(_translate("MainWindow", "Automate", None))
        self.autopushButton.setText(_translate("MainWindow", "Correct Orbit", None))
        self.checkBox_2.setText(_translate("MainWindow", "RF", None))
        self.checkBox.setText(_translate("MainWindow", "SOL", None))
        self.manualgroupBox.setTitle(_translate("MainWindow", "Manual", None))
        self.SOLlabel.setText(_translate("MainWindow", "SOL", None))
        self.name_5.setText(_translate("MainWindow", "RF phase", None))
        self.name_3.setText(_translate("MainWindow", "Laser x", None))
        self.name_6.setText(_translate("MainWindow", "Laser y", None))
        self.Mag_PSU_State_Button.setText(_translate("MainWindow", "ERR", None))
        self.Mag_PSU_State_Button_5.setText(_translate("MainWindow", "ERR", None))
        self.Mag_PSU_State_Button_3.setText(_translate("MainWindow", "ERR", None))
        self.Mag_PSU_State_Button_6.setText(_translate("MainWindow", "ERR", None))
        self.checkBox_3.setText(_translate("MainWindow", "Reverse", None))
        self.monitorgroupBox.setTitle(_translate("MainWindow", "Monitor", None))
        self.groupBox.setTitle(_translate("MainWindow", "VC", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "BPM01", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "YAG01", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


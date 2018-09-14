# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_mainView.ui'
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

class Ui_mainView(object):
    def setupUi(self, mainView):
        mainView.setObjectName(_fromUtf8("mainView"))
        mainView.resize(954, 877)
        self.centralwidget = QtGui.QWidget(mainView)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.graphicsView = GraphicsLayoutWidget(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(230, 10, 711, 611))
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.x_proj = GraphicsLayoutWidget(self.centralwidget)
        self.x_proj.setGeometry(QtCore.QRect(230, 640, 711, 192))
        self.x_proj.setObjectName(_fromUtf8("x_proj"))
        self.y_proj = GraphicsLayoutWidget(self.centralwidget)
        self.y_proj.setGeometry(QtCore.QRect(10, 10, 201, 611))
        self.y_proj.setObjectName(_fromUtf8("y_proj"))
        self.reset_mean_pushButton = QtGui.QPushButton(self.centralwidget)
        self.reset_mean_pushButton.setGeometry(QtCore.QRect(20, 642, 151, 61))
        font = QtGui.QFont()
        font.setPointSize(21)
        self.reset_mean_pushButton.setFont(font)
        self.reset_mean_pushButton.setObjectName(_fromUtf8("reset_mean_pushButton"))
        self.cam_name_text = QtGui.QTextEdit(self.centralwidget)
        self.cam_name_text.setGeometry(QtCore.QRect(30, 720, 141, 31))
        self.cam_name_text.setObjectName(_fromUtf8("cam_name_text"))
        self.average_cbox = QtGui.QCheckBox(self.centralwidget)
        self.average_cbox.setGeometry(QtCore.QRect(30, 780, 161, 41))
        font = QtGui.QFont()
        font.setPointSize(23)
        self.average_cbox.setFont(font)
        self.average_cbox.setObjectName(_fromUtf8("average_cbox"))
        mainView.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 954, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        mainView.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainView)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainView.setStatusBar(self.statusbar)

        self.retranslateUi(mainView)
        QtCore.QMetaObject.connectSlotsByName(mainView)

    def retranslateUi(self, mainView):
        mainView.setWindowTitle(_translate("mainView", "MainWindow", None))
        self.reset_mean_pushButton.setText(_translate("mainView", "Reset Mean", None))
        self.cam_name_text.setHtml(_translate("mainView", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Cam Name</span></p></body></html>", None))
        self.average_cbox.setText(_translate("mainView", "average", None))

from pyqtgraph import GraphicsLayoutWidget

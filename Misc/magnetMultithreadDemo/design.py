# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'threading_design.ui'
#
# Created: Thu Aug  6 13:47:18 2015
#      by: PyQt4 UI code generator 4.10.4
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
        MainWindow.resize(526, 373)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_submissions_list = QtGui.QLabel(self.centralwidget)
        self.label_submissions_list.setObjectName(_fromUtf8("label_submissions_list"))
        self.verticalLayout.addWidget(self.label_submissions_list)
        self.list_submissions = QtGui.QListWidget(self.centralwidget)
        self.list_submissions.setBatchSize(1)
        self.list_submissions.setObjectName(_fromUtf8("list_submissions"))
        self.verticalLayout.addWidget(self.list_submissions)
        self.progress_bar = QtGui.QProgressBar(self.centralwidget)
        self.progress_bar.setProperty("value", 0)
        self.progress_bar.setObjectName(_fromUtf8("progress_bar"))
        self.verticalLayout.addWidget(self.progress_bar)
        self.buttons_layout = QtGui.QHBoxLayout()
        self.buttons_layout.setObjectName(_fromUtf8("buttons_layout"))
        self.btn_setSI = QtGui.QPushButton(self.centralwidget)
        self.btn_setSI.setObjectName(_fromUtf8("btn_setSI"))
        self.buttons_layout.addWidget(self.btn_setSI)
        self.btn_start = QtGui.QPushButton(self.centralwidget)
        self.btn_start.setObjectName(_fromUtf8("btn_start"))
        self.buttons_layout.addWidget(self.btn_start)
        self.verticalLayout.addLayout(self.buttons_layout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Threading Demo", None))
        #self.edit_subreddits.setPlaceholderText(_translate("MainWindow", "python,programming,linux,etc (comma separated)", None))
        #self.label_submissions_list.setText(_translate("MainWindow", "Text:", None))
        self.btn_setSI.setText(_translate("MainWindow", "SET SI", None))
        self.btn_start.setText(_translate("MainWindow", "TEST", None))

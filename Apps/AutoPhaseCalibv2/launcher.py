# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import os,sys
from PyQt4 import QtCore, QtGui
from mainApp import *
from launcherUI import *

class launcherUI(QtCore.QObject):
    def __init__(self, *sys_argv):
        super(launcherUI, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(MainWindow)
        self.ui.pushButton.clicked.connect(self.launch)

    def launch(self):
        # print 'launching!'
        # os.system("python mainApp.py "+str(self.comboBox.currentText())+' '+str(self.comboBox_2.currentText())+' '+str(self.comboBox_3.currentText()))
        self.workerThread = runMainApp(self, str(self.ui.comboBox.currentText()), str(self.ui.comboBox_2.currentText()), str(self.ui.comboBox_3.currentText()))
        MainWindow.hide()
        self.workerThread.finished.connect(MainWindow.show)
        self.workerThread.start()

class runMainApp(QtCore.QThread):
    def __init__(self, *sys_argv):
        super(runMainApp, self).__init__()
        self.args = sys_argv

    def start(self):
        global app
        self.appObject = App(app, self.args)

if __name__ == "__main__":
    import sys
    global app
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    launcher = launcherUI()
    MainWindow.show()
    sys.exit(app.exec_())

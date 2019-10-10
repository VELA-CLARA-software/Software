# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'launcher.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
import os,sys, time
from PyQt4 import QtCore, QtGui
from mainApp import *
from launcherUI import *

class launcherUI(QtCore.QObject):
    def __init__(self, *sys_argv):
        super(launcherUI, self).__init__()

    def launch(self):
        # self.timerThread = updateGUI()
        # self.timerThread.finished.connect(MainWindow.show)
        # self.timerThread.start()

        self.workerThread = runMainApp(self, 'Physical', 'CLARA','10Hz')
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

class updateGUI(QtCore.QThread):
    def __init__(self):
        super(updateGUI, self).__init__()
        # self.app = app
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateGUI)

    def updateGUI(self):
        print 'updating GUI = ', time.time()
        global app
        app.processEvents()

    def start(self):
        self.timer.start(100)

if __name__ == "__main__":
    import sys
    global app
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    launcher = launcherUI()
    MainWindow.show()
    launcher.launch()
    sys.exit(app.exec_())

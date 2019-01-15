import sys,os
'''if needed'''
# from epics import caget,caput

from PyQt4 import QtGui, QtCore
import model.model as model
import controller.controller as controller
import view.view as view
import images_qr
import numpy as np
import time

class GenericThread(QtCore.QThread):
    def __init__(self, function, *args, **kwargs):
        QtCore.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.object = self.function(*self.args, **self.kwargs)

class mySplashScreen(QtGui.QSplashScreen):
    def __init__(self, *args, **kwargs):
        super(mySplashScreen, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        print 'mousepress'

class App(QtCore.QObject):
    def __init__(self, app, sys_argv):
        super(App, self).__init__()
        self.app = app
        self.view = view.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.view.setupUi(self.MainWindow)
        self.MainWindow.setWindowIcon(QtGui.QIcon(':/laserShooter.png'))
        splash_pix = QtGui.QPixmap(':/laserShooter.jpg')
        self.splash = QtGui.QSplashScreen(QtGui.QDesktopWidget().screen(), splash_pix)
        self.splash.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.splash.setEnabled(False)
        self.splash.show()
        self.splash.showMessage("<h1><font color='#6BBAFD'>laserShooter Initialising...</font></h1>", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        self.machineType, self.lineType, self.gunType = sys_argv[1],sys_argv[2],sys_argv[3]
        app.processEvents()
        self.model = model.Model(self.machineType, self.lineType, self.gunType)
        app.processEvents()
        self.controller = controller.Controller(app, self.view, self.model)
        self.MainWindow.show()
        self.splash.finish(self.MainWindow)

    def setupModel(self):
        self.model = model.Model(self.machineType, self.lineType, self.gunType)

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    appObject = App(app, sys.argv)
    sys.exit(app.exec_())

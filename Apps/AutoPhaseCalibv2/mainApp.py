import sys,os
'''if needed'''
# from epics import caget,caput

from PyQt4 import QtGui, QtCore
import model.model as model
import controller.controller as controller
import view.view as view
import images_qr
import numpy as np

class App(QtCore.QObject):
    def __init__(self, sys_argv):
        super(App, self).__init__()
        self.view = view.Ui_MainWindow()
        self.MainWindow = QtGui.QMainWindow()
        self.view.setupUi(self.MainWindow)
        self.MainWindow.setWindowIcon(QtGui.QIcon(':/crester.png'))
        splash_pix = QtGui.QPixmap(':/crester.png')
        splash = QtGui.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
        splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
        splash.setEnabled(False)
        splash.show()
        splash.showMessage("<h1><font color='#6BBAFD'>Autocrester Initialising...</font></h1>", QtCore.Qt.AlignTop | QtCore.Qt.AlignCenter, QtCore.Qt.black)
        self.machineType, self.lineType, self.gunType = sys_argv[1],sys_argv[2],sys_argv[3]
        self.model = model.Model(self.machineType, self.lineType, self.gunType)
        self.controller = controller.Controller(self.view, self.model)
        self.MainWindow.show()
        splash.finish(self.MainWindow)

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    appObject = App(sys.argv)
    sys.exit(app.exec_())

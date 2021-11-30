import sys,os
'''if needed'''
# from epics import caget,caput
sys.path.append("../../../")
import Software.Procedures.qt as qt
import Software.Procedures.linacTiming as linacTiming
import model.model as model
import controller.controller as controller
# if (float(qt.QT_VERSION_STR.split('.')[0]) < 5.0):
import view.view4 as view
import images_qr4
# else:
    # import view.view as view
    # import images_qr
import numpy as np
import time

class GenericThread(qt.QThread):
    def __init__(self, function, *args, **kwargs):
        qt.QThread.__init__(self)
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.object = self.function(*self.args, **self.kwargs)

class mySplashScreen(qt.QSplashScreen):
    def __init__(self, *args, **kwargs):
        super(mySplashScreen, self).__init__(*args, **kwargs)

    def mousePressEvent(self, event):
        print('mousepress')

class App(qt.QObject):
    def __init__(self, app, sys_argv):
        super(App, self).__init__()
        self.view = view.Ui_MainWindow()
        self.MainWindow = qt.QMainWindow()
        self.view.setupUi(self.MainWindow)
        self.MainWindow.setWindowIcon(qt.QIcon(':/ctr.png'))
        splash_pix = qt.QPixmap(':/ctr.png')
        self.splash = qt.QSplashScreen(splash_pix)
        self.splash.setWindowFlags(qt.Qt.FramelessWindowHint)
        self.splash.setEnabled(False)
        self.splash.show()
        self.splash.showMessage("<h1><font color='#6BBAFD'>CTRApp Initialising...</font></h1>", qt.Qt.AlignTop | qt.Qt.AlignCenter, qt.Qt.black)
        self.machineType, self.lineType, self.gunType = ['Physical', 'CLARA', '10Hz']
        app.processEvents()
        self.model = model.Model(self.machineType, self.lineType, self.gunType)
        app.processEvents()
        self.controller = controller.Controller(self.view, self.model)
        self.MainWindow.show()
        self.splash.finish(self.MainWindow)

    def setupModel(self):
        self.model = model.Model(self.machineType, self.lineType, self.gunType)

if __name__ == '__main__':
    app = qt.QApplication(sys.argv)
    appObject = App(app, sys.argv)
    sys.exit(app.exec_())

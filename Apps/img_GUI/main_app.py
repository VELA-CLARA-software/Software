import sys
import os

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

sys.path.append(os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'Model'))
sys.path.append(os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'Controller'))
sys.path.append(os.path.join(str(os.path.dirname(os.path.abspath(__file__))), 'View'))

from Controller import unified_controller, ControllerRun, ControllerPostProcessing
from View import view
from Model import model


class MainApp(QObject):

    def __init__(self, app, sys_argv):

        super(MainApp, self).__init__()
        self.app = app
        self.view = view.Ui_MainWindow()
        self.model = model.Model()
        self.MainWindow = QMainWindow()
        self.view.setupUi(self.MainWindow)
        self.ControllerRun = ControllerRun.ControllerRun(app, self.view, self.model)
        self.UnifiedController = unified_controller.UnifiedController(self.ControllerRun)
        self.MainWindow.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app_object = MainApp(app, sys.argv)
    sys.exit(app.exec_())

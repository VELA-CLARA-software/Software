import sys,os
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\View')
from PyQt4 import QtGui, QtCore
import win32com.client
import mainModel
import mainController
import mainView

scope=win32com.client.Dispatch("LeCroy.XStreamDSO")

class App(QtGui.QApplication):
    def __init__(self, sys_argv):
		super(App, self).__init__(sys_argv)


		
		self.model = mainModel.Model()#Function fot when stuff ist change and buttons are clicked

		self.view = mainView.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)

		self.controller = mainController.Controller(self.view, self.model)

		self.MainWindow.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

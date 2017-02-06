import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM 
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"



sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\Controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\View')
from PyQt4 import QtGui, QtCore

import mainModel
import mainController
import mainView_v1_1 as mainView

class App(QtGui.QApplication):
    def __init__(self, sys_argv):
		super(App, self).__init__(sys_argv)


		print'Well this is fun'
		#self.model = mainModel.Model()#Function fot when stuff ist change and buttons are clicked
		self.view = mainView.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)
		self.model = mainModel.Model(self.view)#Function fot when stuff ist change and buttons are clicked
		self.controller = mainController.Controller(self.view, self.model)

		self.MainWindow.show()

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

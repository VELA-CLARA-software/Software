import sys,os
os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12" #BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
from PyQt4 import QtGui, QtCore
#import model_VELA as model
import model_CLARA as model
import controller.controller
import view.view


class App(QtGui.QApplication):
	def __init__(self, sys_argv):
		super(App, self).__init__(sys_argv)
		print'Well this is fun'
		print view
		self.view = view.view.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)
		self.model = model.Model(self.view)
		print 'Model done'
		self.controller = controller.controller.Controller(self.view,self.model)
		self.MainWindow.show()


if __name__ == '__main__':
	app = App(sys.argv)
	sys.exit(app.exec_())

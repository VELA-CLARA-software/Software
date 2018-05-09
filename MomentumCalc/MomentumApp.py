import sys,os
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
from PyQt4 import QtGui, QtCore
import model.mtmcalc as mtmcalc
import controller.controller as controller
import view.mtmgui as mtmgui

class App(QtGui.QApplication):
	def __init__(self, sys_argv):
		super(App, self).__init__(sys_argv)
		self.view= mtmgui.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)
		self.model = mtmcalc.calc()
		self.controller = controller.controllerer(self.view,self.model)
		self.MainWindow.show()


if __name__ == '__main__':

	app = App(sys.argv)
	sys.exit(app.exec_())

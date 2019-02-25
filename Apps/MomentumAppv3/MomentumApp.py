from PyQt4 import QtGui, QtCore
import controller.control as controller
import view.view_v2 as view
import model.model as model
import data.data as data
import sys

class App(QtCore.QObject):
	def __init__(self, sys_argv):
		super(App, self).__init__()
		self.view = view.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.data = data.data()
		self.view.setupUi(self.MainWindow)
		self.model = model.Model(self, self.view, self.data)
		self.controller = controller.Controller(self.view, self.model)
		self.MainWindow.show()

if __name__ == '__main__':
	app = QtGui.QApplication(sys.argv)
	appObject = App(sys.argv)
	sys.exit(app.exec_())

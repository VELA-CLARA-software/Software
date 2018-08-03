import sys,os
'''if needed'''
# from epics import caget,caput

from PyQt4 import QtGui, QtCore
import model.model as model
import controller.controller as controller
import view.view as view

class App(QtCore.QObject):
	def __init__(self, sys_argv):
		super(App, self).__init__()
		self.view = view.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)
		self.machineType, self.lineType, self.gunType = sys_argv[1],sys_argv[2],sys_argv[3]
		self.model = model.Model(self.machineType, self.lineType, self.gunType)
		self.controller = controller.Controller(self.view, self.model)
		self.MainWindow.show()


if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	appObject = App(sys.argv)
	sys.exit(app.exec_())

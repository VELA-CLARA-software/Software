import sys,os
os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\root_v5.34.34\\bin\\'
os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage\\'
from PyQt4 import QtGui, QtCore
import model.model as model
import controller.controller as controller
import view.view as view
<<<<<<< HEAD
#import qdarkstyle
#import qdarkgraystyle
=======

>>>>>>> refs/remotes/origin/master

class App(QtGui.QApplication):
	def __init__(self, sys_argv):     
		super(App, self).__init__(sys_argv)
		print'Well this is fun'
		self.view= view.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)
		self.model = model.Model()
		self.controller = controller.Controller(self.view,self.model)
		self.MainWindow.show()


if __name__ == '__main__':

	app = App(sys.argv)
<<<<<<< HEAD
	#app.setStyleSheet(qdarkstyle.load_stylesheet())
#	app.setStyleSheet(qdarkgraystyle.load_stylesheet())
=======

>>>>>>> refs/remotes/origin/master
	sys.exit(app.exec_())

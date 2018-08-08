import sys,os

#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
#from PyQt4 import QtGui, QtCore
#import model_VELA as model
# if mode=='virtual':
# 	import model_CLARA_SAMPL as model
# 	import controller.controller_SAMPL as controller
# 	import view.view1_2 as view
# elif mode=='physical':
# 	import model_CLARA as model
# 	import controller.controller as controller
# 	import view.view1_2 as view
import camera_test_class as camera

class App():
	def __init__(self):
		#super(App, self).__init__()
		print'Well this is fun'
		self.model = camera.Model()
		print 'Model done'

a = App()

# if __name__ == '__main__':
# 	#app = App(sys.argv)
# 	#sys.exit(app.exec_())
# 	app = QtGui.QApplication(sys.argv)
# 	appObject = App(sys.argv)
# 	sys.exit(app.exec_())

# Message Pad widget testing
# Version Jan 2019
# DJS
# rf_ccondition owns all other objects and does nothing else
#An attmept to make a message pad that echos stdout to an overloaded QT widget

import sys

sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Realse')

from PyQt4 import QtGui
from src.controller.controller import controller


class main_application(QtGui.QApplication):
	def __init__(self, argv):
		#
		# you need this init line here to instantiate a QTApplication
		QtGui.QApplication.__init__(self, argv)
		#
		# only run if a config file was passed
		if len(argv) == 2:
			#
			# Everything is handled by a main _controller
			self.controller = controller(argv)


if __name__ == '__main__':
	print('Starting Application')
	app = main_application(sys.argv)
	sys.exit(app.exec_())





































# from PyQt4.QtGui import *
# import gui.splash as splash
# import time
#
# if __name__ == "__main__":
#
# 	# movie = QMovie(os.getcwd()+'\splash\' + random.choice(os.listdir(os.getcwd()+'\splash')))
# 	# movie = QMovie(a)
#     #
# 	# splash = MovieSplashScreen(movie)
#     #
# 	# splash.show()
#
# 	pp = QApplication(sys.argv)
#
# 	movie = splash.work()
#
#
# 	app = rf_condition(sys.argv)
#
# 	start = time.time()
# 	while movie.state() == QMovie.Running and time.time() < start + 10:
# 		pp.processEvents()
#
#
#
# 	#app = rf_condition(sys.argv)
#
# 	# start = time.time()
#     #
# 	# while movie.state() == QMovie.Running and time.time() < start + 10:
# 	# 	app.processEvents()
#
# 	sys.exit(app.exec_())
#
# 	#window = QWidget()
# 	#window.show()
# 	splash.splash.finish()
#
# 	sys.exit(app.exec_())
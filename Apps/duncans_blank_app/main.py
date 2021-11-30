'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   05-06-2018
//  FileName:    main.py
//  Description: Generic template for __main__ for general High Level Application
//
//
//*/
'''

'''******** Import modules *********'''
'''
the sys module is used to add to the PATH environment variable and to enable arguments to be 
passed to the application on start-up 
'''
import sys
''' 
QApplication is the top-level class we create, 
'''
from PyQt4.QtGui import QApplication
'''
Import the controller class, everything 
'''
from src.controller.controller import controller

# Add the release folder to the path to get latest HWC
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\packages\\vcc\\bin\\Stage\\')


class main_application(QApplication):
	'''
		Simple class to own the main controller
		Everything else is crated is amanged controller
	'''
	def __init__(self, argv):
		#
		# you need this init line here to instantiate a QApplication
		QApplication.__init__(self, argv)
		#
		# Everything is handled by a controller
		self.controller = controller(argv)


if __name__ == '__main__':
	APPLICATION_NAME = "Demonstration Application"
	print('Starting ' + APPLICATION_NAME)
	''' 
		sys.argv are the paramters passed from the command line
		e.g to run this you might type python 
	'''
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
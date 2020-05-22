# RF conditioning Script
# Version Dec 2018
# DJS
# This is the main filoe that creates the rf_condition object
# rf_ccondition owns all other objects and does nothing else
# os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
# os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
# os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
# Hardware Controllers (.pyd)
import os
import sys
from src.controllers.output_redirection import *
# if os.environ['COMPUTERNAME'] == "DJS56PORT2":
# 	sys.path.append(os.getcwd())
# else:
<<<<<<< HEAD
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
=======
>>>>>>> parent of 8dd1763... push old stuff ...  :(
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')

from PyQt4 import QtGui
import VELA_CLARA_enums

print('import main_controller')
from src.controllers.main_controller import main_controller





class rf_condition(QtGui.QApplication):
    DEBUG_MODE = True
    def __init__(self, argv):
        #
        # you need this init line here to instantiate a QTApplication
        QtGui.QApplication.__init__(self, argv)
        #
        # only run if a config file was passed
        if len(argv) == 3:
            #
            # Everything is handled by a main _controller
            self.controller = main_controller(argv, config_file=argv[1], debug=argv[2],
                                              debug2=rf_condition.DEBUG_MODE)

if __name__ == '__main__':
    print('Starting rf_condition Application')
    app = rf_condition(sys.argv)
    sys.exit(app.exec_())






# from PyQt4.QtGui import *
# import gui.splash as splash
# import time
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
#

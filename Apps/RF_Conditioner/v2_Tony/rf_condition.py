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

#TODO AJG: use'\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage' not'
# \\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage'

sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')
#TODO AJG: I had to append this (below)on to the sys.path... it couldn't find it in stePackages
sys.path.append('C:\\Users\\zup98752\\PycharmProjects\\Software\\Apps\\RF_Conditioner\\v2_Tony\\src\\view')

#Checking sys.path members
print 'os.path = ', os.path
print 'sys.path = ', sys.path

from PyQt4 import QtGui

#TODO AJG: Getting "ImportError: DLL load failed: %1 is not a valid Win32 application."
# trying to resolve below....
# It is being read correctly from <open file '\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers
# \\bin\\stage\\VELA_CLARA_enums.pyd', mode 'rb' at 0x000000000307A420>
# It is having trouble reading the 'VELA_CLARA_enums.pyd file'.
import platform
print 'platform.architecture()[0] = ', platform.architecture()[0]
import imp
DLLFail = imp.find_module("rf_condition_view_base")
print DLLFail

#Trying these...



from rf_condition_view_base import Ui_rf_condition_mainWindow


from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
##
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from VELA_CLARA_RF_Protection_Control import RF_PROT_TYPE
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_RF_Modulator_Control import L01_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
#######################################
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

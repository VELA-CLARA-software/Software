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
#sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\stage')

#TODO AJG: I had to append this (below)on to the sys.path... it couldn't find it in stePackages
sys.path.append('C:\\Users\\zup98752\\PycharmProjects\\Software\\Apps\\RF_Conditioner\\v2_Tony\\src\\view')
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\release')

#Checking sys.path members
#print 'os.path = ', os.path
#print 'sys.path = ', sys.path


#TODO RESOLVED AJG: Getting "ImportError: DLL load failed: %1 is not a valid Win32 application."
# trying to resolve below....
# It is being read correctly from <open file '\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers
# \\bin\\stage\\VELA_CLARA_enums.pyd', mode 'rb' at 0x000000000307A420>
# It is having trouble reading the 'VELA_CLARA_enums.pyd file'.
# The RESOLUTION was to completely uninstall python, delete the python27 folder
# and reinstall python and all modules.
import VELA_CLARA_enums
from VELA_CLARA_enums import *
from VELA_CLARA_enums import MACHINE_MODE

import platform
print 'platform.architecture()[0] = ', platform.architecture()[0]
import imp
DLLFail = imp.find_module("VELA_CLARA_enums")
print 'importing module from:', DLLFail
from PyQt4 import QtGui
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from VELA_CLARA_RF_Protection_Control import RF_PROT_TYPE
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_RF_Modulator_Control import L01_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from rf_condition_view_base import Ui_rf_condition_mainWindow

#######################################

print('import main_controller')
from src.controllers.main_controller import main_controller


class rf_condition(QtGui.QApplication):
    DEBUG_MODE = True
    def __init__(self, argv):

        '''
        # TODO AJG: trying to get more details about why python is crashing
        #  with "Process finished with exit code -1073741819 (0xC0000005)"
        #  as suggested online
        sys._excepthook = sys.excepthook

        def my_exception_hook(exctype, value, traceback):
            # Print the error and traceback
            print(exctype, value, traceback)
            # Call the normal Exception hook after
            sys._excepthook(exctype, value, traceback)
            sys.exit(1)

        # Set the exception hook to our wrapping function
        sys.excepthook = my_exception_hook
        '''
        #
        # you need this init line here to instantiate a QTApplication
        QtGui.QApplication.__init__(self, argv)
        #
        # only run if a config file was passed
        print 'len(argv) = ', len(argv)
        if len(argv) == 3:
            #
            # Everything is handled by a main _controller
            self.controller = main_controller(argv, config_file=argv[1], debug=argv[2],
                                              debug2=rf_condition.DEBUG_MODE)

if __name__ == '__main__':

    print('Starting rf_condition Application (rf_condition.py)')
    app = rf_condition(sys.argv)

    '''
    # TODO AJG: Second part of trying to get more details about why python is crashing
    # with "Process finished with exit code -1073741819 (0xC0000005)"
    # as suggested online:

    try:
        sys.exit(app.exec_())
    except:
        print("Exiting")
    '''
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

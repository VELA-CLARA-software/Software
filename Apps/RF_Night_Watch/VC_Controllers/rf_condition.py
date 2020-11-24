'''

    August 2020
    This is a simple class, and the __main__ attribute for the RF conditioning app v2.x

'''
import sys
sys.path.append('\\\\claraserv3\\claranet\\test\\Controllers\\bin\\Release')
#sys.path.append('\\\\claraserv3\\claranet\\test\\Controllers\\bin\\stage')
#
# often hen bugfixing which libraries get loaded it helps to print the path variable
# if os.environ['COMPUTERNAME'] == "DJS56PORT2":
# 	sys.path.append(os.getcwd())
# else:
# sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\')
# sys.path.append('\\\\claraserv3\\apclara\\test\\Controllers\\bin\\stage')
from PyQt4 import QtGui
from src.controllers.output_redirection import *# enables us to resend stdout adn stderr statements to a qt widget
print('import main_controller')
from src.controllers.main_controller import main_controller



class rf_condition(QtGui.QApplication):
    '''
        mainly a wrapper class that just gets things started, doesn't do much except pyqt app and main_controller  startup
    '''
    # DEBUG_MODE = True
    DEBUG_MODE = False
    def __init__(self, argv):
        #
        # you need this init line here to instantiate a QTApplication
        QtGui.QApplication.__init__(self, argv)
        #
        # only run if a config file and a number  was passed
        if len(argv) == 3:
            self.controller = main_controller(argv, config_file=argv[1], debug = int(argv[2]), debug2=rf_condition.DEBUG_MODE)
        else:
            config_file = "\\\\claraserv3\\claranet\\apps\\legacy\\config\\RF_Night_Watch\\CLARA_LRRG.yml"
            self.controller = main_controller(argv, config_file=config_file, debug = 0,
                                              debug2=rf_condition.DEBUG_MODE)
            print("!!ERROR!! WHEN STARTING RF_CONDITION __MAIN__  NOT ENOUGH INPUT VARIABLES PASSED ")


if __name__ == '__main__':
    print('Starting rf_condition Application')
    app = rf_condition(sys.argv)
    sys.exit(app.exec_())

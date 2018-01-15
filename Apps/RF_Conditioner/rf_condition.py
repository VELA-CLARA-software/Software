# RF conditioning Script
# Version 3
# DJS
# This is the main filoe that creates the rf_condition object
# rf_ccondition owns all other objects and does nothing else
import os
import sys
from PyQt4 import QtGui
import VELA_CLARA_enums
from controllers.main_controller import main_controller

if os.environ['COMPUTERNAME'] == "DJS56PORT2":
	print 'port'
	sys.path.append(os.getcwd())
else:
	print 'desk'
	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')


# os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
# os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
# os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
# Hardware Controllers (.pyd)



class rf_condition(QtGui.QApplication):
	def __init__(self, argv):
		# you need this init line here to instantiate a QTApplication
		QtGui.QApplication.__init__(self, argv)
		# Everything else is handled by a main _controller
		self.controller = main_controller(argv, config_file='test.config')


if __name__ == '__main__':
	print('Starting rf_condition Application')
	app = rf_condition(sys.argv)
	sys.exit(app.exec_())

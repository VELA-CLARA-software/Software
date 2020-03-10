import os
import sys
print(sys.path)
# if os.environ['COMPUTERNAME'] == "ASTECDELL10":
# 	print 'port'
# 	sys.path.append(os.getcwd())
# 	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
# else:
# 	print 'desk'
# 	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
from PyQt5 import QtGui
from controllers.main_controller import main_controller

# os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
# os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"# 192.168.83.255"
# os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
# os.environ["EPICS_CA_SERVER_PORT"] = "6000"

class bpm_calibrate(QtGui.QApplication):
	def __init__(self, argv):
		# you need this init line here to instantiate a QTApplication
		QtGui.QApplication.__init__(self, argv)
		# Everything else is handled by a main _controller
		self.controller = main_controller(argv, config_file='bpm_calibrate.config')


if __name__ == '__main__':
	print('Starting bpm_calibrate Application')
	app = bpm_calibrate(sys.argv)
	sys.exit(app.exec_())
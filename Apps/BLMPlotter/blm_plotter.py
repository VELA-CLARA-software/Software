import os
import sys
import VELA_CLARA_enums as vce
print sys.path
# if os.environ['COMPUTERNAME'] == "ASTECDELL10":
# 	print 'port'
# 	sys.path.append(os.getcwd())
# 	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
# else:
# 	print 'desk'
# 	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')
from PyQt4 import QtGui
from controllers.main_controller import main_controller

#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
#os.environ["EPICS_CA_SERVER_PORT"] = "6000"

class blm_plotter(QtGui.QApplication):
	def __init__(self, argv):
		# you need this init line here to instantiate a QTApplication
		QtGui.QApplication.__init__(self, argv)
		# Everything else is handled by a main _controller
		self.controller = main_controller(argv, machine_mode=vce.MACHINE_MODE.PHYSICAL, machine_area=vce.MACHINE_AREA.CLARA_2_BA1_BA2, blm_name="CLARABLM01")# , config_file='bpm_calibrate.config')


if __name__ == '__main__':
	print('Starting blm_plotter Application')
	app = blm_plotter(sys.argv)
	sys.exit(app.exec_())
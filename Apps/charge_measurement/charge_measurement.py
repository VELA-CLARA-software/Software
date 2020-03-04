import os
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
dir_path = os.path.dirname(os.path.realpath(__file__))

parent_dir_path = os.path.abspath(os.path.join(dir_path, os.pardir))

sys.path.insert(0, parent_dir_path)
sys.path.append(os.path.join(sys.path[0],'base'))
sys.path.append(os.path.join(sys.path[0],'controllers'))
sys.path.append(os.path.join(sys.path[0],'data'))
sys.path.append(os.path.join(sys.path[0],'data_monitors'))
sys.path.append(os.path.join(sys.path[0],'gui'))
sys.path.append(os.path.join(sys.path[0],'logs'))
sys.path.append(dir_path)
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
# os.environ["EPICS_CA_SERVER_PORT"] = "600"

class charge_measurement(QtGui.QApplication):
	def __init__(self, argv):
		# you need this init line here to instantiate a QTApplication
		QtGui.QApplication.__init__(self, argv)
		# Everything else is handled by a main _controller
		self.controller = main_controller(argv, config_file='\\\\apclara1\\ControlRoomApps\\Stage\\Software\\Apps\\charge_measurement\\charge_measurement.config')


if __name__ == '__main__':
	print('Starting charge_measurement Application')
	app = charge_measurement(sys.argv)
	sys.exit(app.exec_())
import sys, os
sys.path.append(os.path.join(sys.path[0],'base'))
sys.path.append(os.path.join(sys.path[0],'controllers'))
sys.path.append(os.path.join(sys.path[0],'data'))
sys.path.append(os.path.join(sys.path[0],'data_monitors'))
sys.path.append(os.path.join(sys.path[0],'gui'))
sys.path.append(os.path.join(sys.path[0],'logs'))


for item in sys.path:
  if "PythonInterface" not in str(item):
    continue
  else:
    sys.path.remove(item)
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\development\\CATAP\\djs56\\new_pc\\build\\PythonInterface\\Release\\CATAP')
sys.path.append('\\\\192.168.83.14\\claranet\\test\\Controllers\\bin\\python3_x64')



from PyQt5 import QtGui, QtWidgets
from controllers.main_controller import main_controller

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255" #"10.10.0.12"#
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
# os.environ["EPICS_CA_SERVER_PORT"] = "600"

class charge_measurement(QtWidgets.QApplication):
	def __init__(self, argv):
		# you need this init line here to instantiate a QTApplication
		QtWidgets.QApplication.__init__(self, argv)
		# Everything else is handled by a main _controller
		self.controller = main_controller(argv,
										  config_file='\\\\192.168.83.14\\claranet\\apps\\stage\\config\\charge_measurement\\charge_measurement.config')


if __name__ == '__main__':
	print('Starting charge_measurement Application')
	app = charge_measurement(sys.argv)
	sys.exit(app.exec_())
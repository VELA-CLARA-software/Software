import sys,os
'''if needed'''
# from epics import caget,caput

'''This is the place to get contollers'''
sys.path.append(r'\\apclara1\ControlRoomApps\Controllers\bin\Release')
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_BPM_Control as bpm
import VELA_CLARA_LLRF_Control as llrf
import VELA_CLARA_Charge_Control as scope

from PyQt4 import QtGui, QtCore
import model.model as model
import controller.controller as controller
import view.view as view

class App(QtCore.QObject):
	def __init__(self, sys_argv):
		super(App, self).__init__()
		print'Well this is fun'
		self.view= view.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)
		self.machineType, self.lineType, self.gunType = sys_argv[1],sys_argv[2],sys_argv[3]
		self.setUpCtrls()
		self.model = model.Model(self, self.view, self.machineType, self.lineType, self.gunType, self.magnets, self.scope, self.bpms, self.gun, self.linac)
		self.controller = controller.Controller(self.view, self.model)
		self.MainWindow.show()

	def setUpCtrls(self):
		self.magInit = mag.init()
		# self.magInit.setVerbose()
		self.bpmInit = bpm.init()
		self.llrfInit = llrf.init()
		self.scopeInit = scope.init()
		if self.machineType == 'Virtual':
			os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
			os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
			os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
			os.environ["EPICS_CA_SERVER_PORT"]="6000"
		if self.lineType == 'VELA'and self.machineType == 'Physical':
			self.magnets = self.magInit.physical_VELA_INJ_Magnet_Controller()
			self.scope = self.scopeInit.physical_VELA_INJ_Charge_Controller()
			self.bpms = self.bpmInit.physical_VELA_INJ_BPM_Controller()
			self.gun = self.llrfInit.physical_VELA_LRRG_LLRF_Controller()
			self.linac = None
		elif self.lineType == 'CLARA'and self.machineType == 'Physical':
			self.magnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
			self.scope = self.scopeInit.physical_CLARA_PH1_Charge_Controller()
			self.bpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
			self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
			self.linac = self.llrfInit.physical_L01_LLRF_Controller()
		elif self.lineType == 'VELA'and self.machineType == 'Virtual':
			self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
			self.scope = self.scopeInit.virtual_VELA_INJ_Charge_Controller()
			self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
			self.gun = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
			self.linac = None
		elif self.lineType == 'CLARA'and self.machineType == 'Virtual':
			self.magnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
			self.scope = self.scopeInit.virtual_CLARA_PH1_Charge_Controller()
			self.bpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
			self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
			self.linac = self.llrfInit.virtual_L01_LLRF_Controller()

if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	appObject = App(sys.argv)
	sys.exit(app.exec_())

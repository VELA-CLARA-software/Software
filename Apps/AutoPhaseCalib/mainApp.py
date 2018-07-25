import sys,os
'''if needed'''
# from epics import caget,caput

from PyQt4 import QtGui, QtCore
import model.model as model
import controller.controller as controller
import view.view as view

class App(QtCore.QObject):
	def __init__(self, sys_argv):
		super(App, self).__init__()
		self.view = view.Ui_MainWindow()
		self.MainWindow = QtGui.QMainWindow()
		self.view.setupUi(self.MainWindow)
		self.machineType, self.lineType, self.gunType = sys_argv[1],sys_argv[2],sys_argv[3]
		self.setUpCtrls()
		self.model = model.Model(self.machineType, self.lineType, self.gunType, self.magnets, self.scope, self.bpms, self.gun, self.linac, self.cameras)
		self.controller = controller.Controller(self.view, self.model)
		self.MainWindow.show()

	def setUpCtrls(self):
		if self.machineType == 'None':
			print 'No controllers!'
			self.magnets = None
			self.scope = None
			self.bpms = None
			self.gun = None
			self.linac = None
			self.cameras = None
		else:
			'''This is the place to get contollers'''
			sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release')
			os.environ["PATH"] = os.environ["PATH"]+";\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\root_v5.34.34\\bin\\"
			import VELA_CLARA_Magnet_Control as mag
			import VELA_CLARA_BPM_Control as bpm
			import VELA_CLARA_LLRF_Control as llrf
			import VELA_CLARA_Charge_Control as scope
			import VELA_CLARA_Camera_IA_Control as camIA
			
			self.magInit = mag.init()
			self.magInit.setQuiet()
			self.bpmInit = bpm.init()
			self.bpmInit.setQuiet()
			self.llrfInit = llrf.init()
			self.llrfInit.setQuiet()
			self.scopeInit = scope.init()
			self.scopeInit.setQuiet()
			self.camInit = camIA.init()
			self.camInit.setQuiet()
			if self.machineType == 'Virtual':
				os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
				os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
				os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
				os.environ["EPICS_CA_SERVER_PORT"]="6000"
				sys.path.append('C:\\anaconda32\\Work\\OnlineModel')
				if self.lineType == 'VELA':
					self.magnets = self.magInit.virtual_VELA_INJ_Magnet_Controller()
					self.scope = self.scopeInit.virtual_VELA_INJ_Charge_Controller()
					self.bpms = self.bpmInit.virtual_VELA_INJ_BPM_Controller()
					self.gun = self.llrfInit.virtual_VELA_LRRG_LLRF_Controller()
					self.linac = None
					self.cameras = None
				else:
					self.magnets = self.magInit.virtual_CLARA_PH1_Magnet_Controller()
					self.scope = self.scopeInit.virtual_CLARA_PH1_Charge_Controller()
					self.bpms = self.bpmInit.virtual_CLARA_PH1_BPM_Controller()
					self.gun = self.llrfInit.virtual_CLARA_LRRG_LLRF_Controller()
					self.linac = self.llrfInit.virtual_L01_LLRF_Controller()
					self.cameras = self.camInit.virtual_CLARA_Camera_IA_Controller()
			elif self.machineType == 'Physical':
				print 'PHYSICAL CONTROLLERS!'
				if self.lineType == 'VELA':
					self.magnets = self.magInit.physical_VELA_INJ_Magnet_Controller()
					self.scope = self.scopeInit.physical_VELA_INJ_Charge_Controller()
					self.bpms = self.bpmInit.physical_VELA_INJ_BPM_Controller()
					self.gun = self.llrfInit.physical_VELA_LRRG_LLRF_Controller()
					self.linac = None
					self.cameras = None
				else:
					self.magnets = self.magInit.physical_CLARA_PH1_Magnet_Controller()
					self.scope = self.scopeInit.physical_CLARA_PH1_Charge_Controller()
					self.bpms = self.bpmInit.physical_CLARA_PH1_BPM_Controller()
					self.gun = self.llrfInit.physical_CLARA_LRRG_LLRF_Controller()
					self.linac = self.llrfInit.physical_L01_LLRF_Controller()
					self.cameras = None


if __name__ == '__main__':

	app = QtGui.QApplication(sys.argv)
	appObject = App(sys.argv)
	sys.exit(app.exec_())

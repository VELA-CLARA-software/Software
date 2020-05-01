import os, sys
import numpy
sys.path.append(os.path.abspath(__file__+'/../../CATAP-build/PythonInterface/Debug'))
import CATAP
import unit_conversion

mode = "virtual"

catap_modules = ['BPM','Charge','Screen','Magnet']
vc_controller_modules = ['Camera', 'LLRF','PILaser']

class GetDataFromCATAP(object):

	def __init__(self):
		object.__init__(self)
		self.my_name="GetDataFromCATAP"
		self.unitConversion = unit_conversion.UnitConversion()
		self.energy = 1
		self.magDict = {}
		self.gunRFDict = {}
		self.l01RFDict = {}
		self.pilaserDict = {}
		self.chargeDict = {}
		self.cameraDict = {}
		self.bpmDict = {}
		self.screenDict = {}
		self.allDataDict = {}
		
		self.bpmdata = {}
		self.chargedata = {}
		self.cameradata = {}
		self.screendata = {}
		self.magnetdata = {}
		self.pildata = {}
		self.gundata = {}
		self.linacdata = {}
		self.alldata = {}
		
		self.dictsSet = False
		
	def initCATAP(self, mode):
		# setup environment
		#if mode == CATAP.STATE.VIRTUAL:
		os.environ["EPICS_CA_ADDR_LIST"]="10.10.0.12"
		os.environ["EPICS_CA_AUTO_ADDR_LIST"]="NO"
		os.environ["EPICS_CA_SERVER_PORT"]="6000"
		os.environ["EPICS_CA_MAX_ARRAY_BYTES"]="1000000000"
			# get factories
		self.hf = CATAP.HardwareFactory(mode)
		self.hf.debugMessagesOff()
		self.chargeFac = self.hf.getChargeFactory()
		self.bpmFac = self.hf.getBPMFactory()
		self.scrFac = self.hf.getScreenFactory()
		self.magFac = self.hf.getMagnetFactory()
		#self.gunFac = hf.getGUN()
		#self.l01Fac = hf.getl01()
		#self.pilFac = hf.getPILa()
		#self.camFac = hf.getcam()
			
	def setBPMDict(self):
		self.bpmnames = self.bpmFac.getAllBPMNames()
		for i in self.bpmnames:
			self.bpmDict[i] = self.bpmFac.getBPM(i)
		self.allDataDict.update({"BPM": self.bpmDict})

	def setMagDict(self):
		self.magnames = self.magFac.getAllMagnetNames()
		for i in self.magnames:
			self.magDict[i] = self.magFac.getMagnet(i)
		self.allDataDict.update({"Magnet": self.magDict})
	
	def setChargeDict(self):
		self.chargenames = self.chargeFac.getAllChargeDiagnosticNames()
		for i in self.chargenames:
			self.chargeDict[i] = self.chargeFac.getChargeDiagnostic(i)
		self.allDataDict.update({"Charge": self.chargeDict})

			
	def setCameraDict(self):
		self.camnames = self.camFac.getAllCameraNames()
		for i in self.camnames:
			self.cameraDict[i] = self.camFac.getCamera(i)
		self.allDataDict.update({"Camera": self.cameraDict})

			
	def setScreenDict(self):
		self.screennames = self.scrFac.getAllScreenNames()
		for i in self.screennames:
			self.screenDict[i] = self.scrFac.getScreen(i)
		self.allDataDict.update({"Screen": self.screenDict})

			
	def setAllDicts(self):
		self.setBPMDict()
		self.setMagDict()
		self.setChargeDict()
		# self.setCameraDict()
		self.setScreenDict()
		self.dictsSet = True
		return self.allDataDict
			
	def getBPMData(self,name):
		if self.dictsSet:
			self.bpmdata[name] = {}
			self.bpmdata[name]['x'] = self.bpmDict[name].x
			self.bpmdata[name]['y'] = self.bpmDict[name].y
			self.bpmdata[name]['q'] = self.bpmDict[name].q
			self.bpmdata[name]['resolution'] = self.bpmDict[name].resolution
			self.alldata.update({name: self.bpmdata[name]})
		else:
			self.setAllDicts()
			self.getBPMData(name)
		
	def getChargeData(self,name):
		if self.dictsSet:
			self.chargedata[name] = {}
			self.chargedata[name]['q'] = self.chargeDict[name].q
			self.alldata.update({name: self.chargedata[name]})
		else:
			self.setAllDicts()
			self.getChargeData(name)
		
	def getScreenData(self,name):
		if self.dictsSet:
			self.screendata[name] = {}
			self.screendata[name]['state'] = self.screenDict[name].screenState
			self.alldata.update({name: self.screendata[name]})
		else:
			self.setAllDicts()
			self.getScreenData(name)
		
	def getMagnetData(self, name, energy):
		if self.dictsSet:
			self.magnetdata[name] = {}
			self.magnetdata[name]['READI'] = self.magDict[name].READI
			# self.magnetdata[name]['k1l'] = self.unitConversion.currentToK(self.magDict[name].magnet_type,
			# 													self.magDict[name].READI,
			# 													self.magDict[name].field_integral_coefficients,
			# 													self.magDict[name].magnetic_length,
			# 													energy)
			self.alldata.update({name: self.magnetdata[name]})
		else:
			self.setAllDicts()
			self.getMagnetData(name)
		
	def getAllData(self):
		if self.dictsSet:
			for i in self.bpmnames:
				self.getBPMData(i)
			for i in self.magnames:
				self.getMagnetData(i, self.energy)
			for i in self.chargenames:
				self.getChargeData(i)
			for i in self.screennames:
				self.getScreenData(i)
		else:
			self.setAllDicts()
			self.getAllData()
		return self.alldata


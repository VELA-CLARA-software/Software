import os, sys
import numpy
import time
sys.path.append(os.path.abspath(__file__+'/../../CATAP-build/PythonInterface/Debug'))
sys.path.append('\\apclara1\ControlRoomApps\Controllers\bin\stage\Python3_x64')
import CATAP.HardwareFactory
import unit_conversion
import aliases

catap_modules = ['BPM', 'Charge', 'Screen', 'Magnet']
vc_controller_modules = ['Camera', 'LLRF', 'PILaser']

class GetDataFromCATAP(object):

	def __init__(self):
		object.__init__(self)
		self.my_name="GetDataFromCATAP"
		self.unitConversion = unit_conversion.UnitConversion()
		self.alias_names = aliases.alias_names
		self.type_alias = aliases.type_alias
		self.screen_alias = aliases.screen_alias
		self.energy = {}
		self.magDict = {}
		self.gunRFDict = {}
		self.l01RFDict = {}
		self.pilaserDict = {}
		self.chargeDict = {}
		self.cameraDict = {}
		self.bpmDict = {}
		self.screenDict = {}
		self.allDataDict = {}
		self.allDictStatus = {}
		
		self.bpmdata = {}
		self.chargedata = {}
		self.cameradata = {}
		self.screendata = {}
		self.magnetdata = {}
		self.pildata = {}
		self.gundata = {}
		self.linacdata = {}
		self.alldata = {}
		self.alldata.update({"INJ": {}})
		self.alldata.update({"S01": {}})
		self.alldata.update({"L01": {}})
		self.alldata.update({"S02": {}})
		self.alldata.update({"C2V": {}})
		self.alldata.update({"BA1": {}})
		self.alldata.update({"VCA": {}})
		self.alldataset = False

		self.linacnames = {}
		self.gunStartTime = 1.0 # MAGIC NUMBER
		self.gunEndTime = 1.4  # MAGIC NUMBER
		self.linacStartTimes = {}
		self.linacEndTimes = {}
		self.guntraces = ['CAVITY_FORWARD_POWER']#, "CAVITY_FORWARD_PHASE"]
		self.linactraces = ['CAVITY_FORWARD_POWER']#, "CAVITY_FORWARD_PHASE"]
		self.gunDataSet = False
		self.linacDataSet = {}
		self.gunEnergyGain = 0.0
		self.linacEnergyGain = {}
		self.gun_length = 0.17 # MAGIC NUMBER (BUT IT WON'T CHANGE)
		self.gun_position = 0.17 # MAGIC NUMBER (BUT IT WON'T CHANGE)
		self.linac_length = {}
		self.linac_length.update({"L01": 2.033}) # MAGIC NUMBER (BUT IT WON'T CHANGE)
		self.linac_position = {}
		self.linac_position.update({"L01": 3.2269}) # MAGIC NUMBER (BUT IT WON'T CHANGE)

		self.CATAPmodeToVCControllermode = {}
		
		self.dictsSet = False
		
	def initCATAP(self,
				  mode,
				  addr_list="10.10.0.12",
				  auto_addr_list="NO",
				  server_port="6000",
				  max_array_bytes="1000000"):
		# setup environment
		if mode == CATAP.HardwareFactory.STATE.VIRTUAL:
			os.environ["EPICS_CA_ADDR_LIST"]=addr_list
			os.environ["EPICS_CA_AUTO_ADDR_LIST"]=auto_addr_list
			os.environ["EPICS_CA_SERVER_PORT"]=server_port
			os.environ["EPICS_CA_MAX_ARRAY_BYTES"]=max_array_bytes
		# get factories / controllers
		self.hf = CATAP.HardwareFactory.HardwareFactory(mode)
		self.hf.debugMessagesOff()
		self.gun_llrf_type = CATAP.HardwareFactory.TYPE.LRRG_GUN
		self.gunFac = self.hf.getLLRFFactory(self.gun_llrf_type)
		self.l01_llrf_type = CATAP.HardwareFactory.TYPE.L01
		self.l01Fac = self.hf.getLLRFFactory(self.l01_llrf_type)
		self.chargeFac = self.hf.getChargeFactory()
		self.bpmFac = self.hf.getBPMFactory()
		self.scrFac = self.hf.getScreenFactory()
		self.magFac = self.hf.getMagnetFactory()
		self.camFac = self.hf.getCameraFactory()

		# #self.pilFac = hf.getPILa()
		# #self.camFac = hf.getcam()
		self.gunname = "LRRG_GUN"
		self.linacnames.update({"L01": self.l01_llrf_type})
		self.linacFac = {}
		self.setGunStartEndTime(self.gunStartTime, self.gunEndTime)
		for key, value in self.linacnames.items():
			self.linacFac.update({key: self.hf.getLLRFFactory(value)})
			self.linacStartTimes.update({key: 0.1}) # MAGIC NUMBER
			self.linacEndTimes.update({key: 1.0}) # MAGIC NUMBER
			self.setLinacStartEndTime(key, self.linacStartTimes[key], self.linacEndTimes[key])
			self.linacDataSet.update({key: False})
			self.linacEnergyGain.update({key: 0.0})
		return True

	def getMachineAreaString(self, name):
		if "INJ" in name or "GUN" in name or "LRG1" in name:
			return "INJ"
		elif "S01" in name:
			return "S01"
		elif "S02" in name:
			return "S02"
		elif "L01" in name:
			return "L01"
		elif "C2V" in name:
			return "C2V"
		elif "BA1" in name:
			return "BA1"
		elif "VCA" in name:
			return "VCA"

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
		self.camnames = self.camFac.getCameraNames()
		for i in self.camnames:
			self.cameraDict[i] = self.camFac.getCamera(i)
			if i == "CLA-VCA-DIA-CAM-01":
				self.cameraDict[i].setX(0)
				self.cameraDict[i].setY(0)
				self.cameraDict[i].setSigX(0.35)
				self.cameraDict[i].setSigY(0.35)
				self.cameraDict[i].setSigXY(0.35)
		self.allDataDict.update({"Camera": self.cameraDict})

	def setScreenDict(self):
		self.screennames = self.scrFac.getAllScreenNames()
		for i in self.screennames:
			self.screenDict[i] = self.scrFac.getScreen(i)
		self.allDataDict.update({"Screen": self.screenDict})

	def setGunLLRFDict(self):
		self.gunLLRFObj = self.gunFac.getLLRF('LRRG_GUN')
		self.allDataDict.update({"LRRG_GUN": self.gunLLRFObj})

	def setLinacLLRFDict(self):
		self.linacLLRFObj = {}
		for key, value in self.linacnames.items():
			self.linacLLRFObj[key] = self.linacFac[key].getLLRF(key)
			self.linacdata.update({key: {}})
			self.allDataDict.update({key: self.linacLLRFObj[key]})

	def setAllDicts(self):
		self.setBPMDict()
		self.setMagDict()
		self.setChargeDict()
		self.setCameraDict()
		self.setScreenDict()
		self.setGunLLRFDict()
		self.setLinacLLRFDict()
		self.dictsSet = True
		return self.allDataDict
			
	def getBPMData(self,name):
		if self.dictsSet:
			self.bpmdata[name] = {}
			self.bpmdata[name]['x'] = self.bpmDict[name].x
			self.bpmdata[name]['y'] = self.bpmDict[name].y
			self.bpmdata[name]['q'] = self.bpmDict[name].q
			self.bpmdata[name]['resolution'] = self.bpmDict[name].resolution
			self.bpmdata[name]['type'] = "bpm"
			self.alldata[self.getMachineAreaString(name)].update({name: self.bpmdata[name]})
		else:
			self.setAllDicts()
			self.getBPMData(name)

	def getCameraData(self,name):
		if self.dictsSet:
			self.cameradata[name] = {}
			self.cameradata[name]['x_pix'] = self.cameraDict[name].getXPix()
			self.cameradata[name]['y_pix'] = self.cameraDict[name].getYPix()
			# self.cameradata[name]['xy_pix'] = self.cameraDict[name].getXYPix()
			self.cameradata[name]['x_mm'] = self.cameraDict[name].getXmm()
			self.cameradata[name]['y_mm'] = self.cameraDict[name].getYmm()
			# self.cameradata[name]['xy_mm'] = self.cameraDict[name].getXYmm()
			self.cameradata[name]['x_pix_sig'] = self.cameraDict[name].getSigXPix()
			self.cameradata[name]['y_pix_sig'] = self.cameraDict[name].getSigYPix()
			# self.cameradata[name]['xy_pix_sig'] = self.cameraDict[name].getSigXYPix()
			self.cameradata[name]['x_mm_sig'] = self.cameraDict[name].getSigXmm()
			self.cameradata[name]['y_mm_sig'] = self.cameraDict[name].getSigYmm()
			# self.cameradata[name]['xy_mm_sig'] = self.cameraDict[name].getSigXYmm()
			self.cameradata[name]['sum_intensity'] = self.cameraDict[name].getSumIntensity()
			self.cameradata[name]['avg_intensity'] = self.cameraDict[name].getAvgIntensity()
			self.cameradata[name]['screen'] = self.cameraDict[name].getScreen()
			if self.cameradata[name]['screen'] in self.screen_alias.keys():
				self.cameradata[name].update({'screen': self.screen_alias[self.cameradata[name]['screen']]})
			self.cameradata[name]['type'] = "camera"
			self.alldata[self.getMachineAreaString(name)].update({name: self.cameradata[name]})
		else:
			self.setAllDicts()
			self.getCameraData(name)
		
	def getChargeData(self,name):
		if self.dictsSet:
			self.chargedata[name] = {}
			self.chargedata[name]['q'] = self.chargeDict[name].q
			self.chargedata[name]['type'] = "charge"
			self.alldata[self.getMachineAreaString(name)].update({name: self.chargedata[name]})
		else:
			self.setAllDicts()
			self.getChargeData(name)
		
	def getScreenData(self,name):
		if self.dictsSet:
			self.screendata[name] = {}
			self.screendata[name]['state'] = str(self.screenDict[name].screenState)
			self.screendata[name]['type'] = "screen"
			self.alldata[self.getMachineAreaString(name)].update({name: self.screendata[name]})
		else:
			self.setAllDicts()
			self.getScreenData(name)
		
	def getMagnetData(self, name, energy):
		if self.dictsSet:
			self.magnetdata[name] = {}
			self.magnetdata[name]['READI'] = self.magDict[name].READI
			self.magnetdata[name]['SETI'] = self.magDict[name].getSETI()
			self.magnetdata[name]['type'] = self.type_alias[self.magDict[name].getMagnetType()]
			self.magnetdata[name]['psu_state'] = str(self.magDict[name].psu_state)
			self.magnetdata[name]['field_integral_coefficients'] = self.magDict[name].getFieldIntegralCoefficients()
			self.magnetdata[name]['magnetic_length'] = self.magDict[name].getMagneticLength()
			self.energy_at_magnet = 0
			if "GUN" in name or "LRG1" in name:
				self.energy_at_magnet = energy[self.gun_position]
			else:
				for key, value in energy.items():
					if key < self.magDict[name].position:
						self.energy_at_magnet += value
			if self.energy_at_magnet == 0:
				self.energy_at_magnet = energy[self.linac_position['L01']]
			self.unitConversion.currentToK(self.magnetdata[name]['type'],
			 								 self.magDict[name].READI,
											 self.magDict[name].getFieldIntegralCoefficients(),
											 self.magDict[name].magnetic_length,
											 self.energy_at_magnet,
											 self.magnetdata[name])
			self.magnetdata[name]['energy'] = self.energy_at_magnet
			self.magnetdata[name]['position'] = self.magDict[name].position
			self.alldata[self.getMachineAreaString(name)].update({name: self.magnetdata[name]})
		else:
			self.setAllDicts()
			self.getMagnetData(name)

	def setGunStartEndTime(self, start_time, end_time):
		self.gunStartTime = start_time
		self.gunEndTime = end_time
		for trace in self.guntraces:
			self.gunFac.setMeanStartEndTime(self.gunname, trace, start_time, end_time)

	def setLinacStartEndTime(self, name, start_time, end_time):
		for trace in self.linactraces:
			self.linacStartTimes[name] = start_time
			self.linacEndTimes[name] = end_time
			self.linacFac[name].setMeanStartEndTime(name, trace, start_time, end_time)

	def getGunLLRFData(self):
		if self.dictsSet:
			for trace in self.guntraces:
				self.gundata.update({trace: self.gunFac.getCutMean(self.gunname, trace)})
				self.gundata.update({trace: self.gundata[trace]})
			self.gunLLRFObj.setAmpMW(10 * 10 ** 6)
			self.pulse_length = 2.5
			self.getenergy = self.unitConversion.getEnergyGain(self.gunname,
																self.gunLLRFObj.getAmpMW(),
																self.gunLLRFObj.getPhiDEG(),
															    self.pulse_length,
																self.gun_length)
			#self.gundata.update({"phase": self.gundata["CAVITY_FORWARD_POWER"]})
			self.gundata.update({"phase": self.gunLLRFObj.getPhiDEG()})
			self.gundata.update({"amplitude_MW": self.gunLLRFObj.getAmpMW()})
			self.gundata.update({"amplitude": self.gunLLRFObj.getAmp()})
			self.gundata.update({"energy_gain": float(self.getenergy[0])})
			self.gundata.update({"field_amplitude": self.getenergy[1]})
			self.gundata.update({"type": 'cavity'})
			self.gundata.update({"length": self.gun_length})
			self.gundata.update({"pulse_length": self.pulse_length})
			self.gundata.update({"catap_alias": self.gunname})
			self.alldata[self.getMachineAreaString(self.gunname)].update({self.gunname: self.gundata})
			self.gunDataSet = True
		else:
			self.setAllDicts()
			self.getGunLLRFData()

	def getLinacLLRFData(self, linac_name):
		if self.dictsSet:
			for trace in self.linactraces:
				self.linacdata[linac_name].update({trace: self.linacFac[linac_name].getCutMean(linac_name, trace)})
				self.linacdata[linac_name].update({trace: self.linacdata[linac_name][trace]})
			self.linacLLRFObj[linac_name].setAmpMW(20 * 10 ** 6)
			self.pulse_length = 0.75
			self.getenergy = self.unitConversion.getEnergyGain(linac_name,
																self.linacLLRFObj[linac_name].getAmpMW(),
																self.linacLLRFObj[linac_name].getPhiDEG(),
															    0.75,
																self.linac_length[linac_name])
			#self.linacdata[linac_name].update({"phase":self.linacdata[linac_name]["CAVITY_FORWARD_PHASE"]})
			self.linacdata[linac_name].update({"phase": self.linacLLRFObj[linac_name].getPhiDEG()})
			self.linacdata[linac_name].update({"amplitude_MW": self.linacLLRFObj[linac_name].getAmpMW()})
			self.linacdata[linac_name].update({"amplitude": self.linacLLRFObj[linac_name].getAmp()})
			self.linacdata[linac_name].update({"energy_gain": float(self.getenergy[0])})
			self.linacdata[linac_name].update({"field_amplitude": self.getenergy[1]})
			self.linacdata[linac_name].update({"type": 'cavity'})
			self.linacdata[linac_name].update({"length": self.linac_length[linac_name]})
			self.linacdata[linac_name].update({"pulse_length": self.pulse_length})
			self.linacdata[linac_name].update({"catap_alias": linac_name})
			self.alldata[self.getMachineAreaString(linac_name)].update({linac_name: self.linacdata[linac_name]})
			self.linacDataSet.update({linac_name: True})

		else:
			self.setAllDicts()
			self.getLinacLLRFData(linac_name)

	def setGunEnergyGain(self):
		if self.gunDataSet:
			self.gunEnergyGain = 1

	def setLinacEnergyGain(self, name):
		if self.linacDataSet[name]:
			self.linacEnergyGain[name] = 1

	def getAllData(self):
		if self.dictsSet:
			self.getGunLLRFData()
			self.energy.update({self.gun_position: self.gundata['energy_gain']})
			for i in self.linacnames.keys():
				self.getLinacLLRFData(i)
				self.energy.update({self.linac_position[i]: self.linacdata[i]['energy_gain']})
			for i in self.bpmnames:
				self.getBPMData(i)
			for i in self.magnames:
				self.getMagnetData(i, self.energy)
			for i in self.chargenames:
				self.getChargeData(i)
			for i in self.screennames:
				self.getScreenData(i)
			for i in self.camnames:
				self.getCameraData(i)
			for i in self.alldata.keys():
				self.checkType(self.alldata[i])
				self.getSimFrameAlias(self.alldata[i])
		else:
			self.setAllDicts()
			self.getAllData()
		self.alldataset = True
		return self.alldata

	def getVCObject(self):
		if not self.alldataset:
			self.getAllData()
		else:
			return self.alldata['VCA']['CLA-VCA-DIA-CAM-01']

	def getWCMObject(self):
		if not self.alldataset:
			self.getAllData()
		else:
			return self.alldata['S01']['CLA-S01-DIA-WCM-01']

	def checkType(self, datadict):
		for i in datadict.keys():
			for j in self.type_alias.keys():
				if datadict[i]['type'] == j:
					datadict[i].update({'type': self.type_alias[j]})

	def getSimFrameAlias(self, datadict):
		for i in datadict.keys():
			if i in self.alias_names.keys():
				datadict[i]['simframe_alias'] = self.alias_names[i]


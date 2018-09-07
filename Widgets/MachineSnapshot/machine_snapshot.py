import VELA_CLARA_enums as vce
import h5py, json, numpy, math, os
import dict_to_h5, time, datetime
from scipy import constants

SPEED_OF_LIGHT = constants.c / 1e6

class MachineSnapshot(object):
	def __init__(self, MAG_Ctrl=None, BPM_Ctrl=None, CHG_Ctrl=None,
				 SCR_Ctrl=None, CAM_Ctrl=None, GUN_Ctrl=None,
				 GUN_Type=None, L01_Ctrl=None, PIL_Ctrl=None,
				 MACHINE_MODE=vce.MACHINE_MODE.PHYSICAL, MACHINE_AREA=vce.MACHINE_AREA.CLARA_2_BA1_BA2, messages=False):


		self.BPM_Ctrl = BPM_Ctrl
		self.CHG_Ctrl = CHG_Ctrl
		self.MAG_Ctrl = MAG_Ctrl
		self.SCR_Ctrl = SCR_Ctrl
		self.CAM_Ctrl = CAM_Ctrl
		self.GUN_Ctrl = GUN_Ctrl
		self.GUN_Type = GUN_Type
		self.L01_Ctrl = L01_Ctrl
		self.PIL_Ctrl = PIL_Ctrl
		self.MACHINE_MODE = MACHINE_MODE
		self.MACHINE_AREA = MACHINE_AREA
		self.bpm_data = {}
		self.chg_data = {}
		self.mag_data = {}
		self.gun_data = {}
		self.l01_data = {}
		self.cam_data = {}
		self.cam_objs = {}
		self.dip_objs = {}
		self.mag_objs = {}
		self.momentum = {}
		self.int_strengthdip = {}
		self.scr_data = {}
		self.bpm_ctrl = self.checkBPMController()
		self.cam_ctrl = self.checkCameraController()
		self.chg_ctrl = self.checkChargeController()
		self.gun_ctrl = self.checkLLRFController()[0]
		self.l01_ctrl = self.checkLLRFController()[1]
		self.mag_ctrl = self.checkMagnetController()
		#self.pil_ctrl = self.checkPILaserController()
		self.scr_ctrl = self.checkScreenController()
		time.sleep(1)


	def checkBPMController(self):
		if self.BPM_Ctrl is not None:
			self.bpm_ctrl = self.BPM_Ctrl
		else:
			import VELA_CLARA_BPM_Control as bpm
			self.bpm_init = bpm.init()
			self.bpm_ctrl = self.bpm_init.getBPMController(self.MACHINE_MODE,self.MACHINE_AREA)
		return self.bpm_ctrl

	def checkChargeController(self):
		if self.CHG_Ctrl is not None:
			self.chg_ctrl = self.CHG_Ctrl
		else:
			import VELA_CLARA_Charge_Control as chg
			self.chg_init = chg.init()
			self.chg_ctrl = self.chg_init.getChargeController(self.MACHINE_MODE,self.MACHINE_AREA)
		return self.chg_ctrl

	def checkMagnetController(self):
		if self.MAG_Ctrl is not None:
			self.mag_ctrl = self.MAG_Ctrl
		else:
			import VELA_CLARA_Magnet_Control as mag
			self.mag_init = mag.init()
			self.mag_ctrl = self.mag_init.getMagnetController(self.MACHINE_MODE,self.MACHINE_AREA)
		return self.mag_ctrl

	def checkScreenController(self):
		if self.SCR_Ctrl is not None:
			self.scr_ctrl = self.SCR_Ctrl
		else:
			import VELA_CLARA_Screen_Control as scr
			self.scr_init = scr.init()
			self.scr_ctrl = self.scr_init.getScreenController(self.MACHINE_MODE,self.MACHINE_AREA)
		return self.scr_ctrl

	def checkCameraController(self):
		if self.CAM_Ctrl is not None:
			self.cam_ctrl = self.CAM_Ctrl
		else:
			import VELA_CLARA_Camera_Control as cam
			self.cam_init = cam.init()
			if self.MACHINE_MODE == vce.MACHINE_MODE.PHYSICAL:
				self.cam_ctrl = self.cam_init.physical_Camera_Controller()
			elif self.MACHINE_MODE == vce.MACHINE_MODE.VIRTUAL:
				self.cam_ctrl = self.cam_init.virtual_Camera_Controller()
		return self.cam_ctrl

	def checkPILaserController(self):
		if self.PIL_Ctrl is not None:
			self.pil_ctrl = self.PIL_Ctrl
		else:
			import VELA_CLARA_PILaser_Control as pil
			self.pil_init = pil.init()
			if self.MACHINE_MODE == vce.MACHINE_MODE.PHYSICAL:
				self.pil_ctrl = self.pil_init.physical_PILaser_Controller()
				time.sleep(10)
			elif self.MACHINE_MODE == vce.MACHINE_MODE.VIRTUAL:
				self.pil_ctrl = self.pil_init.virtual_PILaser_Controller()

		return self.pil_ctrl

	def checkLLRFController(self):
		if self.L01_Ctrl is not None:
			self.l01_ctrl = self.L01_Ctrl
		if self.GUN_Ctrl is not None:
			self.gun_ctrl = self.GUN_Ctrl
		else:
			import VELA_CLARA_LLRF_Control as lrf
			self.lrf_init = lrf.init()
			self.GUN_Type = lrf.LLRF_TYPE.CLARA_LRRG # for now we can assume CLARA_LRRG??????
			self.gun_ctrl = self.lrf_init.getLLRFController(self.MACHINE_MODE, self.GUN_Type)
			if "CLARA" in str(self.GUN_Type):
				self.l01_ctrl = self.lrf_init.getLLRFController(self.MACHINE_MODE,lrf.LLRF_TYPE.L01)
		return self.gun_ctrl, self.l01_ctrl

	def getmagnetdata(self):
		self.mag_names = self.mag_ctrl.getMagnetNames()
		self.dip_names = self.mag_ctrl.getDipNames()
		for i in self.dip_names:
			if i == "S02-DIP01":
				self.dip_objs[i] = self.mag_ctrl.getMagObjConstRef(i)
				self.sign = -1
				self.current = self.dip_objs[i].readi
				self.coeffs = numpy.append(self.dip_objs[i].fieldIntegralCoefficients[:-1], self.dip_objs[i].fieldIntegralCoefficients[-1])
				self.int_strengthdip['L01'] = numpy.polyval(self.coeffs, abs(self.current))
				self.angle = 45
				self.momentum['L01'] = 0.001 * SPEED_OF_LIGHT * self.int_strengthdip['L01'] / numpy.radians(self.angle)
		for i in self.mag_names:
			self.mag_objs[i] = self.mag_ctrl.getMagObjConstRef(i)
			self.mag_data[i] = {}
			self.coeffs = numpy.append(self.mag_objs[i].fieldIntegralCoefficients[:-1], self.mag_objs[i].fieldIntegralCoefficients[-1])
			self.int_strength = numpy.polyval(self.coeffs, abs(self.mag_objs[i].siWithPol))
			self.effect = SPEED_OF_LIGHT * self.int_strength / self.momentum['L01']
			self.mag_data[i]["readi"] = self.mag_objs[i].readi
			# self.mag_data[i]["seti"] = self.mag_objs[i].siWithPol
			self.mag_data[i]["psu_state"] = self.mag_objs[i].psuState
			self.mag_type = str(self.mag_objs[i].magType)
			if self.mag_type == 'DIP':
					# Get deflection in degrees
					# int_strength was in T.mm so we divide by 1000
					self.mag_data[i]['angle'] = math.degrees(self.effect / 1000)
			elif self.mag_type in ('QUAD', 'SEXT'):
				self.mag_data[i]['k'] = self.effect / self.mag_objs[i].magneticLength  # focusing term K
			elif self.mag_type in ('HCOR', 'VCOR'):
				pass
				#self.mag_data[i]['deflection'] = self.effect  # deflection in mrad
			elif self.mag_type == 'BSOL':  # bucking coil
				# For the BSOL, coefficients refer to the solenoid current as well as the BSOL current
				# The 'K' value is the field at the cathode
				# x is BC current, y is solenoid current
				self.x = self.mag_data[i]["readi"]
				self.y = self.mag_objs[i].siWithPol
				self.k_coeffs = numpy.array(self.mag_objs[i].fieldIntegralCoefficients[:-4])
				self.mag_data[i]['cathode_field'] = numpy.dot(self.k_coeffs,
						   [self.y, self.y**2, self.y**3, self.x, self.x*self.y, self.x*self.y**2, self.x**2, self.x**2*self.y, self.x**2*self.y**2, self.x**2*self.y**3, self.x**3, self.x**3*self.y])
			elif self.mag_type == 'SOL': # solenoids
				# For the solenoid, coefficients also refer to the momentum
				# The 'K' value is the Larmor angle
				self.I = self.mag_data[i]["readi"]
				self.p = self.momentum['L01']
				self.k_coeffs = numpy.array(self.mag_objs[i].fieldIntegralCoefficients[:-4])
				self.mag_data[i]['larmor_angle'] = numpy.dot(self.k_coeffs, [self.I, self.p*self.I, self.p**2*self.I, self.p**3*self.I, self.p**4*self.I])
		return self.mag_data

	def getbpmdata(self):
		self.bpm_names = self.bpm_ctrl.getBPMNames()
		for i in self.bpm_names:
			self.bpm_data[i] = {}
			self.bpm_data[i]["x"] = self.bpm_ctrl.getXFromPV(i)
			self.bpm_data[i]["y"] = self.bpm_ctrl.getYFromPV(i)
			self.bpm_data[i]["q"] = self.bpm_ctrl.getQ(i)
			self.bpm_data[i]["status"] = self.bpm_ctrl.getBPMStatus(i)
		return self.bpm_data

	def getchargedata(self):
		self.chg_names = self.chg_ctrl.getChargeDiagnosticNames()
		for i in self.chg_names:
			self.chg_data[i] = self.chg_ctrl.getCharge(i)
		return self.chg_data

	def getgundata(self):
		self.gun_data["amp_sp"] = self.gun_ctrl.getAmpSP()
		self.gun_data["amp_mvm"] = self.gun_ctrl.getAmpMVM()
		self.gun_data["phase_sp"] = self.gun_ctrl.getPhiSP()
		self.gun_data["phase_llrf"] = self.gun_ctrl.getPhiLLRF()
		return self.gun_data

	def getl01data(self):
		self.l01_data["amp_sp"] = self.l01_ctrl.getAmpSP()
		self.l01_data["amp_mvm"] = self.l01_ctrl.getAmpMVM()
		self.l01_data["phase_sp"] = self.l01_ctrl.getPhiSP()
		self.l01_data["phase_llrf"] = self.l01_ctrl.getPhiLLRF()
		return self.l01_data

	def getscreendata(self):
		self.screen_names = self.scr_ctrl.getScreenNames()
		for i in self.screen_names:
			self.scr_data[i] = self.scr_ctrl.getScreenState(i)
		return self.scr_data

	def getcameradata(self):
		self.cam_names = self.cam_ctrl.getCameraNames()
		for i in self.cam_names:
			if self.cam_ctrl.isAcquiring(i):
				self.cam_data[i] = {}
				self.cam_data[i]['acquiring'] = True
				if self.cam_ctrl.isAnalysing(i):
					self.cam_data[i]['analysing'] = True
					self.cam_objs[i] = self.cam_ctrl.getAnalysisObj(i)
					self.cam_data[i]['avg_pix'] = self.cam_objs[i].avg_pix
					self.cam_data[i]['avg_pix_full'] = self.cam_objs[i].avg_pix_full
					self.cam_data[i]['avg_pix_mean'] = self.cam_objs[i].avg_pix_mean
					self.cam_data[i]['avg_pix_n'] = self.cam_objs[i].avg_pix_n
					self.cam_data[i]['sig_x'] = self.cam_objs[i].sig_x
					self.cam_data[i]['sig_x_full'] = self.cam_objs[i].sig_x_full
					self.cam_data[i]['sig_x_mean'] = self.cam_objs[i].sig_x_mean
					self.cam_data[i]['sig_x_n'] = self.cam_objs[i].sig_x_n
					self.cam_data[i]['sig_x_pix'] = self.cam_objs[i].sig_x_pix
					self.cam_data[i]['sig_x_pix_full'] = self.cam_objs[i].sig_x_pix_full
					self.cam_data[i]['sig_x_pix_mean'] = self.cam_objs[i].sig_x_pix_mean
					self.cam_data[i]['sig_x_pix_n'] = self.cam_objs[i].sig_x_pix_n
					self.cam_data[i]['sig_x_pix_sd'] = self.cam_objs[i].sig_x_pix_sd
					self.cam_data[i]['sig_xy'] = self.cam_objs[i].sig_xy
					self.cam_data[i]['sig_xy_full'] = self.cam_objs[i].sig_xy_full
					self.cam_data[i]['sig_xy_mean'] = self.cam_objs[i].sig_xy_mean
					self.cam_data[i]['sig_xy_n'] = self.cam_objs[i].sig_xy_n
					self.cam_data[i]['sig_xy_pix'] = self.cam_objs[i].sig_xy_pix
					self.cam_data[i]['sig_xy_pix_full'] = self.cam_objs[i].sig_xy_pix_full
					self.cam_data[i]['sig_y_mean'] = self.cam_objs[i].sig_y_mean
					self.cam_data[i]['sig_y_n'] = self.cam_objs[i].sig_y_n
					self.cam_data[i]['sig_y_pix'] = self.cam_objs[i].sig_y_pix
					self.cam_data[i]['sig_y_pix_full'] = self.cam_objs[i].sig_y_pix_full
					self.cam_data[i]['sig_y_pix_mean'] = self.cam_objs[i].sig_y_pix_mean
					self.cam_data[i]['sig_y_pix_n'] = self.cam_objs[i].sig_y_pix_n
					self.cam_data[i]['sig_y_pix_sd'] = self.cam_objs[i].sig_y_pix_sd
					self.cam_data[i]['sig_y_sd'] = self.cam_objs[i].sig_y_sd
					self.cam_data[i]['step_size'] = self.cam_objs[i].step_size
					self.cam_data[i]['sum_pix'] = self.cam_objs[i].sum_pix
					self.cam_data[i]['sum_pix_full'] = self.cam_objs[i].sum_pix_full
					self.cam_data[i]['sum_pix_mean'] = self.cam_objs[i].sum_pix_mean
					self.cam_data[i]['sum_pix_n'] = self.cam_objs[i].sum_pix_n
					self.cam_data[i]['x'] = self.cam_objs[i].x
					self.cam_data[i]['x_mean'] = self.cam_objs[i].x_mean
					self.cam_data[i]['x_pix'] = self.cam_objs[i].x_pix
					self.cam_data[i]['x_pix_full'] = self.cam_objs[i].x_pix_full
					self.cam_data[i]['x_pix_mean'] = self.cam_objs[i].x_pix_mean
					self.cam_data[i]['x_pix_n'] = self.cam_objs[i].x_pix_n
					self.cam_data[i]['x_pix_sd'] = self.cam_objs[i].x_pix_sd
					self.cam_data[i]['x_sd'] = self.cam_objs[i].x_sd
					self.cam_data[i]['y'] = self.cam_objs[i].y
					self.cam_data[i]['y_full'] = self.cam_objs[i].y_full
					self.cam_data[i]['y_mean'] = self.cam_objs[i].y_mean
					self.cam_data[i]['y_n'] = self.cam_objs[i].y_n
					self.cam_data[i]['y_full'] = self.cam_objs[i].y_full
					self.cam_data[i]['y_mean'] = self.cam_objs[i].y_mean
					self.cam_data[i]['y_n'] = self.cam_objs[i].y_n
					self.cam_data[i]['y_pix'] = self.cam_objs[i].y_pix
					self.cam_data[i]['y_pix_full'] = self.cam_objs[i].y_pix_full
					self.cam_data[i]['y_pix_mean'] = self.cam_objs[i].y_pix_mean
					self.cam_data[i]['y_pix_n'] = self.cam_objs[i].y_pix_n
					self.cam_data[i]['y_pix_sd'] = self.cam_objs[i].y_pix_sd
					self.cam_data[i]['y_sd'] = self.cam_objs[i].y_sd
		return self.cam_data

	def getdata(self):
		self.bpmdata = self.getbpmdata()
		self.chargedata = self.getchargedata()
		self.magnetdata = self.getmagnetdata()
		self.gundata = self.getgundata()
		self.l01data = self.getl01data()
		self.screendata = self.getscreendata()
		self.cameradata = self.getcameradata()

		self.data = { "machine_mode" : self.MACHINE_MODE,
					  "machine_area" : self.MACHINE_AREA,
					  "bpm_data" : self.bpmdata,
					  "chg_data" : self.chargedata,
					  "mag_data" : self.magnetdata,
					  "gun_data" : self.gundata,
					  "l01_data" : self.l01data,
					  "scr_data" : self.screendata,
					  "cam_data" : self.cameradata }
		return self.data

	def writetojson(self, filename=None, directory=None):
		self.filename = filename
		self.directory = directory
		self.timestamp = time.time()
		self.st = datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d-%H-%M-%S')
		self.now = datetime.datetime.now()
		if self.directory == None:
			self.year = str(self.now.year)
			self.month = str(self.now.month)
			self.day = str(self.now.day)
			if len(self.month) == 1:
				self.month = "0"+self.month
			if len(self.day) == 1:
				self.day= "0"+self.day
			self.directory = "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\"+self.year+"\\"+self.month+"\\"+self.day+"\\"
		os.chdir(self.directory)
		self.json_data = self.getdata()
		if self.filename == None:
			self.filename = "snapshot-"
		self.fullname = self.filename + self.st + ".json"
		with open(self.fullname, 'w') as outfile:
			outfile.write(json.dumps(self.json_data, indent=4, sort_keys=True))

	def writetohdf5(self, filename=None, directory=None):
		self.filename = filename
		self.directory = directory
		self.timestamp = time.time()
		self.st = datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d-%H-%M-%S')
		self.now = datetime.datetime.now()
		if self.directory == None:
			self.year = str(self.now.year)
			self.month = str(self.now.month)
			self.day = str(self.now.day)
			if len(self.month) == 1:
				self.month = "0"+self.month
			if len(self.day) == 1:
				self.day= "0"+self.day
			self.directory = "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\"+self.year+"\\"+self.month+"\\"+self.day+"\\"
		os.chdir(self.directory)
		self.hdf5_data = self.getdata()
		if self.filename == None:
			self.filename = "snapshot-"
		self.fullname = self.filename + self.st + ".hdf5"
		dict_to_h5.save_dict_to_hdf5(self.hdf5_data, self.fullname)


if __name__ == "__main__":
	data = MachineSnapshot(MAG_Ctrl=None, BPM_Ctrl=None, CHG_Ctrl=None,
				 SCR_Ctrl=None, CAM_Ctrl=None, GUN_Ctrl=None,
				 GUN_Type=None, L01_Ctrl=None, PIL_Ctrl=None,
				 MACHINE_MODE=vce.MACHINE_MODE.PHYSICAL, MACHINE_AREA=vce.MACHINE_AREA.CLARA_2_BA1_BA2, messages=False)
	data.writetojson()
	data.writetohdf5()
	print "fin"
	time.sleep(5)

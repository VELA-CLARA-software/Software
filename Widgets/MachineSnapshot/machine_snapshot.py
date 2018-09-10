import VELA_CLARA_enums as vce
import h5py, json, numpy, math, os
import dict_to_h5, time, datetime
from scipy import constants

SPEED_OF_LIGHT = constants.c / 1e6

class MachineSnapshot(object):
	def __init__(self, MAG_Ctrl=None, BPM_Ctrl=None, CHG_Ctrl=None,
				 SCR_Ctrl=None, CAM_Ctrl=None, GUN_Ctrl=None, GUN_Crest=0.0,
				 GUN_Type=None, L01_Ctrl=None, L01_Crest=0.0,
				 PIL_Ctrl=None, GUN_MOD_Ctrl = None, L01_MOD_Ctrl = None,
				 MACHINE_MODE=vce.MACHINE_MODE.PHYSICAL, MACHINE_AREA=vce.MACHINE_AREA.CLARA_2_BA1_BA2, bufferSize=10, messages=False):


		self.BPM_Ctrl = BPM_Ctrl
		self.CHG_Ctrl = CHG_Ctrl
		self.MAG_Ctrl = MAG_Ctrl
		self.SCR_Ctrl = SCR_Ctrl
		self.CAM_Ctrl = CAM_Ctrl
		self.GUN_Ctrl = GUN_Ctrl
		self.GUN_Type = GUN_Type
		self.L01_Ctrl = L01_Ctrl
		self.PIL_Ctrl = PIL_Ctrl
		self.GUN_MOD_Ctrl = GUN_MOD_Ctrl
		self.L01_MOD_Crtl = L01_MOD_Ctrl
		self.MACHINE_MODE = MACHINE_MODE
		self.MACHINE_AREA = MACHINE_AREA
		self.bufferSize = bufferSize
		self.GUN_Crest = GUN_Crest
		self.L01_Crest = L01_Crest
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
		self.gun_mod_data = {}
		self.l01_mod_data = {}
		self.pil_data = {}
		self.int_strengthdip = {}
		self.scr_data = {}
		self.pil_ctrl = self.checkPILaserController()
		self.bpm_ctrl = self.checkBPMController()
		self.cam_ctrl = self.checkCameraController()
		self.chg_ctrl = self.checkChargeController()
		self.gun_ctrl = self.checkLLRFController()[0]
		self.l01_ctrl = self.checkLLRFController()[1]
		self.mag_ctrl = self.checkMagnetController()
		# self.gun_mod_ctrl = self.checkModController()[0]
		# self.l01_mod_ctrl = self.checkModController()[1]
		self.scr_ctrl = self.checkScreenController()
		self.cam_ctrl.setBufferMaxCount(self.bufferSize)
		self.bpm_ctrl.setBufferSize(self.bufferSize)
		self.chg_ctrl.setBufferSize(self.bufferSize)
		self.gun_ctrl.setNumBufferTraces(self.bufferSize)
		self.l01_ctrl.setNumBufferTraces(self.bufferSize)
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

	def checkModController(self):
		if self.GUN_MOD_Ctrl is not None:
			self.gun_mod_ctrl = self.GUN_MOD_Ctrl
		if self.L01_MOD_Crtl is not None:
			self.l01_mod_ctrl = self.L01_MOD_Crtl
		else:
			import VELA_CLARA_RF_Modulator_Control as rmc
			self.rmc_init = rmc.init()
			self.gun_mod_ctrl = self.rmc_init.physical_GUN_MOD_Controller()
			self.l01_mod_ctrl = self.rmc_init.physical_L01_MOD_Controller()
		return self.gun_mod_ctrl, self.l01_mod_ctrl

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
		self.timenow = time.time()
		for i in self.bpm_names:
			self.bpm_data[i] = {}
			self.bpm_data[i]["x"] = self.bpm_ctrl.getXFromPV(i)
			self.bpm_data[i]["y"] = self.bpm_ctrl.getYFromPV(i)
			self.bpm_data[i]["q"] = self.bpm_ctrl.getQ(i)
			self.bpm_data[i]["status"] = self.bpm_ctrl.getBPMStatus(i)
			self.bpm_data[i]['sa1'] = self.bpm_ctrl.getSA1(i)
			self.bpm_data[i]['sa2'] = self.bpm_ctrl.getSA2(i)
			self.bpm_data[i]['sd1'] = self.bpm_ctrl.getSD1(i)
			self.bpm_data[i]['sd2'] = self.bpm_ctrl.getSD2(i)
			if self.bpm_ctrl.getBPMStatusStr(i) == "GOOD":
				while self.bpm_ctrl.isDataBufferNotFull(i):
					time.sleep(0.1)
					self.timesleep = time.time()
					if self.timesleep > (self.timenow + (self.bufferSize/10) + 10):
						break
			self.bpm_data[i]['x_buffer'] = self.bpm_ctrl.getBPMXBuffer(i)
			self.bpm_data[i]['y_buffer'] = self.bpm_ctrl.getBPMYBuffer(i)
			self.bpm_data[i]['q_buffer'] = self.bpm_ctrl.getBPMQBuffer(i)
			self.bpm_data[i]['status_buffer'] = self.bpm_ctrl.getStatusBuffer(i)
		return self.bpm_data

	def getchargedata(self):
		self.chg_names = self.chg_ctrl.getChargeDiagnosticNames()
		self.timenow = time.time()
		for i in self.chg_names:
			self.chg_data[i] = {}
			self.chg_data[i]['q'] = self.chg_ctrl.getCharge(i)
			while self.chg_ctrl.isChargeBufferNotFull(i):
				time.sleep(0.1)
				self.timesleep = time.time()
				if self.timesleep > (self.timenow + (self.bufferSize / 10) + 10):
					break
			self.chg_data[i]['q_buffer'] = self.chg_ctrl.getChargeBuffer(i)
		return self.chg_data

	def getgundata(self):
		self.gun_ctrl.setCrestPhiLLRF(self.GUN_Crest)
		self.gun_obj = self.gun_ctrl.getLLRFObjConstRef()
		self.gun_data["amp_sp"] = self.gun_obj.amp_sp
		self.gun_data["amp_mvm"] = self.gun_obj.amp_MVM
		self.gun_data["phase_sp"] = self.gun_obj.phi_sp
		self.gun_data["phase_from_crest"] = self.gun_obj.phi_DEG
		self.gun_data["crest"] = self.gun_obj.crestPhi
		self.gun_data["name"] = self.gun_obj.name
		self.gun_data["pulse_length"] = self.gun_obj.pulse_length
		self.gun_data["pulse_offset"] = self.gun_obj.pulse_offset
		# if self.gun_mod_data['main_state'] == "RF_ON":
		self.getllrfdata(self.gun_obj, self.gun_ctrl, self.gun_data)
		'''if True:
			self.gun_data["kly_fwd_power_av"] = self.gun_ctrl.getKlyFwdPowerAv()
			self.gun_data["kly_rev_power_av"] = self.gun_ctrl.getKlyRevPowerAv()
			self.gun_data["kly_fwd_phase_av"] = numpy.mean(self.gun_ctrl.getKlyFwdPhase())
			self.gun_data["kly_rev_phase_av"] = numpy.mean(self.gun_ctrl.getKlyRevPhase())
			self.gun_data["probe_power_av"] = self.gun_ctrl.getProbePowerAv()
			self.gun_data["probe_phase_av"] = self.gun_ctrl.getProbePhaseAv()
			self.gun_data["cav_fwd_power_av"] = self.gun_ctrl.getCavFwdPowerAv()
			self.gun_data["cav_rev_power_av"] = self.gun_ctrl.getCavRevPowerAv()
			self.gun_data["cav_fwd_phase_av"] = self.gun_ctrl.getCavFwdPhaseAv()
			self.gun_data["cav_rev_phase_av"] = self.gun_ctrl.getCavRevPhaseAv()
			self.gun_data["kly_fwd_power"] = self.gun_ctrl.getKlyFwdPower()
			self.gun_data["kly_rev_power"] = self.gun_ctrl.getKlyRevPower()
			self.gun_data["kly_fwd_phase"] = self.gun_ctrl.getKlyFwdPhase()
			self.gun_data["kly_rev_phase"] = self.gun_ctrl.getKlyRevPhase()
			self.gun_data["probe_power"] = self.gun_ctrl.getProbePower()
			self.gun_data["probe_phase"] = self.gun_ctrl.getProbePhase()
			self.gun_data["cav_fwd_power"] = self.gun_ctrl.getCavFwdPower()
			self.gun_data["cav_rev_power"] = self.gun_ctrl.getCavRevPower()
			self.gun_data["cav_fwd_phase"] = self.gun_ctrl.getCavFwdPhase()
			self.gun_data["cav_rev_phase"] = self.gun_ctrl.getCavRevPhase()'''
		return self.gun_data

	def getl01data(self):
		self.l01_ctrl.setCrestPhiLLRF(self.L01_Crest)
		self.l01_obj = self.l01_ctrl.getLLRFObjConstRef()
		self.l01_data["amp_sp"] = self.l01_obj.amp_sp
		self.l01_data["amp_mvm"] = self.l01_obj.amp_MVM
		self.l01_data["phase_sp"] = self.l01_obj.phi_sp
		self.l01_data["phase_from_crest"] = self.l01_obj.phi_DEG
		self.l01_data["crest"] = self.l01_obj.crestPhi
		self.l01_data["name"] = self.l01_obj.name
		self.getllrfdata(self.l01_obj,self.l01_ctrl,self.l01_data)
		'''self.l01_data["pulse_length"] = self.l01_obj.pulse_length
		self.l01_data["pulse_offset"] = self.l01_obj.pulse_offset
		self.l01_data["kly_fwd_power_av"] = self.l01_ctrl.getKlyFwdPowerAv()
		self.l01_data["kly_rev_power_av"] = self.l01_ctrl.getKlyRevPowerAv()
		self.l01_data["kly_fwd_phase_av"] = numpy.mean(self.gun_ctrl.getKlyFwdPhase())
		self.l01_data["kly_rev_phase_av"] = numpy.mean(self.gun_ctrl.getKlyRevPhase())
		self.l01_data["probe_power_av"] = self.l01_ctrl.getProbePowerAv()
		self.l01_data["probe_phase_av"] = self.l01_ctrl.getProbePhaseAv()
		self.l01_data["cav_fwd_power_av"] = self.l01_ctrl.getCavFwdPowerAv()
		self.l01_data["cav_rev_power_av"] = self.l01_ctrl.getCavRevPowerAv()
		self.l01_data["cav_fwd_phase_av"] = self.l01_ctrl.getCavFwdPhaseAv()
		self.l01_data["cav_rev_phase_av"] = self.l01_ctrl.getCavRevPhaseAv()
		self.l01_data["kly_fwd_power"] = self.l01_ctrl.getKlyFwdPower()
		self.l01_data["kly_rev_power"] = self.l01_ctrl.getKlyRevPower()
		self.l01_data["kly_fwd_phase"] = self.l01_ctrl.getKlyFwdPhase()
		self.l01_data["kly_rev_phase"] = self.l01_ctrl.getKlyRevPhase()
		self.l01_data["probe_power"] = self.l01_ctrl.getProbePower()
		self.l01_data["probe_phase"] = self.l01_ctrl.getProbePhase()
		self.l01_data["cav_fwd_power"] = self.l01_ctrl.getCavFwdPower()
		self.l01_data["cav_rev_power"] = self.l01_ctrl.getCavRevPower()
		self.l01_data["cav_fwd_phase"] = self.l01_ctrl.getCavFwdPhase()
		self.l01_data["cav_rev_phase"] = self.l01_ctrl.getCavRevPhase()'''
		return self.l01_data

	def getllrfdata(self, llrfobj, llrfctrl, data_dict):
		self.llrfobj = llrfobj
		self.llrfctrl = llrfctrl
		self.data_dict = data_dict
		if self.llrfobj.name == "CLA-LRRG-LLRF":
			self.all_traces_to_monitor = ["KLYSTRON_FORWARD_POWER","KLYSTRON_FORWARD_PHASE","KLYSTRON_REVERSE_PHASE","KLYSTRON_REVERSE_POWER","LRRG_CAVITY_REVERSE_PHASE",
									  "LRRG_CAVITY_FORWARD_PHASE", "LRRG_CAVITY_REVERSE_POWER", "LRRG_CAVITY_FORWARD_POWER"]
		elif self.llrfobj.name == "CLA-HRRG-LLRF":
			self.all_traces_to_monitor = ["KLYSTRON_FORWARD_POWER", "KLYSTRON_FORWARD_PHASE", "KLYSTRON_REVERSE_PHASE",
										  "KLYSTRON_REVERSE_POWER", "HRRG_CAVITY_REVERSE_PHASE",
										  "HRRG_CAVITY_FORWARD_PHASE", "HRRG_CAVITY_REVERSE_POWER",
										  "HRRG_CAVITY_FORWARD_POWER"]
		elif self.llrfobj.name == "CLA-L01-LLRF":
			self.all_traces_to_monitor = ["KLYSTRON_FORWARD_POWER", "KLYSTRON_FORWARD_PHASE", "KLYSTRON_REVERSE_PHASE",
										  "KLYSTRON_REVERSE_POWER", "L01_CAVITY_REVERSE_PHASE",
										  "L01_CAVITY_FORWARD_PHASE", "L01_CAVITY_REVERSE_POWER",
										  "L01_CAVITY_FORWARD_POWER", "L01_PROBE_PHASE", "L01_PROBE_POWER"]

		for trace in self.all_traces_to_monitor:
			self.a = self.llrfctrl.startTraceMonitoring(trace)
			self.llrfctrl.setNumRollingAverageTraces(trace, self.bufferSize)
			self.llrfctrl.setKeepRollingAverage(trace, True)

		self.timevector = self.llrfobj.time_vector.value
		self.pulse_end = self.timevector[self.llrfobj.pulse_latency] + self.llrfctrl.getPulseLength()
		self.pulse_end_index = len([x for x in self.timevector if x <= self.pulse_end])
		self.trace_mean_start = self.pulse_end_index - 50
		self.trace_mean_end = self.pulse_end_index - 20
		if self.trace_mean_start < 0:
			self.trace_mean_start = 1
		if self.trace_mean_end < 0:
			self.trace_mean_end = 1017

		for trace in self.all_traces_to_monitor:
			self.trace_data_const_ref = self.llrfctrl.getTraceDataConstRef(trace)
			self.llrfctrl.setMeanStartIndex(trace, self.trace_mean_start)
			self.llrfctrl.setMeanStopIndex(trace, self.trace_mean_end)
			while len(self.llrfobj.trace_data[trace].traces) < self.bufferSize:
				print "sleep"
				time.sleep(1)
		time.sleep(2)

		for trace in self.all_traces_to_monitor:
				self.trace_data = self.trace_data_const_ref.traces
				self.data_dict[trace] = []
				for i in self.trace_data[-1].value:
					self.data_dict[trace].append(i)
				self.data_dict[trace+'_time'] = self.trace_data[-1].time
				self.data_dict[trace+'_AV'] = numpy.mean(self.trace_data[-1].value)
				self.data_dict[trace + '_AV_buffer'] = []
				for i in range(0,len(self.trace_data)-1):
					self.data_dict[trace + '_AV_buffer'].append(numpy.mean(self.trace_data[i].value))
		return True

	def getscreendata(self):
		self.screen_names = self.scr_ctrl.getScreenNames()
		for i in self.screen_names:
			self.scr_data[i] = self.scr_ctrl.getScreenState(i)
		return self.scr_data

	def getpildata(self):
		self.pil_data['energy'] = self.pil_ctrl.getEnergy()
		self.pil_data['hwp'] = self.pil_ctrl.getHWP()
		self.pil_data['on_status'] = self.pil_ctrl.isOn()
		self.pil_data['off_status'] = self.pil_ctrl.isOff()
		return self.pil_data

	def getl01modulatordata(self):
		self.l01modobj = self.l01_mod_ctrl.getObjConstRef()
		self.l01_mod_data['l01_fault'] = str(self.l01modobj.l01_fault)
		self.l01_mod_data['system_state_read'] = str(self.l01modobj.system_state_read)

	def getgunmodulatordata(self):
		self.gunmodobj = self.gun_mod_ctrl.getGunObjConstRef()
		self.gun_mod_data['main_state'] = str(self.gunmodobj.main_state)
		self.gun_mod_data['error_state'] = str(self.gunmodobj.error_state)

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
		# self.gunmoddata = self.getgunmodulatordata()
		# self.l01moddata = self.getl01modulatordata()
		self.screendata = self.getscreendata()
		self.pildata = self.getpildata()
		self.cameradata = self.getcameradata()
		self.gundata = self.getgundata()
		self.l01data = self.getl01data()

		self.data = { "machine_mode" : self.MACHINE_MODE,
					  "machine_area" : self.MACHINE_AREA,
					  "bpm_data" : self.bpmdata,
					  "chg_data" : self.chargedata,
					  "mag_data" : self.magnetdata,
					  # "gun_mod_data" : self.gunmoddata,
					  # "l01_mod_data" : self.l01moddata,
					  "pil_data" : self.pildata,
					  "gun_data" : self.gundata,
					  "l01_data" : self.l01data,
					  "scr_data" : self.screendata,
					  "cam_data" : self.cameradata }
		print "data saved"
		return self.data

	def setfilename(self, filename=None, directory=None):
		self.filename = filename
		self.directory = directory
		self.timestamp = time.time()
		self.st = datetime.datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d-%H-%M-%S')
		self.now = datetime.datetime.now()
		if self.directory == None:
			self.directory = self.getdirectory()
		os.chdir(self.directory)
		if self.filename == None:
			self.filename = "snapshot-" + self.st
		return self.filename

	def writetojson(self, filename=None, directory=None):
		self.filename = self.setfilename(filename, directory)
		self.json_data = self.getdata()
		self.fullname = self.filename + ".json"
		with open(self.fullname, 'w') as outfile:
			outfile.write(json.dumps(self.json_data, indent=4, sort_keys=True))

	def writetohdf5(self, filename=None, directory=None):
		self.filename = self.setfilename(filename, directory)
		self.hdf5_data = self.getdata()
		self.fullname = self.filename + ".hdf5"
		dict_to_h5.save_dict_to_hdf5(self.hdf5_data, self.fullname)

	def getdirectory(self):
		self.now = datetime.datetime.now()
		self.year = str(self.now.year)
		self.month = str(self.now.month)
		self.day = str(self.now.day)
		if len(self.month) == 1:
			self.month = "0" + self.month
		if len(self.day) == 1:
			self.day = "0" + self.day
		self.directory = "\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\" + self.year + "\\" + self.month + "\\" + self.day + "\\"
		if not os.path.isdir(self.directory):
			os.mkdir(self.directory)
		return self.directory


if __name__ == "__main__":
	data = MachineSnapshot(MAG_Ctrl=None, BPM_Ctrl=None, CHG_Ctrl=None,
				 SCR_Ctrl=None, CAM_Ctrl=None, GUN_Ctrl=None,
				 GUN_Type=None, GUN_Crest=0.0, L01_Ctrl=None, L01_Crest=0.0,
				PIL_Ctrl=None, MACHINE_MODE=vce.MACHINE_MODE.PHYSICAL, MACHINE_AREA=vce.MACHINE_AREA.CLARA_2_BA1_BA2, bufferSize=10, messages=False)
	data.writetojson()
	data.writetohdf5()
	print "fin"
	time.sleep(5)

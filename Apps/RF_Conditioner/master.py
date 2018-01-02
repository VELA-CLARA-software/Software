# holds everything
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import pyqtSlot
import os
import sys
import time
from state import state

if os.environ['COMPUTERNAME'] == "DJS56PORT2":
	print 'port'
	sys.path.append(os.getcwd())
else:
	print 'desk'
	sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage')

# Hardware Controllers (.pyd)
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_enums import MACHINE_MODE
import VELA_CLARA_General_Monitor
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control

# import VELA_CLARA_RF_Modulator_Control
# Python Classes that do work
import LLRF_monitor
import mask_setter
import vac_valve_monitor
import value_monitor
import spike_monitor
import config_reader
import gun_modulator
import llrf_handler
import libera_interlocks
import break_down_monitor
import gui_conditioning
import rf_protection
import llrf_gui_param_monitor

#os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
#os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255"
#os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"


class master(object):
	# whoami
	my_name = 'master'
	# what type of RF structure are we conditioning
	llrf_type = LLRF_TYPE.UNKNOWN_TYPE
	# general monitoring for parameters with no controller
	# the master will handle ALL gen mon connections
	# it will then pass of keys and objects to monitor classes
	gen_mon = VELA_CLARA_General_Monitor.init()
	# every key from gen_mon will be stored here
	gen_mon_keys = {}
	# we can make some reasonable guesses as to what will be included
	vac_id = 'VAC_ID'
	dc_id  = 'DC_ID'
	mod_id = 'MOD_ID'
	cavity_temp_id = 'CAVITY_TEMP_ID'
	water_temp_id  = 'WATER_TEMP_ID'
	all_id = [vac_id,dc_id,mod_id,cavity_temp_id,water_temp_id]
	[gen_mon_keys.update({x:None}) for x in all_id]

	# explicit flags for possible monitors & monitors states
	# below
	# flags for known monitors
	# these are used to determine if monitoring these items is happening
	# they're not for defining vacuum good, / bad etc.
	modulator_monitoring 	= "modulator_monitoring"
	DC_monitoring 			= "DC_monitoring"
	rf_prot_monitoring 		= "rf_prot_monitoring"
	vacuum_monitoring 		= "vacuum_monitoring"
	breakdown_monitoring 	= "breakdown_monitoring"
	water_temp_monitoring 	= "water_temp_monitoring"
	cavity_temp_monitoring 	= "cavity_temp_monitoring"
	vac_valve_monitoring 	= "vac_valve_monitoring"
	monitoring_flags = {}
	all_monitors = [modulator_monitoring,DC_monitoring,rf_prot_monitoring,
						 vacuum_monitoring,breakdown_monitoring,water_temp_monitoring,
					     cavity_temp_monitoring]
	[monitoring_flags.update({x:False})for x in all_monitors]


	# which things are monitored
	vacuum_state="vacuum_state"
	vac_valve_state="vac_valve_state"
	water_temp_state="water_temp_state"
	cavity_temp_state="cavity_temp_state"
	dc_state="dc_state"
	breakdown_rate_state = "breakdown_rate_state"
	rf_prot_state = "rf_prot_state"
	modulator_state = "modulator_state"
	all_state_names = [vacuum_state, dc_state, breakdown_rate_state]
	all_states={}
	[all_states.update({x:state.UNKNOWN})for x in all_state_names]

	# gui
	gui = None

	# # gui value dict
	# vacuum_level = 'vacuum_level'
	# all_gui_values = [vacuum_level]
	# gui_values={}
	# [gui_values.update({x:0})for x in all_gui_values]


	# Create LLRF Hardware Controllers
	# llrf_controller     = llrf_init.physical_VELA_HRRG_LLRF_Controller()
	llrf_init = VELA_CLARA_LLRF_Control.init()
	llrf_init.setVerbose()
	# The Gun Modulator
	#gun_mod_controller = rf_mod_init.physical_GUN_MOD_Controller()

	# create Python monitoring / control classes
	#llrf = LLRF_monitor.LLRF_monitor(llrf_controller)



	#libera_interlocks = libera_interlocks.libera_interlocks(llrf_controller)
	#gun_modulator = gun_modulator.gun_modulator(gun_mod_controller)

	def __init__(self, argv, config_file, vac_pv = 'EBT-HRG1-VAC-IMG-01:PRES'):
		#QObject.__init__(self)
		# create Python monitoring / control classes


		# mask_setter monitoring
		# self.mask_setter = mask_setter.mask_setter( llrf_controller = self.llrf_controller )
		# self.mask_setter.start()

		# break_down monitoring
		# self.break_down_monitor = break_down_monitor.break_down_monitor(self.llrf_controller)
		# self.break_down_monitor.newBreakDownSignal.connect(self.new_break_down)

		# build a gui
		self.init_gui()


		# read a config
		self.get_config(config_file)

		# init monitors
		# self.init_vac_monitor()
		# self.init_vac_valve_monitor()
		# self.init_cavity_temp_monitor()
		# self.init_water_temp_monitor()
		# self.init_mod_monitor()
		# self.init_rfprot_monitor()



		if self.llrf_type is not LLRF_TYPE.UNKNOWN_TYPE:
			self.llrf_controller = self.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL,
																	self.llrf_type)
			# init the llrf_handler, mainclass to do llrf_stuff
			# self.init_llrf_handler()
			self.llrf_handler = llrf_handler.llrf_handler(
				llrf_controller=self.llrf_controller,
				trace_to_save  = self.llrf_param['TRACES_TO_SAVE']
				)

			# init the llrf gui monitor, this updates gui param
			self.llrf_gui_param_monitor = llrf_gui_param_monitor.llrf_gui_param_monitor(
				llrf_controller = self.llrf_controller,
				gui_dict = self.gui.gui_values,
				enable_key = self.gui.llrf_enabled,
				lock_key = self.gui.llrf_locked,
				pulse_length_key = self.gui.pulse_length,
				monitored_traces = self.llrf_param['TRACES_TO_SAVE'],
				kly_fwd_pwr_key = self.gui.fwd_kly_power,
				kly_rev_pwr_key = self.gui.rev_kly_power,
				cav_fwd_pwr_key = self.gui.fwd_cav_power,
				cav_rev_pwr_key = self.gui.rev_cav_power,
				pulse_count_key = self.gui.pulse_count,
				probe_pwr =self.gui.probe_power
			)

			#llrfObj = [gun.getLLRFObjConstRef()]
			#self.llrf_init.
		else:
			print 'LLRF controller is unknown application weill not work'

		QApplication.processEvents()

		if self.gui is not None:
			self.gui.show()
			self.gui.activateWindow()


	def init_llrf_handler(self):
		if bool(self.llrf_param):
			self.llrf_handler = llrf_handler.llrf_handler()



	def get_config(self,fn):
		reader = config_reader.config_reader(fn)
		self.have_config = reader.get_config()

		self.vac_param = reader.get_vac_parameter()
		self.vac_valve_param = reader.get_vac_valve_parameter()


		self.cavity_temp_param = reader.get_cavity_temp_parameter()
		self.water_temp_param = reader.get_water_temp_parameter()

		self.llrf_param = reader.get_llrf_param()

		self.mod_param = reader.get_mod_param()

		self.rfprot_param = reader.get_rfprot_param()

		self.llrf_param = reader.get_llrf_param()

		self.llrf_type = reader.llrf_type
		if self.have_config:
			self.config = reader.config
		return self.have_config


	def init_gui(self):
		self.gui = gui_conditioning.gui_conditioning()

	def init_mod_monitor(self):
		if self.mod_param:
			self.gun_modulator = gun_modulator.gun_modulator(
				param=self.mod_param,
				gui_dict=self.gui.gui_values,
				gui_dict_key=self.gui.modulator_state
			)

	def init_rfprot_monitor(self):
		if self.rfprot_param:
			self.rf_prot_monitor = rf_protection.rf_protection(
				controller_type = self.rfprot_param['RF_STRUCTURE'],  # MAGIC_STRING
				gui_dict=self.gui.gui_values,
				gui_dict_key=self.gui.rfprot_state
			)




	def init_cavity_temp_monitor(self):
		if bool(self.cavity_temp_param):
			# NOT HAPPY ABOUT HARDCODED STRINGS...
			if self.connectPV(self.cavity_temp_id, self.cavity_temp_param.get('CAVITY_TEMPERATURE_PV')):  # MAGIC_STRING
				self.cavity_temp_param[self.cavity_temp_id] = self.gen_mon_keys[self.cavity_temp_id]
				self.all_states[self.cavity_temp_state] = state.GOOD
				self.cavity_temp_monitor = value_monitor.value_monitor(
					gen_mon=self.gen_mon,
					settings_dict=self.cavity_temp_param,
					id_key=self.cavity_temp_id,
					gui_dict=self.gui.gui_values,
					gui_dict_key=self.gui.cav_temp,
					update_time=self.cavity_temp_param['CAVITY_TEMPERATURE_CHECK_TIME']  # MAGIC_STRING
				)
				self.cavity_temp_monitor.my_name = 'cavity_temp_monitor'
			else:
				self.all_states[self.cavity_temp_state] = state.BAD
		else:
			self.all_states[self.cavity_temp_state] = state.BAD

	def init_water_temp_monitor(self):
		if bool(self.water_temp_param):
			# NOT HAPPY ABOUT HARDCODED STRINGS...
			if self.connectPV(self.water_temp_id,self.water_temp_param.get('WATER_TEMPERATURE_PV')):#MAGIC_STRING
				self.water_temp_param[self.water_temp_id] = self.gen_mon_keys[self.water_temp_id]
				self.all_states[self.water_temp_state] = state.GOOD
				self.water_temp_monitor = value_monitor.value_monitor(
				gen_mon = self.gen_mon,
				settings_dict = self.water_temp_param,
				id_key = self.water_temp_id,
				gui_dict =self.gui.gui_values ,
				gui_dict_key = self.gui.water_temp,
				update_time = self.water_temp_param['WATER_TEMPERATURE_CHECK_TIME']# MAGIC_STRING
				)
				self.water_temp_monitor.my_name = 'water_temp_monitor'
			else:
				self.all_states[self.water_temp_state] = state.BAD
		else:
			self.all_states[self.water_temp_state] = state.BAD


	def init_vac_valve_monitor(self):
		if bool(self.vac_valve_param):
			self.vac_valve_monitor = vac_valve_monitor.vac_valve_monitor(
				area=self.vac_valve_param['VAC_VALVE_CONTROLLER'],#MAGIC_STRING
				valve=self.vac_valve_param['VAC_VALVE'],#MAGIC_STRING
				state_dict=self.all_states,
				state_dict_key= self.vac_valve_state,  # MAGIC_STRING
				gui_dict=self.gui.gui_values,
				gui_dict_key=self.gui.vac_valve_status,
				update_time=self.vac_valve_param['VAC_VALVE_CHECK_TIME']# MAGIC_STRING
				)

	def init_vac_monitor(self):
		if bool(self.vac_param):
			# NOT HAPPY ABOUT HARDCODED STRINGS...
			if self.connectPV(self.vac_id,self.vac_param.get('VAC_PV')):#MAGIC_STRING
				self.vac_param[self.vac_id] = self.gen_mon_keys[self.vac_id]
				# Vacuum monitoring requires a vacuum PV
				self.vacuum_monitor = spike_monitor.spike_monitor(
								gen_mon=self.gen_mon,
								settings_dict = self.vac_param,
								id_key = 'VAC_ID',#MAGIC_STRING
								decay_mode_key = 'VAC_DECAY_MODE',#MAGIC_STRING
								spike_delta_key = 'VAC_SPIKE_DELTA',#MAGIC_STRING
								spike_decay_level_key = 'VAC_SPIKE_DECAY_LEVEL',#MAGIC_STRING
								spike_decay_time_key = 'VAC_SPIKE_DECAY_TIME',#MAGIC_STRING
								num_samples_to_average_key = 'VAC_NUM_SAMPLES_TO_AVERAGE',#MAGIC_STRING
								update_time_key = 'VAC_CHECK_TIME',#MAGIC_STRING
								state_dict = self.all_states,
								state_dict_key ='vacuum_state',#MAGIC_STRING
								gui_dict = self.gui.gui_values,
								gui_dict_val_key=self.gui.vac_level,
								gui_dict_state_key=self.gui.vac_spike_status
								)#MAGIC_STRING
				if self.vacuum_monitor.set_success:
					self.vacuum_monitor.my_name = 'vacuum_monitor'#MAGIC_STRING
					self.vacuum_monitor.start()
					self.monitoring_flags[self.vacuum_monitoring] = True

	@pyqtSlot()
	def new_break_down(self):
		print('Received new break down signal')
		# record current state
		# set powers accordingly
		# set a timer
		# or just set some flags that are handled in main loop?



	# connect to process variable pv
	def connectPV(self, pvKey, pvValue):
		connected = False
		if pvValue is not None:
			id = self.gen_mon.connectPV(pvValue)
			if id != 'FAILED':
				connected = True
				print('Connected to PV = ', pvValue, ' with ID = ', id, ' acquiring data')
				self.gen_mon_keys[pvKey] = id
			else:
				print('Failed to connect to PV = ',pvValue, ' ID = ', id, ' NOT acquiring data')
		else:
			print 'connectPV passed empty PV'
		return connected

	def main_loop(self):

		print('The RF Conditioning Master is Entering Main_Loop ')

		i = 0

		self.llrf.set_klystron_forward_power_trace_mean_range(71, 201)


		while i < 10:

			print self.llrf.get_mean_klystron_foward_power()


			# if self.gun_modulator.is_gun_modulator_in_Trig:
			# 	print 'modulator trig'
			# else:
			# 	print 'modulator NOT IN trig'

			# if self.vacuum_monitor.is_good:
			# 	print 'vacuum_monitor good'
			# else:
			# 	print 'vacuum_monitor bad'

			print 'self.llrf.get_mean_klystron_foward_power()'
			print self.llrf.get_mean_klystron_foward_power()



			#QApplication.processEvents()
			time.sleep(0.1)
			i += 1
			print(' i = ', i)


	def check_breakdown(self):
		print('checking for a break down')






	# OLD AND DEPRICATED
	# slot for vacuum monitor signal to connect to
	# @pyqtSlot()
	# def vac_signal(self,val):
	# 	if val:
	# 		self.all_states[self.vacuum_state] = self.state.GOOD
	# 		print(self.my_name,': Vacuum is good!')
	# 	elif not val:
	# 		self.all_states[self.vacuum_state] = self.state.BAD
	# 		print(self.my_name,': Vacuum is bad!')
	# 	else:
	# 		self.all_states[self.vacuum_state] = self.state.UNKNOWN
	# 		print(self.my_name, ': Vacuum is in UNKNOWN STATE')



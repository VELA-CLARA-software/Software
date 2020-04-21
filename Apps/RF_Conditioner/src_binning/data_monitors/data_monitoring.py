# from VELA_CLARA_LLRF_Control import LLRF_TYPE
# import VELA_CLARA_General_Monitor
# import vac_valve_monitor
# import value_monitor
# import spike_monitor
# import modulator_monitor
# import outside_mask_trace_monitor
# import rf_protection_monitor
# import llrf_simple_param_monitor
import src.data.rf_condition_data_base as dat
from data_monitoring_base import data_monitoring_base
from src.data.state import state
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_RF_Modulator_Control import L01_MOD_STATE
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS



class data_monitoring(data_monitoring_base):
	#whoami
	my_name = 'data_monitoring'

	monitor_funcs = {}
	def __init__(self):
		data_monitoring_base.__init__(self)
		# these are the monitors for the main_loop param
		# they are VAC,DC,BREAKDOWN,BREAKDOWN_RATE,RF 
		# and connected if monitoring those parameters
		self.main_monitor_states = data_monitoring.data.main_monitor_states
		self.enable_RF_monitor_states  = data_monitoring.data.enable_RF_monitor_states
		#self.previous_main_monitor_states = data_monitoring.data.previous_main_monitor_states

	def init_monitor_states(self):
		'''
			based on the manin data dictionary values, we keep a simplified list of states
			These states are required for the conditioning procedure
		'''
		data_monitoring.logger.header(self.my_name + ' init_monitor_states, setting up main monitors ', True)
		if self.is_monitoring[dat.vac_spike_status]:
			self.main_monitor_states[dat.vac_spike_status] = state.GOOD
			self.monitor_funcs['VAC'] = self.vac
			data_monitoring.logger.message('adding vac_spike to main loop checks', True)
		else:
			data_monitoring.logger.message('NOT adding vac_spike_status to main loop checks', True)

		if self.is_monitoring[dat.DC_spike_status]:
			self.main_monitor_states[dat.DC_spike_status] = state.GOOD
			#self.previous_main_monitor_states[dat.DC_spike_status] = state.UNKNOWN
			self.monitor_funcs['DC'] = self.DC
			data_monitoring.logger.message('adding DC_spike_status to main loop checks', True)
		else:
			data_monitoring.logger.message('NOT adding DC_spike to main loop checks', True)
		if self.is_monitoring[dat.breakdown_status]:
			data_monitoring.logger.message('adding breakdown_status to main loop checks', True)
			self.main_monitor_states[dat.breakdown_status] = state.GOOD
			#self.previous_main_monitor_states[dat.breakdown_status] = state.UNKNOWN
			self.monitor_funcs['breakdown'] = self.breakdown
		else:
			data_monitoring.logger.message('NOT adding breakdown_status to main loop checks', True)


		''' These are the RF paramters states required for enable_RF'''
		if self.is_monitoring[dat.modulator_state]:
			data_monitoring.logger.message('adding modulator to main loop checks', True)
			self.enable_RF_monitor_states[dat.mod_output_status] = state.INIT
			#self.previous_main_monitor_states[dat.mod_output] = state.UNKNOWN
			self.monitor_funcs['RF_Mod'] = self.RF_Mod
		else:
			data_monitoring.logger.message('NOT adding modulator to main loop checks', True)

		if self.is_monitoring[dat.rfprot_state]:
			data_monitoring.logger.message('adding RF Protection to main loop checks', True)
			self.enable_RF_monitor_states[dat.rfprot_state] = state.INIT
			self.monitor_funcs['RF_Prot'] = self.RF_Prot
		else:
			data_monitoring.logger.message('NOT adding RF Protection to to main loop checks', True)

		#
		# next we add in the LLRF monitoring stats
		#
		# CAN RF output is a combination of all LLRF states AND the gui llrf_enable_button  state
		# it is update dby its own funciton, which is passed in the state of the GUI button
		#self.main_monitor_states[dat.can_rf_output] = state.INIT
		self.enable_RF_monitor_states[dat.llrf_interlock_status] = state.INIT
		self.enable_RF_monitor_states[dat.llrf_trigger_status] = state.INIT
		self.enable_RF_monitor_states[dat.pulse_length_status] = state.INIT
		self.enable_RF_monitor_states[dat.llrf_output_status] = state.INIT
		self.enable_RF_monitor_states[dat.llrf_ff_amp_locked_status] = state.INIT
		self.enable_RF_monitor_states[dat.llrf_ff_ph_locked_status] = state.INIT
		# add can_rf_output to main monitor states, so it can go new bad and

		#self.enable_RF_monitor_states[dat.llrf_DAQ_rep_rate_status] = state.INIT

	def update_enable_LLRF_state(self, gui_enable_rf):
		''' checks everything to enable RF power '''
		#self.main_monitor_states[dat.can_rf_output] = state.BAD
		#print('update_enable_LLRF_state,', gui_enable_rf)
		self.data.values[dat.can_rf_output] = state.BAD
		if gui_enable_rf:

			# probably don;t need to copy this data  ...
			self.enable_RF_monitor_states[dat.llrf_interlock_status] = self.data.values[dat.llrf_interlock_status]
			self.enable_RF_monitor_states[dat.llrf_trigger_status] = self.data.values[dat.llrf_trigger_status]
			self.enable_RF_monitor_states[dat.pulse_length_status] = self.data.values[dat.pulse_length_status]
			self.enable_RF_monitor_states[dat.llrf_output_status] = self.data.values[dat.llrf_output_status]
			self.enable_RF_monitor_states[dat.llrf_ff_amp_locked_status] = self.data.values[dat.llrf_ff_amp_locked_status]
			self.enable_RF_monitor_states[dat.llrf_ff_ph_locked_status] = self.data.values[dat.llrf_ff_ph_locked_status]

			if all(value == state.GOOD for value in self.enable_RF_monitor_states.values()):
				self.data.values[dat.can_rf_output] = state.GOOD

			if self.data.values[dat.can_rf_output_OLD] == state.GOOD:
				if self.data.values[dat.can_rf_output] == state.BAD:
					self.data.values[dat.can_rf_output] = state.NEW_BAD
					#print('Print RF OUTPUT IN NEW BAD')

			if self.data.values[dat.can_rf_output_OLD] == state.BAD:
				if self.data.values[dat.can_rf_output] == state.GOOD:
					self.data.values[dat.can_rf_output] = state.NEW_GOOD
					#print('Print RF OUTPUT IN NEW GOOD')

			self.data.values[dat.can_rf_output_OLD] = self.data.values[dat.can_rf_output]

				#print('self.data.values[dat.can_rf_output] = state.GOOD')

		else:
			pass
			#print('gui_enable_rf = FALSE')
		# now update the state

		#self.update_state(dat.can_rf_output)

	def daq_freq_bad(self):
		return self.data.values[dat.llrf_DAQ_rep_rate_status] == state.BAD

	def daq_freq_new_good(self):
		return self.data.values[dat.llrf_DAQ_rep_rate_status] == state.NEW_GOOD

	def enable_RF_bad(self):
		#return state.BAD in self.enable_RF_monitor_states.values()
		if self.data.values[dat.can_rf_output] == state.BAD:
			return True
		if self.data.values[dat.can_rf_output] == state.NEW_BAD:
			return True


	def update_states(self ):
		''' updates main_monitor_states using function sdefined in self.monitor_funcs'''
		#print('update_state')
		for key in self.monitor_funcs.keys():
			#print ('def update_states(self):  ',key)
			self.monitor_funcs[key]()

	def new_bad(self):
		return state.NEW_BAD in self.main_monitor_states.values()

	def new_good_no_bad(self):
		if self.enable_RF_bad():
			return False
		if self.no_bad():
			if state.NEW_GOOD in self.main_monitor_states.values():
				return True
			if self.data.values[dat.can_rf_output] == state.NEW_GOOD:
				return True
		return False

	def no_bad(self):
		for item in self.main_monitor_states.values():
			if item == state.BAD or item == state.NEW_BAD:
				return False
		return True

	def bad(self):
		return state.BAD in self.main_monitor_states.values()

	def all_good(self):
		for key,value in self.main_monitor_states.iteritems():
			#print("def all_good(self): ", key," ",value)
			if value != state.GOOD:
				return False
		return True

	def vac_new_bad(self):
		try:
			return self.main_monitor_states[dat.vac_spike_status] == state.NEW_BAD
		except:
			return False

	def dc_new_bad(self):
		try:
			return self.main_monitor_states[dat.DC_spike_status] == state.NEW_BAD
		except:
			return False

	def print_main_monitor_states(self):
		for key,value in self.main_monitor_states.iteritems():
			print(key," ", state.statename[value])

	def new_bad_is_not_outside_mask(self):
		return self.main_monitor_states[dat.breakdown_status] != state.NEW_BAD

	def check_if_new_bad_is_vac_or_DC(self):
		if self.vac_new_bad():
			data_monitoring_base.logger.message('MAIN-LOOP New VAC BAD State', True)
		if self.dc_new_bad():
			data_monitoring.logger.message('MAIN-LOOP New DC BAD State', True)

	def DC(self):
		#print('DC')
		self.update_state(dat.DC_spike_status)

	# this function updates parameters used in main_loop that decide what the programme should do
	def vac(self):
		self.update_state(dat.vac_spike_status)

	# its horrible atm but can be cleaned up later .. ?
	def breakdown(self):
		#print('breakdown(self)')
		self.update_state(dat.breakdown_status)

	# is RF goof, have mod, have locks?
	def RF_Mod(self):
		#print('RF')
		# assume there is one PV that gives the RF state,
		# MODULATOR, INTERLOCKS, LLRF
		# wich MAY NOT be true
		if self.data.values[dat.modulator_state] == GUN_MOD_STATE.RF_ON:
			self.enable_RF_monitor_states[dat.mod_output_status] = state.GOOD
		elif self.data.values[dat.modulator_state] == L01_MOD_STATE.L01_RF_ON:
			self.enable_RF_monitor_states[dat.mod_output_status] = state.GOOD
		else:
			self.enable_RF_monitor_states[dat.mod_output_status] = state.BAD
		# if self.is_gun_type(data_monitoring_base.llrf_type):
		# 	if self.data.values[dat.modulator_state] !=  GUN_MOD_STATE.RF_ON:
		# 		self.main_monitor_states[dat.mod_output_status] = state.BAD
		# 	else:
		# 		self.main_monitor_states[dat.mod_output_status] = state.GOOD
		# else:
		# 	if self.data.values[dat.modulator_state] != L01_MOD_STATE.L01_RF_ON:
		# 		self.main_monitor_states[dat.mod_output_status] = state.BAD
		# 	else:
		# 		self.main_monitor_states[dat.mod_output_status] = state.GOOD

	def RF_Prot(self):
		if self.data.values[dat.rfprot_state] == RF_PROT_STATUS.GOOD:
			self.enable_RF_monitor_states[dat.rfprot_state] = state.GOOD
		else:
			self.enable_RF_monitor_states[dat.rfprot_state] = state.BAD

	def is_bad_or_new_bad(self, key):
		if self.main_monitor_states[key] == state.NEW_BAD:
			return True
		elif self.main_monitor_states[key] == state.BAD:
			return True
		return False

	def update_state(self,key):
		if self.data.values[key] == state.BAD:
			if self.main_monitor_states[key] == state.GOOD:
				self.main_monitor_states[key] = state.NEW_BAD

			elif self.main_monitor_states[key] == state.NEW_GOOD:
				self.main_monitor_states[key] = state.NEW_BAD

			elif self.main_monitor_states[key] == state.NEW_BAD:
				self.main_monitor_states[key] = state.BAD

			elif self.main_monitor_states[key] == state.BAD:
				self.main_monitor_states[key] = state.BAD

			elif self.main_monitor_states[key] == state.BAD:
				pass
			else:
				self.main_monitor_states[key] = state.BAD

		elif self.data.values[key] == state.GOOD:
			if self.main_monitor_states[key] == state.BAD:
				self.main_monitor_states[key] = state.NEW_GOOD

			elif self.main_monitor_states[key] == state.NEW_GOOD:
				self.main_monitor_states[key] = state.GOOD

			elif self.main_monitor_states[key] == state.NEW_BAD:
				self.main_monitor_states[key] = state.NEW_GOOD

			elif self.main_monitor_states[key] == state.GOOD:
				pass
			else:
				self.main_monitor_states[key] = state.GOOD

		elif self.data.values[key] == state.UNKNOWN:
			data_monitoring_base.logger.message(self.my_name + ' update_state UNKNOWN', True)

		elif self.data.values[key] == state.INIT:
			data_monitoring_base.logger.message(self.my_name + ' update_state INIT', True)

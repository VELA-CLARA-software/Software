# from VELA_CLARA_LLRF_Control import LLRF_TYPE
# import VELA_CLARA_General_Monitor
# import vac_valve_monitor
# import value_monitor
# import spike_monitor
# import modulator_monitor
# import outside_mask_trace_monitor
# import rf_protection_monitor
# import llrf_simple_param_monitor
import data.rf_condition_data_base as dat
from data_monitoring_base import data_monitoring_base
from data.state import state
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE



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
		#self.previous_main_monitor_states = data_monitoring.data.previous_main_monitor_states

	def init_monitor_states(self):
		self.logger.header(self.my_name + ' init_monitor_states, setting up main monitors ')
		if self.is_monitoring[dat.vac_spike_status]:
			self.logger.message('adding vac_spike to main loop checks')
			self.main_monitor_states[dat.vac_spike_status] = state.INIT
			#self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['VAC'] = self.vac
		else:
			self.logger.message('NOT adding vac_spike_status to main loop checks')

		if self.is_monitoring[dat.DC_spike_status]:
			self.logger.message('adding DC_spike_status to main loop checks')
			self.main_monitor_states[dat.DC_spike_status] = state.INIT
			#self.previous_main_monitor_states[dat.DC_spike_status] = state.UNKNOWN
			self.monitor_funcs['DC'] = self.DC
		else:
			self.logger.message('NOT adding DC_spike to main loop checks')

		if self.is_monitoring[dat.breakdown_status]:
			self.logger.message('adding breakdown_status to main loop checks')
			self.main_monitor_states[dat.breakdown_status] = state.INIT
			#self.previous_main_monitor_states[dat.breakdown_status] = state.UNKNOWN
			self.monitor_funcs['breakdown'] = self.breakdown
		else:
			self.logger.message('NOT adding breakdown_status to main loop checks')
		if self.is_monitoring[dat.modulator_state]:
			self.logger.message('adding llrf_output to main loop checks')
			self.main_monitor_states[dat.llrf_output] = state.INIT
			#self.previous_main_monitor_states[dat.llrf_output] = state.UNKNOWN
			self.monitor_funcs['RF'] = self.RF
		else:
			self.logger.message('NOT adding llrf_output to main loop checks')
		self.main_monitor_states[dat.llrf_output] = state.INIT		

	def update_states(self):
		#print('update_state')
		for key in self.monitor_funcs.keys():
			self.monitor_funcs[key]()

	def new_bad(self):
		return state.NEW_BAD in self.main_monitor_states.values()

	def new_good_no_bad(self):
		if self.no_bad():
			return state.NEW_GOOD in self.main_monitor_states.values()
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
			#print(key," ",value)
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
		#print('vac')
		self.update_state(dat.vac_spike_status)

	# its horrible atm but can be cleaned up later .. ?
	def breakdown(self):
		#print('breakdown(self)')
		self.update_state(dat.breakdown_status)
		#print('breakdown state = ',)

	# is RF goof, have mod, have locks?
	def RF(self):
		#print('RF')
		# assume there is one PV that gives the RF state,
		# MODULATOR, INTERLOCKS, LLRF
		# wich MAY NOT be true
		if self.data.values[dat.modulator_state] != GUN_MOD_STATE.Trig:
			self.main_monitor_states[dat.llrf_output] = state.BAD
		else:
			if self.data.values[dat.llrf_output]:
				self.main_monitor_states[dat.llrf_output] = state.GOOD
			else:
				self.main_monitor_states[dat.llrf_output] = state.BAD

	# its horrible atm but can be cleaned up later .. ?
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


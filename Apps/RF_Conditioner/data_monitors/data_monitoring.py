from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_General_Monitor
import vac_valve_monitor
import value_monitor
import spike_monitor
import modulator_monitor
import outside_mask_trace_monitor
import rf_protection_monitor
import llrf_simple_param_monitor
import data.rf_condition_data_base as dat
from data_monitoring_base import data_monitoring_base
from data.state import state


class data_monitoring(data_monitoring_base):
	#whoami
	my_name = 'data_monitoring'

	monitor_funcs = {}
	def __init__(self,data):
		data_monitoring_base.__init__(self,data=data)
		# these are the monitors for the main_loop param
		# they are VAC,DC,BREAKDOWN,BREAKDOWN_RATE,RF 
		# and connected if monitoring those parameters
		self.main_monitor_states = data.main_monitor_states
		self.previous_main_monitor_states = data.previous_main_monitor_states


	def init_monitor_states(self):
		if self.is_monitoring[dat.vac_spike_status]:
			print(self.my_name + ' adding vac_spike to main loop checks')
			self.main_monitor_states[dat.vac_spike_status] = state.INIT
			self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['VAC'] = self.vac
		else:
			print(self.my_name + ' NOT adding vac_spike_status to main loop checks')
		if self.is_monitoring[dat.DC_spike_status]:
			print(self.my_name + ' adding DC_spike_status to main loop checks')
			self.main_monitor_states[dat.DC_spike_status] = state.INIT
			self.previous_main_monitor_states[dat.DC_spike_status] = state.UNKNOWN
			self.monitor_funcs['DC'] = self.vac
		else:
			print(self.my_name + ' NOT adding DC_spike to main loop checks')
		if self.is_monitoring[dat.breakdown_status]:
			print(self.my_name + ' adding breakdown_status to main loop checks')
			self.main_monitor_states[dat.breakdown_status] = state.INIT
			self.previous_main_monitor_states[dat.breakdown_status] = state.UNKNOWN
			self.monitor_funcs['breakdown'] = self.vac
		else:
			print(self.my_name + ' NOT adding breakdown_status to main loop checks')
		if self.is_monitoring[dat.breakdown_rate]:
			print(self.my_name + ' adding breakdown_rate to main loop checks')
			self.main_monitor_states[dat.breakdown_rate] = state.INIT
			self.previous_main_monitor_states[dat.breakdown_rate] = state.UNKNOWN
			self.monitor_funcs['RF'] = self.vac
		else:
			print(self.my_name + ' NOT adding breakdown_rate to main loop checks')
		self.main_monitor_states[dat.llrf_output] = state.INIT		

	def update(self):
		for key in self.monitor_funcs.keys():
			self.main_monitor_states[key]()

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
		for item in self.main_monitor_states.values():
			if item != state.GOOD:
				return False
		return True


			# # this sets up a dict of states for things that ARE being monitored
		# # run this function after setting up monitor!
		# for key,val in self.is_monitoring.iteritems():
		# 	if key not in self.passive_monitors:
		# 		if val:
		# 			self.main_monitor_states[key] = state.INIT
		# # set the previous  values
		# for key,value in self.main_monitor_states:
		# 	self.previous_main_monitor_states[key] = state.UNKNOWN

	# this function updates parameters used in main_loop that decide what the programme should do
	def DC(self):
		self.update_state(dat.DC_spike_status)

	# this function updates parameters used in main_loop that decide what the programme should do
	def vac(self):
		self.update_state(dat.vac_spike_status)

	# its horrible atm but can be cleaned up later .. ?
	def breakdown(self):
		self.update_state(dat.breakdown_status)

	# is RF goof, have mod, have locks?
	def RF(self):
		# assume there is one PV that gives the RF state,
		# MODULATOR, INTERLOCKS, LLRF
		# wich MAY NOT be true
		# if data.values[dat.modulator_state] != GUN_MOD_STATE.Trig:
		if self.data.values[dat.llrf_output]:
			self.main_monitor_states[dat.llrf_output] = state.GOOD
		else:
			self.main_monitor_states[dat.llrf_output] = state.GOOD

	# its horrible atm but can be cleaned up later .. ?
	def update_state(self,key):
		if self.data.values[key] == STATE.GOOD:
			if self.previous_main_monitor_states[key] == STATE.GOOD:
				#assume main state i sgood
				pass
			elif self.previous_main_monitor_states[key] == STATE.BAD:
				self.set_state(key, state.NEW_GOOD)
			elif self.previous_main_monitor_states[key] == STATE.NEW_GOOD:
				self.set_state(key, state.GOOD)
			else:
				self.set_state(key, state.GOOD)

		elif self.data.values[key] == STATE.BAD:
			if self.previous_main_monitor_states[key] == STATE.GOOD:
				self.set_state(key, state.NEW_BAD)
			elif self.previous_main_monitor_states[key] == STATE.NEW_BAD:
				self.set_state(key, state.BAD)
			elif self.previous_main_monitor_states[key] == STATE.BAD:
				pass
			else:
				self.set_state(key, state.BAD)
		elif self.data.values[key] == STATE.UNKNOWN:
			self.set_state(key, state.UNKNOWN)

	def set_state(self,key,state):
		self.previous_main_monitor_states[key] =self.main_monitor_states[key]
		self.main_monitor_states[dat.vac_valve_status] = state

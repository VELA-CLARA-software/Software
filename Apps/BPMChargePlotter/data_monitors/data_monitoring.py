import charge_monitor
import bpm_monitor
import data.bpm_charge_plotter_data_base as dat
from data_monitoring_base import data_monitoring_base
from data.state import state

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
		self.main_monitor_states[dat.scan_status] = 'not_scanning'
		self.logger.header(self.my_name + ' init_monitor_states, setting up main monitors ')
		if self.is_monitoring[dat.bpm_status]:
			self.logger.message('adding bpms to monitor checks')
			self.main_monitor_states[dat.bpm_status] = True
			#self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['BPM'] = True
		else:
			self.logger.message('NOT adding bpm_status to main loop checks')

		if self.is_monitoring[dat.charge_status]:
			self.logger.message('adding charge to monitor checks')
			self.main_monitor_states[dat.charge_status] = True
			# self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['CHARGE'] = True
		else:
			self.logger.message('NOT adding charge_status to main loop checks')
    #
	def update_states(self):
		for key in self.monitor_funcs.keys():
			self.monitor_funcs[key]()
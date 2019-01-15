import charge_monitor
import blm_monitor
import data.blm_plotter_data_base as dat
from data_monitoring_base import data_monitoring_base
from data.state import state

class data_monitoring(data_monitoring_base):
	#whoami
	my_name = 'data_monitoring'

	monitor_funcs = {}
	def __init__(self):
		data_monitoring_base.__init__(self)
		self.main_monitor_states = data_monitoring.data.main_monitor_states
		#self.previous_main_monitor_states = data_monitoring.data.previous_main_monitor_states

	def init_monitor_states(self):
		self.main_monitor_states[dat.scan_status] = 'not_scanning'
		self.logger.header(self.my_name + ' init_monitor_states, setting up main monitors ')
		if self.is_monitoring[dat.blm_status]:
			self.logger.message('adding blms to monitor checks')
			self.main_monitor_states[dat.blm_status] = True
			self.monitor_funcs['BLM'] = True
		else:
			self.logger.message('NOT adding bpm_status to main loop checks')

		if self.is_monitoring[dat.charge_status]:
			self.logger.message('adding charge to monitor checks')
			self.main_monitor_states[dat.charge_status] = True
			# self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['CHARGE'] = True
		else:
			self.logger.message('NOT adding charge_status to main loop checks')
		if self.main_monitor_states[dat.blm_status] == True and self.main_monitor_states[dat.charge_status] == True:
			self.main_monitor_states[dat.ready_to_go] = True
		return self.main_monitor_states[dat.ready_to_go]

	def update_states(self):
		for key in self.monitor_funcs.keys():
			self.monitor_funcs[key]()
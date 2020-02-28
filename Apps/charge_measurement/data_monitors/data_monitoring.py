import data_monitors.pil_monitor
import data_monitors.llrf_monitor
import data_monitors.mag_monitor
import data.charge_measurement_data_base as dat
from data_monitors.data_monitoring_base import data_monitoring_base
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
		if dat.pil_status:
			self.logger.message('adding PIL to monitor checks')
			self.main_monitor_states[dat.pil_status] = True
			#self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['PIL'] = True
		else:
			self.logger.message('NOT adding pil_status to main loop checks')

		if dat.llrf_status:
			self.logger.message('adding gun llrf to monitor checks')
			self.main_monitor_states[dat.llrf_status] = True
			# self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['LLRF'] = True
		else:
			self.logger.message('NOT adding llrf_status to main loop checks')

		if dat.mag_status:
			self.logger.message('adding magnets to monitor checks')
			self.main_monitor_states[dat.mag_status] = True
			# self.previous_main_monitor_states[dat.vac_spike_status] = state.UNKNOWN
			self.monitor_funcs['MAG'] = True
		else:
			self.logger.message('NOT adding mag_status to main loop checks')

	def update_states(self):
		for key in self.monitor_funcs.keys():
			self.monitor_funcs[key]()
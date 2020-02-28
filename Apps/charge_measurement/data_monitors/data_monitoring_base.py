from data_monitors.pil_monitor import pil_monitor
from data_monitors.llrf_monitor import llrf_monitor
from data_monitors.mag_monitor import mag_monitor
import data.charge_measurement_data_base as dat
from base.base import base

class data_monitoring_base(base):
	#whomai
	my_name = 'data_monitoring_base'
	# we can make some reasonable guesses as to what will be
	# monitored from gen_mon
	# every key from gen_mon will be stored here
	gen_mon_keys = {}
	# we can make some reasonable guesses as to what will be included
	pil_id = 'PIL_ID'
	llrf_id = 'LLRF_ID'
	mag_id = 'MAG_ID'
	all_id = [pil_id, llrf_id, mag_id]
	gen_mon_keys.update({pil_id:None})
	gen_mon_keys.update({llrf_id:None})
	gen_mon_keys.update({mag_id:None})
	# explicit flags for possible monitors & monitors states
	# these are used to determine if monitoring these items is happening
	# they're NOT for defining vacuum good, / bad etc.
	# we use the same keys as the data.dict etc

	pil_monitoring = "pil_monitoring"
	llrf_monitoring = "llrf_monitoring"
	mag_monitoring = "mag_monitoring"

	is_monitoring = {}
	all_monitors = [pil_monitoring,
					llrf_monitoring,
					mag_monitoring]
	is_monitoring.update({pil_monitoring:False})
	is_monitoring.update({llrf_monitoring: False})
	is_monitoring.update({mag_monitoring: False})
	#
	#all poossible monitors
	pil_monitor = None
	llrf_monitor = None
	mag_monitor = None

	def __init__(self):
		base.__init__(self)

	def start_monitors(self):
		self.logger.header(self.my_name + ' start_monitors ')
		##
		if base.config.pil_config:
			if self.start_pil_monitor():
				self.logger.message('Monitoring PIL', True)
			else:
				self.logger.message('Not monitoring PIL - failed', True)
		else:
			self.logger.message('Not monitoring PIL - No config data',True)
		##
		if base.config.llrf_config:
			if self.start_llrf_monitor():
				self.logger.message('Monitoring gun LLRF', True)
			else:
				self.logger.message('Not monitoring gun LLRF - start_llrf_monitor failed', True)
		else:
			self.logger.message('Not monitoring gun LLRF - No config data', True)
		if base.config.mag_config:
			if self.start_mag_monitor():
				self.logger.message('Monitoring magnets', True)
			else:
				self.logger.message('Not monitoring magnets - start_mag_monitor failed', True)
		else:
			self.logger.message('Not monitoring magnets - No config data',True)

	def start_pil_monitor(self):
		data_monitoring_base.pil_monitor = pil_monitor()
		data_monitoring_base.is_monitoring[dat.pil_status] = data_monitoring_base.pil_monitor.set_success
		self.check_mode()
		return data_monitoring_base.pil_monitor.set_success

	def start_llrf_monitor(self):
		data_monitoring_base.llrf_monitor = llrf_monitor()
		data_monitoring_base.is_monitoring[dat.llrf_status] = data_monitoring_base.llrf_monitor.set_success
		return data_monitoring_base.llrf_monitor.set_success

	def start_mag_monitor(self):
		data_monitoring_base.mag_monitor = mag_monitor()
		data_monitoring_base.is_monitoring[dat.mag_status] = data_monitoring_base.mag_monitor.set_success
		return data_monitoring_base.mag_monitor.set_success

	def check_mode(self):
		print(dat.machine_mode)
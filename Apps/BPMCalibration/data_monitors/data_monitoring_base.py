import scope_monitor
import bpm_monitor
import data.bpm_calibrate_data_base as dat
from base.base import base

class data_monitoring_base(base):
	#whomai
	my_name = 'data_monitoring_base'
	# we can make some reasonable guesses as to what will be
	# monitored from gen_mon
	# every key from gen_mon will be stored here
	gen_mon_keys = {}
	# we can make some reasonable guesses as to what will be included
	bpm_id = 'BPM_ID'
	scope_id = 'SCOPE_ID'
	all_id = [bpm_id, scope_id]
	[gen_mon_keys.update({x: None}) for x in all_id]
	# explicit flags for possible monitors & monitors states
	# these are used to determine if monitoring these items is happening
	# they're NOT for defining vacuum good, / bad etc.
	# we use the same keys as the data.dict etc

	bpm_monitoring = "bpm_monitoring"
	scope_monitoring = "scope_monitoring"

	is_monitoring = {}
	all_monitors = [bpm_monitoring,
					bpm_monitoring]
	[is_monitoring.update({x: False}) for x in all_monitors]
	#
	#all poossible monitors
	bpm_monitor = None
	scope_monitor = None

	def __init__(self):
		base.__init__(self)

	def start_monitors(self):
		self.logger.header(self.my_name + ' start_monitors ')
		##
		if base.config.bpm_config:
			if self.start_bpm_monitor():
				self.logger.message('Monitoring BPMs', True)
			else:
				self.logger.message('Not monitoring BPMs - failed', True)
		else:
			self.logger.message('Not monitoring BPMs - No config data',True)
		##
		if base.config.scope_config:
			if self.start_scope_monitor():
				self.logger.message('Monitoring Scope', True)
			else:
				self.logger.message('Not monitoring Scope - start_scope_monitor failed', True)
		else:
			self.logger.message('Not monitoring Scope - No config data',True)

	def start_bpm_monitor(self):
		data_monitoring_base.bpm_monitor = bpm_monitor.bpm_monitor()
		data_monitoring_base.is_monitoring[dat.bpm_status] = data_monitoring_base.bpm_monitor.set_success
		self.check_mode()
		return data_monitoring_base.bpm_monitor.set_success

	def start_scope_monitor(self):
		data_monitoring_base.scope_monitor = scope_monitor.scope_monitor()
		data_monitoring_base.is_monitoring[dat.scope_status] = data_monitoring_base.scope_monitor.set_success
		return data_monitoring_base.scope_monitor.set_success

	def check_mode(self):
		print dat.machine_mode
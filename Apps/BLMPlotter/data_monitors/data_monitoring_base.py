import charge_monitor
import blm_monitor
import data.blm_plotter_data_base as dat
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
	charge_id = 'CHARGE_ID'
	all_id = [bpm_id, charge_id]
	[gen_mon_keys.update({x: None}) for x in all_id]
	# explicit flags for possible monitors & monitors states
	# these are used to determine if monitoring these items is happening
	# they're NOT for defining vacuum good, / bad etc.
	# we use the same keys as the data.dict etc

	blm_monitoring = "blm_monitoring"
	charge_monitoring = "charge_monitoring"

	is_monitoring = {}
	all_monitors = [blm_monitoring,
					charge_monitoring]
	[is_monitoring.update({x: False}) for x in all_monitors]
	#
	#all poossible monitors
	bpm_monitor = None
	charge_monitor = None

	def __init__(self):
		base.__init__(self)

	def start_monitors(self):
		self.logger.header(self.my_name + ' start_monitors ')
		##
		if self.start_blm_monitor():
			self.logger.message('Monitoring BLMs', True)
		else:
			self.logger.message('Not monitoring BLMs - failed', True)
		if self.start_charge_monitor():
			self.logger.message('Monitoring charge', True)
		else:
			self.logger.message('Not monitoring charge - start_charge_monitor failed', True)

	def start_blm_monitor(self):
		data_monitoring_base.blm_monitor = blm_monitor.blm_monitor()
		data_monitoring_base.is_monitoring[dat.blm_status] = data_monitoring_base.blm_monitor.set_success
		self.check_mode()
		return data_monitoring_base.blm_monitor.set_success

	def start_charge_monitor(self):
		data_monitoring_base.charge_monitor = charge_monitor.charge_monitor()
		data_monitoring_base.is_monitoring[dat.charge_status] = data_monitoring_base.charge_monitor.set_success
		return data_monitoring_base.charge_monitor.set_success

	def check_mode(self):
		print dat.machine_mode
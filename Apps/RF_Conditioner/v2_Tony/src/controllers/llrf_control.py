# llrf_handler.py
import src.data.rf_condition_data_base as dat
#from VELA_CLARA_LLRF_Control import LLRF_SCAN

from src.data import config
from src.data import rf_conditioning_logger
from src.data.rf_conditioning_data import rf_conditioning_data
import hardware_control_hub


class llrf_control(object):
	"""
	This class is for controlling the LLRF,
	All "puts" should happen here
	All "gets" should happen in the LLRF monitor
	"""
	# whoami
	# init attributes
	power_traces = []
	pulse_end_index = 0
	pulse_end = 0
	mask_set = False
	mask_count = 0

	def __init__(self):
		self.my_name = 'hardware_control_hub'
		# owns a config and logging class
		self.config = config.config()
		self.config_data = self.config.raw_config_data

		self.logger = rf_conditioning_logger.rf_conditioning_logger()
		self.llrf_type = self.config_data[self.config.RF_STRUCTURE]

		# the data class
		self.data = rf_conditioning_data()
		self.values = rf_conditioning_data.values
		self.expert_values = rf_conditioning_data.expert_values

		self.hardware = hardware_control_hub.hardware_control_hub()
		self.llrf_control = self.hardware.llrf_control


	def set_trace_mean_positions(self):
		"""
		sets the mean start and end positions from the config file
		:return:
		"""
		cd =self.config_data
		c =self.config


		for trace in cd[c.MEAN_TRACES]:
			print("set_trace_mean_positions trace = ", trace)
			if 'KLYSTRON_FORWARD_POWER' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.KFPOW_MEAN_START], cd[c.KFPOW_MEAN_END], trace)
			elif 'KLYSTRON_REVERSE_POWER' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.KRPOW_MEAN_START], cd[c.KRPOW_MEAN_END], trace)
			elif 'CAVITY_FORWARD_POWER' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.CFPOW_MEAN_START], cd[c.CFPOW_MEAN_END], trace)
			elif 'CAVITY_REVERSE_POWER' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.CRPOW_MEAN_START], cd[c.CRPOW_MEAN_END], trace)
			elif 'CAVITY_PROBE_POWER' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.CPPOW_MEAN_START], cd[c.CPPOW_MEAN_END], trace)

			elif 'KLYSTRON_FORWARD_PHASE' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.KFPHA_MEAN_START], cd[c.KFPHA_MEAN_END], trace)
			elif 'KLYSTRON_REVERSE_PHASE' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.KRPHA_MEAN_START], cd[c.KRPHA_MEAN_END], trace)
			elif 'CAVITY_FORWARD_PHASE' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.CFPHA_MEAN_START], cd[c.CFPHA_MEAN_END], trace)
			elif 'CAVITY_REVERSE_PHASE' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.CRPHA_MEAN_START], cd[c.CRPHA_MEAN_END], trace)
			elif 'CAVITY_PROBE_PHASE' in trace:
				self.llrf_control.setMeanStartEndTime(cd[c.CPPHA_MEAN_START], cd[c.CPPHA_MEAN_END], trace)


		#
		#
		# self.get_pulse_end()
		# # MUST BE CALLED AFTER CHANGING PULSE WIDTH ' CANCER
		# base.logger.header(self.my_name + ' set_mean_pwr_position',True)
		# base.logger.message([
		# 	'rf pulse end time = ' + str(self.pulse_end) + ', index = ' + str(self.pulse_end_index),
		# 	'pulse_latency     = '  + str(base.llrfObj[0].pulse_latency),
		# 	'.getPulseLength() = ' + str(base.llrf_control.getPulseLength())],True)
		# s = None
		# e = None
		# if base.config.llrf_config.has_key('MEAN_TRACES'):
		# 	i = 0
		# 	for trace in base.config.llrf_config['MEAN_TRACES']:
		# 		base.logger.message(trace + ' found in config file', True)
		# 		i += 1
		# 		r = self.has_mean_start_end_key_i(i)
		# 		if r != False:
		# 			if base.llrf_control.setMeanStartEndTime(r[0], r[1], trace):
		# 				base.logger.message(trace + ' mean monitoring started', True)
		# 				base.logger.message(['trace_mean_start/end Set Times (us) = ' + str(r[0]) +
		# 				                     '/' +
		# 				                     str(r[1]),
		# 									 'meantime = ' + str(r[1] - r[0])], True)
		#
		# 				actual_start_index = base.llrf_control.getMeanStartIndex(trace)
		# 				actual_stop_index = base.llrf_control.getMeanStopIndex(trace)
		#
		# 				actual_start_time = base.llrf_control.getTime(actual_start_index)
		# 				actual_stop_time = base.llrf_control.getTime(actual_stop_index)
		#
		#
		#
		# 				base.logger.message(['trace_mean_start/end Read Times (us) = ' +
		# 				                     str(actual_start_time) + '/' + str(actual_stop_time),
		# 									 'meantime = ' + str(actual_stop_time - actual_start_time)], True)
		#
		# 		else:
		# 			base.logger.message(trace + ' setting mean monitoring failed', True)
		# else:
		# 	base.logger.message('keyword MEAN_TRACES not found in config file, no mean value for traces applied', True)
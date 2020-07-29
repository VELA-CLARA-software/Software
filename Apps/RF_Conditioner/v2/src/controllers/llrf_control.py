# llrf_handler.py
#import src.data.rf_condition_data_base as dat
#from VELA_CLARA_LLRF_Control import LLRF_SCAN
from VELA_CLARA_LLRF_Control import TRIG
from src.data import config
from src.data import rf_conditioning_logger
from src.data.rf_conditioning_data import rf_conditioning_data
import hardware_control_hub
from time import sleep
import inspect
from timeit import default_timer as timer

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


		self.should_show_llrf_interlock_active = True
		self.should_show_llrf_trig_external = True
		self.should_show_llrf_rf_output = True
		self.should_show_llrf_amp_ff_locked = True
		self.should_show_llrf_pha_ff_locked = True
		self.should_show_reset_daq_freg = True


	def enable_llrf(self):
		# go through each possible LLRF paramter (except HOLD_RF_ON_COM mod / protection parmaters
		# and try and reset them
		# cancer cancer cancer
		#
		if self.llrf_control.isInterlockActive():  #this means is the interlock BAD
			if self.should_show_llrf_interlock_active:
				self.logger.message('enable_llrf, isInterlockActive = True, attempting setInterlockNonActive()')
				self.should_show_llrf_interlock_active = False
			# try and reset
			self.llrf_control.setInterlockNonActive()
			# meh
			sleep(0.02)
		else:
			if self.should_show_llrf_interlock_active == False:
				self.logger.message('enable_llrf, isInterlockActive = False')
				self.should_show_llrf_interlock_active = True
		#
		#print("llrf_handler_base.llrf_control.isTrigExternal() = ", llrf_handler_base.llrf_control.isTrigExternal())
		if self.llrf_control.isTrigExternal():
			if self.should_show_llrf_trig_external == False:
				self.logger.message('enable_llrf, isTrigExternal = True')
				self.should_show_llrf_trig_external = True
		else:
			if self.should_show_llrf_trig_external:
				self.logger.message('enable_llrf, isTrigExternal = False, attempting trigExt()')
				self.should_show_llrf_trig_external = False
			# try and reset
			self.llrf_control.trigExt()
			# meh
			sleep(0.02)
		#
		#
		if self.llrf_control.isRFOutput():
			if self.should_show_llrf_rf_output == False:
				self.logger.message('enable_llrf, isRFOutput = True')
				self.should_show_llrf_rf_output = True
		else:
			if self.should_show_llrf_rf_output:
				self.logger.message('enable_llrf, isRFOutput = False, attempting enableRFOutput()')
				self.should_show_llrf_rf_output = False
			# reset
			self.llrf_control.enableRFOutput()
			# meh
			sleep(0.02)
		#
		#
		if self.llrf_control.isAmpFFLocked():
			if self.should_show_llrf_amp_ff_locked == False:
				self.logger.message('enable_llrf, isAmpFFLocked = True')
				self.should_show_llrf_rf_output = True
				# TODO this is the opposite logic to how  things  used to be ...
				self.llrf_control.unlockAmpFF()
		else:
			if self.should_show_llrf_amp_ff_locked:
				self.logger.message('enable_llrf, isAmpFFLocked = False, attempting lockAmpFF()')
				self.should_show_llrf_rf_output = False
			self.llrf_control.lockAmpFF()
			sleep(0.02)
		#
		#should_show_llrf_pha_ff_locked
		if self.llrf_control.isPhaseFFLocked():
			if self.should_show_llrf_pha_ff_locked == False:
				self.logger.message('enable_llrf, isPhaseFFLocked = True')
				self.should_show_llrf_pha_ff_locked = True
		else:
			if self.should_show_llrf_pha_ff_locked:
				self.logger.message('enable_llrf, isPhaseFFLocked = False, attempting lockPhaseFF()')
				self.should_show_llrf_pha_ff_locked = False
			self.llrf_control.lockPhaseFF()
			sleep(0.02)

		# this is sketchy AF

	def disableRFOutput(self):
		self.llrf_control.disableRFOutput() # the c++ check is RF output is enabled, if not it disables rf output

	def set_trace_SCAN(self):
		self.llrf_control.setAllSCANToPassive()
		self.llrf_control.setPowerRemoteTraceSCAN10sec('KLYSTRON_FORWARD_POWER')
		self.llrf_control.setPowerRemoteTraceSCAN10sec('CAVITY_PROBE_POWER')
		self.llrf_control.resetTORSCANToIOIntr()
		self.llrf_control.setTORACQMEvent()

	def enable_trigger(self):
		if self.llrf_control.getTrigSource() == TRIG.OFF:
			self.llrf_control.trigExt()

	def set_amp(self, val1, update_last_amp_sp = False):

		start_amp_sp = self.values[rf_conditioning_data.amp_sp]
		self.logger.message('set_amp (' + str(val1) + ') called from ' + str(inspect.stack()[1][3]))

		success = False
		#if val != self.llrf_control.getAmpFF(): # TODO this has chnged from amp_SP due to
		current_value = self.llrf_control.getAmpSP()
		if val1 != current_value: # TODO this has chnged from amp_SP due to
			self.logger.message('requested value {} is different to current value {}'.format(val1, current_value))
			self.llrf_control.setAmpSP(val1)
			#self.llrf_control.setAmpFF(val) # TODO THIS SHOULD BE SP!!!!!!!!!!!!!!!!
			self.mask_set = False
			start = timer()
			end = start
			success = True
			#while self.llrf_control.getAmpFF() != val: #  this has chnged from amp_SP due to controls group not setting  LLRF
			while self.llrf_control.getAmpSP() != val1:
				#print("stuck in the whie loop, ", start, end, end-start)
				end = timer()
				if end - start > 3.0:#MAGIC_NUMBER
					success = False
					break
			if success:
				self.logger.message('set_amp(' + str(val1) + '), took ' + str(end - start) + ' time,  averages NOT reset, mask_set = False')
				# update values dict to reflect new value

				if update_last_amp_sp:
					self.values[rf_conditioning_data.last_amp_sp] = start_amp_sp
					print('last_amp_sp = ', self.values[rf_conditioning_data.last_amp_sp])
					self.values[rf_conditioning_data.kfpower_at_last_amp_sp] = self.data.amp_vs_kfpow_running_stat[self.values[
						rf_conditioning_data.last_amp_sp]][1]

				self.values[rf_conditioning_data.amp_sp] = self.llrf_control.getAmpSP()
			else:
				self.logger.message('set_amp(' + str(val1) + '), FAILED to set amp in less than 3 seconds '
				                                                         'averages NOT reset, mask_set = False')
		else:
			self.logger.message('requested value is THE SAME  to current value')

		# TODO this function is so the app has a copy of the last value it had set ...
		# TODO i think in v2 we won't bother with this, and just use the ramp curve and fitting
		#  to move down
		#self.set_last_sp_above_100()
		#     def set_last_sp_above_100(self):
		#         llrf_handler_base.data.values[dat.amp_sp] = llrf_handler_base.llrfObj[0].amp_sp
		#         if llrf_handler_base.llrfObj[0].amp_sp > 100: #MAGIC_NUMBER
		#             llrf_handler_base.data.values[dat.last_sp_above_100] =
		#             llrf_handler_base.llrfObj[0].amp_sp
		#             llrf_handler_base.logger.message('last_sp_above_100 = ' + str(
		#             llrf_handler_base.data.values[dat.last_sp_above_100]), True)

		return success


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
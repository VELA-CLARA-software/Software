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
import time
from src.data.state import state

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
		# owns a config and logging class
		self.config = config.config()
		self.config_data = self.config.raw_config_data
		self.logger = rf_conditioning_logger.rf_conditioning_logger()
		self.llrf_type = self.config_data[self.config.RF_STRUCTURE]
		# the data class
		self.data = rf_conditioning_data()
		self.values = rf_conditioning_data.values
		self.expert_values = rf_conditioning_data.expert_values
		# get the llrf_control from hardware_control_hub
		self.hardware = hardware_control_hub.hardware_control_hub()
		self.llrf_control = self.hardware.llrf_control # TODO awfuil awfukl name
		self.llrf_obj = self.hardware.llrf_obj

		# init some display switches
		self.should_show_llrf_interlock_active = True
		self.should_show_llrf_trig_external = True
		self.should_show_llrf_rf_output = True
		self.should_show_llrf_amp_ff_locked = True
		self.should_show_llrf_pha_ff_locked = True
		self.should_show_reset_daq_freg = True

		# TODO AJG  check DAQ_rep_rate_state and reset if state == state.BAD
		# TODO DJS why is this in the init for llrf_control ? it will get called from main_loop
		#   if self.values[self.data.llrf_DAQ_rep_rate_status] == state.BAD:
		# 	    self.reset_daq_freg()

		# On startup disable mask checking and rolling averages
		self.set_global_check_mask(False)
		self.stop_trace_average()

		# pass some config setting to c++ LLRF_control
		self.llrf_control.setTracesToSaveOnOutsideMaskEvent( self.config_data['TRACES_TO_SAVE'])
		self.llrf_control.setTracesToSaveWhenDumpingCutOneTraceData( self.config_data['VAC_SPIKE_TRACES_TO_SAVE'])
		self.llrf_control.setAllTraceBufferSize(self.config_data['NUM_BUFFER_TRACES'])
		self.llrf_control.setNumExtraTracesOnOutsideMaskEvent(self.config_data['EXTRA_TRACES_ON_BREAKDOWN'])

		self.set_trace_SCANs()

		# TODO AJG: input the "KLY_PWR_FOR_ACTIVE_PULSE" value from config.yaml into the C++ function "setActivePulsePowerLimit"
		self.hardware.llrf_control.setActivePulsePowerLimit(self.config.raw_config_data['KLY_PWR_FOR_ACTIVE_PULSE'])
		# TODO check the value  to update has been read by now (it probably has...)
		self.hardware.llrf_control.setActivePulseCount(self.values[rf_conditioning_data.log_pulse_count])
		#



		self.set_trace_mean_positions()
		# set up terace for omed and rollgin averages
		self.setup_traces_for_omed_and_rolling_averages()


	def enable_llrf(self):
		# go through each possible LLRF paramter (except HOLD_RF_ON_COM mod / protection parameters
		# and try and reset them cancer cancer cancer
		#
		# the first thing this needs to do is set 0 amp_sp,
		self.llrf_control.setAmpHP(0.0) # HP 'high priority' it disables the trigger, then sets 0.0 amp_sp


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


		if self.data.values[self.data.llrf_DAQ_rep_rate_status] == state.BAD:
			self.reset_daq_freg()
		if self.data.values[self.data.llrf_DAQ_rep_rate_status] == state.NEW_BAD:
			self.reset_daq_freg()

		# this is sketchy AF

	def reset_daq_freg(self):
		start_time = time.time()
		if self.should_show_reset_daq_freg:
			self.logger.message('reset_daq_freg, llrf_DAQ_rep_rate_status == BAD')
			self.should_show_reset_daq_freg = False
		# for a
		if self.llrf_control.getAmpSP() != 0:
			self.logger.message('reset_daq_freg forcing set_amp(0)')
			self.llrf_control.setAmpSP(0.0)
			start_time = time.time()

		while time.time() - start_time < 0.02:
			pass
		self.logger.message('reset_daq_freg, time passed > 0.02s')
		self.llrf_control.setTORSCANToIOIntr()
		time.sleep(0.02) # TODO meh ...
		self.llrf_control.setTORACQMEvent()
		#self.set_iointr_counter = 0

	def disableRFOutput(self):
		self.llrf_control.disableRFOutput() # the c++ check is RF output is enabled, if not it disables rf output

	def set_trace_SCANs(self):
		self.logger.message(__name__ + ' setting all SCAN to passive')
		self.llrf_control.setAllSCANToPassive()
		self.logger.message(__name__ + ' setting KLYSTRON_FORWARD_POWER SCAN to 10 seconds')
		self.llrf_control.setPowerRemoteTraceSCAN10sec('KLYSTRON_FORWARD_POWER')
		self.logger.message(__name__ + ' setting CAVITY_PROBE_POWER SCAN to 10 seconds')
		self.llrf_control.setPowerRemoteTraceSCAN10sec('CAVITY_PROBE_POWER')
		self.logger.message(__name__ + ' setting One Record SCAN to IO/intr')
		self.llrf_control.resetTORSCANToIOIntr()
		self.logger.message(__name__ + ' setting One Record ACQM to event')
		self.llrf_control.setTORACQMEvent()

	def start_trace_average_no_reset(self,value):
		for trace in self.config_data['BREAKDOWN_TRACES']:
			self.llrf_control.setKeepRollingAverageNoReset(trace,value)

	def start_trace_average(self):
		for trace in self.config_data['BREAKDOWN_TRACES']:
			self.llrf_control.setShouldKeepRollingAverage(trace)

	def stop_trace_average(self):
		for trace in self.config_data['BREAKDOWN_TRACES']:
			self.llrf_control.setShouldNotKeepRollingAverage(trace)

	def enable_trigger(self):
		if self.llrf_control.getTrigSource() == TRIG.OFF:
			self.llrf_control.trigExt()

	def set_amp(self, val1, update_last_amp_sp = False):
		start_amp_sp = self.values[rf_conditioning_data.amp_sp]
		self.logger.message('set_amp (' + str(val1) + ') called from ' + str(inspect.stack()[1][3]), show_time_stamp = False)
		success = False
		#if val != self.llrf_control.getAmpFF(): # TODO this has chnged from amp_SP due to
		current_value = self.llrf_control.getAmpSP()
		if val1 != current_value:
			# don't need thsi message?
			#self.logger.message('set_amp requested value {} is different to current value {}'.format(val1, current_value), show_time_stamp = False)
			self.llrf_control.setAmpSP(val1)
			# timer so we know how long this function  takes, and to crash out if setting fails for some reason
			start = timer()
			end = start
			success = True
			while self.llrf_control.getAmpSP() != val1:
				#print("stuck in the whie loop, ", start, end, end-start)
				end = timer()
				if end - start > 3.0:#MAGIC_NUMBER
					success = False
					break
			if success:
				# self.logger.message('set_amp(' + str(val1) + '), took ' + str(end - start) + ' time,  averages NOT reset, mask_set = False',
				#                     show_time_stamp = False)
				if update_last_amp_sp:
					#self.values[rf_conditioning_data.last_amp_sp] = start_amp_sp
					self.values[rf_conditioning_data.last_amp_sp] = start_amp_sp
					self.values[rf_conditioning_data.latest_amp_sp_from_ramp] = val1
					self.logger.message('set_amp is updating last_amp_sp set to  {}'.format(start_amp_sp))
					self.values[rf_conditioning_data.kfpower_at_last_amp_sp] = self.data.amp_vs_kfpow_running_stat[self.values[
						rf_conditioning_data.last_amp_sp]][1]

					# self.logger.message('set_amp  updating, last_amp_sp = {}, last_amp_sp =  '.format(start_amp_sp, self.values[rf_conditioning_data.last_amp_sp] ))

				self.values[rf_conditioning_data.amp_sp] = self.llrf_control.getAmpSP()
			else:
				self.logger.message('set_amp(' + str(val1) + '), FAILED to set amp in less than 3 seconds '
				                                             'averages NOT reset, mask_set = False')
		else:
			self.logger.message('requested value is THE SAME as current value', show_time_stamp = False)

		return success

	def set_trace_mean_positions(self):
		"""
		sets the mean start and end positions from the config file
		:return:
		"""
		print("set_trace_mean_positions (add log entry here)")
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

	# enable / disable checking masks
	def set_global_check_mask(self,val):
		if self.llrf_obj[0].check_mask != val:
			self.llrf_control.setGlobalCheckMask(val)
			self.logger.message('set_global_check_mask setGlobalCheckMask ' + str(val))

	# setting the masks,
	# set the mask parameters (general function based on config settings
	#
	# then  need to start the a rolling average,
	#
	# enable / disable checking masks
	#
	# function to switch between log_ramp mask and normal_ramp mask
	#

	def setup_traces_for_omed_and_rolling_averages(self):
		print("setup_traces_for_omed_and_rolling_averages")
		# a dictionary to convert long to short trace names, smh
		full_race_name_toShort_trace_name_dict = {
		'KLYSTRON_REVERSE_PHASE' : 'KRPHA',
		'KLYSTRON_FORWARD_PHASE' : 'KFPHA',
		'KLYSTRON_REVERSE_POWER' : 'KRPOW',
		'KLYSTRON_FORWARD_POWER' : 'KFPOW',
		'CAVITY_REVERSE_PHASE' : 'CRPHA',
		'CAVITY_FORWARD_PHASE' : 'CFPHA',
		'CAVITY_REVERSE_POWER' : 'CRPOW',
		'CAVITY_FORWARD_POWER' : 'CFPOW',
		'CAVITY_PROBE_PHASE' : 'CPPHA',
		'CAVITY_PROBE_POWER' : 'CPPOW'}
		print('BREAKDOWN_TRACES = ',self.config_data['BREAKDOWN_TRACES'])
		for trace in self.config_data['BREAKDOWN_TRACES']:
			print("trace = ", trace)
			print("short trace = ",  full_race_name_toShort_trace_name_dict[trace])
			self.setup_trace_for_omed( full_race_name_toShort_trace_name_dict[trace] )
		for trace in self.config_data['BREAKDOWN_TRACES']:
			self.set_trace_rolling_average( full_race_name_toShort_trace_name_dict[trace] )

	def clear_all_rolling_averages(self):
		print("clear_all_rolling_averages")
		self.llrf_control.clearAllRollingAverage()

	def set_infinite_hi_mask(self):
		for trace in self.config_data['BREAKDOWN_TRACES']:
			print("set_inifinit_hi_mask trace = ", trace)
			self.llrf_control.setInfiniteHiMask(trace)

	def set_infinite_masks(self):
		for trace in self.config_data['BREAKDOWN_TRACES']:
			print("set_inifinit_hi_mask trace = ", trace)
			self.llrf_control.setInfiniteMasks(trace)



	def set_nominal_masks(self):
		'''
			call this after a log ramp to reset the nominal masks WITH NO RESTTING OF THE ROLLING AVERAGE
		'''
		print("set_nominal_masks")
		# a dictionary to convert long to short trace names, smh
		full_race_name_toShort_trace_name_dict = {
			'KLYSTRON_REVERSE_PHASE' : 'KRPHA',
			'KLYSTRON_FORWARD_PHASE' : 'KFPHA',
			'KLYSTRON_REVERSE_POWER' : 'KRPOW',
			'KLYSTRON_FORWARD_POWER' : 'KFPOW',
			'CAVITY_REVERSE_PHASE' : 'CRPHA',
			'CAVITY_FORWARD_PHASE' : 'CFPHA',
			'CAVITY_REVERSE_POWER' : 'CRPOW',
			'CAVITY_FORWARD_POWER' : 'CFPOW',
			'CAVITY_PROBE_PHASE' : 'CPPHA',
			'CAVITY_PROBE_POWER' : 'CPPOW'}
		print('BREAKDOWN_TRACES = ',self.config_data['BREAKDOWN_TRACES'])
		for trace in self.config_data['BREAKDOWN_TRACES']:
			print("trace = ", trace)
			print("short trace = ",  full_race_name_toShort_trace_name_dict[trace])
			self.setup_trace_for_omed( full_race_name_toShort_trace_name_dict[trace] )

	def setup_trace_for_omed(self, trace):
		'''
		setup the trace for outside mask event deteciton (all required parameters)
		:param trace_type: a string for the trace type that is prepends to each of the outside mask settign keyweords (defined in the config)
		fast_ramp_mode !! is a setting the c++ that sets hi mask to max of KFPower
		'''
		# these are all the possible config parameters, THEY MUST EXIST IN THE CONFIG OR THIS BREAK!!
		auto_set = self.config_data[trace + '_AUTO_SET']  # NOT USED ANYMORE REALLY,
		mask_set_type = self.config_data[trace + '_MASK_SET_TYPE']  # using indices or time on pusle to set mask positions
		mask_start = self.config_data[trace + '_MASK_START']  # START TIME / INDEX
		mask_end = self.config_data[trace + '_MASK_END']  # END TIME / INDEX
		mask_window_start = self.config_data[trace + '_MASK_WINDOW_START']  # WINDOW START TIME / INDEX
		mask_window_end = self.config_data[trace + '_MASK_WINDOW_END']  # WINDOW END TIME / INDEX
		mask_type = self.config_data[trace + '_MASK_TYPE']  # is mask based on 'percent' of rolling mean, or "absolute" watts(phase)
		mask_level = self.config_data[trace + '_MASK_LEVEL']  # AMOUNT OF MASK
		mask_floor = self.config_data[trace + '_MASK_FLOOR']
		mask_lo_min = self.config_data[trace + '_MASK_LO_MIN']  # mask_abs_min in c++
		if mask_type == 'ABSOLUTE':
			is_percent = False
		elif mask_type == 'PERCENT':
			is_percent = True
		else:
			is_percent = True
		# send mask settings to c++
		print("Setting these Mask parameters")
		print("trace, is_percent, mask_level, mask_floor, mask_lo_min, mask_start, mask_end, mask_window_start,mask_window_end")
		print(trace, is_percent, mask_level, mask_floor, mask_lo_min, mask_start, mask_end, mask_window_start,mask_window_end)
		# # check values have got set correctly
		# has_error = False
		if mask_set_type == 'TIME':
			self.llrf_control.setMaskParamatersTimes(trace, is_percent, mask_level, mask_floor, mask_lo_min, mask_start, mask_end, mask_window_start,
			                                         mask_window_end)
			# [s,e,ws,ws] = [self.llrf_control.getMaskStartTime(trace), self.llrf_control.getMaskEndTime(trace),self.llrf_control.getMaskWindowStartTime(trace), self.llrf_control.getMaskWindowEndTime(trace)]
			#
			# print("Manually compare these atm")
			# print([s,e,ws,ws])
			# print([mask_start, mask_end, mask_window_start, mask_window_end ])
		elif mask_set_type == 'INDEX':
			self.llrf_control.setMaskParamatersIndices(trace, is_percent, mask_level, mask_floor, mask_lo_min, mask_start, mask_end,
			                                           mask_window_start, mask_window_end)
			# [s,e,ws,ws] = [self.llrf_control.getMaskStartIndex(trace), self.llrf_control.getMaskEndIndex(trace),
			#                self.llrf_control.getMaskWindowStartIndex(trace), self.llrf_control.getMaskWindowEndIndex(trace)]
			# if [s,e,ws,ws] == [ mask_start, mask_end, mask_window_start, mask_window_end ] :
			# 	pass
			# else:
			# 	print("!!ERROR!! {} trace not checking mask".format(trace))
			# 	has_error = True
		# if self.llrf_control.isCheckingMask(trace):
		# 	pass
		# else:
		# 	print("!!ERROR!! {} trace not checking mask".format(trace))
		# 	has_error = True
		# if self.llrf_control.getMaskFloor(trace) == mask_floor:
		# 	pass
		# else:
		# 	print("!!ERROR!! {} trace mask_floor = {}, expected {}".format(trace,self.llrf_control.getMaskFloor(trace), mask_floor))
		# 	has_error = True
		#
		# if self.llrf_control.getMaskValue(trace) == mask_floor:
		# 	pass
		# else:
		# 	print("!!ERROR!! {} trace mask_level = {}, expected {}".format(trace,self.llrf_control.getMaskValue(trace), mask_level))
		# 	has_error = True
		#
		#
		# if has_error:
		# 	raw_input()





		#
		# set the check streak (how many points to trigger event)
		check_streak = self.config_data[trace + '_CHECK_STREAK']
		# TODO errrrrrrrrrrrrrrrr
		self.llrf_control.setNumContinuousOutsideMaskCount('CAVITY_REVERSE_PHASE', check_streak)
		#
		# set drop amp state and value)
		drop_amp = self.config_data[trace+'_DROP_AMP']
		drop_amp_value = self.config_data[trace+'_DROP_AMP_VALUE']
		self.llrf_control.setDropAmpOnOutsideMaskEvent(trace, drop_amp, drop_amp_value)

		# enable checking masks for this trace
		self.llrf_control.setCheckMask(trace, True)



	def set_trace_rolling_average(self, trace):
		self.logger.message('Attempting to start rolling average for ' + trace)
		num_average_traces = self.config_data[trace + '_NUM_AVERAGE_TRACES']
		self.llrf_control.setTraceRollingAverageSize(trace, num_average_traces)
		#self.llrf_control.setInfiniteMasks(trace)
		self.llrf_control.setShouldKeepRollingAverage(trace)
		if self.llrf_obj[0].trace_data[  self.llrf_control.fullLLRFTraceName(trace) ].keep_rolling_average:
			self.logger.message('STARTED rolling average for ' + trace)
			self.logger.message('RollingAverageSize = ' + str(self.llrf_control.getTraceRollingAverageSize(trace)))
			self.logger.message('RollingAverageCount = ' + str(self.llrf_control.getTraceRollingAverageCount(trace)))
		else:
			self.logger.message('!!ERROR!! STARTING rolling average FAILED for ' + trace)

	def set_trace_scans(self):
		self.logger.message(__name__ + ' setting all SCAN to passive')
		self.llrf_control.setAllSCANToPassive()
		self.llrf_control.setAllSCANToPassive()
		self.llrf_control.setAllTraceBufferSize(self.config_data['NUM_BUFFER_TRACES'])
		self.logger.message(__name__ + ' setting KLYSTRON_FORWARD_POWER SCAN to 10 seconds')
		self.llrf_control.setPowerRemoteTraceSCAN10sec('KLYSTRON_FORWARD_POWER')
		self.logger.message(__name__ + ' setting CAVITY_PROBE_POWER SCAN to 10 seconds')
		self.llrf_control.setPowerRemoteTraceSCAN10sec('CAVITY_PROBE_POWER')
		self.logger.message(__name__ + ' setting One Record SCAN to IO/intr')
		self.llrf_control.resetTORSCANToIOIntr()
		self.logger.message(__name__ + ' setting One Record ACQM to event')
		self.llrf_control.setTORACQMEvent()


# llrf_handler.py
import data.rf_condition_data_base as dat
from VELA_CLARA_LLRF_Control import LLRF_SCAN
from base.base import base


class llrf_handler_base(base):
	# whoami
	my_name = 'llrf_handler_base'
	# init attributes
	power_traces = []
	pulse_end_index = 0
	pulse_end = 0
	mask_set = False
	mask_count = 0

	def __init__(self):
		super(llrf_handler_base, self).__init__()
		#base.__init__(self)
		#self.num_buffer_traces = 40

		#self.timevector = base.llrfObj[0].time_vector.value
		self.timevector = base.llrfObj[0].time_vector
		#self.timevector_dt = self.timevector[1]-self.timevector[0]
		base.config.llrf_config = base.config.llrf_config
		self.start_trace_monitoring( base.config.llrf_config['TRACES_TO_SAVE'])#MAGIC_STRING
		# must come after start_trace_monitoring
		self.setup_trace_rolling_average()

		base.llrf_control.setTracesToSaveOnOutsideMaskEvent( base.config.llrf_config['TRACES_TO_SAVE'])#MAGIC_STRING

		# this is where the data for each mask, for each trace is held
		# yes its a dict of dict,
		self.all_mask_dict = {}
		self.set_infinite_mask_end_by_power()

	def set_infinite_mask_end_by_power(self):
		if base.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_POWER_TRACE_1'):#MAGIC_STRING
			if base.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_1'):#MAGIC_STRING
				if base.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_LEVEL_1'):#MAGIC_STRING
					pwr = base.config.breakdown_config['PHASE_MASK_BY_POWER_POWER_TRACE_1']#MAGIC_STRING
					pha = base.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_1']#MAGIC_STRING
					lev = base.config.breakdown_config['PHASE_MASK_BY_POWER_LEVEL_1']#MAGIC_STRING
					base.data.values[dat.phase_mask_by_power_trace_1_set] = self.apply_infinite_mask_end_by_power(pwr, pha, lev)
		if base.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_POWER_TRACE_2'):#MAGIC_STRING
			if base.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_PHASE_TRACE_2'):#MAGIC_STRING
				if base.config.breakdown_config.has_key('PHASE_MASK_BY_POWER_LEVEL_2'):#MAGIC_STRING
					pwr = base.config.breakdown_config['PHASE_MASK_BY_POWER_POWER_TRACE_2']#MAGIC_STRING
					pha = base.config.breakdown_config['PHASE_MASK_BY_POWER_PHASE_TRACE_2']#MAGIC_STRING
					lev = base.config.breakdown_config['PHASE_MASK_BY_POWER_LEVEL_2']#MAGIC_STRING
					base.data.values[dat.phase_mask_by_power_trace_2_set] = self.apply_infinite_mask_end_by_power(pwr, pha, lev)

	def apply_infinite_mask_end_by_power(self,power,phase,level, ):
		success = base.llrf_control.setInfiniteMaskEndByPower(power, phase, level)
		st = 'Set Infinite End Mask by Power 1, power trace = ' + power + ', phase trace = ' \
			 + phase + ', power level ' + str(level)
		if success:
			base.logger.message(st + ' SUCCESS', True)
		else:
			base.logger.message(st + ' FAIL', True)
		return success

	def set_trace_masks(self):
		for key,value in self.all_mask_dict.iteritems():
			if value['update_func'](value):
				pass
			else:
				base.logger.message(key + 'ERROR SETTING MASK', True)

	# more cancer but hopefully will be neatened up
	def setup_outside_mask_trace_param(self):
		# loop over each trace in 'BREAKDOWN_TRACES'
		# these means we EXPECT TO FIND DATA FOR EACH TRACE
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			# create a mask dictionary for each trace, held in all_mask_dict
			shortname = base.llrf_control.shortLLRFTraceName(trace)
			self.all_mask_dict[shortname] = {}
			self.all_mask_dict[shortname]['TRACE'] = trace
			self.set_mask_dict( self.all_mask_dict[shortname], shortname)


	def get_breakdown_config_value(self, shortname, end_phrase):
		''' Looks through each key and returns the value that has the same shortnam and end_phrase
			We expect this function to NEVER return None if things are set-up correctly
		'''
		for key in base.config.breakdown_config.keys():
			#print key
			if shortname in key:
				if end_phrase in key:
					return base.config.breakdown_config[key]
		print 'get_breakdown_config_param ERROR ' + shortname + ' ,' + end_phrase
		return None

	def set_mask_dict(self,dict, shortname):

		# create a dictionary from config data used to update the masks, for each trace

		#dict.update({'AUTO': base.config.breakdown_config['C'+l+'P_AUTO_SET']})#MAGIC_STRING
		dict.update({'AUTO': self.get_breakdown_config_value(shortname,'_AUTO_SET')})#MAGIC_STRING

		# are we defining a mask in term of time or index??
		#if 'TIME' in base.config.breakdown_config['C'+l+'P_MASK_SET_TYPE']:#MAGIC_STRING
		if 'TIME' in self.get_breakdown_config_value(shortname,'_MASK_SET_TYPE'):#MAGIC_STRING
			dict.update({'IS_TIME': True}) # MAGIC_STRING
		elif 'INDEX' in self.get_breakdown_config_value(shortname,'_MASK_SET_TYPE'):  ## MAGIC_STRING
			dict.update({'IS_TIME': False})  # MAGIC_STRING

		# is a mask defined in terms of percentage or absolute value??
		if 'PERCENT' in self.get_breakdown_config_value(shortname,'_MASK_TYPE'):#MAGIC_STRING
			dict.update({'IS_PERCENT': True})  # MAGIC_STRING
		elif 'ABSOLUTE' in self.get_breakdown_config_value(shortname,'_MASK_TYPE'):#MAGIC_STRING
			dict.update({'IS_PERCENT': False})  # MAGIC_STRING

		# which function to call to update masks (now always update_mask
		dict.update({'update_func': self.update_mask})#MAGIC_STRING

		# get the rest of the mask parameters # MAGIC_STRING !!!!!!!!!!
		dict.update({'MASK_START': self.get_breakdown_config_value(shortname,'_MASK_START')})
		dict.update({'MASK_END': self.get_breakdown_config_value(shortname,'_MASK_END')})
		dict.update({'MASK_WINDOW_START': self.get_breakdown_config_value(shortname,'_MASK_WINDOW_START')})
		dict.update({'MASK_WINDOW_END': self.get_breakdown_config_value(shortname,'_MASK_WINDOW_END')})
		dict.update({'LEVEL': self.get_breakdown_config_value(shortname,'_MASK_LEVEL')})
		dict.update({'FLOOR': self.get_breakdown_config_value(shortname,'_MASK_FLOOR')})
		dict.update({'MASK_ABS_MIN': self.get_breakdown_config_value(shortname,'_MASK_ABS_MIN')})

		streak = self.get_breakdown_config_value(shortname,'_CHECK_STREAK')#MAGIC_STRING
		drop = self.get_breakdown_config_value(shortname,'_DROP_AMP')#MAGIC_STRING
		drop_val = self.get_breakdown_config_value(shortname,'_AMP_DROP_VAL')

		string = [dict['TRACE'] + ', streak = ' + str(streak)  + ', drop = ' + str(drop) + ', ' \
		         'drop_val= ' + str(drop_val) + ', update func = ' + str(dict['update_func']) ]
		base.logger.message(string, True)

		if base.llrf_control.setNumContinuousOutsideMaskCount( dict['TRACE'], streak) == False:
			base.logger.message(dict['TRACE'] + ' ERROR setNumContinuousOutsideMaskCount = False', True)
		else:
			base.logger.message('setNumContinuousOutsideMaskCount = True', True)

		# if base.llrf_control.setMaskFloor(dict['TRACE'], floor) == False:
		# 	base.logger.message(dict['TRACE'] + ' ERROR setMaskFloor = False', True)
		# else:
		# 	base.logger.message('setMaskFloor = True', True)

		if base.llrf_control.setShouldCheckMask(dict['TRACE']) == False:
			base.logger.message(dict['TRACE'] + ', setShouldCheckMask = False', True)
		else:
			base.logger.message(dict['TRACE'] + ', setShouldCheckMask = True', True)

		if base.llrf_control.setDropAmpOnOutsideMaskEvent(dict['TRACE'], drop, drop_val) == False:
			base.logger.message(dict['TRACE'] + ', setDropAmpOnOutsideMaskEvent = False', True)
		else:
			base.logger.message(dict['TRACE'] + ', setDropAmpOnOutsideMaskEvent = True', True)

	# setMaskParamatersTimes(const std::string& name, bool isPercent,
	# double mask_value, double mask_floor, double mask_abs_min,
	# double start, double end,
	# double window_start, double window_end)
#	if gun.setMaskParamatersTimes(cfpha, False, 50.0, 0.0, 0.0, 0.7, 2.0, 1.2, 1.45):

	def update_mask(self,dict):
		if dict['IS_TIME']:
			if self.llrf_control.setMaskParamatersTimes(dict['TRACE'], dict['IS_PERCENT'],
			                                            dict['LEVEL'], dict['FLOOR'],
			                                            dict['MASK_ABS_MIN'], dict['MASK_START'],
			                                            dict['MASK_END'],
			                                            dict['MASK_WINDOW_START'],
			                                            dict['MASK_WINDOW_END']):
				base.logger.message(dict['TRACE'] + ', set time_percent_mask', True)
				return True
			else:
				base.logger.message(dict['TRACE'] + ', Failed to set set time_percent_mask', True)
				return False
		else:
			if self.llrf_control.setMaskParamatersIndices(dict['TRACE'], dict['IS_PERCENT'],
			                                              dict['LEVEL'], dict['FLOOR'],
			                                              dict['MASK_ABS_MIN'], dict['MASK_START'],
			                                              dict['MASK_END'],
			                                              dict['MASK_WINDOW_START'],
			                                              dict['MASK_WINDOW_END']):
				base.logger.message(dict['TRACE'] + ', set time_percent_mask', True)
				return True
			else:
				base.logger.message(dict['TRACE'] + ', Failed to set set time_percent_mask', True)
				return False

	def time_percent_mask(self,dict):
		if self.llrf_control.setPercentTimeMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE']):
			base.logger.message(dict['TRACE'] + ', set time_percent_mask', True)
			return True
		else:
			base.logger.message(dict['TRACE'] + ', Failed to set set time_percent_mask', True)
			return False

	def time_absolute_mask(self,dict):
		if self.llrf_control.setAbsoluteTimeMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE']):
			base.logger.message(dict['TRACE'] + ', set time_absolute_mask', True)
			return True
		else:
			base.logger.message(dict['TRACE'] + ', Failed to set set time_absolute_mask', True)
			return False
		#print 'time_absolute_mask'

	def index_percent_mask(self,dict):
		#print 'index_percent_mask'
		if self.llrf_control.setPercentMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE']):
			base.logger.message(dict['TRACE'] + ', set index_percent_mask', True)
			return True
		else:
			base.logger.message(dict['TRACE'] + ', Failed to set set index_percent_mask', True)
			return False

	def index_absolute_mask(self,dict):
		if self.llrf_control.setAbsoluteMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE']):
			base.logger.message(dict['TRACE'] + ', set index_absolute_mask', True)
			return True
		else:
			base.logger.message(dict['TRACE'] + ', Failed to set set index_absolute_mask', True)
			return False

	# return stre if all breakdown traces have averages, we could do this slightly more clever like
	def have_averages(self):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			if base.llrfObj[0].trace_data[trace].has_average == False:
				return False
		return True

	def start_trace_average_no_reset(self,value):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			base.llrf_control.setKeepRollingAverageNoReset(trace,value)

	def start_trace_average(self):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			base.llrf_control.setShouldKeepRollingAverage(trace)

	def stop_trace_average(self):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			base.llrf_control.setShouldNotKeepRollingAverage(trace)

	def start_trace_monitoring(self,trace_to_save):
		base.logger.header(self.my_name + ' setting all SCAN to passive', True)
		base.llrf_control.setAllSCANToPassive()
		base.logger.header(self.my_name + ' start_trace_monitoring', True)
		if "error" not in trace_to_save:
			base.llrf_control.setAllSCANToPassive()

			base.llrf_control.setAllTraceBufferSize(base.config.llrf_config['NUM_BUFFER_TRACES'])

			# for trace in trace_to_save:
			# 	if base.llrf_control.setTraceSCAN(trace, LLRF_SCAN.ZERO_POINT_ONE): # SHOULD BE INPUIT Parameter
			# 		base.logger.message(trace + ' SCAN set to LLRF_SCAN.ZERO_POINT_ONE', True) # SHOULD BE INPUIT Parameter
			# 	else:
			# 		base.logger.message(' ERROR trying to set LLRF_SCAN.ZERO_POINT_ONE SCAN for ' + trace, True)
            #
			# 	#a = base.llrf_control.startTraceMonitoring(trace)
			# 	base.llrf_control.setNumBufferTraces(trace,
			# 	if a:
			# 		base.logger.message('started monitoring ' + trace, True)
			# 		if 'POWER' in trace:  # MAGIC_STRING
			# 			self.power_traces.append(trace)
			# 			base.logger.message('added ' + self.power_traces[-1] + ' to power_traces. [should be' + trace + ']', True)
			# 	else:
			# 		base.logger.message(' ERROR trying to monitor ' + trace, True)
		else:
			base.logger.message('!!! ERROR IN TRACES TO SAVE !!!', True)

	def setup_trace_rolling_average(self):
		base.logger.header(self.my_name + ' setup_trace_rolling_average', True)
		# the cavity trace need a mean
		num_mean = 3  # MAGIC_NUM
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			sn = base.llrf_control.shortLLRFTraceName(trace)
			base.logger.message('starting rolling average for ' + trace + ' (' + sn + ')', True)

			# this needs updating cos its cnacer
			num_mean = self.get_breakdown_config_value(base.llrf_control.shortLLRFTraceName(
					trace),  "NUM_AVERAGE_TRACES")

			base.llrf_control.setTraceRollingAverageSize(trace, num_mean)
			base.llrf_control.setInfiniteMasks(trace)
			base.llrf_control.setShouldKeepRollingAverage(trace)
			if base.llrfObj[0].trace_data[trace].keep_rolling_average:
				base.logger.message('STARTED rolling average for ' + trace, True)
			else:
				base.logger.message('STARTED rolling average FAILED for ' + trace, True)

	def get_pulse_end(self):
		# must be called after setting a pulse length
		self.pulse_end_index = base.llrfObj[0].pulse_latency + self.llrf_control.getIndex(base.llrf_control.getPulseLength())
		self.pulse_end = self.llrf_control.getTime( self.pulse_end_index)#len([x for x in self.timevector if x <= self.pulse_end])

	# this can be tidied up a lot
	def set_mean_pwr_position(self):
		self.get_pulse_end()
		# MUST BE CALLED AFTER CHANGING PULSE WIDTH ' CANCER
		base.logger.header(self.my_name + ' set_mean_pwr_position',True)
		base.logger.message([
			'rf pulse end time = ' + str(self.pulse_end) + ', index = ' + str(self.pulse_end_index),
			'pulse_latency     = '  + str(base.llrfObj[0].pulse_latency),
			'.getPulseLength() = ' + str(base.llrf_control.getPulseLength())],True)
		s = None
		e = None
		if base.config.llrf_config.has_key('MEAN_TRACES'):
			i = 0
			for trace in base.config.llrf_config['MEAN_TRACES']:
				base.logger.message(trace + ' found in config file', True)
				i += 1
				r = self.has_mean_start_end_key_i(i)
				if r != False:
					if base.llrf_control.setMeanStartEndTime(r[0], r[1], trace):
						base.logger.message(trace + ' mean monitoring started', True)
						base.logger.message(['trace_mean_start/end (us) = ' + str(r[0]) + '/' + str(r[1]),
											 'meantime = ' + str(r[1] - r[0])], True)
				else:
					base.logger.message(trace + ' setting mean monitoring failed', True)
		else:
			base.logger.message('keyword MEAN_TRACES not found in config file, no mean value for traces applied', True)

	def has_mean_start_end_key_i(self,i):
		if base.config.llrf_config.has_key(str(i) + '_MEAN_START'):#MAGIC_STRING
			s = base.config.llrf_config[str(i) + '_MEAN_START']#MAGIC_STRING
			if base.config.llrf_config.has_key(str(i) + '_MEAN_END'):#MAGIC_STRING
				e = base.config.llrf_config[str(i) + '_MEAN_END']#MAGIC_STRING
				print s
				print e
				return [s,e]
		return False

	def set_global_check_mask(self,val):
		if base.llrfObj[0].check_mask != val:
			base.llrf_control.setGlobalCheckMask(val)
			base.logger.message('set_global_check_mask setGlobalCheckMask '+str(val),True)
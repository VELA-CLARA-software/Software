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

		self.timevector = base.llrfObj[0].time_vector.value
		#self.timevector_dt = self.timevector[1]-self.timevector[0]
		base.config.llrf_config = base.config.llrf_config
		self.start_trace_monitoring( base.config.llrf_config['TRACES_TO_SAVE'])#MAGIC_STRING
		# must come after start_trace_monitoring
		self.setup_trace_rolling_average()

		base.llrf_control.setTracesToSaveOnBreakDown( base.config.llrf_config['TRACES_TO_SAVE'])#MAGIC_STRING

		self.reverse_mask_dict = {}
		self.forward_mask_dict = {}
		self.probe_mask_dict = {}

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
		if 'update_func' in self.forward_mask_dict:
			if self.forward_mask_dict['update_func'](self.forward_mask_dict):
				pass
			else:
				base.logger.message(self.forward_mask_dict['TRACE'] + 'ERROR SETTING MASK', True)

		if 'update_func' in self.probe_mask_dict:
			if self.probe_mask_dict['update_func'](self.probe_mask_dict):
				pass
			else:
				base.logger.message(self.probe_mask_dict['TRACE'] + 'ERROR SETTING MASK', True)
		# temp
		if 'update_func' in self.reverse_mask_dict:
			if self.reverse_mask_dict['update_func'](self.reverse_mask_dict):
				pass
			else:
				base.logger.message(self.reverse_mask_dict['TRACE'] + 'ERROR SETTING MASK', True)

	# more cancer but hopefully will be neatened up
	def setup_outside_mask_trace_param(self):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			if self.is_reverse(trace):
				self.reverse_mask_dict.update({'TRACE':trace})
				self.set_mask_dict(self.reverse_mask_dict,'R') # MEH !!!!!!! CANCER
			elif self.is_probe(trace):
				self.probe_mask_dict.update({'TRACE':trace})
				self.set_mask_dict(self.probe_mask_dict,'P') # MEH !!!!!!! CANCER
			elif self.is_forward(trace):
				self.forward_mask_dict.update({'TRACE':trace})
				self.set_mask_dict(self.forward_mask_dict,'F') # MEH !!!!!!! CANCER


	def set_mask_dict(self,dict,l):
		dict.update({'AUTO': base.config.breakdown_config['C'+l+'P_AUTO_SET']})#MAGIC_STRING
		if 'TIME' in base.config.breakdown_config['C'+l+'P_MASK_SET_TYPE']:#MAGIC_STRING
			if 'PERCENT' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:#MAGIC_STRING
				dict.update({'update_func': self.time_percent_mask })#MAGIC_STRING
			elif 'ABSOLUTE' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:#MAGIC_STRING
				dict.update({'update_func': self.time_absolute_mask })#MAGIC_STRING
		elif 'INDEX' in base.config.breakdown_config['C'+l+'P_MASK_SET_TYPE']:#MAGIC_STRING
			if 'PERCENT' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:#MAGIC_STRING
				dict.update({'update_func': self.index_percent_mask})#MAGIC_STRING
			elif 'ABSOLUTE' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:#MAGIC_STRING
				dict.update({'update_func': self.index_absolute_mask})#MAGIC_STRING
		dict.update({'S1': base.config.breakdown_config['C'+l+'P_S1']})#MAGIC_STRING
		dict.update({'S2': base.config.breakdown_config['C'+l+'P_S2']})#MAGIC_STRING
		dict.update({'S3': base.config.breakdown_config['C'+l+'P_S3']})#MAGIC_STRING
		dict.update({'S4': base.config.breakdown_config['C'+l+'P_S4']})#MAGIC_STRING
		dict.update({'LEVEL': base.config.breakdown_config['C'+l+'P_MASK_LEVEL']})#MAGIC_STRING

		streak = base.config.breakdown_config['C'+l+'P_CHECK_STREAK']#MAGIC_STRING
		floor = base.config.breakdown_config['C'+l+'P_MASK_FLOOR']#MAGIC_STRING
		drop = base.config.breakdown_config['C'+l+'P_AMP_DROP']#MAGIC_STRING
		drop_val = base.config.breakdown_config['C'+l+'P_AMP_DROP_VAL']#MAGIC_STRING

		string = [dict['TRACE'] + ', streak = ' + str(streak) + ', floor = ' + str(floor) \
				  + ', drop = ' + str(drop) + ', drop_val= ' + str(drop_val) + ', update func = ' + str(dict['update_func']) ]
		base.logger.message(string, True)

		if base.llrf_control.setNumContinuousOutsideMaskCount( dict['TRACE'], streak) == False:
			base.logger.message(dict['TRACE'] + ' ERROR setNumContinuousOutsideMaskCount = False', True)
		else:
			base.logger.message('setNumContinuousOutsideMaskCount = True', True)

		if base.llrf_control.setMaskFloor(dict['TRACE'], floor) == False:
			base.logger.message(dict['TRACE'] + ' ERROR setMaskFloor = False', True)
		else:
			base.logger.message('setMaskFloor = True', True)

		if base.llrf_control.setShouldCheckMask(dict['TRACE']) == False:
			base.logger.message(dict['TRACE'] + ', setShouldCheckMask = False', True)
		else:
			base.logger.message(dict['TRACE'] + ', setShouldCheckMask = True', True)

		if base.llrf_control.setDropAmpOnOutsideMaskDetection(dict['TRACE'], drop, drop_val) == False:
			base.logger.message(dict['TRACE'] + ', setDropAmpOnOutsideMaskDetection = False', True)
		else:
			base.logger.message(dict['TRACE'] + ', setDropAmpOnOutsideMaskDetection = True', True)

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
			for trace in trace_to_save:
				if base.llrf_control.setTraceSCAN(trace, LLRF_SCAN.ZERO_POINT_ONE): # SHOULD BE INPUIT Parameter
					base.logger.message(trace + ' SCAN set to LLRF_SCAN.ZERO_POINT_ONE', True) # SHOULD BE INPUIT Parameter
				else:
					base.logger.message(' ERROR trying to set LLRF_SCAN.ZERO_POINT_ONE SCAN for ' + trace, True)

				a = base.llrf_control.startTraceMonitoring(trace)
				base.llrf_control.setNumBufferTraces(trace, base.config.llrf_config['NUM_BUFFER_TRACES'])
				if a:
					base.logger.message('started monitoring ' + trace, True)
					if 'POWER' in trace:  # MAGIC_STRING
						self.power_traces.append(trace)
						base.logger.message('added ' + self.power_traces[-1] + ' to power_traces. [should be' + trace + ']', True)
				else:
					base.logger.message(' ERROR trying to monitor ' + trace, True)
		else:
			base.logger.message('!!! ERROR IN TRACES TO SAVE !!!', True)

	def setup_trace_rolling_average(self):
		base.logger.header(self.my_name + ' setup_trace_rolling_average', True)
		# the cavity trace need a mean
		num_mean = 3  # MAGIC_NUM
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			base.logger.message('starting rolling average for ' + trace, True)

			if self.is_reverse(trace):
				num_mean = base.config.breakdown_config['CRP_NUM_AVERAGE_TRACES']
			elif self.is_forward(trace):
				num_mean = base.config.breakdown_config['CFP_NUM_AVERAGE_TRACES']
			elif self.is_probe(trace):
				num_mean = base.config.breakdown_config['CPP_NUM_AVERAGE_TRACES']

			base.llrf_control.clearRollingAverage(trace)
			base.llrf_control.setNumRollingAverageTraces(trace, num_mean)
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
				return [s,e]
		return False

	def set_global_check_mask(self,val):
		if base.llrfObj[0].check_mask != val:
			base.llrf_control.setGlobalCheckMask(val)
			base.logger.message('set_global_check_mask setGlobalCheckMask '+str(val),True)
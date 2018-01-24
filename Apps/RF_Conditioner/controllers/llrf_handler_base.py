# llrf_handler.py

from VELA_CLARA_enums import MACHINE_AREA
import VELA_CLARA_LLRF_Control
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from base.base import base


class llrf_handler_base(base):
	# whoami
	my_name = 'llrf_handler_base'
	# init attributes
	power_traces = []
	pulse_end_index = 0
	pulse_end = 0

	mask_set = False

	def __init__(self):
		super(base, self).__init__()
		#base.llrf_control = llrf_handler_base.llrf_control
		base.llrf_control = base.llrf_control
		#base.llrfObj = llrf_handler_base.llrfObj
		base.llrf_control_type = base.llrfObj[0].type
		self.timevector = base.llrfObj[0].time_vector.value
		self.timevector_dt = self.timevector[1]-self.timevector[0]
		#base.config.breakdown_config = base.config.breakdown_config
		base.config.llrf_config = base.config.llrf_config
		self.start_trace_monitoring( base.config.llrf_config['TRACES_TO_SAVE'])
		# you have to tell the HWC what to save on
		base.llrf_control.setTracesToSaveOnBreakDown( base.config.llrf_config['TRACES_TO_SAVE'])

		#self.set_mean_pwr_position()
		self.start_trace_rolling_average()
		#self.set_outside_mask_trace_param()

		#self.setup_outside_mask_trace_param()
		#self.set_mask()
		self.reverse_mask_dict = {}
		self.forward_mask_dict = {}
		self.probe_mask_dict = {}
		self.mask_count = 0

	def set_trace_masks(self):

		if 'update_func' in self.forward_mask_dict:
			a = self.forward_mask_dict['update_func'](self.forward_mask_dict)
			if a == False:
				print('ERROR SETTING FORWARD MASK')

		if 'update_func' in self.probe_mask_dict:
			a = self.probe_mask_dict['update_func'](self.probe_mask_dict)
			if a == False:
				print('ERROR SETTING PROBE MASK')
		# temp
		if 'update_func' in self.reverse_mask_dict:
			a = self.reverse_mask_dict['update_func'](self.reverse_mask_dict)
			if a == False:
				print('ERROR SETTING REVERSE MASK')
		# else:
		# 	self.logger.write_list(self.llrf_control.getHiMask(self.reverse_mask_dict['TRACE']),'C:\\Users\\dlerlp\\Documents\\RF_condition_2018\\hi_' +str(self.mask_count)+'.txt')
		# 	self.logger.write_list(self.llrf_control.getLoMask(self.reverse_mask_dict['TRACE']),'C:\\Users\\dlerlp\\Documents\\RF_condition_2018\\lo_' +str(self.mask_count)+ '.txt')
		# 	self.mask_count +=1

	# more cancer but hopefully will be neatened up
	def setup_outside_mask_trace_param(self):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			if 'REVERSE' in trace:
				self.reverse_mask_dict.update({'TRACE':trace})
				self.set_mask_dict(self.reverse_mask_dict,'R') # MEH !!!!!!! CANCER
			elif 'PROBE' in trace:
				self.probe_mask_dict.update({'TRACE':trace})
				self.set_mask_dict(self.probe_mask_dict,'P') # MEH !!!!!!! CANCER
			elif 'FORWARD' in trace:
				self.forward_mask_dict.update({'TRACE':trace})
				self.set_mask_dict(self.forward_mask_dict,'F') # MEH !!!!!!! CANCER


	def set_mask_dict(self,dict,l):
		dict.update({'AUTO': base.config.breakdown_config['C'+l+'P_AUTO_SET']})
		if 'TIME' in base.config.breakdown_config['C'+l+'P_MASK_SET_TYPE']:
			if 'PERCENT' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:
				dict.update({'update_func': self.time_percent_mask })
			elif 'ABSOLUTE' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:
				dict.update({'update_func': self.time_absolute_mask })
		elif 'INDEX' in base.config.breakdown_config['C'+l+'P_MASK_SET_TYPE']:
			if 'PERCENT' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:
				dict.update({'update_func': self.index_percent_mask})
			elif 'ABSOLUTE' in base.config.breakdown_config['C'+l+'P_MASK_TYPE']:
				dict.update({'update_func': self.index_absolute_mask})
		dict.update({'S1': base.config.breakdown_config['C'+l+'P_S1']})
		dict.update({'S2': base.config.breakdown_config['C'+l+'P_S2']})
		dict.update({'S3': base.config.breakdown_config['C'+l+'P_S3']})
		dict.update({'S4': base.config.breakdown_config['C'+l+'P_S4']})
		dict.update({'LEVEL': base.config.breakdown_config['C'+l+'P_MASK_LEVEL']})

		streak = base.config.breakdown_config['C'+l+'P_CHECK_STREAK']
		floor = base.config.breakdown_config['C'+l+'P_MASK_FLOOR']
		drop = base.config.breakdown_config['C'+l+'P_AMP_DROP']
		drop_val = base.config.breakdown_config['C'+l+'P_AMP_DROP_VAL']

		string = [dict['TRACE'],
				  'streak  = ' + str(streak),
				  ' floor   = ' + str(floor),
				  ' drop    = ' + str(drop),
				  ' drop_val= ' + str(drop_val)]
		base.logger.message(string, True)

		if base.llrf_control.setNumContinuousOutsideMaskCount( dict['TRACE'], streak) == False:
			base.logger.message('ERROR setNumContinuousOutsideMaskCount = False', True)
		else:
			base.logger.message('setNumContinuousOutsideMaskCount = True', True)

		if base.llrf_control.setMaskFloor(dict['TRACE'], floor) == False:
			base.logger.message('ERROR setMaskFloor = False', True)
		else:
			base.logger.message('setMaskFloor = True', True)

		if base.llrf_control.setShouldCheckMask(dict['TRACE']) == False:
			base.logger.message('setShouldCheckMask = False', True)
		else:
			base.logger.message('setShouldCheckMask = True', True)

		if base.llrf_control.setDropAmpOnOutsideMaskDetection(dict['TRACE'], drop, drop_val) == False:
			base.logger.message('setDropAmpOnOutsideMaskDetection = False', True)
		else:
			base.logger.message('setDropAmpOnOutsideMaskDetection = True', True)



	def time_percent_mask(self,dict):
		return self.llrf_control.setPercentTimeMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE'])
		#print 'time_percent_mask'

	def time_absolute_mask(self,dict):
		return self.llrf_control.setAbsoluteTimeMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE'])
		#print 'time_absolute_mask'

	def index_percent_mask(self,dict):
		#print 'index_percent_mask'
		return self.llrf_control.setPercentMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE'])

	def index_absolute_mask(self,dict):
		return self.llrf_control.setAbsoluteMask(dict['S1'],dict['S2'],dict['S3'],dict['S4'],dict['LEVEL'],dict['TRACE'])
		#print 'time_absolute_mask'



	def is_checking_masks(self):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			if base.llrf_control.setShouldCheckMask(trace) == False:
				return False
		return True

	def have_averages(self):
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			if base.llrfObj[0].trace_data[trace].has_average == False:
				return False
		return True





	def start_trace_monitoring(self,trace_to_save):
		base.logger.header(self.my_name + ' start_trace_monitoring', True)
		if "error" not in trace_to_save:
			for trace in trace_to_save:
				print 'trace = ' + trace
				a = base.llrf_control.startTraceMonitoring(trace)
				if a:
					base.logger.message('started monitoring ' + trace, True)
					if 'POWER' in trace:  # MAGIC_STRING
						self.power_traces.append(trace)
						base.logger.message('added ' + trace + ' to power_traces', True)
				else:
					base.logger.message(' ERROR trying to monitor ' + trace, True)
		else:
			base.logger.message('ERROR IN TRACES TO SAVE', True)
			base.logger.message('ERROR IN TRACES TO SAVE', True)

	def start_trace_rolling_average(self):
		base.logger.header(self.my_name + ' start_trace_rolling_average', True)
		# the cavity trace need a mean
		num_mean = 3  # MAGIC_NUM
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			base.logger.message('starting rolling average for ' + trace, True)
			try:
				if 'REVERSE' in trace:
					num_mean = base.config.breakdown_config['CRP_NUM_AVERAGE_TRACES']
				elif 'FORWARD' in trace:
					num_mean = base.config.breakdown_config['CFP_NUM_AVERAGE_TRACES']
				elif 'PROBE' in trace:
					num_mean = base.config.breakdown_config['CPP_NUM_AVERAGE_TRACES']
			except:
				num_mean = 3#MAGIC_NUM
			base.llrf_control.clearRollingAverage(trace)
			base.llrf_control.setNumRollingAverageTraces(trace, num_mean)
			base.llrf_control.setShouldKeepRollingAverage(trace)
			if base.llrfObj[0].trace_data[trace].keep_rolling_average:
				base.logger.message('STARTED rolling average for ' + trace, True)
			else:
				base.logger.message('STARTED rolling average FAILED for ' + trace, True)

	def get_pulse_end(self):
		self.pulse_end = self.timevector[base.llrfObj[0].pulse_latency] + self.llrf_control.getIndex(base.llrf_control.getPulseLength())
		self.pulse_end_index = self.llrf_control.getTime( self.pulse_end)#len([x for x in self.timevector if x <= self.pulse_end])

	def set_mean_pwr_position(self):
		# MUST BE CALLED AFTER CHANGING PULSE WIDTH ' CANCER
		base.logger.header(self.my_name + ' set_mean_pwr_position',True)
		base.logger.message([
			#'timevector_dt = ' +str(self.timevector_dt ),
			'rf pulse end time = ' + str(self.pulse_end) + ', index = ' + str(self.pulse_end_index),
			'pulse_latency     = '  + str(base.llrfObj[0].pulse_latency),
			'.getPulseLength() = ' + str(base.llrf_control.getPulseLength())],True)
		s = None
		e = None
		for trace in self.power_traces:
			if 'KLYSTRON_FORWARD' in trace:
				s = base.config.llrf_config['KFP_MEAN_TIME_TO_AVERAGE_START']
				e = base.config.llrf_config['KFP_MEAN_TIME_TO_AVERAGE_END']
			elif 'KLYSTRON_REVERSE' in trace:
				s = base.config.llrf_config['KRP_MEAN_TIME_TO_AVERAGE_START']
				e = base.config.llrf_config['KRP_MEAN_TIME_TO_AVERAGE_END']
			elif 'CAVITY_REVERSE' in trace:
				s= base.config.llrf_config['CRP_MEAN_TIME_TO_AVERAGE_START']
				e= base.config.llrf_config['CRP_MEAN_TIME_TO_AVERAGE_END']
			elif 'CAVITY_FORWARD' in trace:
				s = base.config.llrf_config['CFP_MEAN_TIME_TO_AVERAGE_START']
				e = base.config.llrf_config['CFP_MEAN_TIME_TO_AVERAGE_END']
			elif 'CAVITY_PROBE' in trace:
				s = base.config.llrf_config['CPP_MEAN_TIME_TO_AVERAGE_START']
				e = base.config.llrf_config['CPP_MEAN_TIME_TO_AVERAGE_END']
			a = base.llrf_control.setMeanStartEndTime(s,e,trace)

			if a:
				base.logger.message(trace + ' mean monitoring started')
				base.logger.message(['trace_mean_start/end (us) = ' + str(s) +'/'+str((e)),
				'meantime = ' + str(e - s)])

			else:
				base.logger.message(trace + ' mean monitoring NOT started')






	def set_mask_4_param(self):
		self.get_pulse_end()
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			# try:
			if 'REVERSE' in trace:
				self.mask_4[trace] = self.pulse_end_index + len(
					[x for x in self.timevector if x <= base.config.breakdown_config['CRP_MASK_END']])

			elif 'FORWARD' in trace:
				self.mask_4[trace] = self.pulse_end_index + len(
					[x for x in self.timevector if x <= base.config.breakdown_config['CFP_MASK_END']])

			elif 'PROBE' in trace:
				self.mask_4[trace] = self.pulse_end_index + len(
					[x for x in self.timevector if x <= base.config.breakdown_config['CPP_MASK_END']])

			base.logger.message(trace + ' mask_4 index/us = ' + str(self.mask_4[trace]) + '/' + str(self.timevector[self.mask_4[trace]]), True)

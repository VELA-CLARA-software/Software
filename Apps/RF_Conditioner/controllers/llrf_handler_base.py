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

	CRP = 'LRRG_CAVITY_REVERSE_POWER'
	CFP = 'LRRG_CAVITY_FORWARD_POWER'
	CPP = 'CAVITY_PROBE_POWER'

	# these are the indices for the mask set in set_outside_mask_trace_param()
	mask_1 = 0
	mask_2 = 0
	mask_3 = 0
	# this is allowed to change from trace to trace
	mask_4 = {}

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


	def set_mask(self):
		#print(self.my_name + ' setting mask')
		r = False
		if self.have_averages():
			for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
				if 'REVERSE' in trace:
					a = base.llrf_control.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
											 self.mask_4[trace], base.config.breakdown_config['CRP_MASK_LEVEL'],trace)
					if a == False:
						print(self.my_name + ' ERROR SETTING MASK for ' + trace)
				if 'FORWARD' in trace:
					a = base.llrf_control.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
											 self.mask_4[trace], base.config.breakdown_config['CFP_MASK_LEVEL'],trace)
					if a == False:
						print(self.my_name + ' ERROR SETTING MASK for ' + trace)
				if 'PROBE' in trace:
					a = base.llrf_control.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
											 self.mask_4[trace], base.config.breakdown_config['CPP_MASK_LEVEL'],trace)
					if a == False:
						print(self.my_name + ' ERROR SETTING MASK for ' + trace)

			if base.llrf_control.shouldCheckMasks(self.CFP):
				pass
			else:
				print( 'Not checking masks for ' + self.CFP)
			if base.llrf_control.shouldCheckMasks(self.CRP):
				pass
			else:
				print( 'Not checking masks for ' + self.CRP)

			r =  True
		else:
			#print self.my_name + ' cant set mask, NO AVERAGE Traces'
			pass
		return r




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
						print('added ' + trace + ' to power_traces')
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
		self.pulse_end = self.timevector[base.llrfObj[0].pulse_latency] + base.llrf_control.getPulseLength()
		self.pulse_end_index = len([x for x in self.timevector if x <= self.pulse_end])
		base.logger.header(self.my_name + ' set_mean_pwr_position',True)


	def set_mean_pwr_position(self):
		# MUST BE CALLED AFTER CHANGING PULSE WIDTH '
		self.get_pulse_end()
		meantime= int(base.config.llrf_config['MEAN_TIME_TO_AVERAGE'] / self.timevector_dt  )
		trace_mean_start = self.pulse_end_index - 5 - meantime # -10 fudgefactor
		trace_mean_end = self.pulse_end_index - 5 # -10 fudgefactor

		base.logger.header(self.my_name + ' set_mean_pwr_position',True)
		base.logger.message([
			'timevector_dt = ' +str(self.timevector_dt ),
			'rf pulse end time = ' + str(self.pulse_end) + ', index = ' + str(self.pulse_end_index),
			'pulse_latency     = '  + str(base.llrfObj[0].pulse_latency),
			'.getPulseLength() = ' + str(base.llrf_control.getPulseLength()),
			'trace_mean_start/end (index) = ' + str(trace_mean_start) + ', ' + str(trace_mean_end),
			'trace_mean_start/end    (us) = ' + str(self.timevector[trace_mean_start]) + \
			', ' + str(self.timevector[trace_mean_end])],True)

		for trace in self.power_traces:
			base.llrf_control.setMeanStartIndex(trace, trace_mean_start)
			base.llrf_control.setMeanStopIndex(trace, trace_mean_end)
			#print(trace+' mean cal star/end = ' +str(trace_mean_start)+' ' +str(trace_mean_end))


	# these are the main outside_mask_trace parameters that shouldn't change after init
	def set_outside_mask_trace_param(self):
		# much cancer??
		streak= None
		floor= None
		drop= None
		drop_val= None

		# base.logger.message([
		# 	'timevector_dt = ' +str(self.timevector_dt ),
		# 	'rf pulse end time = ' + str(self.pulse_end) + ', index = ' + str(self.pulse_end_index),
		# 	'pulse_latency     = '  + str(base.llrfObj[0].pulse_latency),
		# 	'.getPulseLength() = ' + str(base.llrf_control.getPulseLength()),
		# 	'trace_mean_start/end (index) = ' + str(trace_mean_start) + ', ' + str(trace_mean_end),
		# 	'trace_mean_start/end    (us) = ' + str(self.timevector[trace_mean_start]) + ', ' + str(self.timevector[trace_mean_end])])



		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
		# try:
			if 'REVERSE' in trace:
				streak = base.config.breakdown_config['CRP_CHECK_STREAK']
				floor = base.config.breakdown_config['CRP_MASK_FLOOR']
				drop = base.config.breakdown_config['CRP_AMP_DROP']
				drop_val   = base.config.breakdown_config['CRP_AMP_DROP_VAL']

				self.mask_4[trace] = self.pulse_end_index + len(
					[x for x in self.timevector if x <= base.config.breakdown_config['CRP_MASK_END']])

			elif 'FORWARD' in trace:
				streak = base.config.breakdown_config['CFP_CHECK_STREAK']
				floor = base.config.breakdown_config['CFP_MASK_FLOOR']
				drop = base.config.breakdown_config['CFP_AMP_DROP']
				drop_val   = base.config.breakdown_config['CFP_AMP_DROP_VAL']
				self.mask_4[trace] = self.pulse_end_index + len([x for x in self.timevector if x <= base.config.breakdown_config['CFP_MASK_END']])

			elif 'PROBE' in trace:
				streak = base.config.breakdown_config['CPP_CHECK_STREAK']
				floor = base.config.breakdown_config['CPP_MASK_FLOOR']
				drop = base.config.breakdown_config['CPP_AMP_DROP']
				drop_val   = base.config.breakdown_config['CPP_AMP_DROP_VAL']
				self.mask_4[trace] = self.pulse_end_index + len(
				[x for x in self.timevector if x <= base.config.breakdown_config['CPP_MASK_END']])

			if base.llrf_control.setNumContinuousOutsideMaskCount(trace, streak) == False:
				print('ERROR setNumContinuousOutsideMaskCount ' + trace)
			if base.llrf_control.setMaskFloor(trace, floor)  == False:
					print('ERROR setMaskFloor ' + trace)
			if base.llrf_control.setShouldCheckMask(trace) == False:
				print('ERROR SETTING SHOULD CHECK MASK ' + trace)
			if base.llrf_control.setDropAmpOnOutsideMaskDetection(trace,drop,drop_val) == False:
				print('ERROR setDropAmpOnOutsideMaskDetection ' + trace)
		# except:
		# 	print('set_outside_mas_trace_param ERROR')
		self.mask_1 = base.llrfObj[0].pulse_latency + 15  # MAGIC_INT
		self.mask_2 = self.pulse_end_index - 10  # MAGIC_INT
		self.mask_3 = self.pulse_end_index + 3  # MAGIC_INT
		self.set_mask_4_param()

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
# llrf_handler.py

from VELA_CLARA_enums import MACHINE_AREA
import VELA_CLARA_LLRF_Control
from VELA_CLARA_LLRF_Control import LLRF_TYPE



class llrf_handler_base(object):
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

	def __init__(self,llrf_controller,breakdown_param,llrf_param):
		self.llrf = llrf_controller
		self.llrfObj = [self.llrf.getLLRFObjConstRef()]
		self.llrf_type = self.llrfObj[0].type
		self.timevector = self.llrfObj[0].time_vector.value
		self.breakdown_param = breakdown_param
		self.llrf_param = llrf_param
		self.start_trace_monitoring(llrf_param['TRACES_TO_SAVE'])
		self.set_mean_pwr_position()
		self.start_trace_rolling_average()
		self.set_outside_mask_trace_param()

	def is_checking_masks(self):
		for trace in self.breakdown_param['BREAKDOWN_TRACES']:
			if self.llrf.setShouldCheckMask(trace) == False:
				return False
		return True

	def have_averages(self):
		for trace in self.breakdown_param['BREAKDOWN_TRACES']:
			if self.llrfObj[0].trace_data[trace].has_average == False:
				return False
		return True


	def set_mask(self):
		#print(self.my_name + ' setting mask')
		r = False
		if self.have_averages():
			for trace in self.breakdown_param['BREAKDOWN_TRACES']:
				if 'REVERSE' in trace:
					a = self.llrf.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
					                         self.mask_4[trace], self.breakdown_param['CRP_MASK_LEVEL'],trace)
					if a == False:
						print(self.my_name + ' ERROR SETTING MASK for ' + trace)
				if 'FORWARD' in trace:
					a = self.llrf.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
					                         self.mask_4[trace], self.breakdown_param['CFP_MASK_LEVEL'],trace)
					if a == False:
						print(self.my_name + ' ERROR SETTING MASK for ' + trace)
				if 'PROBE' in trace:
					a = self.llrf.setPercentMask(self.mask_1, self.mask_2, self.mask_3,
					                         self.mask_4[trace], self.breakdown_param['CPP_MASK_LEVEL'],trace)
					if a == False:
						print(self.my_name + ' ERROR SETTING MASK for ' + trace)

			if self.llrf.shouldCheckMasks(self.CFP):
				pass
			else:
				print( 'Not checking masks for ' + self.CFP)
			if self.llrf.shouldCheckMasks(self.CRP):
				pass
			else:
				print( 'Not checking masks for ' + self.CRP)

			r =  True
		else:
			#print self.my_name + ' cant set mask, NO AVERAGE Traces'
			pass
		return r


	# these are the main outside_mask_trace parameters that shouldn't change after init
	def set_outside_mask_trace_param(self):
		# much cancer??
		for trace in self.breakdown_param['BREAKDOWN_TRACES']:
		# try:
			if 'REVERSE' in trace:
				streak = self.breakdown_param['CRP_CHECK_STREAK']
				floor = self.breakdown_param['CRP_MASK_FLOOR']
				drop = self.breakdown_param['CRP_AMP_DROP']
				drop_val   = self.breakdown_param['CRP_AMP_DROP_VAL']

				self.mask_4[trace] = self.pulse_end_index + len(
					[x for x in self.timevector if x <= self.breakdown_param['CRP_MASK_END']])

			elif 'FORWARD' in trace:
				streak = self.breakdown_param['CFP_CHECK_STREAK']
				floor = self.breakdown_param['CFP_MASK_FLOOR']
				drop = self.breakdown_param['CFP_AMP_DROP']
				drop_val   = self.breakdown_param['CFP_AMP_DROP_VAL']
				self.mask_4[trace] = self.pulse_end_index + len([x for x in self.timevector if x <= self.breakdown_param['CFP_MASK_END']])

			elif 'PROBE' in trace:
				streak = self.breakdown_param['CPP_CHECK_STREAK']
				floor = self.breakdown_param['CPP_MASK_FLOOR']
				drop = self.breakdown_param['CPP_AMP_DROP']
				drop_val   = self.breakdown_param['CPP_AMP_DROP_VAL']
				self.mask_4[trace] = self.pulse_end_index + len(
				[x for x in self.timevector if x <= self.breakdown_param['CPP_MASK_END']])

			if self.llrf.setNumContinuousOutsideMaskCount(trace, streak) == False:
				print('ERROR setNumContinuousOutsideMaskCount ' + trace)
			if self.llrf.setMaskFloor(trace, floor)  == False:
					print('ERROR setMaskFloor ' + trace)
			if self.llrf.setShouldCheckMask(trace) == False:
				print('ERROR SETTING SHOULD CHECK MASK ' + trace)
			if self.llrf.setDropAmpOnOutsideMaskDetection(trace,drop,drop_val) == False:
				print('ERROR setDropAmpOnOutsideMaskDetection ' + trace)
		# except:
		# 	print('set_outside_mas_trace_param ERROR')
		self.mask_1 = self.llrfObj[0].pulse_latency + 15  # MAGIC_INT
		self.mask_2 = self.pulse_end_index - 10  # MAGIC_INT
		self.mask_3 = self.pulse_end_index + 3  # MAGIC_INT

	def start_trace_monitoring(self,trace_to_save):
		if "error" not in trace_to_save:
			for trace in trace_to_save:
				print 'trace = ' + trace
				a = self.llrf.startTraceMonitoring(trace)
				if a:
					print(self.my_name + ' started monitoring ' + trace)
					if 'POWER' in trace:  # MAGIC_STRING
						self.power_traces.append(trace)
						print('added ' + trace + ' to power_traces')
				else:
					print(self.my_name + ' ERROR trying to monitor ' + trace)
		else:
			print('ERROR IN TRACES TO SAVE')
			print('ERROR IN TRACES TO SAVE')
			print('ERROR IN TRACES TO SAVE')
			print('ERROR IN TRACES TO SAVE')
			print('ERROR IN TRACES TO SAVE')

	def start_trace_rolling_average(self):
		# the cavity trace need a mean
		num_mean = 3  # MAGIC_NUM
		for trace in self.breakdown_param['BREAKDOWN_TRACES']:
			print self.my_name + ' starting rolling average for ' + trace
			try:
				if 'REVERSE' in trace:
					num_mean = self.breakdown_param['CRP_NUM_AVERAGE_TRACES']
				elif 'FORWARD' in trace:
					num_mean = self.breakdown_param['CFP_NUM_AVERAGE_TRACES']
				elif 'PROBE' in trace:
					num_mean = self.breakdown_param['CPP_NUM_AVERAGE_TRACES']
			except:
				num_mean = 3#MAGIC_NUM
			self.llrf.clearRollingAverage(trace)
			self.llrf.setNumRollingAverageTraces(trace, num_mean)
			self.llrf.setShouldKeepRollingAverage(trace)

			if self.llrfObj[0].trace_data[trace].keep_rolling_average:
				print self.my_name + ' started rolling average for ' + trace
			else:
				print self.my_name + ' starting rolling average FAILED for ' + trace



	def set_mean_pwr_position(self):
		# MUST BE CALLED AFTER CHANGING PULSE WIDTH '
		print('llrfObj[0].pulse_latency = ', self.llrfObj[0].pulse_latency)
		self.pulse_end = self.timevector[self.llrfObj[0].pulse_latency] + self.llrf.getPulseLength()
		self.pulse_end_index = len([x for x in self.timevector if x <= self.pulse_end])
		dt = self.timevector[1]-self.timevector[0]
		print 'dt = ' +str(dt)
		meantime= int(self.llrf_param['MEAN_TIME_TO_AVERAGE'] / dt )
		trace_mean_start = self.pulse_end_index - 1- meantime # -1 fudgefactor
		trace_mean_end = self.pulse_end_index - 1 # -1 fudgefactor
		print(
		self.my_name + ' rf pulse end time = ' + str(self.pulse_end) + ', end index      = ' + str(self.pulse_end_index))
		print(self.my_name + ' trace_mean_start  = ' + str(trace_mean_start) + ', trace_mean_end = ' + str(trace_mean_end))
		for trace in self.power_traces:
			self.llrf.setMeanStartIndex(trace, trace_mean_start)
			self.llrf.setMeanStopIndex(trace, trace_mean_end)
			print(trace+' mean cal star/end = ' +str(trace_mean_start)+' ' +str(trace_mean_end))

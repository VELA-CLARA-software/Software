import data.charge_measurement_data_base as dat
from base.base import base

class llrf_handler_base(base):
	# whoami
	my_name = 'llrf_handler'
	# init attributes
	power_traces = []
	pulse_end_index = 0
	pulse_end = 0
	mask_set = False
	mask_count = 0

	def __init__(self):
		#super(bpm_handler_base, self).__init__()
		#base.__init__(self)
		self.num_buffer_traces = 40

		self.timevector = base.data.values[dat.llrf_object]["CLARA_LRRG"].time_vector
		base.config.llrf_config = base.config.llrf_config
		#self.start_trace_monitoring()
		#self.setup_trace_rolling_average()

		self.llrf_data_values_dict = {}
		self.start_trace_monitoring()

	def get_mask_rolling_average_dict(self):
		r = {}
		for trace in base.config.breakdown_config['TRACES_TO_SAVE']:
			r[ trace + '_RA'] = self.llrf_control.getRollingAverage(trace)
			r[ trace + '_HI'] = self.llrf_control.getHiMask(trace)
			r[ trace + '_LO'] = self.llrf_control.getLoMask(trace)
		return r

	def start_trace_monitoring(self):
		self.kly_pwr_start = base.config.llrf_config['1_MEAN_START']
		self.kly_pwr_end = base.config.llrf_config['1_MEAN_END']
		self.kly_pha_start = base.config.llrf_config['2_MEAN_START']
		self.kly_pha_end = base.config.llrf_config['2_MEAN_END']
		self.cav_fwd_start = base.config.llrf_config['3_MEAN_START']
		self.cav_fwd_end = base.config.llrf_config['3_MEAN_END']
		self.cav_pha_start = base.config.llrf_config['4_MEAN_START']
		self.cav_pha_end = base.config.llrf_config['4_MEAN_END']
		self.start_vals = [self.kly_pwr_start,self.kly_pha_start,self.cav_fwd_start,self.cav_pha_start]
		self.end_vals = [self.kly_pwr_end, self.kly_pha_end, self.cav_fwd_end, self.cav_pha_end]
		self.i = 0
		for trace in base.config.llrf_config['TRACES_TO_SAVE']:
			print(trace)
			print(self.i)
			base.llrf_control.setIndividualTraceBufferSize(trace,base.config.llrf_config['NUM_BUFFER_TRACES'])
			base.llrf_control.setKeepRollingAverage(trace, True)
			base.llrf_control.setMeanStartEndTime(self.start_vals[self.i],self.end_vals[self.i],trace)
			self.i += 1

		else:
			#print(2)
			base.logger.message('!!! ERROR IN TRACES TO SAVE !!!', True)


	def setup_trace_rolling_average(self):
		base.logger.header(self.my_name + ' setup_trace_rolling_average', True)
		# the cavity trace need a mean
		num_mean = 3  # MAGIC_NUM
		for trace in base.config.llrf_config['NUM_BUFFER_TRACES']:
			sn = base.llrf_control.shortLLRFTraceName(trace)
			base.logger.message('starting rolling average for ' + trace + ' (' + sn + ')', True)

			# this needs updating cos its cnacer
			num_mean = self.get_breakdown_config_value(base.llrf_control.shortLLRFTraceName(
					trace),  "NUM_BUFFER_TRACES")

			base.llrf_control.setTraceRollingAverageSize(trace, num_mean)
			base.llrf_control.setShouldKeepRollingAverage(trace)
			if base.llrfObj[0].trace_data[trace].keep_rolling_average:
				base.logger.message('STARTED rolling average for ' + trace, True)
				base.logger.message('RollingAverageSize = ' + str(
						self.llrf_control.getTraceRollingAverageSize(trace)), True)
				base.logger.message('RollingAverageCount = ' + str(
						self.llrf_control.getTraceRollingAverageCount(trace)), True)
			else:
				base.logger.message('STARTED rolling average FAILED for ' + trace, True)
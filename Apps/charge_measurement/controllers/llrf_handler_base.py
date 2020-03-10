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
		#self.start_trace_monitoring(base.config.llrf_config['TRACES_TO_SAVE'])#MAGIC_STRING
		#self.setup_trace_rolling_average()

		self.llrf_data_values_dict = {}

	def get_mask_rolling_average_dict(self):
		r = {}
		for trace in base.config.breakdown_config['BREAKDOWN_TRACES']:
			r[ trace + '_RA'] = self.llrf_control.getRollingAverage(trace)
			r[ trace + '_HI'] = self.llrf_control.getHiMask(trace)
			r[ trace + '_LO'] = self.llrf_control.getLoMask(trace)
		return r

	def start_trace_monitoring(self,trace_to_save):
		base.logger.header(self.my_name + ' setting all SCAN to passive', True)
		base.llrf_handler.setAllSCANToPassive()
		if "error" not in trace_to_save:
			#print(1)
			base.llrf_handler.setAllSCANToPassive()
			base.llrf_handler.setAllTraceBufferSize(base.config.llrf_config['NUM_BUFFER_TRACES'])

			# ADDING IN THIS SO THAT ARCHIVING OF KFPow and CPPow can happen using cursor

			base.llrf_handler.setPowerRemoteTraceSCAN10sec('KLYSTRON_FORWARD_POWER')
			base.llrf_handler.setPowerRemoteTraceSCAN10sec('CAVITY_PROBE_POWER')

		else:
			#print(2)
			base.logger.message('!!! ERROR IN TRACES TO SAVE !!!', True)

		base.logger.header(self.my_name + ' setting One Record SCAN to IO/intr', True)
		base.llrf_handler.resetTORSCANToIOIntr()

		base.logger.header(self.my_name + ' setting One Record ACWM to event', True)
		base.llrf_handler.setTORACQMEvent()


	def setup_trace_rolling_average(self):
		base.logger.header(self.my_name + ' setup_trace_rolling_average', True)
		# the cavity trace need a mean
		num_mean = 3  # MAGIC_NUM
		for trace in base.config.llrf_config['BREAKDOWN_TRACES']:
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
				base.logger.message('RollingAverageSize = ' + str(
						self.llrf_control.getTraceRollingAverageSize(trace)), True)
				base.logger.message('RollingAverageCount = ' + str(
						self.llrf_control.getTraceRollingAverageCount(trace)), True)
			else:
				base.logger.message('STARTED rolling average FAILED for ' + trace, True)
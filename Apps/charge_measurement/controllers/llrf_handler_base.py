# import data.bpm_attenuation_calibration_data_base as dat
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

		self.timevector = base.llrfObj[0].time_vector.value
		base.config.llrf_config = base.config.llrf_config
		self.start_trace_monitoring( base.config.llrf_config['TRACES_TO_SAVE'])#MAGIC_STRING

		self.llrf_data_values_dict = {}
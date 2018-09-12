# import data.bpm_attenuation_calibration_data_base as dat
from base.base import base

class blm_handler_base(base):
	# whoami
	my_name = 'blm_handler'
	# init attributes
	power_traces = []
	pulse_end_index = 0
	pulse_end = 0
	mask_set = False
	mask_count = 0

	def __init__(self):
		super(blm_handler_base, self).__init__()
		#base.__init__(self)
		#self.num_buffer_traces = 40

		# self.timevector = base.bpmObj[0].time_vector.value
		base.config.blm_config = base.config.blm_config
		# self.start_trace_monitoring( base.config.bpm_config['TRACES_TO_SAVE'])#MAGIC_STRING

		self.blm_data_values_dict = {}
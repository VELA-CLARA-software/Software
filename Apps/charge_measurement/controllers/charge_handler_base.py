from base.base import base

class charge_handler_base(base):
	# whoami
	my_name = 'charge_handler'
	# init attributes

	def __init__(self):
		super(charge_handler_base, self).__init__()
		#base.__init__(self)
		#self.num_buffer_traces = 40

		# self.timevector = base.bpmObj[0].time_vector.value
		#base.config.pil_config = base.config.pil_config
		base.config.charge_config = base.config.charge_config
		# self.start_trace_monitoring( base.config.bpm_config['TRACES_TO_SAVE'])#MAGIC_STRING
		self.charge_data_values_dict = {}
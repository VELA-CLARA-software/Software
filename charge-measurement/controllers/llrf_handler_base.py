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

		base.config.llrf_config = base.config.llrf_config

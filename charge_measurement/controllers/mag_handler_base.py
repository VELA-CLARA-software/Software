# import data.bpm_attenuation_calibration_data_base as dat
from base.base import base

class mag_handler_base(base):
	# whoami
	my_name = 'mag_handler'

	def __init__(self):
		super(mag_handler_base, self).__init__()
		#base.__init__(self)
		#self.num_buffer_traces = 40

		base.config.mag_config = base.config.mag_config

		self.mag_data_values_dict = {}
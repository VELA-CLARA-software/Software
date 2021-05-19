from base.base import base

class shutter_handler_base(base):
	# whoami
	my_name = 'shutter_handler'
	# init attributes

	def __init__(self):
		super(shutter_handler_base, self).__init__()
		base.config.shutter_config = base.config.shutter_config
		self.shutter_data_values_dict = {}
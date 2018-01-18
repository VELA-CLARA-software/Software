import monitor
from VELA_CLARA_LLRF_Control import LLRF_TYPE

class state_monitor(monitor.monitor):
	# whoami
	my_name = 'state_monitor'
	def __init__(self,
	             controller=None,
	             data_dict=None,
	             data_dict_key='',
	             update_time=1000,
	             llrf_type=LLRF_TYPE.UNKNOWN_TYPE,
	             ):
		monitor.monitor.__init__(self,
		                         llrf_type=llrf_type,
		                         update_time=update_time
			)
		self.localcontrol = controller
		self.dict = data_dict
		self.key = data_dict_key
		self.update_time = update_time
		self.timer.timeout.connect(self.check)
		self.timer.start(update_time)
		self.set_success = True

	def start(self):
		self.check()
		print(self.my_name + ' starting monitoring, update time = ' + str(self.update_time))
		self.timer.timeout.connect(self.check)
		self.timer.start(self.update_time)

	def check(self):
		a = 1
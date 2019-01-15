from VELA_CLARA_enums import MACHINE_MODE,MACHINE_AREA
from data.config_reader import config_reader
from data.data_logger import data_logger
import blm_handler
import charge_handler
import datetime
import data.blm_plotter_data_base as dat
from data_monitors.data_monitoring import data_monitoring
from base.base import base


class controller_base(base):
	# whoami
	my_name = 'controller_base'

	have_config = False
	data_monitor = data_monitoring()

	blm_handler = None
	charge_handler = None

	def __init__(self, argv, machine_mode=MACHINE_MODE.PHYSICAL, machine_area=MACHINE_AREA.CLARA_2_BA1_BA2):
		#super(base, self).__init__()
		base.__init__(self)
		self.argv = argv
		# read the config file
		# base.config.config_file = config_file
		self.read_config()
		self.machine_mode = machine_mode
		self.machine_area = machine_area

		# data logging
		base.logger = base.logger

		base.logger.header(self.my_name + ' creating HWC ', True)

		self.start_blm_control()
		self.start_charge_control()

	def start_charge_control(self):
		base.charge_control = base.charge_init.getChargeController(self.machine_mode,self.machine_area)
		base.logger.message('Monitoring Charge: ' + ' ' + self.get_charge_names()[0], True)
		base.config.charge_config['CHARGE_NAME'] = "WCM"
		controller_base.charge_handler = charge_handler.charge_handler()

	def start_blm_control(self):
		base.blm_control = base.blm_init.physical_C2B_BLM_Controller()#(self.machine_mode,self.machine_area)
		base.logger.message('Monitoring BLMs: ' + ' '.join(self.get_blm_names()), True)
		base.config.blm_config['BLM_NAMES'] = self.get_blm_names()
		controller_base.blm_handler = blm_handler.blm_handler()

	def get_blm_names(self):
		temp = []
		blm_names = base.blm_control.getBLMNames()
		for names in blm_names:
			temp.append(names)
		return temp

	def get_charge_names(self):
		temp = []
		charge_names = base.charge_control.getChargePVs()
		for names in charge_names:
			temp.append(names)
		return temp

	def read_config(self):
		print('read_config')
		# read config
		base.have_config = base.config.get_config()



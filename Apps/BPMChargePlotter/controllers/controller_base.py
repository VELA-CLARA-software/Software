from VELA_CLARA_BPM_Control import MACHINE_MODE,MACHINE_AREA
from data.config_reader import config_reader
from data.data_logger import data_logger
import bpm_handler
import datetime
import data.bpm_charge_plotter_data_base as dat
from data_monitors.data_monitoring import data_monitoring
from base.base import base


class controller_base(base):
	# whoami
	my_name = 'controller_base'

	have_config = False
	data_monitor = data_monitoring()

	bpm_handler = None

	def __init__(self, argv, config_file):
		#super(base, self).__init__()
		base.__init__(self)
		self.argv = argv
		# read the config file
		base.config.config_file = config_file
		self.read_config()

		# data logging
		base.logger = base.logger

	# read config
	def read_config(self):
		print('read_config')
		# read config
		base.have_config = base.config.get_config()
		# set llr_typ e(i.e. which cavity to value in reader
		# to continue this MUST NOT BE UNKNOWN
		# base.llrf_type = base.config.llrf_type
		self.set_config()
		if base.have_config:

			base.logger.header(self.my_name + ' creating HWC ', True)

			if bool(base.config.bpm_config):
				self.start_bpm_control()
			if bool(base.config.charge_config):
				self.start_charge_control()
		else:
			base.logger.header(self.my_name + ' read_config failed sanity checks!!!', True)

		base.logger.header(controller_base.my_name +' has read config',True)
		logdata = ['config file = ' + base.config.config_file,
		'dumping data to log']
		for item in base.config.all_config_data:
			logdata.append(''.join(['%s:%s, ' % (key, value) for (key, value) in item.iteritems()]))
		base.logger.message(logdata, True)

	def start_charge_control(self):
		try:
			a = base.config.charge_config['CHARGE_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			b = base.config.charge_config['CHARGE_MODE']
			base.charge_control = base.charge_init.getChargeController(b,a)
			# base.scope_control = base.scope_init.physical_VELA_INJ_Scope_Controller()
			base.logger.message('start_charge_control created ' + str(base.config.charge_config['CHARGE_AREA']) + ' object', True)
			base.logger.message('Monitoring Charge: ' + ' ' + self.get_charge_names()[0], True)
			base.config.charge_config['CHARGE_NAME'] = self.get_charge_names()
		else:
			base.logger.message('start_charge_control UNKNOWN_MACHINE area cannot create charge object', True)

	def start_bpm_control(self):
		try:
			a = base.config.bpm_config['BPM_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			b = base.config.bpm_config['BPM_MODE']
			base.bpm_control = base.bpm_init.getBPMController(b,a)
			# base.bpm_control = base.bpm_init.virtual_CLARA_PH1_BPM_Controller()
			base.logger.message('start_bpm_control created ' + str(base.config.bpm_config['BPM_AREA']) + ' object', True)
			base.logger.message('Monitoring BPMs: ' + ' '.join(self.get_bpm_names()), True)
			base.config.bpm_config['BPM_NAMES'] = self.get_bpm_names()
			base.data.values[dat.machine_mode] = 'virtual'
			base.data.values[dat.num_bpms] = len(base.config.bpm_config['BPM_NAMES'])
			base.data.values[dat.bpm_names] = base.config.bpm_config['BPM_NAMES']
			controller_base.bpm_handler = bpm_handler.bpm_handler()
		else:
			base.logger.message('start_bpm_control UNKNOWN_MACHINE area cannot create bpm object', True)

	def get_bpm_names(self):
		temp = []
		bpm_names = base.bpm_control.getBPMNames()
		for names in bpm_names:
			temp.append(names)
		return temp

	def get_charge_names(self):
		temp = []
		charge_names = base.charge_control.getChargePVs()
		for names in charge_names:
			temp.append(names)
		return temp



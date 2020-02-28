from VELA_CLARA_LLRF_Control import MACHINE_MODE,MACHINE_AREA,LLRF_TYPE
from data.config_reader import config_reader
from data.data_logger import data_logger
import controllers.pil_handler
import controllers.llrf_handler
import controllers.mag_handler
import datetime
import data.charge_measurement_data_base as dat
from data_monitors.data_monitoring import data_monitoring
from base.base import base


class controller_base(base):
	# whoami
	my_name = 'controller_base'

	have_config = False
	data_monitor = data_monitoring()

	pil_handler = None
	llrf_handler = None
	mag_handler = None

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

			if bool(base.config.pil_config):
				self.start_pil_control()
			if bool(base.config.llrf_config):
				self.start_llrf_control()
			if bool(base.config.mag_config):
				self.start_mag_control()
		else:
			base.logger.header(self.my_name + ' read_config failed sanity checks!!!', True)

		base.logger.header(controller_base.my_name +' has read config',True)
		logdata = ['config file = ' + base.config.config_file,
		'dumping data to log']
		for item in base.config.all_config_data:
			logdata.append(''.join(['%s:%s, ' % (key, value) for (key, value) in item.items()]))
		base.logger.message(logdata, True)

	def start_pil_control(self):
		# try:
		# 	a = base.config.pil_config['PIL_AREA']# MAGIC_STRING
		# except:
		# 	a = MACHINE_AREA.UNKNOWN_AREA
		# if a is not MACHINE_AREA.UNKNOWN_AREA:
		# base.pil_control = base.pil_init.getPILaserController(a)
		# base.scope_control = base.scope_init.physical_VELA_INJ_Scope_Controller()
		base.logger.message('start_pil_control created PIL object', True)
		base.logger.message('Monitoring PIL', True)
		# base.config.charge_config['CHARGE_NAME'] = self.get_charge_names()

	def start_llrf_control(self):
		try:
			a = base.config.llrf_config['LLRF_TYPE']  # MAGIC_STRING
		except:
			a = LLRF_TYPE.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_TYPE:
			b = base.config.llrf_config['MACHINE_MODE']
			base.llrf_control = base.llrf_init.getLLRFController(b, a)
			# base.bpm_control = base.bpm_init.virtual_CLARA_PH1_BPM_Controller()
			base.logger.message('start_llrf_control created ' + str(base.config.llrf_config['LLRF_AREA']) + ' object',
								True)
			base.logger.message('Monitoring LLRF: ' + ' '.join(self.get_llrf_names()), True)
			base.config.llrf_config['LLRF_NAME'] = self.get_llrf_names()
			base.data.values[dat.machine_mode] = 'physical'
			controller_base.llrf_handler = llrf_handler.llrf_handler()
		else:
			base.logger.message('start_llrf_control UNKNOWN_MACHINE area cannot create llrf object', True)

	def start_mag_control(self):
		try:
			a = base.config.mag_config['MAG_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			b = base.config.mag_config['LLRF_MODE']
			base.mag_control = base.mag_init.getMagnetController(b,a)
			# base.bpm_control = base.bpm_init.virtual_CLARA_PH1_BPM_Controller()
			base.logger.message('start_mag_control created ' + str(base.config.mag_config['MAG_AREA']) + ' object', True)
			base.logger.message('Monitoring magnets: ' + ' '.join(self.get_mag_names()), True)
			base.config.mag_config['SOL_NAME'] = self.get_mag_names()
			base.config.mag_config['BSOL_NAME'] = self.get_mag_names()
			base.data.values[dat.machine_mode] = 'physical'
			controller_base.mag_handler = mag_handler.mag_handler()
		else:
			base.logger.message('start_mag_control UNKNOWN_MACHINE area cannot create mag object', True)

	def get_mag_names(self):
		temp = []
		mag_names = base.mag_control.getMagnetNames()
		for names in mag_names:
			temp.append(names)
		return temp



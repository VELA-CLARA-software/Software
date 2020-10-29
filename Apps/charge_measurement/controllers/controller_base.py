import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from data.config_reader import config_reader
from data.data_logger import data_logger
from VELA_CLARA_LLRF_Control import MACHINE_MODE,MACHINE_AREA,LLRF_TYPE
from controllers.pil_handler import pil_handler
from controllers.shutter_handler import shutter_handler
from controllers.llrf_handler import llrf_handler
from controllers.mag_handler import mag_handler
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
	shutter_handler = None
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

			if bool(base.config.las_hwp_config):
				self.start_pil_control()
			if bool(base.config.shutter_config):
				self.start_shutter_control()
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
		base.las_hwp_factory = base.hardware_factory.getLaserHWPFactory()
		base.las_em_factory = base.hardware_factory.getLaserEnergyMeterFactory()
		base.hwp_control = base.las_hwp_factory.getLaserHWP(base.config.las_hwp_config['LAS_HWP_NAME'])
		base.las_em_control = base.las_em_factory.getLaserEnergyMeter(base.config.las_em_config['LAS_EM_NAME'])
		base.logger.message('start_pil_control created PIL object', True)
		base.logger.message('Monitoring PIL', True)
		# base.config.charge_config['CHARGE_NAME'] = self.get_charge_names()
		base.cam_control = base.cam_init.physical_CLARA_VC_Camera_Controller()
		base.logger.message('start_cam_control created VC object', True)
		controller_base.pil_handler = pil_handler()

	def start_shutter_control(self):
		base.shutter_factory = base.hardware_factory.getShutterFactory()
		base.shutter_control_1 = base.shutter_factory.getShutter(base.config.shutter_config['SHUTTER_NAME_1'])
		base.shutter_control_2 = base.shutter_factory.getShutter(base.config.shutter_config['SHUTTER_NAME_2'])
		base.logger.message('start_shutter_control created SHUTTER object', True)
		base.logger.message('Monitoring SHUTTER', True)
		controller_base.shutter_handler = shutter_handler()

	def start_llrf_control(self):
		try:
			a = base.config.llrf_config['LLRF_TYPE']  # MAGIC_STRING
		except:
			a = LLRF_TYPE.UNKNOWN_TYPE
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			b = base.config.llrf_config['MACHINE_MODE']
			base.llrf_control = base.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, a)
			base.logger.message('start_llrf_control created ' + str(base.config.llrf_config['LLRF_TYPE']) + ' object',
								True)
			base.data.values[dat.llrf_object]["CLARA_LRRG"] = base.llrf_control.getLLRFObjConstRef()
			base.logger.message('Monitoring LLRF', True)
			base.config.llrf_config['LLRF_NAME'] = base.data.values[dat.llrf_object]["CLARA_LRRG"].name
			base.data.values[dat.machine_mode] = 'physical'
			controller_base.llrf_handler = llrf_handler()
		else:
			base.logger.message('start_llrf_control UNKNOWN_MACHINE area cannot create llrf object', True)

	def start_mag_control(self):
		try:
			a = base.config.mag_config['MACHINE_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			b = base.config.mag_config['MACHINE_MODE']
			#base.mag_control = base.mag_init.getMagnetController(b,a)
			base.logger.message('start_mag_control created ' + str(base.config.mag_config['MACHINE_AREA']) + ' object', True)
			#base.logger.message('Monitoring magnets: ' + ' '.join(self.get_mag_names()), True)
			#base.config.mag_config['SOL_NAME'] = self.get_mag_names()
			#base.config.mag_config['BSOL_NAME'] = self.get_mag_names()
			base.data.values[dat.machine_mode] = 'physical'
			controller_base.mag_handler = mag_handler()
		else:
			base.logger.message('start_mag_control UNKNOWN_MACHINE area cannot create mag object', True)

	def get_mag_names(self):
		temp = []
		mag_names = base.mag_control.getMagnetNames()
		for names in mag_names:
			temp.append(names)
		return temp



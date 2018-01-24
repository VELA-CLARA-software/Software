from VELA_CLARA_enums import MACHINE_MODE
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_LLRF_Control import LLRF_TYPE
# import VELA_CLARA_LLRF_Control
# import VELA_CLARA_Vac_Valve_Control
# import VELA_CLARA_RF_Modulator_Control
# import VELA_CLARA_RF_Protection_Control
from data.config_reader import config_reader
from data.data_logger import data_logger
import llrf_handler
import datetime
from data_monitors.data_monitoring import data_monitoring
from base.base import base



class controller_base(base):
	# whoami
	my_name = 'controller_base'

	have_config = False

	#llrfObj = None
	#
	t_start = None

	data_monitor = data_monitoring()

	def __init__(self, argv, config_file):
		#super(base, self).__init__()
		base.__init__(self)
		self.argv = argv
		# read the config file
		base.config.config_file = config_file
		self.read_config()

		# data logging
		self.logger = base.logger

	# not sur ethese are used anymore
	def start_time(self):
		self.t_start = datetime.datetime.now()
	def seconds_since_start(self):
		return (datetime.datetime.now() - self.t_start).total_seconds()
	def seconds_elapsed(self,val):
		return self.seconds_since_start() >= val

	# read config
	def read_config(self):
		print('read_config')
		# read config
		base.have_config = base.config.get_config()
		# set llr_typ e(i.e. which cavity to value in reader
		# to continue this MUST NOT BE UNKNOWN
		base.llrf_type = base.config.llrf_type
		self.set_config()
		if base.have_config:

			self.logger.header(self.my_name + ' creating HWC ', True)

			if bool(base.config.llrf_config):
				self.start_llrf_control()
			if bool(base.config.mod_config):
				self.start_mod_control()

			if bool(base.config.vac_valve_config):
				self.start_vac_valve_control()
			if bool(base.config.rfprot_config):
				self.start_rf_prot_control()
		else:
			self.logger.header(self.my_name + ' read_config failed sanity checks!!!', True)

		base.logger.header(controller_base.my_name +' has read config',True)
		logdata = ['config file = ' + base.config.config_file,
		'dumping data to log']
		for item in base.config.all_config_data:
			logdata.append(''.join(['%s:%s, ' % (key, value) for (key, value) in item.iteritems()]))
		base.logger.message(logdata, True)

	def is_gun_type(self, type):
		if type == LLRF_TYPE.CLARA_HRRG: return True
		elif type == LLRF_TYPE.CLARA_LRRG: return True
		elif type == LLRF_TYPE.VELA_HRRG: return True
		elif type == LLRF_TYPE.VELA_LRRG: return True
		else: return False

	def start_rf_prot_control(self):
		if self.is_gun_type(base.llrf_type):
			base.prot_control = base.prot_init.physical_Gun_Protection_Controller()
			self.logger.message('start_rf_prot_control created a protection control  object',True)
		elif self.llrf_type == LLRF_TYPE.L01:
			self.prot_control = None
			self.logger.message('start_rf_prot_control did not create a protection control  object',True)
		else:
			self.logger.message('start_rf_prot_control did not create a protection control  object',True)

	def start_vac_valve_control(self):
		try:
			a = base.config.vac_valve_config['VAC_VALVE_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			base.valve_control = base.valve_init.getVacValveController(MACHINE_MODE.PHYSICAL,a)
			self.logger.message('start_vac_valve_control created ' + str(base.config.vac_valve_config['VAC_VALVE_AREA']) + ' object', True)
		else:
			self.logger.message('start_vac_valve_control UNKNOWN_MACHINE area cannot create vac-valve object', True)

	def start_mod_control(self):
		if self.is_gun_type(base.llrf_type):
			base.mod_control = base.mod_init.physical_GUN_MOD_Controller()
			self.logger.message('start_mod_control created a gun modulator object',True)
		elif base.llrf_type == LLRF_TYPE.L01:
			base.mod_control = None
			self.logger.message('start_mod_control can\'t create a linac modulator object',True)
		else:
			self.logger.message('start_mod_control can\'t create a modulator, unknown llrf_type',True)


	def start_llrf_control(self):
		if base.llrf_type is not LLRF_TYPE.UNKNOWN_TYPE:
			base.llrf_control = base.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, base.llrf_type)
			base.llrfObj = [base.llrf_control.getLLRFObjConstRef()]
			# rationalise the trace names
			base.config.llrf_config['TRACES_TO_SAVE'] = self.get_full_trace_name(
				self.config.llrf_config['TRACES_TO_SAVE'])
			base.config.breakdown_config['BREAKDOWN_TRACES'] = self.get_full_trace_name(base.config.breakdown_config[ 'BREAKDOWN_TRACES'])
			self.llrf_handler = llrf_handler.llrf_handler()
			self.logger.message('start_llrf_control created ' + str(base.llrf_type) + ', llrf_handler and got full trace names:',True)
			self.logger.message('TRACES TO SAVE:',True)
			self.logger.message(base.config.llrf_config['TRACES_TO_SAVE'], True)
			self.logger.message('BREAKDOWN_TRACES SAVE:', True)
			self.logger.message(base.config.breakdown_config['BREAKDOWN_TRACES'], True)
		else:
			self.llrf_control = None
			self.logger.message('start_llrf_control can\'t create a llrf_control unknown llrf_type',True)

	# rationalise the trace names
	def get_full_trace_name(self,traces):
		temp = []
		for trace in traces:
			temp.append(self.llrf_control.fullCavityTraceName(trace))
		return temp



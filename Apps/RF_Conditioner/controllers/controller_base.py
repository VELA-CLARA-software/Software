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
	#t_start = None

	data_monitor = data_monitoring()

	llrf_handler = None

	def __init__(self, argv, config_file):
		#super(base, self).__init__()
		base.__init__(self)
		self.argv = argv
		# read the config file
		base.config.config_file = config_file
		self.read_config()

		# data logging
		base.logger = base.logger

	# # not sur ethese are used anymore
	# def start_time(self):
	# 	self.t_start = datetime.datetime.now()
	# def seconds_since_start(self):
	# 	return (datetime.datetime.now() - self.t_start).total_seconds()
	# def seconds_elapsed(self,val):
	# 	return self.seconds_since_start() >= val

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

			base.logger.header(self.my_name + ' creating HWC ', True)

			if bool(base.config.llrf_config):
				self.start_llrf_control()
			if bool(base.config.mod_config):
				self.start_mod_control()

			if bool(base.config.vac_valve_config):
				self.start_vac_valve_control()
			if bool(base.config.rfprot_config):
				self.start_rf_prot_control()
		else:
			base.logger.header(self.my_name + ' read_config failed sanity checks!!!', True)

		base.logger.header(controller_base.my_name +' has read config',True)
		logdata = ['config file = ' + base.config.config_file,
		'dumping data to log']
		for item in base.config.all_config_data:
			logdata.append(''.join(['%s:%s, ' % (key, value) for (key, value) in item.iteritems()]))
		base.logger.message(logdata, True)


	def start_rf_prot_control(self):
		if self.is_gun_type(base.llrf_type):
			base.prot_control = base.prot_init.physical_Gun_Protection_Controller()
			base.logger.message('start_rf_prot_control created a protection control  object',True)
		elif base.llrf_type == LLRF_TYPE.L01:
			# we don't have a linac protection controller yet ..
			#self.prot_control = base.prot_init.physical_L01_Protection_Controller()
			self.prot_control = None
			base.logger.message('start_rf_prot_control did not create a protection control  object',True)
		else:
			base.logger.message('start_rf_prot_control did not create a protection control  object',True)

	def start_vac_valve_control(self):
		try:
			a = base.config.vac_valve_config['VAC_VALVE_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			'''
				THIS IS NOT WORKING CORRECTLY
			'''
			#base.valve_control = base.valve_init.getVacValveController(MACHINE_MODE.PHYSICAL,a)
			base.valve_control = base.valve_init.physical_CLARA_PH1_Vac_Valve_Controller()
			base.logger.message('start_vac_valve_control created ' + str(base.config.vac_valve_config['VAC_VALVE_AREA']) + ' object', True)
		else:
			base.logger.message('start_vac_valve_control UNKNOWN_MACHINE area cannot create vac-valve object', True)

	def start_mod_control(self):
		if self.is_gun_type(base.llrf_type):
			base.mod_control = base.mod_init.physical_GUN_MOD_Controller()
			base.logger.message('start_mod_control created a gun modulator object',True)
		elif base.llrf_type == LLRF_TYPE.L01:
			base.mod_control = base.mod_init.physical_L01_MOD_Controller()
			base.logger.message('start_mod_control created a L01  modulator object', True)
			#base.logger.message('start_mod_control can\'t create a linac modulator object',True)
		else:
			base.logger.message('start_mod_control can\'t create a modulator, unknown llrf_type',True)


	def start_llrf_control(self):
		if base.llrf_type is not LLRF_TYPE.UNKNOWN_TYPE:
			base.llrf_control = base.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, base.llrf_type)
			base.llrfObj = [base.llrf_control.getLLRFObjConstRef()]
			# rationalise the trace names
			base.config.llrf_config['TRACES_TO_SAVE'] = self.get_full_trace_name(base.config.llrf_config['TRACES_TO_SAVE'])
			base.config.breakdown_config['BREAKDOWN_TRACES'] = self.get_full_trace_name(base.config.breakdown_config[ 'BREAKDOWN_TRACES'])
			base.config.llrf_config['MEAN_TRACES'] = self.get_full_trace_name(base.config.llrf_config['MEAN_TRACES'])

			controller_base.llrf_handler= llrf_handler.llrf_handler()
			base.logger.message('start_llrf_control created ' + str(base.llrf_type) + ', llrf_handler and got full trace names:',True)
			base.logger.message('TRACES TO SAVE: '+ ' '.join(base.config.llrf_config['TRACES_TO_SAVE']), True)
			base.logger.message('BREAKDOWN_TRACES:' + ' '.join(base.config.breakdown_config[
																		'BREAKDOWN_TRACES']), True)
		else:
			base.llrf_control = None
			base.logger.message('start_llrf_control can\'t create a llrf_control unknown llrf_type',True)

	# rationalise the trace names
	def get_full_trace_name(self,traces):
		temp = []
		for trace in traces:
			temp.append(base.llrf_control.fullLLRFTraceName(trace))
		return temp



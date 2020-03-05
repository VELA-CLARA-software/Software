from VELA_CLARA_enums import MACHINE_MODE
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_LLRF_Control import LLRF_TYPE
# import VELA_CLARA_LLRF_Control
# import VELA_CLARA_Vac_Valve_Control
# import VELA_CLARA_RF_Modulator_Control
# import VELA_CLARA_RF_Protection_Control
from src.data.config import config_reader
from src.data.logger import logger
import llrf_handler
import datetime
from src.data_monitors.data_monitoring import data_monitoring
from src.base.base import base



class controller_base(base):
	# whoami
	my_name = 'controller_base'

	# Flag for succesful reading of config file
	have_config = False

	# data monitoring calss, spikes, gen_monitors, etc. (NB llrf_handler does LLRF)
	data_monitor = data_monitoring()

	# control/monitor llrf paramters
	llrf_handler = None

	def __init__(self, argv, config_file):
		#
		#super(base, self).__init__()
		# init base class
		base.__init__(self)
		self.argv = argv
		#
		# set then read the config file
		base.config.config_file = config_file
		self.read_config()
		#
		# init data logger
		base.logger = base.logger

	def read_config(self):
		''' Read the config file passed to controller base'''
		# read config
		base.have_config = base.config.get_config()
		# set llr_type (i.e. which cavity to value in reader
		# to continue this MUST NOT BE UNKNOWN
		base.llrf_type = base.config.llrf_type
		self.set_config()
		# if config reading success...
		if base.have_config:

			base.logger.header(self.my_name + ' creating HWC ', True)
			# create required controllers of each possible flavor, depnding on the reuslts from
			# reading config file
			#
			# LLRF
			if bool(base.config.llrf_config):
				self.start_llrf_control()
			## RF Modulator
			if bool(base.config.mod_config):
				self.start_mod_control()
			# vacuum valve
			if bool(base.config.vac_valve_config):
				self.start_vac_valve_control()
			# RF protection
			if bool(base.config.rfprot_config):
				self.start_rf_prot_control()
		else:
			base.logger.header(self.my_name + ' read_config failed sanity checks!!!', True)
		#
		# Log results
		base.logger.header(controller_base.my_name +' has read config',True)

		logdata = ['config file = ' + base.config.config_file, 'dumping data to log']
		for item in base.config.all_config_data:
			logdata.append(''.join(['%s:%s, ' % (key, value) for (key, value) in item.iteritems()]))
		base.logger.message(logdata, True)

		###############################################################################################
		# TODO AJG: replace 'for item in base.config.all_config_data:' with for loop that references
		#  'config.raw_config_data' instead
		logdata_RAW = ['config file = ' + base.config.config_file, 'dumping data to log']
		for item in base.config.raw_config_data:
			logdata_RAW.append(''.join(['%s:%s, ' % (key, value) for (key, value) in item.iteritems()]))
		base.logger.message(logdata, True)
		################################################################################################

	def start_rf_prot_control(self):
		'''Creates the requested RF Protection control object '''
		if self.is_gun_type(base.llrf_type):
			base.prot_control = base.prot_init.physical_Gun_Protection_Controller()
			base.logger.message('start_rf_prot_control created a GUN protection control object',
			                    True)
		elif base.llrf_type == LLRF_TYPE.L01:
			# we don't have a linac protection controller yet ..
			# self.prot_control = base.prot_init.physical_L01_Protection_Controller()
			self.prot_control = None
			base.logger.message('start_rf_prot_control did not create a L01 protection '
			                    'control  object',True)
		else:
			base.logger.message('Unknown LLRF TYPE start_rf_prot_control did not create a '
			                    'protection control object', True)

	def start_vac_valve_control(self):
		'''Creates the requested Vac Valve control object '''
		# if the vac valve area is specified in the config file ...
		try:
			a = base.config.vac_valve_config['VAC_VALVE_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		# create the desired vac-valve controller
		if a == MACHINE_AREA.ALL_VELA_CLARA:
			base.valve_control = base.valve_init.physical_Vac_Valve_Controller()
		elif a == MACHINE_AREA.CLARA_PH1:
			base.valve_control = base.valve_init.physical_CLARA_PH1_Vac_Valve_Controller()
		# sanity check
		if base.valve_control is not None:
			base.logger.message('start_vac_valve_control created ' + str(
					base.config.vac_valve_config['VAC_VALVE_AREA']) + ' object', True)
		else:
			base.logger.message('start_vac_valve_control failed to create vac-valve object', True)

	# START##########################################################################################
	# TODO AJG: Redefine 'start_vac_valve_control' function with 'start_vac_valve_control_ALL'
	#  replacing 'a = base.config.vac_valve_config['VAC_VALVE_AREA']# MAGIC_STRING'
	#  with a = base.config.ALL_config['VAC_VALVE_AREA']# MAGIC_STRING
	#  and base.config.vac_valve_config['VAC_VALVE_AREA']) + ' object', True)
	#  with base.config.ALL_config['VAC_VALVE_AREA']) + ' object', True)

	def start_vac_valve_control_ALL(self):
		'''Creates the requested Vac Valve control object '''
		# if the vac valve area is specified in the config file ...
		try:
			a = base.config.ALL_config['VAC_VALVE_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		# create the desired vac-valve controller
		if a == MACHINE_AREA.ALL_VELA_CLARA:
			base.valve_control = base.valve_init.physical_Vac_Valve_Controller()
		elif a == MACHINE_AREA.CLARA_PH1:
			base.valve_control = base.valve_init.physical_CLARA_PH1_Vac_Valve_Controller()
		# sanity check
		if base.valve_control is not None:
			base.logger.message('start_vac_valve_control created ' + str(
					base.config.ALL_config['VAC_VALVE_AREA']) + ' object', True)
		else:
			base.logger.message('start_vac_valve_control failed to create vac-valve object', True)


	# END###########################################################################################

	def start_mod_control(self):
		'''Creates the requested Modulatro Control object '''
		if self.is_gun_type(base.llrf_type):
			base.mod_control = base.mod_init.physical_GUN_MOD_Controller()
			base.logger.message('start_mod_control created a gun modulator object',True)
		elif base.llrf_type == LLRF_TYPE.L01:
			base.mod_control = base.mod_init.physical_L01_MOD_Controller()
			base.logger.message('start_mod_control created a L01  modulator object', True)
		else:
			base.logger.message('start_mod_control can\'t create a modulator, unknown llrf_type',True)

	def start_llrf_control(self):
		'''Creates the requested LLRF control object '''
		if base.llrf_type is not LLRF_TYPE.UNKNOWN_TYPE:
			base.llrf_control = base.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL, base.llrf_type)
			base.llrfObj = [base.llrf_control.getLLRFObjConstRef()]
			# rationalise the trace names
			base.config.llrf_config['TRACES_TO_SAVE'] = self.get_full_trace_name(
					base.config.llrf_config['TRACES_TO_SAVE'])
			base.config.breakdown_config['BREAKDOWN_TRACES'] = self.get_full_trace_name(
					base.config.breakdown_config[ 'BREAKDOWN_TRACES'])
			base.config.llrf_config['MEAN_TRACES'] = self.get_full_trace_name(
					base.config.llrf_config['MEAN_TRACES'])
			controller_base.llrf_handler= llrf_handler.llrf_handler()
			base.logger.message('start_llrf_control created ' + str(base.llrf_type) +
			                    ', llrf_handler and got full trace names:',True)
			base.logger.message('TRACES TO SAVE: '+ ' '.join(base.config.llrf_config[
				                                                 'TRACES_TO_SAVE']), True)
			base.logger.message('BREAKDOWN_TRACES:' + ' '.join(base.config.breakdown_config[
				                                                   'BREAKDOWN_TRACES']), True)

			base.logger.message('Setting Keep alive to TRUE', True)
			base.llrf_control.setAmpSP(5) # MAGIC_NUMBER
			base.llrf_control.setKeepAlive(True)
			base.llrf_control.keepAlive()
			base.logger.message('Checking canKeepAlive = ' + str(   base.llrf_control.canKeepAlive() ) , True)
		else:
			base.llrf_control = None
			base.logger.message('start_llrf_control can\'t create a llrf_control unknown '
			                    'llrf_type',True)

	# rationalise the trace names
	def get_full_trace_name(self,traces):
		temp = []
		for trace in traces:
			temp.append(base.llrf_control.fullLLRFTraceName(trace))
		return temp



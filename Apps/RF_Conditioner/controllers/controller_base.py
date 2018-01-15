from VELA_CLARA_enums import MACHINE_MODE
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control
import VELA_CLARA_Vac_Valve_Control
import VELA_CLARA_RF_Modulator_Control
import VELA_CLARA_RF_Protection_Control
from data.config_reader import config_reader
import llrf_handler
import datetime


class controller_base(object):
	# whoami
	my_name = 'controller_base'
	#
	# init LLRF Hardware Controllers
	llrf_init = VELA_CLARA_LLRF_Control.init()
	llrf_init.setVerbose()
	llrf_control = None  # LLRF HWC
	llrf_handler = None
	#
	# other attributes that need default values
	# they are used in function below
	llrf_type = LLRF_TYPE.UNKNOWN_TYPE  # what type of RF structure are we conditioning
	# config file read successfully
	have_config = False
	#
	# vaccume valves
	valve_init = VELA_CLARA_Vac_Valve_Control.init()
	valve_init.setQuiet()
	valve_control = None
	#
	mod_init = VELA_CLARA_RF_Modulator_Control.init()
	mod_init.setQuiet()
	mod_control = None
	#
	# RF protection
	prot_init = VELA_CLARA_RF_Protection_Control.init()
	prot_init.setQuiet()
	prot_control = None
	# init attributes
	log_param = None
	vac_param = None
	cavity_temp_param = None
	water_temp_param = None
	mod_param = None
	vac_valve_param = None
	llrf_param = None
	settings = None
	gui_param = None
	breakdown_param = None
	rfprot_param = None
	DC_param = None

	llrfObj = None
	#
	t_start = None

	def __init__(self, argv, config_file):
		self.config_file = config_file
		self.argv = argv
		# read the config file
		self.read_config()

	def start_time(self):
		self.t_start = datetime.datetime.now()

	def seconds_since_start(self):
		return (datetime.datetime.now() - self.t_start).total_seconds()

	def seconds_elapsed(self,val):
		return self.seconds_since_start() >= val

	def read_config(self):
		# create a config reader
		reader = config_reader(self.config_file)
		# read config
		self.have_config = reader.get_config()
		# set llr_typ e(i.e. which cavity to value in reader
		# to continue this MUST NOT BE UNKNOWN
		self.llrf_type = reader.llrf_type
		if self.have_config:
			self.log_param = reader.log_param()
			# vacum spikes monitor

			# self.vac_param = reader.vac_parameter()
			# self.cavity_temp_param = reader.cavity_temp_parameter()
			# self.water_temp_param = reader.water_temp_parameter()
			# self.vac_valve_param = reader.vac_valve_parameter()
			# self.rfprot_param = reader.rfprot_param()
			# self.DC_param = reader.DC_parameter()

			self.mod_param = reader.mod_param()

			if bool(self.mod_param):
				self.start_mod_control()
			if bool(self.vac_valve_param):
				self.start_vac_valve_control()
			if bool(self.rfprot_param):
				self.start_rf_prot_control()


			self.llrf_param = reader.llrf_param()
			self.breakdown_param = reader.breakdown_param()
			if bool(self.llrf_param):
				self.start_llrf_control()
			self.settings = reader.settings()
			self.gui_param = reader.gui_param()

	def is_gun_type(self, type):
		if type == LLRF_TYPE.CLARA_HRRG: return True
		elif type == LLRF_TYPE.CLARA_LRRG: return True
		elif type == LLRF_TYPE.VEAL_HRRG: return True
		elif type == LLRF_TYPE.VELA_LRRG: return True
		else: return False

	def start_rf_prot_control(self):
		if self.is_gun_type(self.llrf_type):
			self.prot_control = self.prot_init.physical_Gun_Protection_Controller()
		elif self.llrf_type == LLRF_TYPE.L01:
			self.prot_control = None
			print 'cannot create rf_prot control object'

	def start_vac_valve_control(self):
		try:
			a = self.vac_valve_param['VAC_VALVE_AREA']# MAGIC_STRING
		except:
			a = MACHINE_AREA.UNKNOWN_AREA
		if a is not MACHINE_AREA.UNKNOWN_AREA:
			self.valve_control = self.valve_init.getVacValveController(MACHINE_MODE.PHYSICAL,a)
		else:
			print 'cannot create vac-valve object'

	def start_mod_control(self):
		if self.is_gun_type(self.llrf_type):
			self.mod_control = self.mod_init.physical_GUN_MOD_Controller()
		elif self.llrf_type == LLRF_TYPE.L01:
			self.mod_control = None
			print 'cannot create modulator control object'

	def start_llrf_control(self):
		if self.llrf_type is not LLRF_TYPE.UNKNOWN_TYPE:
			self.llrf_control = self.llrf_init.getLLRFController(MACHINE_MODE.PHYSICAL,self.llrf_type)
			self.llrfObj = [self.llrf_control.getLLRFObjConstRef()]
			# rationalise the trace names
			self.llrf_param['TRACES_TO_SAVE']   = self.get_full_trace_name(self.llrf_param['TRACES_TO_SAVE'])
			self.breakdown_param['BREAKDOWN_TRACES'] = self.get_full_trace_name(self.breakdown_param['BREAKDOWN_TRACES'])
			self.llrf_handler = llrf_handler.llrf_handler(
				llrf_controller=self.llrf_control,
				llrf_param=self.llrf_param,# MAGIC_STRING
				breakdown_param=self.breakdown_param  # MAGIC_STRING
			)
		else:
			self.llrf_control = None
			print 'cannot create llrf control object'
	# rationalise the trace names
	def get_full_trace_name(self,traces):
		temp = []
		for trace in traces:
			temp.append(self.llrf_control.fullCavityTraceName(trace))
		return temp



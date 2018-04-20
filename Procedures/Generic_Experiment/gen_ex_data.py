# from VELA_CLARA_enums import MACHINE_MODE
# from VELA_CLARA_enums import MACHINE_AREA
# from VELA_CLARA_enums import CONTROLLER_TYPE
import  VELA_CLARA_enums as enum
from collections import namedtuple

# what's required to instantiate a HWC
HWC_data = namedtuple("HWC_data", "type mode area")



class General_Experiment_Data(object):

	# config data
	raw_config_data = None
	# whether the config data is coherent
	config_data_good = False
	# ALL TOP LEVEL KEYWORDS
	GLOBAL  = 'global'
	EXPERIMENT = 'experiment'
	# possible controller types
	GEN_MON = 'gen_mon'
	MAGNETS = 'magnets'
	SCREEN  = 'screen'
	CAMERA  = 'camera'
	LASER   = 'laser'
	LLRF    = 'llrf'
	BPM     = 'bpm'
	all_controllers = [ GEN_MON,
						MAGNETS,
						SCREEN,
						CAMERA,
						LASER,
						LLRF,
						BPM	]
	top_level_kwrds = [GLOBAL,EXPERIMENT ] + all_controllers
	#
	# flags for each top level item in the config file
	# indicating if they exist in the config file
	top_level_kwrds_flags = {}
	[top_level_kwrds_flags.update({x:False}) for x in top_level_kwrds]




	# parse flags, all these flags must go to true for a config file to be
	# parsed
	machine_mode_set = False
	controller_set   = False
	experiment_set   = False
	elements_exist   = False
	# optional flags
	# all these flags may be set after reading a config
	log_file_set = False


	# keywords in global Set
	PROJECT_NAME= 'project_name'
	AUTHOR      = 'author'
	VERSION     = 'version'
	MACHINE_MODE= 'machine_mode'
	WORKING_DIRECTORY  = 'working_directory'
	SCRIPT_LOG_FILE  = 'script_log_file'



	MACHINE_AREA = 'machine_area'
	FIELD_UNITS = 'field_units'
	PHASE_UNITS = 'phase_units'
	AMP_UNITS   = 'amp_units'

	# the top level keywords in config files
	config_keys_1 = [GLOBAL ,MAGNETS, LLRF ,SCREEN, EXPERIMENT]

	# keywords for global level parameters
	config_keys_magnets = [MACHINE_AREA, FIELD_UNITS]
	config_keys_global  = ['project_name', 'author', 'version', 'machine_mode']
	config_keys_llrf    = ['machine_area', 'phase_units', 'amp_units']
	config_keys_screen  = ['machine_area']


	# list of what HWC to create
	# filled after parsing the config file ???
	HWC_data_list = []





	machine_mode = None
	PHYSICAL = 'physical'
	OFFLINE = 'offline'
	VIRTUAL = 'virtual'

	machine_modes ={
		PHYSICAL : enum.MACHINE_MODE.PHYSICAL,
		OFFLINE  : enum.MACHINE_MODE.OFFLINE,
		VIRTUAL  : enum.MACHINE_MODE.VIRTUAL
	}
	machine_modes_inv = {v: k for k, v in machine_modes.iteritems()}

	controller_types ={
		GEN_MON :enum.CONTROLLER_TYPE.GENERAL_MONITOR,
		MAGNETS :enum.CONTROLLER_TYPE.MAGNET,
		SCREEN :enum.CONTROLLER_TYPE.SCREEN,
		CAMERA :enum.CONTROLLER_TYPE.CAMERA_DAQ,
		LASER :enum.CONTROLLER_TYPE.PI_LASER,
		LLRF :enum.CONTROLLER_TYPE.LLRF,
		BPM : enum.CONTROLLER_TYPE.BPM
	}
	controller_types_inv = {v: k for k, v in controller_types.iteritems()}


	UNKNOWN_AREA = "unknown_area"
	CLARA_2_VELA = "clara_2_vela"
	CLARA_INJ    = "clara_inj"
	CLARA_PH1    = "clara_ph1"
	CLARA_S01    = "clara_s01"
	CLARA_S02    = "clara_s02"
	CLARA_L01    = "clara_l01"
	VELA_INJ     = "vela_inj"
	VELA_BA2     = "vela_ba2"
	VELA_BA1     = "vela_ba1"
	RF_GUN     = "rf_gun"
	RF_L01     = "rf_l01"
	USER         = "user"

	machine_areas ={
		UNKNOWN_AREA:enum.MACHINE_AREA.UNKNOWN_AREA,
		CLARA_2_VELA:enum.MACHINE_AREA.CLARA_2_VELA,
		CLARA_INJ   :enum.MACHINE_AREA.CLARA_INJ,
		CLARA_PH1   :enum.MACHINE_AREA.CLARA_PH1,
		CLARA_S01   :enum.MACHINE_AREA.CLARA_S01,
		CLARA_S02   :enum.MACHINE_AREA.CLARA_S02,
		CLARA_L01   :enum.MACHINE_AREA.CLARA_L01,
		VELA_INJ    :enum.MACHINE_AREA.VELA_INJ,
		VELA_BA2    :enum.MACHINE_AREA.VELA_BA2,
		VELA_BA1    :enum.MACHINE_AREA.VELA_BA1,
		RF_GUN      :enum.MACHINE_AREA.RF_GUN,
		RF_L01      :enum.MACHINE_AREA.RF_L01,
		USER        :enum.MACHINE_AREA.USER
	}
	machine_areas_inv = {v: k for k, v in machine_areas.iteritems()}

import VELA_CLARA_enums
from VELA_CLARA_Scope_Control import SCOPE_NAME

class config_reader(object):
	# whoami
	my_name = 'config_reader'
	# config file special characters
	comment = '#'
	end_of_entry = ';'
	string_literal = '"'
	equals = '='
	# parsed config data
	config = {}

	#
	logger = None

	have_config = False
	_config_file = None

	all_config_data = None

	log_config = None
	scope_config = None
	setup_config = None
	zoom_config = None
	gui_config = None

	def __init__(self):
		dummyy = 0

	@property
	def config_file(self):
		return config_reader._config_file
	@config_file.setter
	def config_file(self,value):
		config_reader._config_file = value

	# parse the text file and create config_dict
	def get_config(self):
		# clear existing data
		config_reader.config = {}
		with open(config_reader._config_file) as f:
			content = f.readlines()
			# remove whitespace characters like `\n` at the end of each line
			content = [self.stripWS(x) for x in content]
			# select non-empty strings
			content = [s for s in content if s]
			# remove comment lines
			content = [x for x in content if x[0]!= self.comment ]
			# strip to end of entry
			content = [x.split(self.end_of_entry, 1)[0] for x in content]
			# select key value pairs
			content = [x for x in content if self.equals in x]
			# split on equals
			content = [x.split(self.equals) for x in content]
			# select non-empty pairs
			content = [s for s in content if s[0] and s[1]]
			print content
			[config_reader.config.update({x[0]: x[1]}) for x in content]
		# at  minimum the  config needs to give a llf_type
		try:
			config_reader.scope_type = self.get_scope_type(config_reader.config['SCOPE_NAME'])
		except:
			return False
		self.log_param()
		self.scope_param()
		self.setup_param()
		self.zoom_param()
		self.gui_param()

		print(config_reader.my_name + ' read input from ' + str(config_reader.config_file) )

		config_reader.all_config_data = [config_reader.log_config,
										 config_reader.gui_config,
										 config_reader.setup_config,
										 config_reader.zoom_config,
										 config_reader.scope_config]
		return self.sanity_checks()

	def sanity_checks(self):
		# if self.scope_type == SCOPE_NAME.UNKNOWN_TYPE:
			# return False
		return True

	# strip whitespace except in string literal
	def stripWS(self,txt):
		a = self.string_literal.join(it if i % 2 else ''.join(it.split())for i, it in enumerate(txt.split(self.string_literal)))
		return a.replace("\"", "")

	# check _config dict for keys and put hits in a new dict
	def get_part_dict(self,keys):
		r = {}
		[r.update({key:config_reader.config[key]}) for key in keys if key in config_reader.config ]
		return r
	#//mfw Cancer below\\
	#//we must assume value type\\
	def get_param_dict(self,string_param=[],int_param=[],float_param=[],area_param=[]):
		r = {}
		for item in string_param:
			try:
				r.update({item: config_reader.config[item]})
			except:
				print(self.my_name," FAILED to Find, ",item)
		for item in int_param:
			try:
				r.update({item: int(config_reader.config[item])})
			except:
				print(self.my_name," FAILED to Find, ",item)
		for item in float_param:
			try:
				r.update({item: float(config_reader.config[item])})
			except:
				print(self.my_name," FAILED to Find, ",item)
		for item in area_param:
			try:
				r.update({item: self.get_machine_area(config_reader.config[item])})
			except:
				print(self.my_name, " FAILED to Find, ", item)
		# for item in type_param:
		#	  try:
		#		  r.update({item: self.get_llrf_type(config_reader.config[item])})
		#		  self.llrf_type = r[item]
		#	  except:
		#		  print(self.my_name," FAILED to Find, ",item)
		# for item in monitor_param:
		#	  try:
		#		  r.update({item: self.get_traces_to_monitor(config_reader.config[item])})
		#	  except:
		#		  print(self.my_name, " FAILED to Find, ", item)
		# for k, v in r.iteritems():
		#	  print k, v
		return r
	# neater but not type for values
	# def get_vac_parameter_NO_TYPE(self):
	#	  vac_keys = ['VAC_PV','VAC_SPIKE_DELTA','VAC_DECAY_MODE','VAC_SPIKE_DECAY_LEVEL','VAC_SPIKE_DECAY_LEVEL'
	#				  ,'VAC_SPIKE_DECAY_TIME','VAC_NUM_SAMPLES_TO_AVERAGE']
	#	  vac_param = self.get_part_dict(vac_keys)
	#	  for k, v in vac_param.iteritems():
	#		  print k, v
	#	  return config_reader.vac_param

	def log_param(self):
		string_param = ['LOG_FILENAME','LOG_DIRECTORY','DATA_LOG_FILENAME']
		int_param = ['DATA_LOG_TIME']
		config_reader.log_config = self.get_param_dict(string_param=string_param,int_param=int_param)
		return config_reader.log_config

	def scope_param(self):
		int_param=['TIMEBASE','SCOPE_CHECK_TIME']
		string_param = ['C1_DIAG_TYPE','C2_DIAG_TYPE','C3_DIAG_TYPE','C4_DIAG_TYPE']
		area_param = ['SCOPE_AREA']
		# monitor_param=['TRACES_TO_SAVE','MEASURE_TYPE']
		config_reader.scope_config = self.get_param_dict(string_param=string_param,int_param=int_param,area_param=area_param)
		return config_reader.scope_config

	def setup_param(self):
		# type_param=['TRIGGER_SOURCE']
		float_param=['HOR_OFFSET','HOR_SCALE',
					 'C1_VER_SCALE','C2_VER_SCALE','C3_VER_SCALE','C4_VER_SCALE',
					 'C1_VER_OFFSET','C2_VER_OFFSET','C3_VER_OFFSET','C4_VER_OFFSET']
		int_param=['MAX_SAMPLES','NUM_POINTS','SAMPLE_RATE',
				   'C1_AVERAGE_SWEEPS','C2_AVERAGE_SWEEPS','C3_AVERAGE_SWEEPS','C4_AVERAGE_SWEEPS']
		string_param = ['C1_COUPLING','C2_COUPLING','C3_COUPLING','C4_COUPLING','TRIGGER_SOURCE']
		config_reader.scope_config = self.get_param_dict(string_param=string_param,int_param=int_param,
								   float_param=float_param)
		return config_reader.scope_config

	def zoom_param(self):
		float_param=['Z1_VER_SCALE','Z2_VER_SCALE','Z3_VER_SCALE','Z4_VER_SCALE',
					 'Z1_VER_OFFSET','Z2_VER_OFFSET','Z3_VER_OFFSET','Z4_VER_OFFSET',
					 'Z1_VER_CENTER', 'Z2_VER_CENTER', 'Z3_VER_CENTER', 'Z4_VER_CENTER',
					 'Z1_HOR_SCALE', 'Z2_HOR_SCALE', 'Z3_HOR_SCALE', 'Z4_HOR_SCALE',
					 'Z1_HOR_OFFSET', 'Z2_HOR_OFFSET', 'Z3_HOR_OFFSET', 'Z4_HOR_OFFSET',
					 'Z1_HOR_CENTER', 'Z2_HOR_CENTER', 'Z3_HOR_CENTER', 'Z4_HOR_CENTER']
		int_param=['Z1_VER_ZOOM','Z2_VER_ZOOM','Z3_VER_ZOOM','Z4_VER_ZOOM',
				   'Z1_HOR_ZOOM', 'Z2_HOR_ZOOM', 'Z3_HOR_ZOOM', 'Z4_HOR_ZOOM']
		config_reader.scope_config = self.get_param_dict(int_param=int_param,float_param=float_param)
		return config_reader.scope_config

	def gui_param(self):
		int_param=['GUI_UPDATE_TIME']
		config_reader.gui_config = self.get_param_dict(int_param=int_param)
		return config_reader.gui_config

	def settings(self):
		r ={}
		return r

	def get_bool(self,text):
		if text == 'TRUE':
			return True
		elif text == 'FALSE':
			return False

	def get_scope_type(self,text):
		if text == "CLARASCOPE01":
			return SCOPE_NAME.CLARASCOPE01
		elif text == 'VELASCOPE02':
			return SCOPE_NAME.VELASCOPE02
		else:
			return SCOPE_NAME.UNKNOWN_TYPE

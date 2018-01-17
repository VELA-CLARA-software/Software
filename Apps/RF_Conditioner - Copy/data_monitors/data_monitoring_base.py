from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_General_Monitor
import vac_valve_monitor
import value_monitor
import spike_monitor
import modulator_monitor
import outside_mask_trace_monitor
import rf_protection_monitor
import llrf_simple_param_monitor
import data.rf_condition_data_base as dat


class data_monitoring_base(object):
	#whomai
	my_name = 'data_monitoring_base'
	# we know there will be some LLRF involved
	llrf_type = LLRF_TYPE.UNKNOWN_TYPE
	#
	# general monitoring for parameters with no controller
	gen_mon = VELA_CLARA_General_Monitor.init()
	# we can make some reasonable guesses as to what will be
	# monitored from gen_mon
	# every key from gen_mon will be stored here
	gen_mon_keys = {}
	# we can make some reasonable guesses as to what will be included
	vac_id = 'VAC_ID'
	dc_id = 'DC_ID'
	mod_id = 'MOD_ID'
	cavity_temp_id = 'CAVITY_TEMP_ID'
	water_temp_id = 'WATER_TEMP_ID'
	all_id = [vac_id, dc_id, mod_id, cavity_temp_id, water_temp_id]
	[gen_mon_keys.update({x: None}) for x in all_id]
	# explicit flags for possible monitors & monitors states
	# these are used to determine if monitoring these items is happening
	# they're NOT for defining vacuum good, / bad etc.
	# we use the same keys as the data.dict etc

	llrf_simple_monitoring = "llrf_simple_monitoring"
	cavity_temp_monitoring = "cavity_temp_monitoring"
	water_temp_monitoring = "water_temp_monitoring"
	is_monitoring = {}
	all_monitors = [llrf_simple_monitoring,
	                cavity_temp_monitoring,
	                water_temp_monitoring,
	                dat.vac_valve_status,
	                dat.modulator_state,
	                dat.breakdown_status,
	                dat.rev_power_spike_status,
	                dat.vac_spike_status,
	                dat.rfprot_state,
	                dat.DC_spike_status]
	[is_monitoring.update({x: False}) for x in all_monitors]
	# these monitors have no bearing on the conditioning main_loop
	passive_monitors = [llrf_simple_monitoring,
					cavity_temp_monitoring,
					water_temp_monitoring,
		]

	#
	#all poossible monitors
	vacuum_monitor = None
	DC_monitor = None
	modulator_monitor = None
	cavity_temp_monitor = None
	outside_mask_trace_monitor = None
	llrf_simple_param_monitor = None
	water_temp_monitor = None
	rf_prot_monitor = None
	vac_valve_monitor = None
	def __init__(self, data):
		self.data = data


	def start_monitors(self,
	                   prot_control,
	                   rfprot_param,
	                   valve_control,
	                   vac_valve_param,
	                   mod_control,
	                   mod_param,
	                   cavity_temp_param,
	                   water_temp_param,
	                   vac_param,
	                   llrf_control,
	                   llrf_param,
	                   breakdown_param,
			           log_param,
			           DC_param
	                ):
		if prot_control:
			self.rfprot_monitor(prot_control,rfprot_param)
		if valve_control:
			self.start_valve_monitor(valve_control,vac_valve_param)
		if mod_control:
			self.start_mod_monitor(mod_control,mod_param)
		if bool(cavity_temp_param):
			self.start_cavity_temp_monitor(cavity_temp_param)
		if bool(water_temp_param):
			self.start_water_temp_monitor(water_temp_param)
		if bool(vac_param):
			self.start_vac_monitor(llrf_controller=llrf_control, vac_param=vac_param)
		if bool(DC_param):
			self.start_DC_monitor(llrf_controller=llrf_control, DC_param=DC_param)
		if bool(llrf_param):
			self.start_llrf_simple_param_monitor(llrf_control,llrf_param)
			if bool(log_param):
				self.start_outside_mask_trace__monitor(llrf_control,llrf_param,log_param,breakdown_param)

	def start_vac_monitor(self, llrf_controller, vac_param):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.vac_id, vac_param.get('VAC_PV')):  # MAGIC_STRING
			vac_param[self.vac_id] = self.gen_mon_keys[self.vac_id]
			# Vacuum monitoring requires a vacuum PV
			self.vacuum_monitor = spike_monitor.spike_monitor(
				llrf_control=llrf_controller,
				gen_mon=self.gen_mon,
				settings_dict=vac_param,
				id_key=self.vac_id,
				decay_mode_key='VAC_DECAY_MODE',  # MAGIC_STRING
				spike_delta_key='VAC_SPIKE_DELTA',  # MAGIC_STRING
				spike_decay_level_key='VAC_SPIKE_DECAY_LEVEL',  # MAGIC_STRING
				spike_decay_time_key='VAC_SPIKE_DECAY_TIME',  # MAGIC_STRING
				num_samples_to_average_key='VAC_NUM_SAMPLES_TO_AVERAGE',  # MAGIC_STRING
				update_time_key='VAC_CHECK_TIME',  # MAGIC_STRING
				data_dict=self.data.values,
				data_dict_val_key=dat.vac_level,
				data_dict_state_key=dat.vac_spike_status,
				should_drop_amp = 'VAC_SHOULD_DROP_AMP',  # MAGIC_STRING
				amp_drop_value = 'VAC_SPIKE_AMP_DROP'  # MAGIC_STRING

			)  # MAGIC_STRING
			self.is_monitoring[dat.vac_spike_status] = self.vacuum_monitor.set_success
			self.vacuum_monitor.my_name = 'vacuum_monitor'  # MAGIC_STRING
		return self.vacuum_monitor.set_success

	def start_DC_monitor(self, llrf_controller,DC_param):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.dc_id, DC_param.get('DC_PV')):  # MAGIC_STRING
			DC_param[self.dc_id] = self.gen_mon_keys[self.dc_id]
			# Vacuum monitoring requires a vacuum PV
			self.DC_monitor = spike_monitor.spike_monitor(
				llrf_control=llrf_controller,
				gen_mon=self.gen_mon,
				settings_dict=DC_param,
				id_key=self.dc_id,
				decay_mode_key='DC_DECAY_MODE',  # MAGIC_STRING
				spike_delta_key='DC_SPIKE_DELTA',  # MAGIC_STRING
				spike_decay_level_key='DC_SPIKE_DECAY_LEVEL',  # MAGIC_STRING
				spike_decay_time_key='DC_SPIKE_DECAY_TIME',  # MAGIC_STRING
				num_samples_to_average_key='DC_NUM_SAMPLES_TO_AVERAGE',  # MAGIC_STRING
				update_time_key='DC_CHECK_TIME',  # MAGIC_STRING
				data_dict=self.data.values,
				data_dict_val_key=dat.DC_level,
				data_dict_state_key=dat.DC_spike_status,
				should_drop_amp='DC_SHOULD_DROP_AMP', #MAGIC_STRING
				amp_drop_value= 'DC_SPIKE_AMP_DROP' #MAGIC_STRING
			)  # MAGIC_STRING
			self.is_monitoring[dat.DC_spike_status] = self.DC_monitor.set_success
			self.DC_monitor.my_name = 'DC_monitor'  # MAGIC_STRING
		return self.DC_monitor.set_success

	def rfprot_monitor(self,controller,prot_param):
		self.rf_prot_monitor = rf_protection_monitor.rf_protection_monitor(
			controller =controller,
			data_dict=self.data.values,
			data_dict_key=dat.rfprot_state,
			llrf_type=self.llrf_type,
			update_time=prot_param['RF_PROT_CHECK_TIME']#MAGIC_STRING
		)
		self.is_monitoring[dat.rfprot_state] = self.rf_prot_monitor.set_success
		return self.rf_prot_monitor.set_success

	def start_valve_monitor(self, controller, vac_valve_param):
		self.vac_valve_monitor = vac_valve_monitor.vac_valve_monitor(
			llrf_type=self.llrf_type,
			controller=controller,
			data_dict=self.data.values,
			data_dict_key=dat.vac_valve_status,
			update_time=vac_valve_param['VAC_VALVE_CHECK_TIME'],#MAGIC_STRING
			valve=vac_valve_param['VAC_VALVE']#MAGIC_STRING
		)
		self.is_monitoring[dat.vac_valve_status] =self.vac_valve_monitor.set_success
		return self.vac_valve_monitor.set_success

	def start_mod_monitor(self, controller, mod_param):
		self.modulator_monitor = modulator_monitor.modulator_monitor(
			llrf_type=self.llrf_type,
			controller=controller,
			data_dict=self.data.values,
			data_dict_key=dat.modulator_state,
			update_time=mod_param['MOD_CHECK_TIME'],#MAGIC_STRING
		)
		self.is_monitoring[dat.modulator_state] = self.modulator_monitor.set_success
		return self.modulator_monitor.set_success

	def start_cavity_temp_monitor(self, cavity_temp_param):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.cavity_temp_id, cavity_temp_param.get('CAVITY_TEMPERATURE_PV')):  # MAGIC_STRING
			cavity_temp_param[self.cavity_temp_id] = self.gen_mon_keys[self.cavity_temp_id]
			self.cavity_temp_monitor = value_monitor.value_monitor(
				gen_mon=self.gen_mon,
				settings_dict=cavity_temp_param,
				id_key=self.cavity_temp_id,
				data_dict=self.data.values,
				data_dict_key=dat.cav_temp,
				update_time=cavity_temp_param['CAVITY_TEMPERATURE_CHECK_TIME']  # MAGIC_STRING
			)
			self.cavity_temp_monitor.my_name = 'cavity_temp_monitor'  # MAGIC_STRING
			self.is_monitoring[self.cavity_temp_monitoring] = self.cavity_temp_monitor.set_success
		return self.is_monitoring[self.cavity_temp_monitoring]

	def start_water_temp_monitor(self, water_temp_param):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.water_temp_id, water_temp_param.get('WATER_TEMPERATURE_PV')):  # MAGIC_STRING
			water_temp_param[self.water_temp_id] = self.gen_mon_keys[self.water_temp_id]
			self.water_temp_monitor = value_monitor.value_monitor(
				gen_mon=self.gen_mon,
				settings_dict=water_temp_param,
				id_key=self.water_temp_id,
				data_dict=self.data.values,
				data_dict_key=dat.water_temp,
				update_time=water_temp_param['WATER_TEMPERATURE_CHECK_TIME']  # MAGIC_STRING
			)
			self.water_temp_monitor.my_name = 'water_temp_monitor'  # MAGIC_STRING
			self.is_monitoring[self.water_temp_monitoring] = self.water_temp_monitor.set_success
		return self.is_monitoring[self.water_temp_monitoring]

	def start_llrf_simple_param_monitor(self, llrf_controller, llrf_param):
		self.llrf_simple_param_monitor = llrf_simple_param_monitor.llrf_simple_param_monitor(
			llrf_controller=llrf_controller,
			data_dict=self.data.values,
			monitored_traces=llrf_param['TRACES_TO_SAVE'],  # MAGIC_STRING
			update_time=llrf_param['LLRF_CHECK_TIME']  # MAGIC_STRING
		)
		self.is_monitoring[self.llrf_simple_monitoring] = self.llrf_simple_param_monitor.set_success
		return self.is_monitoring[self.llrf_simple_monitoring]

	def start_outside_mask_trace__monitor(self, llrf_controller, llrf_param, log_param, breakdown_param):
		self.outside_mask_trace_monitor = outside_mask_trace_monitor.outside_mask_trace_monitor(
				llrf_controller=llrf_controller,
				data_dict=self.data.values,
				llrf_param=llrf_param,
				log_param=log_param,
				breakdown_param=breakdown_param
			)
		self.is_monitoring[dat.breakdown_status] = self.outside_mask_trace_monitor.set_success
		self.is_monitoring[dat.rev_power_spike_status] = self.outside_mask_trace_monitor.set_success
		return self.outside_mask_trace_monitor.set_success

	# connect to process variable pv
	def connectPV(self, pvKey, pvValue):
		connected = False
		if pvValue is not None:
			id = self.gen_mon.connectPV(pvValue)
			if id != 'FAILED':
				connected = True
				print(self.my_name + ' Connected to PV = ', pvValue, ' with ID = ', id, ' acquiring data')
				self.gen_mon_keys[pvKey] = id
			else:
				print(self.my_name + ' Failed to connect to PV = ', pvValue, ' ID = ', id, ' NOT acquiring data')
		else:
			print(self.my_name + 'connectPV passed empty PV')
		return connected
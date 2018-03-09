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
from base.base import base

class data_monitoring_base(base):
	#whomai
	my_name = 'data_monitoring_base'
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
	sol_id = 'WATER_TEMP_ID'
	all_id = [vac_id, dc_id, mod_id, cavity_temp_id, water_temp_id,sol_id]
	[gen_mon_keys.update({x: None}) for x in all_id]
	# explicit flags for possible monitors & monitors states
	# these are used to determine if monitoring these items is happening
	# they're NOT for defining vacuum good, / bad etc.
	# we use the same keys as the data.dict etc

	llrf_simple_monitoring = "llrf_simple_monitoring"
	cavity_temp_monitoring = "cavity_temp_monitoring"
	water_temp_monitoring = "water_temp_monitoring"
	sol_monitoring = "sol_monitoring "
	is_monitoring = {}
	all_monitors = [llrf_simple_monitoring,
	                cavity_temp_monitoring,
	                water_temp_monitoring,
	                dat.vac_valve_status,
	                dat.modulator_state,
	                dat.breakdown_status,
	                dat.rev_power_spike_count,
	                dat.vac_spike_status,
	                dat.rfprot_state,
	                dat.DC_spike_status,
					sol_monitoring]
	[is_monitoring.update({x: False}) for x in all_monitors]
	# these monitors have no bearing on the conditioning main_loop
	passive_monitors = [llrf_simple_monitoring,
					cavity_temp_monitoring,
					water_temp_monitoring,
						sol_monitoring
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
	sol_monitor = None
	def __init__(self):
		base.__init__(self)

	def start_monitors(self):
		self.logger.header(self.my_name + ' start_monitors ')
		##
		if base.config.rfprot_config:
			if self.rfprot_monitor():
				self.logger.message('Monitoring RF-PROTECTION', True)
			else:
				self.logger.message('Not monitoring RF-PROTECTION rfprot_monitor failed', True)
		else:
			self.logger.message('Not monitoring RF-PROTECTION No config data',True)
		##
		if base.config.vac_valve_config:
			if self.start_valve_monitor():
				self.logger.message('Monitoring VAC-VALVE', True)
			else:
				self.logger.message('Not monitoring VAC-VALVE valve_monitor failed', True)
		else:
			self.logger.message('Not monitoring VAC-VALVE No config data',True)
		##
		if base.config.mod_config:
			if self.start_mod_monitor():
				self.logger.message('Monitoring MODULATOR', True)
			else:
				self.logger.message('Not monitoring VAC-VALVE mod_monitor failed', True)
		else:
			self.logger.message('Not monitoring VAC-VALVE No config data',True)
		##
		if bool(base.config.cavity_temp_config):
			if self.start_cavity_temp_monitor():
				self.logger.message('Monitoring CAVITY TEMPERATURE', True)
			else:
				self.logger.message('Not monitoring CAVITY TEMPERATURE cavity_temp_monitor failed', True)
		else:
			self.logger.message('Not monitoring CAVITY TEMPERATURE No config data',True)
		##
		if bool(base.config.water_temp_config):
			if self.start_water_temp_monitor():
				self.logger.message('Monitoring WATER TEMP', True)
			else:
				self.logger.message('Not monitoring WATER TEMP valve_monitor failed', True)
		else:
			self.logger.message('Not monitoring WATER TEMP No config data',True)
		##
		if bool(base.config.sol_config):
			if self.start_sol_monitor():
				self.logger.message('Monitoring SOLENOID READI', True)
			else:
				self.logger.message('Not monitoring SOLENOID READI start_sol_monitor failed', True)
		else:
			self.logger.message('Not monitoring SOLENOID READI No config data',True)
		if bool(base.config.vac_config):
			if self.start_vac_monitor():
				self.logger.message('Monitoring VACUUM', True)
			else:
				self.logger.message('Not monitoring VACUUM vac_monitor failed', True)
		else:
			self.logger.message('Not monitoring VACUUM  No config data',True)
		##
		if bool(base.config.DC_config):
			if self.start_DC_monitor():
				self.logger.message('Monitoring DC', True)
			else:
				self.logger.message('Not monitoring DC dc_monitor failed', True)
		else:
			self.logger.message('Not monitoring DC No config data',True)

		if bool(base.config.llrf_config):
			if self.start_llrf_simple_param_monitor():
				self.logger.message('Monitoring llrf', True)
			else:
				self.logger.message('Not monitoring llrf llrf_monitor failed', True)
			if bool(base.config.log_config):
				if self.start_outside_mask_trace__monitor():
					self.logger.message('Monitoring outside_masks', True)
				else:
					self.logger.message('Not monitoring outside_masks outside_mask_trace_monitor failed', True)
			else:
				self.logger.message('Not monitoring outside_masks No config data', True)
		else:
			self.logger.message('Not monitoring llrf No config data', True)


	def start_vac_monitor(self):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.vac_id, base.config.vac_config.get('VAC_PV')):  # MAGIC_STRING
			base.config.vac_config[self.vac_id] = self.gen_mon_keys[self.vac_id]
			# Vacuum monitoring requires a vacuum PV
			data_monitoring_base.vacuum_monitor = spike_monitor.spike_monitor(
				gen_mon=self.gen_mon,
				#settings_dict=base.config.vac_config,
				id_key=self.gen_mon_keys[self.vac_id],
				decay_mode=base.config.vac_config['VAC_DECAY_MODE'],  # MAGIC_STRING
				spike_delta=base.config.vac_config['VAC_SPIKE_DELTA'],  # MAGIC_STRING
				spike_decay_level=base.config.vac_config['VAC_SPIKE_DECAY_LEVEL'],  # MAGIC_STRING
				spike_decay_time=base.config.vac_config['VAC_SPIKE_DECAY_TIME'],  # MAGIC_STRING
				num_samples_to_average=base.config.vac_config['VAC_NUM_SAMPLES_TO_AVERAGE'],  # MAGIC_STRING
				update_time=base.config.vac_config['VAC_CHECK_TIME'],  # MAGIC_STRING
				data_dict_val_key=dat.vac_level,
				data_dict_state_key=dat.vac_spike_status,
				should_drop_amp = base.config.vac_config['VAC_SHOULD_DROP_AMP'],  # MAGIC_STRING
				amp_drop_value = base.config.vac_config['VAC_SPIKE_AMP_DROP'] , # MAGIC_STRING
				my_name='vac_spike_monitor',
                min_cooldown_time=base.config.breakdown_config['OUTSIDE_MASK_COOLDOWN_TIME'], # MAGIC_STRING
				max_level=base.config.vac_config['VAC_MAX_LEVEL'], # MAGIC_STRING
				max_drop_amp=base.config.vac_config['VAC_MAX_AMP_DROP'] # MAGIC_STRING
			)  # MAGIC_STRING
			data_monitoring_base.is_monitoring[dat.vac_spike_status] = data_monitoring_base.vacuum_monitor.set_success
		return data_monitoring_base.vacuum_monitor.set_success

	def start_DC_monitor(self):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.dc_id, base.config.DC_config.get('DC_PV')):  # MAGIC_STRING
			base.config.DC_config[self.dc_id] = self.gen_mon_keys[self.dc_id]
			# Vacuum monitoring requires a vacuum PV
			data_monitoring_base.DC_monitor = spike_monitor.spike_monitor(
				gen_mon=self.gen_mon,
				#settings_dict=base.config.DC_config,
				id_key=self.gen_mon_keys[self.dc_id],
				decay_mode=base.config.DC_config['DC_DECAY_MODE'],  # MAGIC_STRING
				spike_delta=base.config.DC_config['DC_SPIKE_DELTA'],  # MAGIC_STRING
				spike_decay_level=base.config.DC_config['DC_SPIKE_DECAY_LEVEL'],  # MAGIC_STRING
				spike_decay_time=base.config.DC_config['DC_SPIKE_DECAY_TIME'],  # MAGIC_STRING
				num_samples_to_average=base.config.DC_config['DC_NUM_SAMPLES_TO_AVERAGE'],  # MAGIC_STRING
				update_time=base.config.DC_config['DC_CHECK_TIME'],  # MAGIC_STRING
				data_dict_val_key=dat.DC_level,
				data_dict_state_key=dat.DC_spike_status,
				should_drop_amp=base.config.DC_config['DC_SHOULD_DROP_AMP'], #MAGIC_STRING
				amp_drop_value= base.config.DC_config['DC_SPIKE_AMP_DROP'], #MAGIC_STRING
				my_name = 'dc_spike_monitor',
				min_cooldown_time=base.config.breakdown_config['OUTSIDE_MASK_COOLDOWN_TIME']  # MAGIC_STRING
			)  # MAGIC_STRING
			data_monitoring_base.is_monitoring[dat.DC_spike_status] = data_monitoring_base.DC_monitor.set_success
			data_monitoring_base.DC_monitor.my_name = 'DC_monitor'  # MAGIC_STRING
		return data_monitoring_base.DC_monitor.set_success

	def rfprot_monitor(self):
		data_monitoring_base.rf_prot_monitor = rf_protection_monitor.rf_protection_monitor()
		data_monitoring_base.is_monitoring[dat.rfprot_state] = data_monitoring_base.rf_prot_monitor.set_success
		return data_monitoring_base.rf_prot_monitor.set_success

	def start_valve_monitor(self):
		data_monitoring_base.vac_valve_monitor = vac_valve_monitor.vac_valve_monitor()
		data_monitoring_base.is_monitoring[dat.vac_valve_status] =data_monitoring_base.vac_valve_monitor.set_success
		return data_monitoring_base.vac_valve_monitor.set_success

	def start_mod_monitor(self):
		data_monitoring_base.modulator_monitor = modulator_monitor.modulator_monitor()
		data_monitoring_base.is_monitoring[dat.modulator_state] = data_monitoring_base.modulator_monitor.set_success
		return data_monitoring_base.modulator_monitor.set_success

	def start_cavity_temp_monitor(self):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.cavity_temp_id, base.config.cavity_temp_config.get('CAVITY_TEMPERATURE_PV')):  #
			# MAGIC_STRING
			#base.config.cavity_temp_config[self.cavity_temp_id] = data_monitoring_base.gen_mon_keys[
			# data_monitoring_base.cavity_temp_id]
			data_monitoring_base.cavity_temp_monitor = value_monitor.value_monitor(
				gen_mon=self.gen_mon,
				id_key=data_monitoring_base.gen_mon_keys[data_monitoring_base.cavity_temp_id],
				data_dict_key=dat.cav_temp,
				update_time=base.config.cavity_temp_config['CAVITY_TEMPERATURE_CHECK_TIME'],  # MAGIC_STRING
				my_name='cavity_temp_monitor'
			)
			data_monitoring_base.is_monitoring[data_monitoring_base.cavity_temp_monitoring] = data_monitoring_base.cavity_temp_monitor.set_success
		return data_monitoring_base.is_monitoring[data_monitoring_base.cavity_temp_monitoring]

	def start_water_temp_monitor(self):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.water_temp_id, base.config.water_temp_config.get('WATER_TEMPERATURE_PV')):  #
			# MAGIC_STRING
			base.config.water_temp_config[self.water_temp_id] = self.gen_mon_keys[self.water_temp_id]
			data_monitoring_base.water_temp_monitor = value_monitor.value_monitor(
				gen_mon=self.gen_mon,
				id_key=self.gen_mon_keys[self.water_temp_id],
				data_dict_key=dat.water_temp,
				update_time=base.config.water_temp_config['WATER_TEMPERATURE_CHECK_TIME'],  # MAGIC_STRING
				my_name='water_temp_monitor'
			)
			data_monitoring_base.is_monitoring[data_monitoring_base.water_temp_monitoring] = self.water_temp_monitor.set_success
		return data_monitoring_base.is_monitoring[data_monitoring_base.water_temp_monitoring]

	def start_sol_monitor(self):
		# NOT HAPPY ABOUT HARDCODED STRINGS...
		if self.connectPV(self.sol_id, base.config.sol_config.get('SOL_PV')):  #
			# MAGIC_STRING
			base.config.sol_config[self.sol_id] = self.gen_mon_keys[self.sol_id]
			data_monitoring_base.sol_monitor = value_monitor.value_monitor(
				gen_mon=self.gen_mon,
				id_key=self.gen_mon_keys[self.sol_id],
				data_dict_key=dat.sol_value,
				update_time=base.config.sol_config['SOL_CHECK_TIME'],  # MAGIC_STRING
				my_name='solenoid_monitor'
			)
			data_monitoring_base.is_monitoring[data_monitoring_base.sol_monitoring] = self.sol_monitor.set_success
		return data_monitoring_base.is_monitoring[data_monitoring_base.sol_monitoring]


	def start_llrf_simple_param_monitor(self):
		data_monitoring_base.llrf_simple_param_monitor = llrf_simple_param_monitor.llrf_simple_param_monitor()
		data_monitoring_base.is_monitoring[data_monitoring_base.llrf_simple_monitoring] = data_monitoring_base.llrf_simple_param_monitor.set_success
		return data_monitoring_base.is_monitoring[data_monitoring_base.llrf_simple_monitoring]

	def start_outside_mask_trace__monitor(self):
		data_monitoring_base.outside_mask_trace_monitor = outside_mask_trace_monitor.outside_mask_trace_monitor()
		data_monitoring_base.is_monitoring[dat.breakdown_status] = data_monitoring_base.outside_mask_trace_monitor.set_success
		data_monitoring_base.is_monitoring[dat.rev_power_spike_count] = data_monitoring_base.outside_mask_trace_monitor.set_success
		return data_monitoring_base.outside_mask_trace_monitor.set_success

	# connect to process variable pv
	def connectPV(self, pvKey, pvValue):
		connected = False
		if pvValue is not None:
			id = self.gen_mon.connectPV(pvValue)
			if id != 'FAILED':
				connected = True
				self.logger.message(self.my_name + ' Connected to PV = ' + str(pvValue) + ' with ID = ' + str(id) + ' acquiring data',True)
				self.gen_mon_keys[pvKey] = id
			else:
				self.logger.message(self.my_name + ' Failed to connect to PV = ' + str(pvValue) + ' ID = ' + str(id) + ' NOT acquiring data',True)
		else:
			self.logger.message(self.my_name + 'connectPV passed empty PV')
		return connected
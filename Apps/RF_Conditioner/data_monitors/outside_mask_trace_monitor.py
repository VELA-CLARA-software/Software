from  monitor import monitor
import data.rf_condition_data_base as dat
import os
import datetime
#from VELA_CLARA_enums import STATE
from data.state import state
import time



class outside_mask_trace_monitor(monitor):
	#whoami
	my_name = 'outside_mask_trace_monitor'
	outside_mask_trace_count = 0
	previous_outside_mask_trace_count = 0
	forward_power_data = []
	reverse_power_data = []
	probe_power_data = []
	CFP = None
	CRP = None
	CPP = None

	# this is the 'zero' value (i.e. subtracted from pulse count to give event_pulse_count
	event_pulse_count_zero = 0

	def __init__(self):
		# init base-ccaget lass
		monitor.__init__(self,timed_cooldown=True)
		# breakdown param
		#self.breakdown_config = outside_mask_trace_monitor.config.breakdown_config

		# log traces to monitor
		# str=[]
		# for trace in monitor.config.llrf_config['TRACES_TO_SAVE']:
		# 	str.append(self.my_name + ' has ' + trace)
		# monitor.logger.message(str,True)

		self.timer.timeout.connect(self.update_value)
		self.timer.start(monitor.config.breakdown_config['OUTSIDE_MASK_CHECK_TIME'])
		monitor.data.values[dat.breakdown_status] = state.GOOD
		#monitor.data.values[dat.breakdown_rate_aim] = llrf_param['BREAKDOWN_RATE_AIM']
		self.data_to_collect = []

	def reset_event_pulse_count(self):
		self.event_pulse_count_zero = monitor.data.values[dat.pulse_count]
		monitor.data.values[dat.event_pulse_count] = 0
		monitor.logger.header(self.my_name +' reset_event_pulse_count')
		monitor.logger.message('event_pulse_count_zero = ' +str(self.event_pulse_count_zero ))

	def cooldown_function(self):
		monitor.logger.message(self.my_name + ', cool down ended')
		self.incool_down = False
		monitor.data.values[dat.breakdown_status] = state.GOOD

	def update_value(self):
		monitor.data.values[dat.pulse_count] = monitor.llrfObj[0].activePulseCount
		monitor.data.values[dat.event_pulse_count] = monitor.data.values[dat.pulse_count] - self.event_pulse_count_zero
		monitor.data.values[dat.elapsed_time] = monitor.llrf_control.elapsedTime()
		monitor.data.values[dat.num_outside_mask_traces] = monitor.llrfObj[0].num_outside_mask_traces
		_count = monitor.llrfObj[0].num_outside_mask_traces

		if _count > self.previous_outside_mask_trace_count:
			monitor.logger.header(self.my_name + ' NEW OUTSIDE MASK TRACE DETECTED', True)
			self.get_new_outside_mask_traces(_count)
			self.previous_outside_mask_trace_count = _count
		else:
			if len(self.data_to_collect) > 0:
				self.collect_data()
		monitor.data.update_last_million_pulse_log()

	def get_new_outside_mask_traces(self, _count):
		temp = []
		for i in range(self.previous_outside_mask_trace_count, _count):
			new = {}
			new.update( monitor.llrf_control.getOutsideMaskDataPart(i) )
			string = 'new outside_mask_trace = ' + new['trace_name'] + ', count = ' + str(i)

			temp.append(i)
			if self.is_forward(new['trace_name']):
				#string = string + ' forward count = ' + str(len(self.forward_power_data))
				monitor.data.values[dat.rev_power_spike_count] += 1

			elif self.is_reverse(new['trace_name']):
				self.new_breakdown()
				#string = string + ' reverse count = ' + str(len(self.reverse_power_data))

			elif self.is_probe(new['trace_name']):
				self.new_breakdown()
				#self.probe_power_data.append(new)
				#string = string + ' probe count = ' + str(len(self.probe_power_data))

			monitor.logger.message(string, True)

		self.data_to_collect = self.data_to_collect + temp
		self.data_to_collect = list(set(self.data_to_collect))



	def new_breakdown(self):
		# update breakdown count, will only work if all states are not bad
		monitor.data.update_break_down_count()
		# set this state to bad
		monitor.data.values[dat.breakdown_status] = state.BAD
		# start or restart the cooldown_timer
		self.cooldown_timer.start(monitor.config.breakdown_config['OUTSIDE_MASK_COOLDOWN_TIME'])

	def collect_data(self):
		print('collecting data')
		x = []
		for part in self.data_to_collect:
			if monitor.llrf_control.isOutsideMaskDataFinishedCollecting(part):
				new = monitor.llrf_control.getOutsideMaskDataPart(part)
				new.update({ 'vacuum' : monitor.data.values[dat.vac_level] })
				new.update({ 'DC' : monitor.data.values[dat.DC_level] })
				new.update({ 'SOL' : monitor.data.values[dat.sol_value] })
				monitor.logger.message(new['message'], True)

				print'dumping'
				if self.is_forward(new['trace_name']):
					self.forward_power_data.append(new)
					self.logger.dump_forward(new, len(self.forward_power_data))
				elif self.is_reverse(new['trace_name']):
					self.reverse_power_data.append(new)
					self.logger.dump_reverse(new, len(self.reverse_power_data))
					print'r dumped'
				elif self.is_probe(new['trace_name']):
					self.probe_power_data.append(new)
					self.logger.dump_probe(new, len(self.probe_power_data))
				monitor.logger.message('Saved outside_mask_data part = ' + str(part), True)
			else:
				print('data not ready yet')
				x.append(part)
				pass

		self.data_to_collect = x


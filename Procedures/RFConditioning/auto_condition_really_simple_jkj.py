#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS automtic gun conditioning PROTOTYPING SCRIPT, march 2017
import epics, time, math, numpy, sys

# where to write the log 
log_file = "llrf_amp_kly_fwd_pwr_log.txt"

# tweakable parameters
normal_RF_increase = 2  # RF step increment
increase_wait_time = 1 # Time between RF step increments (in seconds)
vac_spike_RF_drop = 50   # RF step drop if spike
permit_RF_drop    = 1000 # RF step drop if RF permit lost 
rf_upper_limit    = 16800 # AW suggestion 16800
maximum_pulse_width = 3 # Absolute max pulse length
nominal_pulse_width = 2.75 # Pulse width we should be at if all is well
pulse_width_tolerance = 0.005 # Pulse width error we can tolerate due to Libera granularity
increase_wait_time_pulse_width = 1 # Time between RF pulse_width step increments (in seconds)
vac_spike_RF_pulse_width_drop = 0.01 #pulse width amount to drop when IMG spike
vac_spike_RF_pulse_width_increase = 0.005 #pulse width amount to drop when IMG spike (NB MUST BE >= 0.005)
time_of_last_increase = time_of_last_increase_pulse_width = time.time()

# ramp_pause_time times (seconds) 
ramp_pause_time = {
'IMG_1'       : 1*60,  	# vac_spike_cooldown_time	 NOT LESS THAN 1 !!
'RF_PERMIT'   : 3*60	# permit_cooldown_time			 NOT LESS THAN 1 !!
}

# timer reset cooldown  times (seconds) 
event_timer_cooldown = {
'IMG_1'       : 1,  	# vac_spike_cooldown_time	NOT LESS THAN 1 !!
'RF_PERMIT'   : 30  	# permit_cooldown_time		NOT LESS THAN 1 !!
}

# the PVs to "continuously" monitor (for now via acquisition)
pv_to_monitor = {
'RF_PERMIT' 			: epics.PV('CLA-GUN-RF-PROTE-01:Cmi'),
'RF_TRIG' 				: epics.PV('CLA-GUNS-HRF-MOD-01:Sys:ErrorRead.SVAL'),
'LLRF_CAVITY_REV_POWER' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch4:power_remote.POWER'),
'RF_PULSE_LENGTH' 	    : epics.PV('CLA-GUNS-LRF-CTRL-01:vm:feed_fwd:duration'),
'IMG_1'        			: epics.PV('CLA-LRG1-VAC-IMG-01:P'),
'DC'        			: epics.PV('EBT-INJ-SCOPE-01:P3'),
'RF_AMPLITUDE'  		: epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_amp:amplitude'),
}

# these are the PVs that we sometimes get / set 
pv_to_use = {
'LLRF_KLY_FWD_PWR' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch1:power_remote.POWER'),
'LLRF_CAV_FWD_PWR' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch3:power_remote.POWER')
}

# not happy about repeating the keys... 
# if the current state IS NOT the value in this table the alarm should sound
# RF rev power and vacuum are more complex as the ylook at arrays and changes from base-level
pv_monitor_not_alarm_values= {
'RF_PERMIT': 65535,
'RF_TRIG': 'D000',
'LLRF_CAVITY_REV_POWER': 500e3,
'IMG_1': 0.5E-9   # This is the level above background at which the pulse width drops
'DC': 0.5E-9   # This is the level above background at which the pulse width drops
}

# keep a record of when the last alarm was 
pv_time_of_last_alarm = {
'IMG_1' 				: time.time() - ramp_pause_time['IMG_1'],  
'DC' 					: time.time() - ramp_pause_time['DC'],    		
'RF_PERMIT' 			: time.time() - ramp_pause_time['RF_PERMIT'],
'LLRF_CAVITY_REV_POWER' : time.time()
}

# to spot a vacuum spike we have a history buffer
last_10_img_values = []
pre_spike_img_mean = pv_to_monitor['IMG-1'].get()
for i in range(11):
	last_10_img_values.append(pre_spike_img_mean)

# to spot a vacuum spike we have a history buffer
last_10_dc_values = []
pre_spike_dc_mean = pv_to_monitor['DC'].get()
for i in range(11):
	last_10_dc_values.append(pre_spike_dc_mean)

	
# Some utility functions
def appendMessageToLog(message, log_file):
	print message
	with open(log_file,"a") as logfile:
		logfile.write(str(message)+ '\n')
def getCurrentValues( pv_dictionary ):
	returndict = {}
	for name,pv in pv_dictionary.iteritems():
		#print name, '  ', pv.get()
		returndict[name] = pv.get()
	return returndict
	
def currentTimeStr():													
	return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()) 		
	
# check if the time since the last alarm is greater than the cool-down time, if so return True
def is_not_in_cool_down( signal ):
	if time.time() - pv_time_of_last_alarm[signal] > event_timer_cooldown[signal]:
		return True
	else:
		return False
		
# check if the time since the last alarm is greater than the cool-down time, if so return True
def is_not_in_pause_ramp( signal ):
	if time.time() - pv_time_of_last_alarm[signal] > ramp_pause_time[signal]:
		return True
	else:
		return False

def check_RF_permit_is_good( rf_permit_signal, rf_trig_signal, rf_amp_signal,  latest_values ):
	global permit_RF_drop, is_not_in_cool_down, pv_time_of_last_alarm
	rf_dropped = False
	rf_permit_lost = False
	rf_trig_lost = False
	if (latest_values[ rf_permit_signal ] != pv_monitor_not_alarm_values[ rf_permit_signal ]):
		rf_dropped = True
		rf_permit_lost = True
	elif (latest_values[ rf_trig_signal ] != pv_monitor_not_alarm_values[ rf_trig_signal ]):
		rf_dropped = True
		rf_trig_lost = True
	if rf_dropped:
		if is_not_in_cool_down( rf_permit_signal ):
			pv_time_of_last_alarm[ rf_permit_signal ] =  time.time()
			if rf_permit_lost:
				print 'RF Permit Lost, Dropping RF amplitude by ' + str(permit_RF_drop) + ' and pausing RF Amplitude Ramp for ' \
				+ str( ramp_pause_time[ rf_permit_signal ] ) + ' seconds'
				change_RF_amp( rf_amp_signal,  latest_values[ rf_amp_signal ] -  permit_RF_drop )
		elif rf_trig_lost:
			pv_time_of_last_alarm[ rf_permit_signal ] =  time.time()
			print 'RF Trig Lost - Please manually re-enable TRIG'
	# else:
		# print 'RF Permit good '

def check_IMG_change_is_small(img_signal, rf_amp_signal, rf_pulse_width_signal, latest_values):
	global vac_spike_RF_drop, vac_spike_RF_pulse_width_drop, nominal_pulse_width, pre_spike_img_mean, last_10_img_values
	if len(last_10_img_values) > 10:
		last_10_img_values.pop(0)
	delta_IMG = latest_values[ img_signal ] - pre_spike_img_mean
	if delta_IMG > pv_monitor_not_alarm_values[ img_signal ]:  
		print 'delta_IMG = ', delta_IMG, '  pre_spike_img_mean = ', pre_spike_img_mean	
		if is_not_in_cool_down( img_signal ):
			pv_time_of_last_alarm[ img_signal ] =  time.time()
			print 'Vac Spike, Dropping RF pulse width to ' + str(latest_values[ rf_pulse_width_signal ] - vac_spike_RF_pulse_width_drop) + ' and pausing RF Ramp for ' \
			+ str( ramp_pause_time[ img_signal ] ) + ' seconds'
			# Changing RF Pulse Width
			change_RF_pulse_width(rf_pulse_width_signal, latest_values[ rf_pulse_width_signal ] - vac_spike_RF_pulse_width_drop)
			time.sleep(0.3) # delays for 0.2 seconds
			#last_10_img_values = [] # reset IMG values after spike
	else:
		#print 'new IMG mean' + str(delta_IMG)
		last_10_img_values.append( latest_values[ img_signal ] )
		pre_spike_img_mean = numpy.mean( last_10_img_values )
																		
def can_increase_rf():
	global time_of_last_increase, increase_wait_time, nominal_pulse_width
	if latest_values['RF_PULSE_LENGTH'] > nominal_pulse_width - pulse_width_tolerance:
		if time.time() - pv_time_of_last_alarm[ 'IMG_1' ] > ramp_pause_time['IMG_1']:
			if time.time() - pv_time_of_last_alarm[ 'RF_PERMIT' ] > ramp_pause_time[ 'RF_PERMIT' ]:
				if time.time() - time_of_last_increase > increase_wait_time:
					return True
			else:
				print 'can_increase_rf thinks we are in RF permit lost cooldown '
		else:
			print 'can_increase_rf thinks we are in vac spike cooldown '
	#else:
		#print 'can_increase_rf thinks we should increase pusle width'
	return False
	
def can_increase_rf_pulse_width():
	global time_of_last_increase_pulse_width, increase_wait_time_pulse_width
	if time.time() - pv_time_of_last_alarm[ 'IMG_1' ] > ramp_pause_time['IMG_1']:
		if time.time() - pv_time_of_last_alarm[ 'RF_PERMIT' ] > ramp_pause_time[ 'RF_PERMIT' ]:
			if time.time() - time_of_last_increase_pulse_width > increase_wait_time_pulse_width:
				return True
	return False

def change_RF_amp(rf_amp_signal, value ):
	pv_to_monitor[ rf_amp_signal ].put( value )

def change_RF_pulse_width(rf_pulse_width_signal, value):
	global nominal_pulse_width, maximum_pulse_width
	if value > maximum_pulse_width:
		print 'TRYING TO SET GREATER THAN MAX PULSE WIDTH - EXITING!'
		sys.exit()
	if value > nominal_pulse_width:
		pv_to_monitor[ rf_pulse_width_signal ].put( nominal_pulse_width )
	if value < 1.5:
		pv_to_monitor[ rf_pulse_width_signal ].put( 1.5 )
	else:
		#print 'changing pulse width to: ', value
		pv_to_monitor[ rf_pulse_width_signal ].put( value )

def log( lrf_index_start, llrf_index_stop, log_file):
	global pre_spike_img_mean
	kly_power_data = pv_to_use[ 'LLRF_KLY_FWD_PWR' ].get()
	cav_power_data = pv_to_use[ 'LLRF_CAV_FWD_PWR' ].get()
	kly_power_cut   = kly_power_data[llrf_index_start:llrf_index_stop]
	cav_power_data = cav_power_data[llrf_index_start:llrf_index_stop]
	kly_power = numpy.mean( kly_power_cut )
	cav_power = numpy.mean( cav_power_data )
	message =  currentTimeStr() +  ' RF to ' + str( pv_to_monitor['RF_AMPLITUDE'].get( ) )	+ ' kly_fwd_power =  ' + str(kly_power) + ' cav_fwd_power =  ' + str(cav_power) + ' pre_spike_img_mean = ' + str(pre_spike_img_mean)+ ' pulse_length = ' +  str( pv_to_monitor['RF_PULSE_LENGTH'].get( ) )
	appendMessageToLog( message, log_file)

	
llrf_check_width =  0.4
llrf_end_offest    =  0.05
llrf_pulse_offset = 0.48 # usec from start of llrf trace until RF ramps on
last_pulse_length = 0		

# return the index (number of points) less than t form the LLRF time 
def get_LLRF_power_trace_index_at_time_t( t ):
	# the LLRF times	
	llrf_time_pv = epics.PV('CLA-GUNS-LRF-CTRL-01:app:time_vector')
	return next( x[0] for x in enumerate( llrf_time_pv.get() ) if x[1] > t)		

while True:
	#global time_of_last_increase, vac_spike_RF_pulse_width_increase, normal_RF_increase, llrf_check_width, llrf_end_offest, llrf_pulse_offset, last_pulse_length

	
	
	latest_values = getCurrentValues( pv_to_monitor )

	if latest_values['RF_AMPLITUDE'] > rf_upper_limit:  #Upper RF limit
		change_RF_amp( 'RF_AMPLITUDE',  15000  ) # this is the value we re-start from when we raise the pulse length
		nominal_pulse_width = nominal_pulse_width + 0.1
		if nominal_pulse_width > maximum_pulse_width:
			sys.exit()
	
	if latest_values['RF_PULSE_LENGTH'] != last_pulse_length:
		llrf_time_stop   = llrf_pulse_offset + latest_values['RF_PULSE_LENGTH'] - llrf_end_offest 
		llrf_time_start  = llrf_pulse_offset + latest_values['RF_PULSE_LENGTH'] - llrf_end_offest - llrf_check_width
		llrf_index_start = get_LLRF_power_trace_index_at_time_t( llrf_time_start )
		llrf_index_stop  = get_LLRF_power_trace_index_at_time_t( llrf_time_stop  )
		print 'new RF pulse-length = ' + str( latest_values['RF_PULSE_LENGTH'] ) + ' micro-seconds'
		print 'new LLRF trace start index ' + str( llrf_index_start ) + ' = ' + str(llrf_time_start) + ' micro-seconds'
		print 'new LLRF trace stop  index ' + str( llrf_index_stop )  + ' = ' + str(llrf_time_stop)  + ' micro-seconds'
	
	check_RF_permit_is_good( 'RF_PERMIT', 'RF_TRIG', 'RF_AMPLITUDE', latest_values )

	
	check_IMG_change_is_small( 'IMG_1', 'RF_AMPLITUDE', 'RF_PULSE_LENGTH', latest_values)
	
	if can_increase_rf_pulse_width() and latest_values['RF_PULSE_LENGTH']  < nominal_pulse_width - pulse_width_tolerance:
		#print 'can increase RF pulse width'
		print 'Increasing RF pulse width to: ', latest_values[ 'RF_PULSE_LENGTH' ] + vac_spike_RF_pulse_width_increase
		increase = latest_values[ 'RF_PULSE_LENGTH' ] + vac_spike_RF_pulse_width_increase
		change_RF_pulse_width('RF_PULSE_LENGTH', increase)
		time_of_last_increase_pulse_width = time.time()
		print 'No Events for ' + str( time.time() - time_of_last_increase ) + '  RF Amp = ' + str( increase )
		log( llrf_index_start, llrf_index_stop, log_file)
	elif can_increase_rf():
		#print 'can increase RF amplitude'
		increase = latest_values['RF_AMPLITUDE'] + normal_RF_increase
		change_RF_amp( 'RF_AMPLITUDE',  increase  )
		time_of_last_increase = time.time()
		print 'No Events for ' + str( time.time() - time_of_last_increase ) + '  RF Amp = ' + str( increase )
		log( llrf_index_start, llrf_index_stop, log_file)
	# else:
		# print 'cannot increase RF '

	last_pulse_length = latest_values['RF_PULSE_LENGTH']
		
	time.sleep(0.1)

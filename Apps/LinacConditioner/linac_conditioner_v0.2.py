import epics, time, math, numpy, sys


# where to write the log
log_file = "breakdowns.txt"
 
# tweakable parameters
normal_RF_increase = 60  # RF step increment
increase_wait_time = 240  # Time between RF step increments (in seconds)
permit_RF_drop = 1000  # RF step drop if RF permit lost
rf_upper_limit = 100000  # AW suggestion 16800
maximum_pulse_width = 2  # Absolute max pulse length
nominal_pulse_width = 0.25  # Pulse width we should be at if all is well
pulse_width_tolerance = 0.005  # Pulse width error we can tolerate due to Libera granularity

ramp_pause_time = {
'IMG_1'       			: 1,  	# vac_spike NOT LESS THAN 1 !!
'DC'          			: 1,  	# DC_spike_ NOT LESS THAN 1 !!
'LLRF_CAVITY_REV_POWER' : 1,  	# REV_power_spike	 NOT LESS THAN 1 !!
'RF_PERMIT'   			: 30,		# permit 	 NOT LESS THAN 1 !!
'RF_PERMIT_RETURN'   	: 1,		# permit 	 NOT LESS THAN 1 !!
}
# ramp_pause_time times (seconds)
event_timer_cooldown = {
    'IMG_1': 2,  # vac_spike_cooldown_time	NOT LESS THAN 1 !!
    'RF_PERMIT': 2  # permit_cooldown_time		NOT LESS THAN 1 !!
}


pv_to_monitor = {
    'RF_PERMIT' 		    : epics.PV('CLA-L01-RF-PROTE-01:Cmi'),
    'RF_TRIG' 				: epics.PV('CLA-L01-HRF-MOD-01:FAULT'),
	'LLRF_CAVITY_REV_POWER' : epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch4:power_remote.POWER'),
    'RF_PULSE_LENGTH' 	    : epics.PV('CLA-L01-LRF-CTRL-01:vm:feed_fwd:duration'),
    'IMG_1'        			: epics.PV('CLA-S01-VAC-IMG-01:PRES'), #needs changing to correct IMG
    'RF_AMPLITUDE'  		: epics.PV('CLA-L01-LRF-CTRL-01:vm:dsp:sp_amp:amplitude'),
    'LLRF_KLY_FWD_PWR'      : epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch1:power_remote.POWER'),
    'LLRF_CAV_FWD_PWR'      : epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch3:power_remote.POWER'),
    'LLRF_LOAD1_FWD_PWR'    : epics.PV('CLA-L01-LRF-CTRL-01:ad1:ch5:power_remote.POWER'),
}

pv_monitor_not_alarm_values= {
    'RF_PERMIT': 65535,
    'RF_TRIG': 0,
    'LLRF_CAVITY_REV_POWER': 100e3,
    'IMG_1': 2E-9  # This is the level above background at which the pulse width drops
}

pv_time_of_last_alarm = {
    'IMG_1' 				: time.time() - ramp_pause_time['IMG_1'],
    'RF_PERMIT' 			: time.time() - ramp_pause_time['RF_PERMIT'],
    'LLRF_CAVITY_REV_POWER' : time.time()
}

# to spot a vacuum spike we have a history buffer
last_10_img_values = []
pre_spike_img_mean = epics.PV('CLA-S01-VAC-IMG-01:PRES').get()
for i in range(11):
    last_10_img_values.append(pre_spike_img_mean)


def getCurrentValues(pv_dictionary ):
    returndict = {}
    for name, pv in pv_dictionary.iteritems():
        # print name, '  ', pv.get()
        returndict[name] = pv.get()
    return returndict


def currentTimeStr():
    return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())

def is_not_in_cool_down(signal):
    return True

rf_dropped = False
rf_permit_lost = False
rf_trig_lost = False

def check_RF_permit_is_good(rf_permit_signal, rf_trig_signal, rf_amp_signal, latest_values):
    global permit_RF_drop, is_not_in_cool_down, rf_dropped, rf_permit_lost, rf_trig_lost

    if (latest_values[rf_permit_signal] != pv_monitor_not_alarm_values[rf_permit_signal]):
        rf_dropped = True
        rf_permit_lost = True
        print 'RF Permit Lost!'
    elif (latest_values[rf_trig_signal] != pv_monitor_not_alarm_values[rf_trig_signal]):
        rf_dropped = True
        rf_trig_lost = True
        print 'RF Trigger Lost!'
    else:
        rf_dropped = False
        rf_trig_lost = False
    if rf_dropped:
        if is_not_in_cool_down(rf_permit_signal):
            pv_time_of_last_alarm[rf_permit_signal] = time.time()
            if rf_permit_lost:
                print 'RF Permit Lost, Dropping RF amplitude by ' + str(
                    permit_RF_drop) + ' and pausing RF Amplitude Ramp for ' \
                      + str(ramp_pause_time[rf_permit_signal]) + ' seconds'
                change_RF_amp(rf_amp_signal, latest_values[rf_amp_signal] - permit_RF_drop)
        elif rf_trig_lost:
            pv_time_of_last_alarm[rf_permit_signal] = time.time()
            print 'RF Trig Lost - Please manually re-enable TRIG'
            # else:
            # print 'RF Permit good '

def get_breakdown_rate():    
    if breakdown_count > 0:
        breakdown_per_minute = breakdown_count / ((time.time() - loop_start_time) / 60)
    else:
        breakdown_per_minute = 0
    return breakdown_per_minute
        
def writelog(type):
    if type == 'vacuum':
        with open(log_file,"a") as logfile:
            logfile.write( str(time.time()) + '\t' + 'Vacuum spike' + '\t' + str(breakdown_count) + '\t' + str(get_breakdown_rate()) + '\t' + str(normal_RF_increase) + '\n')			
    elif type == 'ref':
        with open(log_file,"a") as logfile:
            logfile.write( str(time.time()) + '\t' + 'Reflected power spike' + '\t' + str(breakdown_count) + '\t' + str(get_breakdown_rate()) + '\t' + str(normal_RF_increase) + '\n')			
			
def change_RF_amp(rf_amp_signal, value):
    pv_to_monitor[rf_amp_signal].put(value)

def check_IMG_change_is_small(img_signal, rf_amp_signal, rf_pulse_width_signal, latest_values):
    global vac_spike_RF_drop, vac_spike_RF_pulse_width_drop, nominal_pulse_width, pre_spike_img_mean, last_10_img_values, breakdown_count, reset_rf_value
    if len(last_10_img_values) > 10:
       last_10_img_values.pop(0)
	#print 'img signal = ', latest_values[img_signal], '  pre_spike_img_mean = ', pre_spike_img_mean	
    delta_IMG = latest_values[img_signal] - pre_spike_img_mean
    if delta_IMG > pv_monitor_not_alarm_values[img_signal]:
        #print 'delta_IMG = ', delta_IMG, '  pre_spike_img_mean = ', pre_spike_img_mean
        #if is_not_in_cool_down(img_signal):
        pv_time_of_last_alarm[img_signal] = time.time()
        print 'Vac Spike, Dropping RF power to zero '
        # Changing RF Pulse Width
        breakdown_count = breakdown_count + 1
        reset_rf_value = latest_values['RF_AMPLITUDE'] -100
        change_RF_amp(rf_amp_signal, 0)
		
        while delta_IMG > pv_monitor_not_alarm_values[img_signal]:
            print 'Sleeping for 2 seconds due to VAC spike'
            time.sleep(2)
            latest_values = getCurrentValues(pv_to_monitor)
            delta_IMG = latest_values[img_signal] - pre_spike_img_mean
        change_RF_amp(rf_amp_signal, reset_rf_value)
        writelog('vacuum')
        time.sleep(0.3)  # delays for 0.2 seconds
        #last_10_img_values = [latest_values[img_signal]] # reset IMG values after spike
    else:
        # print 'new IMG mean' + str(delta_IMG)
        last_10_img_values.append(latest_values[img_signal])
        pre_spike_img_mean = numpy.mean(last_10_img_values)

def check_LLRF_rev_power_is_low(ref_signal,rf_amp_signal, rf_pulse_width_signal, latest_values, reset_rf_value):
    global max_rev_power, max_rev_power_pos, breakdown_count
    if latest_values['LLRF_CAVITY_REV_POWER'] is not None:
        max_rev_power = max( latest_values['LLRF_CAVITY_REV_POWER'] )
        max_rev_power_pos =  [i for i,x in enumerate(latest_values['LLRF_CAVITY_REV_POWER']) if x > pv_monitor_not_alarm_values[ 'LLRF_CAVITY_REV_POWER']]
        kly_power_at_breakdown = [latest_values['LLRF_LOAD1_FWD_PWR'][i] / 1e6 for i in max_rev_power_pos]
        #print 'latest values ref power', max( latest_values['LLRF_CAVITY_REV_POWER'])
        if max_rev_power > pv_monitor_not_alarm_values[ 'LLRF_CAVITY_REV_POWER']:
            if is_not_in_cool_down( ref_signal ):
                pv_time_of_last_alarm[ ref_signal ] =  time.time()
                print 'Reflected power spike, Dropping RF power to 0 for 3s'
                print 'Reflected Max Power = ' + str(max_rev_power)
                breakdown_count = breakdown_count + 1
                reset_rf_value = latest_values['RF_AMPLITUDE']- 100
                change_RF_amp(rf_amp_signal, 0)
                print 'Sleeping for 3 seconds'
                time.sleep(3.0)
                change_RF_amp(rf_amp_signal, reset_rf_value)
                writelog('ref')
                time.sleep(0.3) # delays for 0.3 second

def can_increase_rf():
    global time_of_last_increase, increase_wait_time, nominal_pulse_width
    if latest_values['RF_PULSE_LENGTH'] > nominal_pulse_width - pulse_width_tolerance:
        #print 'time is', time.time(), 'pv_time_of_last_alarm is', pv_time_of_last_alarm['RF_PERMIT']	
		#if time.time() - pv_time_of_last_alarm['IMG_1'] > ramp_pause_time['IMG_1']:
        if pv_time_of_last_alarm['RF_PERMIT'] > ramp_pause_time['RF_PERMIT']:
            if time.time() - time_of_last_increase > increase_wait_time:
                return True
        else:
            print 'can_increase_rf thinks we are in RF permit lost cooldown '
        #else:
           # print 'can_increase_rf thinks we are in vac spike cooldown '
            # else:
            # print 'can_increase_rf thinks we should increase pusle width'
    return False

time_of_last_increase = time.time()-increase_wait_time
loop_start_time = time.time()
breakdown_count = 0
reset_rf_value = 100

while True:
    # global time_of_last_increase, vac_spike_RF_pulse_width_increase, normal_RF_increase, llrf_check_width, llrf_end_offest, llrf_pulse_offset, last_pulse_length

    latest_values = getCurrentValues(pv_to_monitor)

    if latest_values['RF_AMPLITUDE'] > rf_upper_limit:  # Upper RF limit
        sys.exit()

    check_RF_permit_is_good('RF_PERMIT', 'RF_TRIG', 'RF_AMPLITUDE', latest_values)

    check_IMG_change_is_small('IMG_1', 'RF_AMPLITUDE', 'RF_PULSE_LENGTH', latest_values)
	
    check_LLRF_rev_power_is_low('LLRF_CAVITY_REV_POWER','RF_AMPLITUDE', 'RF_PULSE_LENGTH', latest_values, reset_rf_value)
	
    if rf_dropped == True or rf_permit_lost == True or rf_trig_lost == True:
        print 'Sleeping for 2 seconds due to RF dropped'
        time.sleep(2)

    if can_increase_rf():
        # print 'can increase RF amplitude'
        increase = latest_values['RF_AMPLITUDE'] + normal_RF_increase
        change_RF_amp('RF_AMPLITUDE', increase)
        print 'Increasing RF amplitude to ' + str(increase) + ' - Last Power Reading was ' + str(max(latest_values['LLRF_CAV_FWD_PWR'])/1e6) + 'MW'
        #print 'No Events for ' + str(time.time() - time_of_last_increase) + '  RF Amp = ' + str(increase)
        time_of_last_increase = time.time()
    # else:
    # print 'cannot increase RF '

    last_pulse_length = latest_values['RF_PULSE_LENGTH']

    if (time.time() - loop_start_time) % 60 < 0.05:
        print 'Breakdown rate is ' + str(get_breakdown_rate()) + ' breakdowns/minute (' + str(get_breakdown_rate() * 30) + ' breakdowns/30mins with ' + str(breakdown_count) + ' breakdowns)'

    time.sleep(0.05)
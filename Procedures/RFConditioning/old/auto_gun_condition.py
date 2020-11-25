import epics, numpy, time, math

# _________                         __                 __          
# \_   ___ \  ____   ____   _______/  |______    _____/  |_  ______
# /    \  \/ /  _ \ /    \ /  ___/\   __\__  \  /    \   __\/  ___/
# \     \___(  <_> )   |  \\___ \  |  |  / __ \|   |  \  |  \___ \ 
 # \______  /\____/|___|  /____  > |__| (____  /___|  /__| /____  >
        # \/            \/     \/            \/     \/          \/ 

required_time_since_last_vacspike  = 2 * 60 # minimum time in seconds with no vacuum spikes, to be able to increase RF power
required_time_since_last_rf_hi_pow = 2 * 60 # minimum time in seconds with no HI RF Power, to be able to increase RF power
required_time_since_last_rf_trip   = 5 * 60 # minimum time in seconds with no RF Trips, to be able to increase RF power

last_vacspike_time  = 0
last_rf_trip_time   = 0
last_rf_hi_pow_time = 0

pv_dictionary = {
'CLARA_LRRG_ON' 	     : epics.PV('CLA-GUN-RF-PROTCL-01:On'),
'CLARA_LRRG_ENABLE_ON'   : epics.PV('CLA-GUN-RF-PROTE-01:On'),
'CLARA_LRRG_RESET'       : epics.PV('CLA-GUN-RF-PROTCL-01:Rst'),
'CLARA_LRRG_ENABLE_RESET': epics.PV('CLA-GUN-RF-PROTE-01:Rst'),
'CLARA_LRRG_STA'	     : epics.PV('CLA-GUN-RF-PROTCL-01:Sta'),
'CLARA_LRRG_ENABLE_STA'  : epics.PV('CLA-GUN-RF-PROTE-01:Sta'),
'MOD_ILOCK' 			 : epics.PV('CLA-GUNS-HRF-MOD-01:Sys:INTLK1'), # modulator interlock
'MOD_COMS_ILOCK'		 : epics.PV('CLA-GUNS-HRF-MOD-01:Sys:INTLK3'), # modulator interlock
'MOD_RESET' 			 : epics.PV('CLA-GUNS-HRF-MOD-01:Sys:Reset'),
'MOD_STATE_READ' 		 : epics.PV('CLA-GUNS-HRF-MOD-01:Sys:StateRead'),
'MOD_STATE_SET' 		 : epics.PV('CLA-GUNS-HRF-MOD-01:Sys:StateSet:W'),
'IMG_01_P' 				 : epics.PV('CLA-LRG1-VAC-IMG-01:P'),
'LLRF_REV_POWER' 		 : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch4:power_remote.POWER'),
'RF_PULSE_LENGTH' 		 : epics.PV('CLA-GUNS-LRF-CTRL-01:vm:feed_fwd:duration'),
'RF_AMPLITUDE' 			 : epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_amp:amplitude')
}

mod_ilock_state_good = 'No Error'
mod_state_trig 	 	 = 13

clara_lrrg_sta_good = 1
clara_lrrg_enable_sta_good = 1

current_values = {}
previous_values = {}

factor_to_drop_RF_amp_after_RF_trip = 0.6;

rf_amplitude_max_limit = 1000;



def Get_Current_Values():
	global current_values
	for name,pv in pv_dictionary.iteritems():
		current_values[name] = pv.get()

def Get_Delta_RF():
	return 1

def Current_Time():
	return time.localtime()	

def Current_Time_String():
	return time.strftime("%Y/%m/%d %H:%M:%S", Current_Time())	

def VacSpike_Occured():
	global last_vacspike_time 
	last_vacspike_time = getTime()

def RF_High_REV_Power_Occured():
	global last_rf_hi_pow_time,previous_values 
	last_rf_hi_pow_time = getTime()
	
def RF_Trip_Occured():
	global last_rf_trip_time,previous_values, last_good_rf_amplitude 
	last_rf_trip_time = getTime()
	last_good_rf_amplitude = previous_values['RF_AMPLITUDE']
	drop_rf_amplitude =  math.floor( previous_values['RF_AMPLITUDE'] * factor_to_drop_RF_amp_after_RF_trip ) 
	Set_RF_Amp( drop_rf_amplitude )
	Reset_From_RF_Trip()

def Set_RF_Amp(value):
	if value < rf_amplitude_max_limit:
		pv_dictionary['RF_AMPLITUDE' ].put(value)
	
# __________                     .__  __          
# \______   \ ___________  _____ |__|/  |_  ______
 # |     ___// __ \_  __ \/     \|  \   __\/  ___/
 # |    |   \  ___/|  | \/  Y Y  \  ||  |  \___ \ 
 # |____|    \___  >__|  |__|_|  /__||__| /____  >
               # \/            \/              \/ 

can_increase_rf	   = False			   
slow_rf_increase   = False
medium_rf_increase = False
fast_rf_increase   = False 
			   
def Time_Since_Last_VacSpike_OK():	
	global last_vacspike_time, can_increase_rf
	if getTime() - last_vacspike_time > required_time_since_last_vacspike:
		can_increase_rf = True
	else:
		can_increase_rf = False
def Time_Since_Last_RF_Trip_OK():	
	global last_rf_trip_time,can_increase_rf
	if currentTime() - last_rf_trip_time > required_time_since_last_rf_trip:
		can_increase_rf =  True
	else:
		can_increase_rf =  False

def Time_Since_Last_RF_Hi_Pow_OK():	
	global last_rf_hi_pow_time,can_increase_rf
	if currentTime() - last_rf_hi_pow_time > required_time_since_last_rf_hi_pow:
		can_increase_rf = True
	else:
		can_increase_rf = False		

def Can_Increase_RF_Amp():
	global can_increase_rf
	return can_increase_rf
	
		
# __________                      __          
# \______   \ ____   ______ _____/  |_  ______
 # |       _// __ \ /  ___// __ \   __\/  ___/
 # |    |   \  ___/ \___ \\  ___/|  |  \___ \ 
 # |____|_  /\___  >____  >\___  >__| /____  >
        # \/     \/     \/     \/          \/ 
		
def Reset_Mod():
	global mod_ilock_state_good 
	count = 0
	failed = False
	while pv_dictionary['MOD_ILOCK'].get() !=  mod_ilock_state_good:
		pv_dictionary['MOD_RESET'].put(1)
		time.sleep(0.01)
		pv_dictionary['MOD_RESET'].put(0)
		count += 1
		time.sleep(0.2)
		if count > 20:
			print '*********** Reset_Mod FAILED ************' 
			print '                                         ' 
			print 'After 20 attempts Rest_Mod_To_Trig Failed'
			print '                                         ' 
			print '************ FAILED ABORTING ************' 
			failed = True
			break
	return failed	

def Rest_Mod_To_Trig():
	global mod_state_trig
	count = 0
	failed = False
	while pv_dictionary['MOD_STATE_READ'].get() !=  mod_state_trig:
		pv_dictionary['MOD_STATE_SET'].put( mod_state_trig )
		count += 1
		time.sleep(0.2)
		if count > 20:
			print '******* Rest_Mod_To_Trig FAILED *********' 
			print '                                         ' 
			print 'After 20 attempts Rest_Mod_To_Trig Failed'
			print '                                         ' 
			print '************ FAILED ABORTING ************' 
			failed = True
			break
	return failed

def Reset_CLARA_LRRG():
	global clara_lrrg_sta_good
	count = 0
	failed = False
	while pv_dictionary['CLARA_LRRG_STA'].get() !=  clara_lrrg_sta_good:
		pv_dictionary['CLARA_LRRG_ON'].put(1)
		time.sleep(0.01)
		pv_dictionary['CLARA_LRRG_ON'].put(0)
		time.sleep(0.01)
		count += 1
		time.sleep(0.2)
		if count > 20:
			print '******* Reset_CLARA_LRRG FAILED *********' 
			print '                                         ' 
			print 'After 20 attempts Reset_CLARA_LRRG Failed'
			print '                                         ' 
			print '************ FAILED ABORTING ************' 
			failed = True
			break
	return failed
def Reset_CLARA_LRRG_Enable():
	global clara_lrrg_enable_sta_good
	count = 0
	failed = False
	while pv_dictionary['CLARA_LRRG_ENABLE_STA'].get() !=  clara_lrrg_enable_sta_good:
		pv_dictionary['CLARA_LRRG_ENABLE_ON'].put( 1 )
		time.sleep(0.01)
		pv_dictionary['CLARA_LRRG_ENABLE_ON'].put( 0 )
		time.sleep(0.01)
		count += 1
		time.sleep(0.2)
		if count > 20:
			print '******** Reset_CLARA_LRRG_ENABLE FAILED ********' 
			print '                                                ' 
			print 'After 20 attempts Reset_CLARA_LRRG_ENABLE Failed'
			print '                                                ' 
			print '**************** FAILED ABORTING ***************' 
			failed = True
			break
	return failed

def Reset_RF_Permits():
	print 'Reset_From_RF_Trip'
	print 'Reset_From_Comms_Trip'
	failedtoreset = Reset_CLARA_LRRG()
	if not failedtoreset:
		return Reset_CLARA_LRRG_Enable()
	return failedtoreset

def Reset_From_Comms_Trip():
	print 'Reset_From_Comms_Trip'
	failedtoreset = Reset_Mod()
	if not failedtoreset:
		return Rest_Mod_To_Trig()
	return failedtoreset	

def Set_Fast_RF_Increase():	
	global slow_rf_increase,medium_rf_increase,fast_rf_increase
	slow_rf_increase   = False
	medium_rf_increase = False
	fast_rf_increase   = True 
	
def Set_Medium_RF_Increase():	
	global slow_rf_increase,medium_rf_increase,fast_rf_increase
	slow_rf_increase   = False
	medium_rf_increase = True
	fast_rf_increase   = False 

def Set_Medium_RF_Increase():	
	global slow_rf_increase,medium_rf_increase,fast_rf_increase
	slow_rf_increase   = False
	medium_rf_increase = True
	fast_rf_increase   = False 
	
Reset_RF_Permits()
Reset_From_Comms_Trip()	
	
# ___________      .__                         .____________ 
# \__    ___/______|__|_____ ______   ____   __| _/\_____   \
  # |    |  \_  __ \  \____ \\____ \_/ __ \ / __ |    /   __/
  # |    |   |  | \/  |  |_> >  |_> >  ___// /_/ |   |   |   
  # |____|   |__|  |__|   __/|   __/ \___  >____ |   |___|   
                    # |__|   |__|        \/     \/   <___>   
	
	
def Is_A_VacSpike():
	return True
	
def Is_A_RF_Trip():
	return True
	
def Is_A_Lost_Comms():
	return True
	
def Is_A_High_Rev_Power():
	return True	
	
	
def Main_Loop():
	
	previous_values = current_values
	
	Get_Current_Values()
	
	if Is_A_RF_Trip():
		RF_Trip_Occured()
		Reset_RF_Permits()
		Reset_From_Comms_Trip()
	
	if Is_A_Lost_Comms():
		success = Reset_From_Comms_Trip()
		if not success:
			should_break = False 
		

	if Is_A_VacSpike():
		VacSpike_Occured()
					
	
	if Is_A_High_Rev_Power():
		RF_High_REV_Power_Occured()		

	if Can_Increase_RF_Amp():
		new_rf_amp = Get_Delta_RF() + current_values['RF_AMPLITUDE']
		print 'Can_Increase_RF_Amp is True, Setting LLRF AMP from ', current_values['RF_AMPLITUDE'], ' to ', new_rf_amp
		Set_RF_Amp(new_rf_amp)

	
	

	
	


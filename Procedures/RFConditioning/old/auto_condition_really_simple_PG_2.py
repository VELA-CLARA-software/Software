#!/usr/bin/env python
# -*- coding: utf-8 -*-
import epics, winsound, time, math, numpy,sys


# the PVs to monitor
pv_dictionary= {
'rf_Permit' : epics.PV('CLA-GUN-RF-PROTE-01:Cmi'),
#'ionp2_pv': epics.PV('CLA-LRG1-VAC-IONP-02:P'),
'llrf_rev_power' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch4:power_remote.POWER'),
'rf_pulse_length' : epics.PV('CLA-GUNS-LRF-CTRL-01:vm:feed_fwd:duration'),
'mod_il' : epics.PV('CLA-GUNS-HRF-MOD-01:Sys:INTLK1'), # modulator interlock
'vacvalve1' : epics.PV('CLA-S01-VAC-VALV-01:Sta'),
'img1' : epics.PV('CLA-LRG1-VAC-IMG-01:P'),
'img1' : epics.PV('CLA-LRG1-VAC-IMG-01:P'),
'cavity_temp' : epics.PV('CLA-GUN-RF-LRRG-04:RT'),
'RF_AMPLITUDE'  : epics.PV('CLA-GUNS-LRF-CTRL-01:vm:dsp:sp_amp:amplitude'),
'kly_power_pv' : epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch1:power_remote.POWER')
}
# not happy about repeating the keys... 
# if the current state IS NOT the value in this table the alarm should sound
# RF rev power and vacuum are more complex as they look at arrays and changes from base-level
pv_Alarm= {
'rf_Permit': 65535,
'llrf_rev_power': 500e3,
'mod_il': 'No Error', # modulator interlock
'vacvalve1': 1,
'img1': 0.5E-9,
'cavity_temp': 28.5
}

delta_RF = 1; #RF step increment
wait_time = 1; #Time between RF step increments (in seconds)
drop_RF = 50; # RF step drop if spike
drop_RF_when_permit_lost = 100; # RF step drop if RF permit lost, atm this is called multiple times, needs fixing! 
cool_down_time = 120; # Time to let system rest (in seconds)

# Counters, used so the alarm doesn't sound too often, i.e. it has a cool-down time before re-sounding
recentlySpiked = 0    		
recentlyTripped = 0
recentlyHighRevPower = 0
recentlyModIlckLost = 0
recentlyClosed = 0
recentlyCold = 0


def getCurrentValues():
	returndict = {}
	for name,pv in pv_dictionary.iteritems():
		#print name, '  ', pv.get()
		returndict[name] = pv.get()
	return returndict

def currenttime():
	return time.strftime("%Y/%m/%d %H:%M:%S", time.localtime())



	
def check_RF_permit_is_good(latest_values):
	global recentlyTripped
	if latest_values['rf_Permit'] != pv_Alarm['rf_Permit']:
		time.sleep(0.1)	

last_10_img_values = []
def appendToIMG10(latest_values):
	last_10_img_values.append( latest_values['img1'] )
	if len(last_10_img_values) > 10:
		last_10_img_values.pop(0)

def have_at_least_10_img():
	return len(last_10_img_values) >= 10

		
def check_IMG_Change_isnot_Large(latest_values):
	global recentlySpiked, drop_RF, time_of_last_vac_spike
	if have_at_least_10_img():
		#print '10 IMG values acquired!'
		delta_IMG = numpy.mean( last_10_img_values ) - latest_values['img1']
		#print 'delta_IMG = ', delta_IMG
		if delta_IMG > pv_Alarm[ 'img1' ]  and recentlySpiked > 15:	
			time_of_last_vac_spike =  time.time()
			print 'Vac Spike'
			change_RF_amp(  latest_values['RF_AMPLITUDE'] - drop_RF  )
			recentlySpiked = 0
	appendToIMG10(latest_values)		


# the LLRF times	
llrf_time_pv = epics.PV('CLA-GUNS-LRF-CTRL-01:app:time_vector')
llrf_time_data = llrf_time_pv.get()
kly_power_start =  2.6
kly_power_end  =  2.9
kly_power_start_index = next( x[0] for x in enumerate(llrf_time_data) if x[1] > kly_power_start)
kly_power_end_index  = next( x[0] for x in enumerate(llrf_time_data) if x[1] >  kly_power_end)



required_time_since_last_vacspike  = cool_down_time # minimum time in seconds with no vacuum spikes, to be able to increase RF power		
time_required_from_last_increase   = wait_time # time between steps up 
		
time_of_last_vac_spike = time.time() - required_time_since_last_vacspike
time_of_last_increase   = time.time() - time_required_from_last_increase

print   time.time() - time_of_last_vac_spike

def can_increase_rf():
	global time_of_last_vac_spike,required_time_since_last_vacspike,time_of_last_increase,time_required_from_last_increase
	if time.time() - time_of_last_vac_spike > required_time_since_last_vacspike:
		#print 'last spike was ' + str(time.time() - time_of_last_vac_spike ) 
		if time.time() - time_of_last_increase > time_required_from_last_increase:
			print 'last increase was ' + str(time.time())
			if latest_values['RF_AMPLITUDE'] < 17000:  #Upper RF limit
				return True
			print '*** Target Voltage Reached ***'	
			sys.exit()
	return False

log_file = "llrf_amp_kly_fwd_pwr_log.txt"	
def appendMessage(message, log_file):
	print message
	with open(log_file,"a") as logfile:
		logfile.write(str(message)+ '\n')	
	
def change_RF_amp( value ):
	global kly_power_start_index, kly_power_end_index
	pv_dictionary['RF_AMPLITUDE'].put( value )
	kly_power_data = pv_dictionary['kly_power_pv' ].get()
	kly_power_cut = kly_power_data[kly_power_start_index:kly_power_end_index]
	kly_power = numpy.mean( kly_power_cut )
	message =  currenttime() +  ' RF to ' + str( value )	+ ' kly_fwd_power =  ' + str(kly_power)
	appendMessage( message, log_file)

	
def check_RF_permit_is_good( latest_values ):
	if latest_values['rf_Permit'] != pv_Alarm['rf_Permit']:
		time_of_last_vac_spike =  time.time()
		change_RF_amp(  latest_values['RF_AMPLITUDE'] -  drop_RF_when_permit_lost )

		
while True:
	global time_of_last_increase
	latest_values = getCurrentValues()

	check_RF_permit_is_good( latest_values )

	check_IMG_Change_isnot_Large(latest_values)
	
	if can_increase_rf():
		change_RF_amp(  latest_values['RF_AMPLITUDE'] + delta_RF  )
		print 'No Events  for ' + str(time.time() - time_of_last_increase ) + '  RF Amp = ' + str(latest_values['RF_AMPLITUDE'] + delta_RF )
		time_of_last_increase = time.time()
		
	time.sleep(0.1)
	recentlySpiked = recentlySpiked + 1

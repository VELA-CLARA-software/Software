import epics
import numpy
import time
from time import gmtime, strftime

numpy.set_printoptions(threshold=numpy.inf)

pv_to_monitor = {
'gun_fw_power' 			: epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch3:power_remote.POWER'),
'gun_rev_power'			: epics.PV('CLA-GUNS-LRF-CTRL-01:ad1:ch4:power_remote.POWER')
}

log_file = "boris_data.txt"

def appendMessageToLog(message, log_file):
	#print message
	with open(log_file,"a") as logfile:
		logfile.write(str(message)+ '\n')


gun_fw_vec = []
gun_rev_vec = []
gun_fw_last = pv_to_monitor['gun_fw_power'].get()
gun_rev_last = pv_to_monitor['gun_rev_power'].get()

while 1:
	
	if len (gun_fw_vec) == 10:
		gun_fw_vec = gun_fw_vec[1:]
		gun_rev_vec = gun_rev_vec[1:]
	
	gun_fw_signal = pv_to_monitor['gun_fw_power'].get()
	gun_rev_signal = pv_to_monitor['gun_rev_power'].get()
	
	if (gun_fw_signal[1:10]!=gun_fw_last[1:10]).all():
	
		print str(time.time()) + " " + strftime("%a, %d %b %Y %H:%M:%S", gmtime()) + " New data " + str(sum(gun_rev_signal)/1e9)
	
		gun_fw_last = gun_fw_signal
		
		gun_fw_vec.append (gun_fw_signal)
		gun_rev_vec.append (gun_rev_signal)
	
		if sum(gun_rev_signal) > 0.5e9:
		
			print str(time.time()) + " " + strftime("%a, %d %b %Y %H:%M:%S", gmtime()) + " Recorded spike"
	
			appendMessageToLog(str(time.time()) + " " + strftime("%a, %d %b %Y %H:%M:%S", gmtime()), log_file)
			appendMessageToLog("fw", log_file)
			appendMessageToLog(gun_fw_vec, log_file)
			appendMessageToLog("rev", log_file)
			appendMessageToLog(gun_rev_vec, log_file)
			
	#else:
		#print str(time.time()) + " " + strftime("%a, %d %b %Y %H:%M:%S", gmtime()) + " Same old data"
	
	time.sleep(0.01)
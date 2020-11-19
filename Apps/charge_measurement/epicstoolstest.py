import sys
import os
sys.path.append("\\\\192.168.83.14\\claranet\\test\\CATAP\\bin\\")
print(sys.path)

from CATAP.EPICSTools import *
import random
import time

os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
os.environ["EPICS_CA_ADDR_LIST"] = "192.168.83.255" #"10.10.0.12"#
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

# Creating an EPICSTools object without the STATE argument
# will force CATAP to use the Virtual EPICS instance.
# i.e. ET = EPICSTools()
#
# Adding a STATE argument will specify which EPICS instance to use.
ET = EPICSTools(STATE.PHYSICAL)

# Monitoring a PV is done via EPICSTools by providing the PV:
readi_pv = "CLA-VCA-DIA-CAM-01:ANA:SigmaXPix_RBV"
ET.monitor(readi_pv)

# To access the monitor object, it can be accessed via EPICSTools:
readi_monitor = ET.getMonitor(readi_pv)
print("Current READI Value: ", readi_monitor.getValue())


# # Putting to a PV can only be done through the EPICSTools object
# seti_pv = "CLA-C2V-MAG-HCOR-01:SETI"
# set_current = int(random.random() * 10)
# # ET.put(seti_pv, set_current)
#
# # Getting a PV value can only be done through the EPICSTools object
# getseti_pv = "CLA-C2V-MAG-HCOR-01:GETSETI"
# ET.get(getseti_pv)
#
# # Example of using monitor, put, and get:
#
# # Turn on HCOR-01
# spower_pv = "CLA-C2V-MAG-HCOR-01:SPOWER"
# # ET.put(spower_pv, 1)
# # Wait for HCOR-01 READI value to reach SETI
# while(readi_monitor.getValue() != ET.get(getseti_pv)):
#     print("READI VALUE: ", readi_monitor.getValue())
#     time.sleep(0.1)
# print("READI VALUE: ", readi_monitor.getValue(), " SETI VALUE: ", ET.get(getseti_pv))
#
# # From the monitor object, buffer, buffer average,
# # and buffer standard deviation can be accessed:
# print("Current READI Buffer: ", readi_monitor.getBuffer())
# print("READI Buffer Average: ", readi_monitor.getBufferAverage())
# print("READI Buffer Standard Deviation: ", readi_monitor.getBufferStdDev())
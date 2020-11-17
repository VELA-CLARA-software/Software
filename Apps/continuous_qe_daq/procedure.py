# get PIL laser controller
# get sol / bsole controller
# get LLRF KFPower trace
# get cavity FWD power trace
#
#
#
# get cavity FWD power trace
import sys
sys.path.append('\\\\claraserv3\\claranet\\test\\CATAP\\bin')
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\test\\CATAP\\bin')
from CATAP.EPICSTools import *
import random
import time
#
# Adding a STATE argument will specify which EPICS instance to use.
ET = EPICSTools(STATE.PHYSICAL)

# Monitoring a PV is done via EPICSTools by providing the PV:
rf_traces_pv = 'CLA-GUN-LRF-CTRL-01:ad1:dod_demod_vec'

pv = 'CLA-GUN-LRF-CTRL-01:ad1:dod_demod_vec'
TRACE_NUM_ELEMENTS_TOTAL = 1024
TRACE_NUM_ELEMENTS_USED = 1017

TRACE_NUM_OF_START_ZEROS = 7
TRACE_MAP = {"KLYSTRON_FORWARD_POWER" :  1,
"KLYSTRON_FORWARD_PHASE" :  2,
"KLYSTRON_REVERSE_POWER" : 4,
"KLYSTRON_REVERSE_PHASE" :  5,
"LRRG_CAVITY_FORWARD_POWER" :  7,
"LRRG_CAVITY_FORWARD_PHASE" :  8,
"LRRG_CAVITY_REVERSE_POWER" :  10,
"LRRG_CAVITY_REVERSE_PHASE" : 11,
"HRRG_CAVITY_FORWARD_POWER" : 13,
"HRRG_CAVITY_FORWARD_PHASE":   14,
"HRRG_CAVITY_PROBE_POWER" :  16,
"HRRG_CAVITY_PROBE_PHASE" :  17,
"CALIBRATION_POWER" : 19,
"CALIBRATION_PHASE" : 20,
"HRRG_CAVITY_REVERSE_POWER" : 22,
"HRRG_CAVITY_REVERSE_PHASE" : 23}
NUM_CHUNKS = 24

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_dmod_data():
    ''' connect to PV, get all trace data, then disconnect  '''
    data = ET.getArray(rf_traces_pv)
    return chunks(data,TRACE_NUM_ELEMENTS_TOTAL)

def get_trace_data(trace_name):
    data = ET.getArray(rf_traces_pv)
    n= NUM_CHUNKS
    final = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n)]
    #raw_data = list(get_dmod_data())
    print(len(final))
    print(final[0])
    input()
    if type(trace_name) == str:
        ans = raw_data[ TRACE_MAP(trace_name) ]
        if "POWER" in trace_name:
            ans = [(i**2)/100 for i in ans]
    if type(trace_name) == list:
        ans = []
        for name in trace_name:
            ans.append(raw_data[ TRACE_MAP(name) ])
            if "POWER" in trace_name:
                ans = [(i**2)/100 for i in ans]
    return ans

print("Current READI Value: ", ET.getArray(rf_traces_pv))

print(get_dmod_data())


print(get_trace_data('LRRG_CAVITY_FORWARD_PHASE'))

input()





def get_dmod_data():
    ''' connect to PV, get all trace data, then diconnect  '''
    data = ET.getArray(rf_traces_pv)
    return chunks(data,TRACE_NUM_ELEMENTS_TOTAL)


def get_trace_data(trace_name):
    raw_data = get_dmod_data()
    if type(trace_name) == str:
        ans = raw_data[ TRACE_MAP(trace_name) ]
        if "POWER" in trace_name:
            ans = [(i**2)/100 for i in ans]
    if type(trace_name) == list:
        ans = []
        for name in trace_name:
            ans.append(raw_data[ TRACE_MAP(name) ])
            if "POWER" in trace_name:
                ans = [(i**2)/100 for i in ans]
    return ans



print(get_dmod_data())


print(get_dmod_data())

input()


















# Putting to a PV can only be done through the EPICSTools object
seti_pv = "CLA-C2V-MAG-HCOR-01:SETI"
set_current = int(random.random() * 10)
ET.put(seti_pv, set_current)

# Getting a PV value can only be done through the EPICSTools object
getseti_pv = "CLA-C2V-MAG-HCOR-01:GETSETI"
ET.get(getseti_pv)

# Example of using monitor, put, and get:

# Turn on HCOR-01
spower_pv = "CLA-C2V-MAG-HCOR-01:SPOWER"
ET.put(spower_pv, 1)
# Wait for HCOR-01 READI value to reach SETI
while(readi_monitor.getValue() != ET.get(getseti_pv)):
    print("READI VALUE: ", readi_monitor.getValue())
    time.sleep(0.1)
print("READI VALUE: ", readi_monitor.getValue(), " SETI VALUE: ", ET.get(getseti_pv))

# From the monitor object, buffer, buffer average,
# and buffer standard deviation can be accessed:
print("Current READI Buffer: ", readi_monitor.getBuffer())
print("READI Buffer Average: ", readi_monitor.getBufferAverage())
print("READI Buffer Standard Deviation: ", readi_monitor.getBufferStdDev())













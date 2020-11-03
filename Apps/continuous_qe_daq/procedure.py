# get PIL laser controller
# get sol / bsole controller
# get LLRF KFPower trace
# get cavity FWD power trace
#
#
#
# get cavity FWD power trace
import sys
sys.path.append('\\\\claraserv3\\claranet\\test\\Controllers\\bin\\stage')
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\test\\Controllers\\bin\\stage')


import VELA_CLARA_General_Monitor
import time
gen_mon = VELA_CLARA_General_Monitor.init()
gen_mon.setVerbose()
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


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def get_dmod_data():
    ''' connect to PV, get all trace data, then diconnect  '''
    id = gen_mon.connectPV(pv)
    print("Connected with id = ", id)
    time.sleep(0.3)
    data = gen_mon.getValue(id)
    if gen_mon.disconnectPV(id):
        print("deleted")
    else:
        print("NOT deleted")
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



# get PIL laser controller
# get sol / bsole controller
# get LLRF KFPower trace
# get cavity FWD power trace
#
# TODO / make new folders for each day
# TODO / reduce amount of saved data
#
# get cavity FWD power trace
import sys
sys.path.append('\\\\claraserv3\\claranet\\test\\CATAP\\bin')
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\test\\CATAP\\bin')
from CATAP.EPICSTools import *
from datetime import datetime
import json
import time

#
# Adding a STATE argument will specify which EPICS instance to use.
ET = EPICSTools(STATE.PHYSICAL)

# Monitoring a PV is done via EPICSTools by providing the PV:
single_pv_dict = {
"gun_rf_phase_FF"  : 'CLA-GUN-LRF-CTRL-01:vm:dsp:ff_ph:phase',
"gun_rf_phase_SP"  : 'CLA-GUN-LRF-CTRL-01:vm:dsp:sp_ph:phase',
"gun_rf_phase_lock"  : 'CLA-GUN-LRF-CTRL-01:vm:dsp:ff_ph:lock',
"Q_pv" : 'CLA-S01-DIA-WCM-01:Q',
"E_pv" : 'CLA-LAS-DIA-EM-06:E_RB',
"E_range_pv" : 'CLA-LAS-DIA-EM-06:Range_RB',
"E_overrange_pv" : 'CLA-LAS-DIA-EM-06:OverRange_RB',
"bsol_seti_pv" : 'CLA-LRG1-MAG-SOL-01:GETSETI',
"bsol_pow_pv" : 'CLA-LRG1-MAG-SOL-01:RPOWER',
"sol2_seti_pv" : 'CLA-GUN-MAG-SOL-02:GETSETI',
"sol2_pow_pv" : 'CLA-GUN-MAG-SOL-02:RPOWER',
"las_sigma_x" : 'CLA-C2V-DIA-CAM-01:ANA:SigmaXPix_RBV',
"las_sigma_y" : 'CLA-C2V-DIA-CAM-01:ANA:SigmaYPix_RBV',
"las_x" : 'CLA-C2V-DIA-CAM-01:ANA:XPix_RBV',
"las_y" : 'CLA-C2V-DIA-CAM-01:ANA:YPix_RBV',
"las_cam_avg_int" : 'CLA-C2V-DIA-CAM-01:ANA:AvgIntensity_RBV',
"las_mirror4_v_pos" : 'CLA-LAS-OPT-PICO-4C-PM-4:V:POS',
"las_mirror4_h_pos" : 'CLA-LAS-OPT-PICO-4C-PM-4:H:POS',
"las_mirror3_h_pos" : 'CLA-LAS-OPT-PICO-4B-PM-3:H:POS',
"las_mirror3_h_pos" : 'CLA-LAS-OPT-PICO-4B-PM-3:V:POS',
"las_mirror5_h_pos" : 'CLA-LAS-OPT-PICO-4B-PM-5:V:POS',
"las_mirror5_h_pos" : 'CLA-LAS-OPT-PICO-4B-PM-5:V:POS',
"las_hwp" : 'EBT-LAS-OPT-HWP-2:ROT:RPOS'
}

network_loc = '\\\\claraserv3\\claranet\\apps\\legacy\\logs\\continuous_qe_daq\\'

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

def split(a, n):
    k, m = divmod(len(a), n)
    return (a[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(n))

def get_trace_data(trace_name):
    gun_rf_traces_pv = 'CLA-GUN-LRF-CTRL-01:ad1:dod_demod_vec'
    final = list(split(ET.getArray(gun_rf_traces_pv),24))
    r = {}
    if type(trace_name) == str:
        ans = final[ TRACE_MAP[trace_name] ]
        if "POWER" in trace_name:
            ans = [(i**2)/100 for i in ans]
        r[trace_name] = ans
    if type(trace_name) == list:
        ans = []
        for name in trace_name:
            ans.append(final[TRACE_MAP[name] ])
            if "POWER" in trace_name:
                ans[-1] = [(i**2)/100 for i in ans]
            r[name] = ans[-1]
    return r

def get_single_Pv_data():
    data = {}
    for key, value in single_pv_dict.items():
        data[key] = ET.get(value)
    return data


def get_data_to_log():
    return {**get_trace_data(['KLYSTRON_FORWARD_POWER','LRRG_CAVITY_FORWARD_POWER']),
             **get_single_Pv_data()}

def log_data(fn, data):
    dt_string = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    fullpath = network_loc + fn + '_' + dt_string + '.json'
    file =  open(fullpath,"w")
    file.write(json.dumps(data))  # use `json.loads` to do the reverse
    file.close()
    print("logged ",fullpath)


def should_log(data):
    if data["Q_pv"] > 10.0:
        return True
    return False


ts = time.time()
log_time = 10
print("Running")
while 1:
    if time.time() - ts > log_time:
        data = get_data_to_log()
        if should_log(data):
            log_data("test", data)
            ts = time.time()



# data_to_write = {**get_trace_data(['KLYSTRON_FORWARD_POWER','LRRG_CAVITY_FORWARD_POWER']),
#       **get_single_Pv_data()}
# print(data_to_write)
# input()

# def calculate_qe(self, d, calibration_factors = [4.66e-6, 15.4], rounding = 6):
# 	# d is a dictionary containing your measurement of WCM and laser energy ("ophir").
# 	# the keys "charge_values" and "ophir_values" are themselves dictionaries
# 	# containing lists of measured data, keyed by the settings of the laser half-wave plate
# 	self.ophirmean = []
# 	self.ophirmeanall = []
# 	self.ophirmeanstderr = []
# 	self.wcmmean = []
# 	self.wcmmeanall = []
# 	self.wcmmeanstderr = []
# 	for j in range(0,len(d["ophir_values"])-1):
# 		self.ophirmean.append(numpy.mean(list(d["ophir_values"].values())[j]))
# 		self.wcmmean.append(numpy.mean(list(d["charge_values"].values())[j]))
# 		self.ophirstderr.append(numpy.std(list(d["ophir_values"].values())[j]) / numpy.sqrt(len(list(d["ophir_values"].values())[j])))
# 		self.wcmstderr.append(numpy.std(list(d["charge_values"].values())[j]) / numpy.sqrt(len(list(d["charge_values"].values())[j])))
# 	for i, j, k, l in zip(self.wcmmean, self.ophirmean, self.wcmstderr, self.ophirstderr):
# 		self.wcmmeanall.append(i)
# 		self.ophirmeanall.append(j)
# 		self.wcmstderrall.append(k)
# 		self.ophirstderrall.append(l)
# 	self.x, self.y = self.ophirmeanall, self.wcmmeanall
# 	try:
# 		self.m, self.c = numpy.around(numpy.polyfit(self.x, self.y, 1), 2)
# 	except:
# 		self.m, self.c = 0, 0
# 	self.fit = self.m
# 	self.cross = self.c
# 	self.QE = numpy.around(calibration_factors[0] * self.m / calibration_factors[1], rounding)
# 	self.qeall = self.QE
# 	d["fit"] = self.m
# 	d["cross"] = self.c
# 	d["qe"] = self.QE * 10**(5)

#
# print(get_dmod_data())
#
#
# print(get_dmod_data())
#
# input()




















# import json
import requests
import sys
import os
import pprint
from datetime import datetime as dt
from datetime import timedelta as td
import pandas as pd


def pull_PV_data(pv_name, time_span):
    # Create URL & params
    URL = "http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json"
    PARAMS = {'pv': pv_name, 'from': time_span[0], 'to': time_span[1]}

    # Pull from URL
    r = requests.get(url=URL, params=PARAMS)
    r.raise_for_status()  # raise error if bad response

    data = r.json()

    return data[0]['meta'], data[0]['data']


def try_PV(pv):
    time_to, time_to_obj = convert_datetime(str(dt.now()))
    time_from_list = [
        time_to_obj - td(hours=2),
        # time_to_obj - td(days = 10),
        # time_to_obj - td(days = 730)
    ]  # THESE ARE DATETIME OBJECTS!!

    # try request with successively larger time spans (cycles time from list if previous time from failed)
    for time_from_obj in time_from_list:
        time_from = time_from_obj.strftime("%Y-%m-%dT%H:%M:%S.00Z")  # this produces str from datetome obj
        try:
            meta, data = pull_PV_data(pv, (time_from, time_to))
            return True, meta, data
        except:
            pass
    return False


def convert_datetime(dt_str):
    dt_obj = dt.strptime(dt_str.split('.')[0], '%Y-%m-%d %H:%M:%S')
    time_to = dt_obj.strftime("%Y-%m-%dT%H:%M:%S.00Z")

    return time_to, dt_obj


print()  # make space after console run command

# Define the PV & time span
PV_LIST = [
    # "CLA-GUNS-HRF:ConScriptAlive",
    # "CLA-GUNS-HRF-MOD-01:EnableEmails",
    # "CLA-GUNS-HRF-MOD-01:Ext:CommTimeout:R",
    # "CLA-GUNS-HRF-MOD-01:Ext:CommTimeout:W",
    # "CLA-GUNS-HRF-MOD-01:Sys:Reset",
    # "CLA-GUNS-HRF-MOD-01:Sys:ExtComm:AccessLevel",
    # "CLA-GUNS-HRF-MOD-01:Sys:ExtComm:AccessLevelR",
    # "CLA-GUNS-HRF-MOD-01:Sys:StateRead",
    # "CLA-GUNS-HRF-MOD-01:Sys:StateReadR",
    # "CLA-GUNS-HRF-MOD-01:Sys:StateSet",
    # "CLA-GUNS-HRF-MOD-01:Sys:StateSetR",
    # "CLA-GUNS-HRF-MOD-01:Sys:StateSet:W",
    # "CLA-GUNS-HRF-MOD-01:Sys:RemainingTime",
    # "CLA-GUNS-HRF-MOD-01:Sys:OffHoursRead",
    # "CLA-GUNS-HRF-MOD-01:Sys:StandbyHoursRead",
    # "CLA-GUNS-HRF-MOD-01:Sys:HvHoursRead",
    # "CLA-GUNS-HRF-MOD-01:Sys:TrigHoursRead",
    # "CLA-GUNS-HRF-MOD-01:Sys:conIlk",
    # "CLA-GUNS-HRF-MOD-01:Sys:Ilks",
    # "CLA-GUNS-HRF-MOD-01:Sys:getIlk",
    "CLA-GUNS-HRF-MOD-01:Sys:INTLK1",
    # "CLA-GUNS-HRF-MOD-01:Sys:INTLK2",
    # "CLA-GUNS-HRF-MOD-01:Sys:INTLK3",
    # "CLA-GUNS-HRF-MOD-01:Sys:INTLK4",
    # "CLA-GUNS-HRF-MOD-01:Sys:INTLK5",
    # "CLA-GUNS-HRF-MOD-01:Sys:ErrorRead",
    # "CLA-GUNS-HRF-MOD-01:Sys:ErrorRead2",
    # "CLA-GUNS-HRF-MOD-01:Sys:Trig:PlswthSet",			#HV pulse
    # "CLA-GUNS-HRF-MOD-01:Sys:Trig:PlswthSet:W",
    # "CLA-GUNS-HRF-MOD-01:Sys:Trig:PrfSet",			#RF pulse
    # "CLA-GUNS-HRF-MOD-01:Sys:Trig:PrfSet:W",
    # "CLA-GUNS-HRF-MOD-01:Pt:FilPs:CurrRead",
    # "CLA-GUNS-HRF-MOD-01:Pt:FilPs:VoltRead",
    "CLA-GUNS-HRF-MOD-01:Pt:Diag:CtRead",  # current transducer?, aka klystron/beam current
    # "CLA-GUNS-HRF-MOD-01:Pt:Diag:CtArc",
    # "CLA-GUNS-HRF-MOD-01:Pt:Diag:CvdRead",			#capacitor voltage divider?, aka klystron/beam voltage
    # "CLA-GUNS-HRF-MOD-01:Pt:Diag:CvdArc",
    # "CLA-GUNS-HRF-MOD-01:Pt:Diag:PlswthFwhmRead",		#pulse width forward  ?
    # "CLA-GUNS-HRF-MOD-01:Pt:Diag:PlswthRead",			#HV pulse width?
    # "CLA-GUNS-HRF-MOD-01:Pt:Diag:PowRead",			#power?
    # "CLA-GUNS-HRF-MOD-01:Pt:Diag:PrfRead",
    # "CLA-GUNS-HRF-MOD-01:HvPs:VoltSet",			#HVPS output voltage
    # "CLA-GUNS-HRF-MOD-01:HvPs:VoltSet:W",
    # "CLA-GUNS-HRF-MOD-01:HvPs:HvPs1:CurrRead",
    # "CLA-GUNS-HRF-MOD-01:HvPs:HvPs1:VoltRead",
    # "CLA-GUNS-HRF-MOD-01:HvPs:HvPs1:TrigCountRead",
    # "CLA-GUNS-HRF-MOD-01:HvPs:HvPs2:CurrRead",
    # "CLA-GUNS-HRF-MOD-01:HvPs:HvPs2:VoltRead",
    # "CLA-GUNS-HRF-MOD-01:HvPs:HvPs3:CurrRead",			#HvPs3 does not exist, but variables have been made for it?
    # "CLA-GUNS-HRF-MOD-01:HvPs:HvPs3:VoltRead",
    # "CLA-GUNS-HRF-MOD-01:Rf:Cool:BodyOutletTemp",		#lets you infer power dissipated in klystron body, rather than collector?
    # "CLA-GUNS-HRF-MOD-01:Rf:Cool:KlystLimit",
    # "CLA-GUNS-HRF-MOD-01:Rf:Cool:KlystPower",
    # "CLA-GUNS-HRF-MOD-01:Rf:Ionp:PresRead1",
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs1:CurrRead",
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs1:VoltRead",
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs2:CurrRead",
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs2:VoltRead",
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs3:CurrRead",
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs3:VoltRead",			#there are 3x coils hence PS for each
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs4:CurrRead",			#why PV for 4th?
    # "CLA-GUNS-HRF-MOD-01:Rf:MagPs4:VoltRead",
    # "CLA-GUNS-HRF-MOD-01:PING2",
    # "CLA-GUNS-HRF-MOD-01:PING2:1",
    # "CLA-GUNS-HRF-MOD-01:PING2:2",
    # "CLA-GUNS-HRF-MOD-01:PING2:3",
    # "CLA-GUNS-HRF-MOD-01:PING2:4",
    # "CLA-GUNS-HRF-MOD-01:PING2:5",
    # "CLA-GUNS-HRF-MOD-01:PING2:6",
    # "CLA-GUNS-HRF-MOD-01:PING2:7",
    # "CLA-GUNS-HRF-MOD-01:PING2:8",
    # "CLA-GUNS-HRF-MOD-01:PING2:9",
    # "CLA-GUNS-HRF-MOD-01:PING2:10",
    # "CLA-GUNS-HRF-MOD-01:PING2:11",
    # "CLA-GUNS-HRF-MOD-01:PING2:12",
    # "CLA-GUNS-HRF-MOD-01:PING2:13",
    # "CLA-GUNS-HRF-MOD-01:PING2:14",
    # "CLA-GUNS-HRF-MOD-01:PING2:15",
    # "CLA-GUNS-HRF-MOD-01:PING2:16",
    # "CLA-GUNS-HRF-MOD-01:PING2:17",
    # "CLA-GUNS-HRF-MOD-01:PING2:18",
    # "CLA-GUNS-HRF-MOD-01:PING2:19",
    # "CLA-GUNS-HRF-MOD-01:PING2:20",
    # "CLA-GUNS-HRF-MOD-01:PING2:F1",
    # "CLA-GUNS-HRF-MOD-01:PING2:F2",
    # "CLA-GUNS-HRF-MOD-01:PING2:F3",
    # "CLA-GUNS-HRF-MOD-01:PING2:F4",
    # "CLA-GUNS-HRF-MOD-01:PING3",
    # "CLA-GUNS-HRF-MOD-01:PING3:1",
    # "CLA-GUNS-HRF-MOD-01:PING3:2",
    # "CLA-GUNS-HRF-MOD-01:PING3:3",
    # "CLA-GUNS-HRF-MOD-01:PING3:4",
    # "CLA-GUNS-HRF-MOD-01:PING3:5",
    # "CLA-GUNS-HRF-MOD-01:PING3:6",
    # "CLA-GUNS-HRF-MOD-01:PING3:7",
    # "CLA-GUNS-HRF-MOD-01:PING3:8",
    # "CLA-GUNS-HRF-MOD-01:PING3:9",
    # "CLA-GUNS-HRF-MOD-01:PING3:F1",
    # "CLA-GUNS-HRF-MOD-01:PING3:F2",
    # "CLA-GUNS-HRF-MOD-01:PING4",
    # "CLA-GUNS-HRF-MOD-01:PING4:1",
    # "CLA-GUNS-HRF-MOD-01:PING4:2",
    # "CLA-GUNS-HRF-MOD-01:PING4:3",
    # "CLA-GUNS-HRF-MOD-01:PING4:4",
    # "CLA-GUNS-HRF-MOD-01:PING4:5",
    # "CLA-GUNS-HRF-MOD-01:PING4:6",
    # "CLA-GUNS-HRF-MOD-01:PING4:7",
    # "CLA-GUNS-HRF-MOD-01:PING4:8",
    # "CLA-GUNS-HRF-MOD-01:PING4:9",
    # "CLA-GUNS-HRF-MOD-01:PING4:10",
    # "CLA-GUNS-HRF-MOD-01:PING4:F1",
    # "CLA-GUNS-HRF-MOD-01:PING4:F2",
    # "CLA-GUNS-RFHOLD:OpMode",
    # "CLA-GUNS-RFHOLD:State",
    # "CLA-GUNS-RFHOLD:CompleteLog",
    # "CLA-GUNS-RFHOLD:LogIndx",
    # "CLA-GUNS-RFHOLD:NumFaults",
    # "CLA-GUNS-RFHOLD:FaultLog",				#list of previous 299 faults in buffer structure
    # "CLA-GUNS-RFHOLD:FaultLog0",
    # "CLA-GUNS-RFHOLD:FaultLog1",
    # "CLA-GUNS-RFHOLD:FaultLog2",
    # "CLA-GUNS-RFHOLD:FaultLog3",
    # "CLA-GUNS-RFHOLD:FaultLog4",
    # "CLA-GUNS-RFHOLD:FaultTimes",
    # "CLA-GUNS-RFHOLD:FaultTimes0",
    # "CLA-GUNS-RFHOLD:FaultTimes1",
    # "CLA-GUNS-RFHOLD:FaultTimes2",
    # "CLA-GUNS-RFHOLD:FaultTimes3",
    # "CLA-GUNS-RFHOLD:FaultTimes4",
    # "CLA-GUNS-RFHOLD:FaultIndx0",
    # "CLA-GUNS-RFHOLD:FaultIndx1",
    # "CLA-GUNS-RFHOLD:FaultIndx2",
    # "CLA-GUNS-RFHOLD:FaultIndx3",
    # "CLA-GUNS-RFHOLD:FaultIndx4",
    # "CLA-GUNS-RFHOLD:TimeIndx0",
    # "CLA-GUNS-RFHOLD:TimeIndx1",
    # "CLA-GUNS-RFHOLD:TimeIndx2",
    # "CLA-GUNS-RFHOLD:TimeIndx3",
    # "CLA-GUNS-RFHOLD:TimeIndx4",
]

## read data
data = {}
data_super = {}
read_fail = []

for PV in PV_LIST:

    print('reading ', PV)
    success, req_meta, req_data = try_PV(PV)

    '''There's some really clever stuff in that script you sent over, your code is a lot neater than mine!
I like the datetime functions you found and the success/fail  condition
    '''

    if success:
        print("success")

        # initialise master key list
        master_key_lst = list(req_data[0].keys())  # memory of keys in case subsequent events drop one

        # copy first event into new dict stucture
        data = {}  # reinitialise dict
        data.update(req_data[0])  # update data with req_data[0] (copy across)
        del req_data[0]  # no longer needed
        for key, val in data.items():
            data[key] = [val]  # put each value into a list initially

        # copy subsequent events into new dict
        # cycle events in request data
        for event in req_data:
            # cycle keys in event dict
            for event_k, event_v in event.items():
                # find corresponding key
                found = False
                for key, val in data.items():
                    if event_k == key:
                        # append val
                        found = True
                        val.append(event_v)
                if not found:
                    master_key_lst.append(event_k)  # update the master key list since a new one was found
                    # create new key and populate
                    n_empty = len(data[list(data.keys())[0]]) - 1  # n_empty = n data points - 1
                    event_v_lst = list(None for i in range(0, n_empty))  # create list of empties for padding
                    event_v_lst.append(event_v)  # append the current data point
                    data.update({event_k: event_v_lst})  # update the dict

            # check all keys accounted for by referencing master key list (some events drop a key, causing data array to not be square)
            curr_key_lst = list(event.keys())
            missing_keys = list(i for i in master_key_lst if (i not in curr_key_lst))  # create list of missing keys
            # cycle each missing key
            for key in missing_keys:
                # find it data dict
                for k, v in data.items():
                    if k == key:
                        data[k].append(None)  # update the value list with a null, now all data is same size

        # update super structure
        data_super.update({PV: data})

    else:
        read_fail.append(PV)
        print("fail")

for PV, PV_data in data_super.items():
    print('\n ', PV)

    df = pd.DataFrame(PV_data, columns=list(PV_data.keys()))
    print(df)
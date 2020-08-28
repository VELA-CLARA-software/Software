#Test script for SVD module using archiver data

import numpy as np
import svd_module
import requests

toTime = '2020-02-12T16:12:11'
fromTime = '2020-02-12T16:11:11'
PV = 'CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ'
url = 'http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=' + PV + '&from=' + fromTime + '.00Z&to=' + toTime + '.00Z';

r = requests.get(url)
data = r.json()

values = []
time = []

event = data[0]["data"]

for event in data[0]["data"]:
    time.append(event["secs"]+event["nanos"]*1E-9)
    values.append(event["val"])

np_values = np.array(values, dtype=np.float)
np_values = (np_values*5.63083E-5)-1.8514 #Convert to voltage
#np_values = (np_values*130.588E-3) #Convert to amps
noiseRemover = svd_module.svdNoiseRemover()

noiseRemover.SVD(values=np_values, dim=1)
noiseRemover.genModes(values = np_values, freq_s = 250e6, n_modes = 11)
noiseRemover.calculateDarkCharge()
noiseRemover.writeToCSV()

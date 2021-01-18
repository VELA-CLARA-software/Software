#Test script for SVD module using archiver data

import numpy as np
import svd_module
import requests
import pyqtgraph as pg

#toTime = '2020-02-12T16:12:11'
#fromTime = '2020-02-21T16:11:11'
#toTime = '2020-02-21T15:23:45'
#fromTime = '2020-02-21T15:22:45'
toTime = '2020-02-26T10:23:55'
fromTime = '2020-02-26T10:23:54'



PV = 'CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ'
url = 'http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=' + PV + '&from=' + fromTime + '.00Z&to=' + toTime + '.00Z';

r = requests.get(url)
data = r.json()

values = []
time = []

event = data[0]["data"]
nshots = 0

for event in data[0]["data"]:
    nshots = nshots + 1
    time.append(event["secs"]+event["nanos"]*1E-9)
    values.append(event["val"])
#    pg.plot(event["val"])
#    raw_input()
    
np_values = np.array(values, dtype=np.float)
np_values = (np_values*5.63083E-5)-1.8514 #Convert to voltage
#np_values = (np_values*130.588E-3) #Convert to amps

mean_array = np.mean(np_values,axis=0)
pg.plot(mean_array)
raw_input()
#pg.plot(np_values[1])
#raw_input()

noiseRemover = svd_module.svdNoiseRemover()


print(np_values)

print ('***************** going to calc SVD')
noiseRemover.SVD(values=np_values, dim=1)
print ('***************** going to genmodes')
noiseRemover.genModes(values = np_values, freq_s = 250e6, n_modes = 11)
print ('***************** going to calc charge')
noiseRemover.calculateDarkCharge()
print ('***************** going to write csv')
noiseRemover.writeToCSV()


print('******************There were ',nshots, ' shots ') 

# Script for testing the svd class

import svdPlugin
import numpy as np
import requests
import matplotlib.pyplot as plt

##Getting data from archiver
fromTime = '2020-02-12T16:11:11' # Time from which to get data from archiver
toTime = '2020-02-12T16:12:11' # Time to which to get data from archiver
PV = 'CLA-C09-IOC-CS-04:FMC_1_ADC_0_READ' # PV to get data from
url = 'http://claraserv2.dl.ac.uk:17668/retrieval/data/getData.json?pv=' + PV + '&from=' + fromTime + '.00Z&to=' + toTime + '.00Z' # Create URL

r = requests.get(url) # Get website
data = r.json() # Parse JSON

values = [] # Initialize
time = []

for event in data[0]["data"]:
    time.append(event["secs"]+event["nanos"]*1E-9)
    values.append(event["val"])
# Extract timestamps and values for each shot

np_values = np.array(values, dtype=np.float) #Convert to numpy array
np_values = (np_values*5.63083E-5)-1.8514 # Convert to voltage

svd = svdPlugin.svdPlugin(size = np_values.shape) # Create module, with pre-allocated array sizes
svd.addData(data=np_values, shotsDim=2, fs=250e6) # Add in data to decompose
svd.SVD() # Carry out SVD
mode1 = svd.extractMode(1) # Extract only the most significant mode
plt.plot(mode1[:,0]) # Plot the most significant mode for shot number 1
plt.show() # THIS IS BLOCKING AS LONG AS THE WINDOW IS OPEN
svd.extractModes() # Extract all modes
svd.extractModes(_n_modes=10) # Extract only the 10 most significant modes
plt.plot(svd.modes[0,:,50]) #Plot the most significant mode for shot number 50
plt.show() # THIS IS BLOCKING AS LONG AS THE WINDOW IS OPEN
svd.saveData(mode = "r") # save raw data
svd.saveData(mode = "SVU") # save SVD matrices
svd.saveData(mode = "m", modes=[1, 2]) # Save modes 1 and 2
"""
Module for removing WCM noise using SVD, to be implemented within DarkCurrent_valve_v2.py
Original release: 21-08-20

Methods:
    SVD - inputs: Data
    genModes - constructs mode decomposition data. Input sample frequency and number of modes
    writeToCSV - writes data to CSV
    fromArchiver - get data from archiver and run SVD

@author: SMathisen
"""

import numpy as np
from datetime import datetime
import os, csv
debug = True

class svdNoiseRemover():
    def __init__(self):
        pass

    def SVD(self, values = None, dim = 0):
        if debug:
            print("Carrying out SVD")
        if dim == 1:
            if debug:
                print("Transposing values")
            values = values.transpose()
        self.values = values
        self.u, self.s, self.vh = np.linalg.svd(values)
        if debug:
            print("SVD completed")

    def genModes(self, values = None, freq_s = 1, n_modes = None):
        if debug:
            print("Generating mode decomposition data")
        if n_modes == None:
            if debug:
                print("Number of modes not set, calculating maximum number of modes")
            n_modes = len(self.s)
        self.fs = freq_s
        self.nm = n_modes
        s_base = np.zeros((self.u.shape[1], len(self.s)), dtype=float)
        if debug:
            print(self.u.shape)
            print(s_base.shape)
        self.modes = np.zeros((self.nm, s_base.shape[0], s_base.shape[1]))
        self.fmodes = np.zeros((self.nm, 1))
        self.freqs = (np.arange(int(len(self.modes[0,0:-1,0:-1]/2))))/(len(self.modes[0,0:-1,0:-1])/self.fs)
        for i in np.arange(0, self.nm,1):
            SN = s_base
            SN[i, i] = self.s[i]
            moden = np.dot(self.u, np.dot(SN, self.vh))
            if debug:
                print(moden.shape)
                print(moden)
            self.modes[i, 0:,0:] = moden
            ft = np.fft.fft(self.modes[i, 0:,0:])
            ft = ft[range(int(len(self.modes[i, 0:,0:]/2)))]
            ft = abs(ft)
            print(ft.shape)
            self.fmodes[i] = self.freqs[np.argmax(ft[:, i])]
        self.ts = np.linspace(0, len(self.modes[1,0:,0:])*(1/self.fs), len(self.modes[1,0:,0:]))

    def writeToCSV(self):
        today = datetime.now()
        year = today.strftime("%Y")
        month = today.strftime("%m")
        day = today.strftime("%d")
        hr = today.strftime("%H")
        min = today.strftime("%M")
        csvDir = "SVD/" + year  + "/" + month + "/" + day + "/" + hr + min

        if debug:
            print("Writing to CSVs in ./"+csvDir)
        if not os.path.exists(csvDir):
            if debug:
                print("Making directories")
            os.makedirs(csvDir)
        if debug:
            print("Writing raw data")
        csvFile = open(csvDir + "/rawData.csv", 'wb')
        csvWriter = csv.writer(csvFile, delimiter=',')
        csvWriter.writerow(self.ts)
        csvWriter.writerows(self.values.transpose())
        if debug:
            print("Writing mode data")
        for i in np.arange(0, self.nm,1):
            csvFile = open(csvDir + "/mode"+ str(i+1) +".csv", 'wb')
            csvWriter = csv.writer(csvFile, delimiter=',')
            csvWriter.writerows(self.modes[i, :, :].transpose())
        if debug:
            print("Writing freq data")
        csvFile = open(csvDir + "/freqData.csv", 'wb')
        csvWriter = csv.writer(csvFile, delimiter=',')
        csvWriter.writerows(self.fmodes.transpose())
        if debug:
            print("Writing charge data")
        csvFile = open(csvDir + "/chargeData.csv", 'wb')
        csvWriter = csv.writer(csvFile, delimiter=',')
        csvWriter.writerow(self.charge.transpose())

    def calculateDarkCharge(self, wcm="clara", mode=1):
        if debug:
            print("calculating dark charge")
        #Specify for clara, anything else gives vela
        if wcm.lower() == "clara":
            if debug:
                print("Using CLARA calibration factor")
            wcm_V2A = 130.588E-3
        else:
            wcm_V2A = 131.631E-3
            if debug:
                print("Using VELA calibration factor")
        try: self.modes
        except NameError: self.modes = None
        if self.modes is None:
            print("Run SVD and mode decomp first")
        else:
            charge = []
            for i in np.arange(0, self.modes.shape[2], 1):
                base = np.mean(self.modes[mode-1, 0:100, i])
                dat = (self.modes[mode-1, :, i] - base)*130.588E-3
                charge.append(np.sum(dat[dat > 0]*(4E-9)))
                if debug:
                    print charge[i]*1e12
            self.charge = np.array(charge)
            print('charge shape', self.charge.shape)
            print('mean charge', np.mean(self.charge)*1e12)
            print('stddev charge', np.std(self.charge)*1e12)


















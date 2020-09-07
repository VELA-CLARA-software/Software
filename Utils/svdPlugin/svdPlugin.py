""""
Generalized version of a module to carry out SVD and mode decomposition of various accelerator data

Prerequisites: Numpy, Python 3.7 (saving data is not compatible with Python 2.7)
To do: Add FFT of modes, output of spectra and most significant frequencies, normalized significance and stats (sig, var, etc)

Author: Storm"""

import numpy as np
import os, csv
from datetime import datetime


class svdPlugin():
    def __init__(self, debug=True, verbose=True, size=None):
        self.debug = debug
        self.verbose = verbose
        if self.debug:
            print("Debug is on")
        if self.verbose:
            print("Verbose is on")
        if size is None:
            if self.debug or self.verbose:
                print("Initializing blank arrays")
            self.data = np.empty(0)
        elif isinstance(size, int):
            if self.debug or self.verbose:
                print("Initializing arrays with size (" + str(size) + ", 1)")
            self.data = np.empty((size, 1))
        else:
            if self.debug or self.verbose:
                print("Initializing arrays with size " + str(size))
            self.data = np.empty(size)
        self.fs = [] # Sample frequency
        self.ta = [] # Sample time array
        self.S = [] # S matrix for SVD
        self.U = [] # U matrix for SVD
        self.V = [] # V matrix for SVD
        self.modes = [] # 3D matrix for storing modes

    def SVD(self):
        if self.debug or self.verbose:
            print("Carrying out SVD")
        if self.data is None:
            pass
            if self.debug:
                print("Data is none, can't make something from nothing")
        else:
            self.U, self.S, self.V = np.linalg.svd(self.data)
            if self.debug or self.verbose:
                print("SVD finished")

    def addData(self, data=None, shotsDim=1, fs=1):
        if data is None:
            if self.debug:
                print("Data is none you fool")
            pass
        else:
            data = np.array(data)
            if shotsDim == 2:
                if self.verbose:
                    print("Transposing data")
                data = data.transpose()
            self.data = data
            if self.debug:
                print(self.data[1])
            self.fs = fs
            self.ta = np.linspace(0, self.data.shape[0]*(1/self.fs), self.data.shape[0])
            if self.debug:
                print("Sample frequency")
                print(self.fs)
                print("Time array")
                print(self.ta*1e6)
            today = datetime.now()
            year = today.strftime("%Y")
            month = today.strftime("%m")
            day = today.strftime("%d")
            hr = today.strftime("%H")
            min = today.strftime("%M")
            self.timeAdded = year + month + day + hr + min

    def saveData(self, mode="all", folder="./", prefix=None, modes = None):
        # Save specified data. r = raw, s = singular values, u and/or v = u and v matrices of SVD, m = modes, f = frequencies
        if prefix is None:
            if self.debug or self.verbose:
                print("Prefix is None, setting it to YYYYmmddHHMM")
            prefix = self.timeAdded
            if self.debug:
                print(prefix)
            if not os.path.exists(folder):
                if self.debug:
                    print("Making directories")
                os.makedirs(folder)
            if "r" in mode.lower() or mode.lower() == "all":
                self._saveCSV(header = self.ta, matrix = self.data, filename = folder+prefix+"raw.csv")
            if "s" in mode.lower() or mode.lower() == "all":
                self._saveCSV(matrix = self.S, filename = folder+prefix+"S_Matrix.csv")
            if "u" in mode.lower() or mode.lower() == "all":
                self._saveCSV(matrix = self.U, filename = folder+prefix+"U_Matrix.csv")
            if "v" in mode.lower() or mode.lower() == "all":
                self._saveCSV(matrix = self.V, filename = folder+prefix+"V_Matrix.csv")
            if "m" in mode.lower() or mode.lower() == "all":
                if modes is None:
                    for i in np.arange(0, self.modes.shape[0], 1):
                        self._saveCSV(matrix=self.modes[i, :, :], filename=folder + prefix + "mode"+str(i+1)+ ".csv")
                else:
                    for i in np.array(modes)-1:
                        self._saveCSV(matrix=self.modes[i, :, :], filename=folder + prefix + "mode"+str(i+1)+ ".csv")

    def _saveCSV(self, header=None, matrix=None, filename = "./test.csv"):
        if self.debug or self.verbose:
            print("Writing to "+ filename)
            print(header)
            print(matrix[0])
        with open(filename, 'w', newline='') as csvFile:
            csvWriter = csv.writer(csvFile, delimiter=',')
            if header is not None:
                csvWriter.writerow(header)
            if matrix is not None:
                if len(matrix.shape) > 1:
                    csvWriter.writerows(matrix.transpose())
                else:
                    csvWriter.writerow(matrix)

    def extractMode(self, mode=1):
        # Generate the specified mode
        if self.debug or self.verbose:
            print("Generating mode no. " + str(mode))
        _s = np.zeros((self.U.shape[1], len(self.S)), dtype=float)
        if self.debug:
            print(_s.shape)
        _s[mode-1, mode-1] = self.S[mode-1]
        _recon = np.dot(self.U, np.dot(_s, self.V))
        if self.debug:
            print(_recon.shape)
            print(_recon[:,1])
        return _recon

    def extractModes(self, _n_modes=None):
        # Generate the n_modes most significant modes
        if self.debug or self.verbose:
            print("Extracting modes")
        if _n_modes is None:
            if self.debug or self.verbose:
                print("Number of modes is None, extracting maximum number")
            _n_modes = len(self.S)
        self.modes = np.zeros((_n_modes, self.U.shape[1], len(self.S)), dtype=float)
        for i in np.arange(0, _n_modes, 1):
            self.modes[i, :, :] = self.extractMode(mode=i+1)

    def modeFrequency(self, mode=1):
        #TODO calculate most significant frequency of given mode
        pass

    def modeSpectrum(self, mode=1):
        #TODO calculate the spectrum of a given mode
        pass

    def modeSignificance(self):
        #TODO normalize the significance of each mode
        pass

    def modeStatistics(self):
        #TODO calculate statistical parameters of each moe
        pass

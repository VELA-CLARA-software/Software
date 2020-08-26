#Test script for SVD module using TestData.csv

import csv
import numpy as np
import svd_module

csvfile = open('TestData.csv', 'rb')
csvreader = csv.reader(csvfile)
values = []

for row in csvreader:
    values.append(row)
np_values = np.array(values, dtype=np.float)
noiseRemover = svd_module.svdNoiseRemover()

noiseRemover.SVD(values=np_values, dim=0)
noiseRemover.genModes(values = np_values, freq_s = 250e6, n_modes = 11)
noiseRemover.writeToCSV()

import sys,os
import time
import scipy.constants as physics
import numpy as np
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline
import random as r
from functools import partial
# sys.path.append("../../../")
# from Software.Utils.dict_to_h5 import *
# import Software.Procedures.Machine.machine as machine
degree = physics.pi/180.0
import h5py

class testClass(object):

    stepSize = 10
    fitOffset = 0

    def longest(self, l):
        if(not isinstance(l, list)): return(0)
        return(max([len(l),] + [len(subl) for subl in l if isinstance(subl, list)] +
            [self.longest(subl) for subl in l]))

    def cutDataLinacQuick(self, allData):
        cutData = [a for a in allData if np.isnan(a[1])]
        alllist = []
        newlist = []
        for i, pt in enumerate(cutData):
            if i < (len(cutData)-1):
                if not cutData[i+1][0] - pt[0] > 2*self.stepSize:
                    newlist.append(pt)
                else:
                    alllist.append(newlist)
                    newlist = []
            elif i == (len(cutData)-1):
                newlist.append(pt)
                alllist.append(newlist)
        # print 'alllist = ', max(alllist, key=len)
        return max(alllist, key=len)

    def doFitLinacQuick(self, allData):
        cutData = self.cutDataLinacQuick(allData)
        x, y, std = zip(*cutData)
        crest_phase = np.mean(x) - 180 + self.fitOffset
        if crest_phase > 180:
            crest_phase -= 360
        if crest_phase < -180:
            crest_phase += 360
        crest_phase = np.round(crest_phase, decimals=1)
        print crest_phase

if __name__ == '__main__':
    test = testClass()
    f = h5py.File('mytestfile.hdf5', 'r')
    allData = list(zip(f['xData'], f['yData'], f['yStd']))
    test.doFitLinacQuick(allData)

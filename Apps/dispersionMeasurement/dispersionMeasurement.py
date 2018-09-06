import model as model
import sys, time
import numpy as np
sys.path.append("../../../")
from Software.Utils.dict_to_h5 import *
dm = model.Model()

timestr = time.strftime("%H%M%S")
dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\'
summary = {}
data, result = dm.measureDispersion(stepSize=100, nSamples=10, start=12500, end=13500, BA1=False)
summary = {}
summary['data'] = data
summary['result'] = result
for a in result:
	print a, ' = ', result[a]['fit']
save_dict_to_hdf5(summary, dir+timestr+'_'+'DispersionMeasurement.h5')

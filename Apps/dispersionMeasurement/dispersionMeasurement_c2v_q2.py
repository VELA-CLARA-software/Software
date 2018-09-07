import model as model
import sys, time
import numpy as np
sys.path.append("../../../")
from Software.Utils.dict_to_h5 import *
dm = model.Model()

timestr = time.strftime("%H%M%S")
dir = '\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Work\\'+time.strftime("%Y\\%m\\%d")+'\\'
quaddata = {}
for qI in np.arange(-45,-33,1):
	dm.machine.setQuad('C2V-QUAD2', qI)
	data, result = dm.measureDispersion(stepSize=100, nSamples=10, start=12500, end=13500, BA1=False)
	quaddata[str(qI)] = {}
	quaddata[str(qI)]['data'] = data
	quaddata[str(qI)]['result'] = result
	quaddata[str(qI)]['I'] = float(qI)
	print result
	save_dict_to_hdf5(result, dir+timestr+'_'+'DispersionMeasurement.h5')

save_dict_to_hdf5(quaddata, dir+timestr+'_'+'DispersionMeasurement_Summary.h5')

import epics
import time
import numpy

def getPV(name):
    val = epics.caget(name)
    time.sleep(0.1)
    return val
    
n_avgs = 100
pv_name = 'CLA-VCA-DIA-CAM-01:ANA:Intensity_RBV'
print 'Taking average of {n_avgs} readings of {pv_name}...'.format(**locals())
mean_val = numpy.mean([getPV(pv_name) for i in range(n_avgs)])
print 'Average value: {mean_val}'.format(**locals())

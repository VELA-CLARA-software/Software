import epics
import numpy
import time


while True:
	start = time.clock()
	wcmQ=[float(1.0)]*20
	# for i in range(0,19999):
		# wcmQ.append[i]
	p=epics.PV('EBT-TST-SCOPE-01')
	
	p.put( numpy.arange(10)/5.0 )
	print p.get(), 1

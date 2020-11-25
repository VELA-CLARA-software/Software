# Instructions for logging scope values to EPICS:

# Use the script lecroy.py on the velascope02 desktop - 
# just double click and it should log the following values to EPICS:
	# WCM - EBT-INJ-SCOPE-01:P1
	# ICT - EBT-INJ-SCOPE-01:P2
import epics
import numpy
import time


while True:
	start = time.clock()
	wcmQ=[1]*2055
	# for i in range(0,19999):
		# wcmQ.append[i]
	
	print len(wcmQ)
	epics.caput( 'EBT-TST-SCOPE-01', wcmQ )

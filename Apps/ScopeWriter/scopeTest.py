import sys,os
import time
# sys.path.append('\\\\fed.cclrc.ac.uk\\Org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\Release')
import csv
import VELA_CLARA_Scope_Control as vcsc
import VELA_CLARA_Vac_Valve_Control as vcvvc
import epics

def main():
	# initialise the scope controller
	s=vcsc.init()
	v=vcvvc.init()
	# create a scope controller object for the VELA injector (we write EPICS process variables to these values)
	scopeController = s.getScopeController(vcsc.MACHINE_MODE.PHYSICAL, vcsc.MACHINE_AREA.VELA_INJ)
	# vacValveController = v.getVacValveController(vcvvc.MACHINE_MODE.OFFLINE, vcvvc.MACHINE_AREA.CLARA_PH1)
	numShotsBeforeAfter = 10
	numShotsDuring = 10
	# "WVF01" is the name of the oscilloscope as defined in the .config file (details...)
	wv01 = "WVF01"
	# these are EPICS PV types defined in our library
	tr1 = vcsc.SCOPE_PV_TYPE.TR1
	tr2 = vcsc.SCOPE_PV_TYPE.TR2
	tr3 = vcsc.SCOPE_PV_TYPE.TR3
	tr4 = vcsc.SCOPE_PV_TYPE.TR4
	
	# now we open a vacuum valve
	# NOTE!!!!!!!! THESE ARE COMMENTED OUT BECAUSE I WOULDN'T RECOMMEND OPENING VACUUM VALVES REMOTELY FROM YOUR COMPUTER
	# YOU CAN DO THIS, BUT YOU SHOULDN'T BE ABLE TO
	# vacValveController.openVacValve('S02-VALV-01')
	# while vacValveController.isClosed('S02-VALV-01'):
		# time.sleep(0.1)
	print 'valve open'
	
	# monitor the scope waveforms for numshots
	traceDataValveOpen1 = monitorScopes( numShotsBeforeAfter, scopeController )
	# now we have a set of four vectors of vectors (100 waveforms of 2000 points for 4 scope channels).
	# we access them as such:
	trace1 = traceDataValveOpen1[tr1]
	trace2 = traceDataValveOpen1[tr2]
	trace3 = traceDataValveOpen1[tr3]
	trace4 = traceDataValveOpen1[tr4]
	print len(trace1)
	
	# rinse and repeat with the valve closed
	# NOTE!!!!!!!! THESE ARE COMMENTED OUT BECAUSE I WOULDN'T RECOMMEND OPENING VACUUM VALVES REMOTELY FROM YOUR COMPUTER
	# YOU CAN DO THIS, BUT YOU SHOULDN'T BE ABLE TO
	# vacValveController.closeVacValve('S02-VALV-01')
	# while vacValveController.isOpen('S02-VALV-01'):
		# time.sleep(0.1)
	print 'valve closed'
	
	# monitor the scope waveforms for numshots
	traceDataValveClosed = monitorScopes( numShotsDuring, scopeController )
	# now we have a set of four vectors of vectors (100 waveforms of 2000 points for 4 scope channels).
	# we access them as such:
	for row in traceDataValveClosed[tr1]:
		trace1.append(row)
	for row in traceDataValveClosed[tr2]:
		trace2.append(row)
	for row in traceDataValveClosed[tr3]:
		trace3.append(row)
	for row in traceDataValveClosed[tr4]:
		trace4.append(row)
	# trace1.append = traceDataValveClosed[tr1]
	# trace2.append = traceDataValveClosed[tr2]
	# trace3.append = traceDataValveClosed[tr3]
	# trace4.append = traceDataValveClosed[tr4]
	print len(trace1)
	# now we open a vacuum valve
	# NOTE!!!!!!!! THESE ARE COMMENTED OUT BECAUSE I WOULDN'T RECOMMEND OPENING VACUUM VALVES REMOTELY FROM YOUR COMPUTER
	# YOU CAN DO THIS, BUT YOU SHOULDN'T BE ABLE TO
	# vacValveController.openVacValve('S02-VALV-01')
	# while vacValveController.isClosed('S02-VALV-01'):
		# time.sleep(0.1)
	print 'valve open'
	
	# monitor the scope waveforms for numshots
	traceDataValveOpen2 = monitorScopes( numShotsBeforeAfter, scopeController )
	# now we have a set of four vectors of vectors (100 waveforms of 2000 points for 4 scope channels).
	# we access them as such:
	for row in traceDataValveOpen2[tr1]:
		trace1.append(row)
	for row in traceDataValveOpen2[tr2]:
		trace2.append(row)
	for row in traceDataValveOpen2[tr3]:
		trace3.append(row)
	for row in traceDataValveOpen2[tr4]:
		trace4.append(row)
	print len(trace1)
 
	with open("output.csv", "wb") as f:
		writer = csv.writer(f)
		writer.writerows(['trace1'])
		for rows in trace1:
			writer.writerows([rows])
		writer.writerows(['trace2'])
		for rows in trace2:
			writer.writerows([rows])
		writer.writerows(['trace3'])
		for rows in trace3:
			writer.writerows([rows])
		writer.writerows(['trace4'])
		for rows in trace4:
			writer.writerows([rows])

def monitorScopes( numshots, scopeController ):
	numshots = numshots
	wv01 = "WVF01"
	# this is a function for recording waveforms into a map of 2d vectors
	scopeController.monitorTracesForNShots( numshots )
	time.sleep(1)
	while scopeController.isMonitoringScopeTraces( wv01 ):
		time.sleep(0.1)
	allTraces = scopeController.getScopeTraceDataStruct(wv01)
	print numshots, ' shots collected'

	return allTraces.traceData

		
if __name__ == "__main__":
	main()

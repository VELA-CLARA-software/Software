import epics, time
import numpy as np

sol2_pv = epics.PV('CLA-GUN-MAG-SOL-02:SETIOUT')

max_current = 155 # the nominal setting of the solenoid Max 250, (or maybe 300) 
Amplitude  = 25 # +- Amps from nominal_current (peak of sin wave)

numPoints = Amplitude # number of points per period 
wait_time = 2 # time in seconds between set points

current_changes = []

for point in range(0, numPoints):
	current_changes.append( Amplitude * np.sin( ( 2*np.pi / numPoints) * point ) )
	#print current_changes[point]

print 'Solenoid Wobbler Active: Amplitude range +-', Amplitude, ' time period   = ', numPoints*wait_time,' seconds'

if sol2_pv.get() < (max_current - Amplitude):
	while sol2_pv.get() < (max_current - Amplitude):
		sol2_pv.put( sol2_pv.get() + 1 )	
		time.sleep( 0.5*wait_time )
elif sol2_pv.get() > (max_current - Amplitude):
	while sol2_pv.get() > (max_current - Amplitude):
		sol2_pv.put( sol2_pv.get() - 1 )	
		time.sleep( 0.5*wait_time )
 	
while True:	
	for current in current_changes:
		new_val = max_current - Amplitude + current
		sol2_pv.put( new_val )	
		time.sleep( wait_time )

	
	

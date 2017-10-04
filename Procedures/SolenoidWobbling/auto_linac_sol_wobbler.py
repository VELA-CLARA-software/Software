import epics, time
import numpy as np

sol1_pv = epics.PV('CLA-L01-MAG-SOL-01:SETI')
sol2_pv = epics.PV('CLA-L01-MAG-SOL-02:SETI')

nominal_current = 0 # the nominal setting of the solenoid Max 250, (or maybe 300) 
Amplitude  = 150 # +- Amps from nominal_current (peak of sin wave)

numPoints = 2*Amplitude # number of points per period 
wait_time = 1 # time in seconds between set points

current_changes = []

for point in range(0, numPoints):
    current_changes.append( Amplitude * np.sin( ( 2*np.pi / numPoints) * point ) )
    #print current_changes[point]

print 'Solenoid Wobbler Active: Amplitude range +-', Amplitude, ' time period   = ', numPoints*wait_time,' seconds'

if sol2_pv.get() < (nominal_current) and sol1_pv.get() < (nominal_current):
    while sol2_pv.get() < (nominal_current) and sol1_pv.get() < (nominal_current):
        sol1_pv.put( sol1_pv.get() + 1 )
        sol2_pv.put( sol2_pv.get() + 1 )    
        time.sleep( 0.5*wait_time )
elif sol2_pv.get() > (nominal_current) and sol1_pv.get() > (nominal_current):
    while sol2_pv.get() > (nominal_current) and sol1_pv.get() > (nominal_current):
        sol1_pv.put( sol1_pv.get() - 1 )    
        sol2_pv.put( sol2_pv.get() - 1 )    
        time.sleep( 0.5*wait_time )
    
while True: 
    for current in current_changes:
        new_val = nominal_current + current
        
        sol1_pv.put( new_val )  
        sol2_pv.put( new_val )  
        
        time.sleep( wait_time )

    
    
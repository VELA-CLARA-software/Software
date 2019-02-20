#!/usr/bin/env python
# -*- coding: utf-8 -*-
from functions import * # not pythonic but meh



# if open_shutter1():
#     print('shutter opened')
#
# if close_shutter1():
#     print('shutter closed')



s1_1 = 'S01-SCR-01'
s2_1 = 'S02-SCR-01'
s2_2 = 'S02-SCR-02'
s2_3 = 'S02-SCR-03'


#screen_in(s1_1, 60)
#rf_cage_in(s1_1, 60)



#screen_in(s2_1, 600)
#rf_cage_in(s2_1, 600)

#screen_in(s2_2, 60)
#rf_cage_in(s2_2, 60)






mag_names = [ 'S02-QUAD1', 'S02-QUAD2', 'S02-QUAD3',  'S02-QUAD4', 'S02-QUAD5' ]



mag_values=[
[-5.4853,	3.9678,	 3.3011, -3.1291,	-0.88653,	'N'],
[-5.4853,	3.9678,	 1.2217, -1.3709,	-1.0482,	'D'],
[-5.4853,	3.9678,	 3.9337, -3.1291,	-1.0482,	'N'],
[-5.4853,	3.9678,	 3.6178, -2.0133,	-1.6926,	'D'],
[-5.4853,	3.9678,	 5.3468, -6.4255,	 1.8679,	'N'],
[-5.4853,	3.9678,	-6.1221,  5.3485,	-2.3331,	'D'],
[-5.4853,	3.9678,	 4.7204, -1.3709,	-2.3331,	'D'],
[-5.4853,	3.9678,	 5.503,	 -1.853,	-2.4928,	'N'],
[-5.4853,	3.9678,	 6.1265, -8.2836,	-2.4928,	'N'],
[-5.4853,	3.9678,	 7.058,	 -9.8221,	 2.5075,	'N'],
[-5.4853,	3.9678,	 7.058,	 -9.6685,	 3.4608,	'D'],
[-5.4853,	3.9678,	-6.7436,  6.4399,	-3.9203,	'D'],
[-5.4853,	3.9678,	-6.7436,  6.7506,	-4.2356,	'N'],
[-5.4853,	3.9678,	-6.1221,  6.2843,	-4.5502,	'D'],
[-5.4853,	3.9678,	-7.2084,  7.3707,	-4.7072,	'N'],
[-5.4853,	3.9678,	-6.7436,  7.0609,	-4.8641,	'D'],
[-5.4853,	3.9678,	-7.5178,  7.2158,	-5.0209,	'N'],
[-5.4853,	3.9678,	-6.1221,  6.5953,	-5.0209,	'D'],
[-5.4853,	3.9678,	 6.1265, -8.2836,   -5.1775,	'N'],
[-5.4853,	3.9678,	 7.058,	 -9.515,	 5.3485,	'N'],
[-5.4853,	3.9678,	-5.8106,  6.5953,	-5.6465,	'D'],
[-5.4853,	3.9678,	-7.2084,  7.3707,	-5.9584,	'N'],
[-5.4853,	3.9678,	-7.5178,  7.6801,	-6.5809,	'N'],
[-5.4853,	3.9678,	 6.1265, -7.8204,   -6.8914,	'D'],
[-5.4853,	3.9678,	-9.2124,  8.7602,	-8.1293,	'N'],
[-5.4853,	3.9678,	 6.5928, -8.4378,   -8.1293,	'D'],
[-5.4853,	3.9678,	-10.745,  9.3755,	-8.2836,	'N'],
[-5.4853,	3.9678,	-8.2894,  8.4521,	-8.5919,	'D'],
[-5.4853,	3.9678,	 6.5928, -8.2836,	-8.7459,	'D'],
[-5.4853,	3.9678,	 6.4375, -7.9749,   -9.0538,	'D'],
[-5.4853,	3.9678,	 6.5928, -8.1293,	-9.2076,	'N'],
[-5.4853,	3.9678,	-8.7513,  9.068,	-10.742,	'N'],
[-5.4853,	3.9678,	 6.1265, -7.5111,	-11.812,	'D'],
[-5.4853,	3.9678,	-8.1353,  9.2218,	-12.271,	'N'],
[-5.4853,	3.9678,	 7.9854, -10.895,	 14.723,	'D'],
[-5.4853,	3.9678,	 7.058,	 -10.895,	-15.013,	'D'],
[-5.4853,	3.9678,	 7.6767, -13.491,	-15.013,	'N'],
[-5.4853,	3.9678,	-8.5974,  15.18,	 15.18,	    'N'],
[-5.4853,	3.9678,	 7.8311, -10.589,	 15.18,	    'D'],
[-5.4853,	3.9678,	 7.6767, -13.491,	-15.622,	'D']]


#screen_names = [ 'S01-SCR-01', 'S02-SCR-01', 'S02-SCR-02',  'S02-SCR-03' ]
screen_names = [ 'S02-SCR-01', 'S02-SCR-02',  'S02-SCR-03' ]


set_magnets(['S02-QUAD2'],[8.023])

is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)
is_ri_steady('S02-QUAD2',0)


raw_input()
raw_input()
raw_input()
raw_input()

########################################################################
#STARTUP
########################################################################
# print('Start-up moving screens in and degaussing')
# degauss(magnets = mag_names)
# screens_in(screens=screen_names)
# wait_for_screen_in(screens=screen_names)
# wait_for_degaussing(magnets = mag_names)
#

screens_in(screens=screen_names)
wait_for_screen_in(screens=screen_names)
print('screens in and degaussed, getting images ')
for screen in screen_names:
     get_image(screen_names[0],10)
     rf_cage_in_and_wait(screen_names[0],45)

screens_in(screens=screen_names)
wait_for_screen_in(screens=screen_names)

smv = [-5.4853,	3.9678]
smt = [-0.001,	0.001]
sm  = [ 'S02-QUAD1', 'S02-QUAD2']

set_magnets_and_wait(mag_names= sm, mag_values = smv, tolerance= smt, timeout = 100)



raw_input()

#
# Startup
# all mags off = 0
# degauss,
# screens 1-1,2-1,2-2,2-3 in
# take images
# screens 2-1,2-2,2-3 in
# set q1, q2
# take images 2-1,2-2,2-3
#

#startup








raw_input()
raw_input()
raw_input()
raw_input()
raw_input()


mag_tolerance =[0.1] * len(mag_names)  # NB can be set for each individual magnet !!
mag_set_timeout = 30

for value in mag_values:
    if set_magnets_and_wait(mag_names, value, mag_tolerance, mag_set_timeout):
        print('Set Magnets Success')
    else:
        print('Set Magnets Fail')



raw_input()



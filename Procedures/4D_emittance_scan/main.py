#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from datetime import datetime
import sys
from functions import * # not pythonic but meh
from shutil import copyfile



#########################################
# GLOBALS
########################################
start_time = time.time()
now = datetime.now()
date_time = now.strftime("%Y-%m-%d-%H-%M-%S")
log_file = 'emittance_log_' + date_time + '.txt'
message('New run: Time Stamp = ' + str(date_time),header=True, log_file = log_file)
log_message = ''
message(log_message,log_file = log_file)

num_beam_on_images = 10
num_beam_off_images = 10
#Flags for each section of the experiment
should_startup = True
startup_success = False
should_get_quad_off_data = True
get_quad_off_data_success = False
should_get_quad_1_2_on_data = True
get_quad_1_2_on_data_success = False
scan_bc = True

should_degauss_in_main_loop = True

message('num_beam_on_images = ' + str(num_beam_on_images),log_file = log_file)
message('num_beam_off_images = ' + str(num_beam_off_images),log_file = log_file)

wcm_id = 'FAILED'



########################################################################
#STARTUP
########################################################################
def start_up(magnets, screens, log_file ):
    '''
        this function puts all the screens in and deguasses the magnets
        it only returns when they have finished
    :param mag_names: magnets to degauss
    :param all_screen_names: screens to put in
    :return:
    '''
    message('start_up called', header=True, log_file=log_file)
    message('start_up: Passed magnets = ' + ",".join(magnets),log_file=log_file)
    message('start_up: Passed screens = ' + ",".join(screens),log_file=log_file)
    global num_beam_on_images
    # vc_images = get_image('VIRTUAL_CATHDOE', num_beam_on_images)
    # if vc_images != 'FAILED':
    #     message('start_up: Got Virtual Cathode Images fn = ' + vc_images,log_file=log_file)
    # else:
    #     message('!!!ERROR!!! start_up: Get Virtual Cathode Images FAILED')
    #     raw_input()

    message('start_up: Close shutter1',log_file=log_file)
    close_shutter1()
    message('start_up: moving screens in and degauss magnets',log_file=log_file)
    degauss(magnets = magnets)
    screens_in(screens=screens)
    wait_for_screens_in(screens=screens)
    wait_for_degaussing(magnets = magnets)
    message('startup complete', log_file=log_file)
    return True

if should_startup:
    message('start_up: start_WCM_bufffer',log_file=log_file)
    wcm_id = start_WCM_bufffer(buffersize=20000)
    message('start_up: WCM = ' + str(get_wcm_value(wcm_id)),log_file=log_file)

    magnets  = ['S02-QUAD1', 'S02-QUAD2', 'S02-QUAD3', 'S02-QUAD4', 'S02-QUAD5']
    screens = ['S01-SCR-01', 'S02-SCR-01', 'S02-SCR-02', 'S02-SCR-03']
    startup_success = start_up(magnets=magnets, screens=screens, log_file=log_file)
else:
    startup_success = True


########################################################################################
# ALL QUADS OFF DATA
########################################################################################
def get_quad_off_data( screens, log_file ):
    message('get_quad_off_data called', header=True, log_file=log_file)
    message('get_quad_off_data: Passed screens = ' + ",".join(screens),log_file=log_file)
    global num_beam_on_images
    global num_beam_off_images
    for screen in screens:
        get_images_and_screen_out(screen, num_beam_on_images, num_beam_off_images, log_file)
    return True

if should_get_quad_off_data:
    screens = ['S01-SCR-01', 'S02-SCR-01', 'S02-SCR-02']
    get_quad_off_data_success = get_quad_off_data( screens=screens, log_file=log_file)
else:
    get_quad_off_data_success = True



########################################################################################
#  QUADS 1 & 2 ON DATA
########################################################################################

def get_quad_1_2_on_data( screens, magnets, magnet_values, log_file ):
    message('get_quad_1_2_on_data called', header=True, log_file=log_file)
    message('get_quad_1_2_on_data: Passed screens = ' + ",".join(screens),log_file=log_file)
    message('get_quad_1_2_on_data: Passed magnets = ' + ",".join(magnets),log_file=log_file)
    message('get_quad_1_2_on_data: Passed magnet_values = ' + ','.join(str(e) for e in
                                                                       magnet_values),log_file=log_file)
    screens_in(screens=screens)
    if set_magnets_and_wait(mag_names=magnets, mag_values=magnet_values, tolerance=0.01,
                            timeout=100):
        message('get_quad_1_2_on_data: Magnets Settled', log_file=log_file)
    else:
        message('!!!ERROR!!! get_quad_1_2_on_data: set_magnets_and_wait Failed')
        raw_input()

    if wait_for_screens_in(screens=screens):
        message('get_quad_1_2_on_data: Screens in ', log_file=log_file)
    else:
        message('!!!ERROR!!! get_quad_1_2_on_data: wait_for_screen_in Failed')
        raw_input()
    for screen in screens:
        get_images_and_screen_out(screen, num_beam_on_images, num_beam_off_images, log_file)
    get_images('S02-SCR-02', num_beam_on_images, num_beam_off_images, log_file)
    return True

if should_get_quad_1_2_on_data:
    screens = ['S02-SCR-01', 'S02-SCR-02']
    magnets = ['S02-QUAD1', 'S02-QUAD2']
    values = [-5.4853,	3.9678]
    get_quad_1_2_on_data_success = get_quad_1_2_on_data( screens=screens, magnets= magnets,
                                                         magnet_values =values, log_file=log_file)
else:
    get_quad_1_2_on_data_success = True




########################################################################################
#  QUADS 1 & 2 ON DATA
#######################################################################################
# MAIN LOOP

def main_loop(magnets, values, log_file):
    message('main_loop called', header=True, log_file=log_file)
    message('main_loop: Passed magnets = ' + ",".join(magnets),log_file=log_file)
    message('main_loop: Passed values  = ' + ','.join(str(e) for e in values)+', tolerance = ', log_file=log_file)
    global num_beam_on_images
    global should_degauss_in_main_loop
    global num_beam_off_images
    for i,setting in enumerate(values):
        message('main_loop: Setting ' + str(i) + '/' +str(len(values)), log_file=log_file)
        vals = setting[:-1]
        message('main_loop: Setting Quad Magnets to = ' + ','.join(str(e) for e in vals),
                log_file=log_file)
        if set_magnets_and_wait(mag_names=magnets, mag_values=vals, tolerance=0.01, timeout=100):
            message('main_loop: set_magnets_and_wait success')

            if scan_bc:
                for:
                    message('main_loop: Setting Quad Magnets to = ' + ','.join(str(e) for e in vals),
                    log_file=log_file)

            if set_magnets_and_wait(mag_names=magnets, mag_values=vals, tolerance=0.01,
                                    timeout=100):
            else:
                get_images('S02-SCR-03', num_beam_on_images, num_beam_off_images, log_file)
        else:
            message('!!!ERROR!!! main_loop: set_magnets_and_wait Failed')
            raw_input()

        if should_degauss_in_main_loop:
            if setting[-1] == "D":
                tstart = time.time()
                fast_degauss(magnets)
                message('Degaussing took ' + str( time.time() - tstart ))

                # we need a pause here, to make sure the isDeguassing signal is updated
                # this can be long ...


                #degauss(magnets)
                # time.sleep(10)
                # if wait_for_degaussing(magnets = magnets):
                #     message('main_loop: degaussed magnets')
                # else:
                #     message('!!!ERROR!!! main_loop: wait_for_degaussing Failed')
                #     raw_input()


        elif setting[-1] == "D":
            message('WE SHOULD DEGUASS HERE')

        message('main_loop: moving to next step.', log_file=log_file)
    return True


mag_values = [
[ 3.3011, -3.1291,	-0.88653,	'N'],
[ 1.2217, -1.3709,	-1.0482,	'D'],
[ 3.9337, -3.1291,	-1.0482,	'N'],
[ 3.6178, -2.0133,	-1.6926,	'D'],
[ 5.3468, -6.4255,	 1.8679,	'N'],
[-6.1221,  5.3485,	-2.3331,	'D'],
[ 4.7204, -1.3709,	-2.3331,	'D'],
[ 5.503,  -1.853,	-2.4928,	'N'],
[ 6.1265, -8.2836,	-2.4928,	'N'],
[ 7.058,  -9.8221,	 2.5075,	'N'],
[ 7.058,  -9.6685,	 3.4608,	'D'],
[-6.7436,  6.4399,	-3.9203,	'D'],
[-6.7436,  6.7506,	-4.2356,	'N'],
[-6.1221,  6.2843,	-4.5502,	'D'],
[-7.2084,  7.3707,	-4.7072,	'N'],
[-6.7436,  7.0609,	-4.8641,	'D'],
[-7.5178,  7.2158,	-5.0209,	'N'],
[-6.1221,  6.5953,	-5.0209,	'D'],
[ 6.1265, -8.2836,  -5.1775,	'N'],
[ 7.058,  -9.515,	 5.3485,	'N'],
[-5.8106,  6.5953,	-5.6465,	'D'],
[-7.2084,  7.3707,	-5.9584,	'N'],
[-7.5178,  7.6801,	-6.5809,	'N'],
[ 6.1265, -7.8204,  -6.8914,	'D'],
[-9.2124,  8.7602,	-8.1293,	'N'],
[ 6.5928, -8.4378,  -8.1293,	'D'],
[-10.745,  9.3755,	-8.2836,	'N'],
[-8.2894,  8.4521,	-8.5919,	'D'],
[ 6.5928, -8.2836,	-8.7459,	'D'],
[ 6.4375, -7.9749,  -9.0538,	'D'],
[ 6.5928, -8.1293,	-9.2076,	'N'],
[-8.7513,  9.068,	-10.742,	'N'],
[ 6.1265, -7.5111,	-11.812,	'D'],
[-8.1353,  9.2218,	-12.271,	'N'],
[ 7.9854, -10.895,	 14.723,	'D'],
[ 7.058,  -10.895,	-15.013,	'D'],
[ 7.6767, -13.491,	-15.013,	'N'],
[-8.5974,  15.18,	 15.18,	    'N'],
[ 7.8311, -10.589,	 15.18,	    'D'],
[ 7.6767, -13.491,	-15.622,	'N']]



bc_values = [ 0.00, 1.40, -1.40, 2.80, -2.80, 4.20, -4.20, 5.60, -5.60 ,7.00, -7.00 ]



magnets = ['S02-QUAD3', 'S02-QUAD4', 'S02-QUAD5']
screen  = ['S02-SCR-03' ]


main_loop(magnets = magnets, values = mag_values, log_file = log_file)


message('MainLoop Complete, dumping WCM data')
dump_wcm_data(id = wcm_id, log_file=log_file)

message('WCM Data dumped, copying console log')

copyfile('console_log.txt', 'console_log_' + date_time + '.txt')


message('Total Time Take = ' + str(time.time() - start_time))
message('FIN FIN FIN FIN FIN ',header = True)


raw_input()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys,os
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\')
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')

import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Shutter_Control as shut
import VELA_CLARA_Screen_Control as scr
import VELA_CLARA_Camera_Control as cam
import VELA_CLARA_Magnet_Control as mag



# sys.stdout.write('Getting PIL controller')
# sys.stdout.write(a)
# sys.stdout.flush()
#
print('Getting PIL controller')
init = pil.init()
#init.setVerbose()
pil_control = init.physical_PILaser_Controller()
print('Getting PIL controller COMPLETE')
#
# print('Getting Shutter controller')
# initShut = shut.init()
# #initShut.setVerbose()
# shut_control = initShut.physical_PIL_Shutter_Controller()
# print('Getting Shutter controller COMPLETE')
#

print('Getting Magnet controller')
maginit = mag.init()
#maginit.setVerbose()
mag_control = maginit.physical_CLARA_PH1_Magnet_Controller()
print('Getting Magnet controller COMPLETE')

# print('Getting Camera controller')
# initCam = cam.init()
# #initCam.setVerbose()
# cam_control = initCam.physical_Camera_Controller()
# print('Getting Camera controller COMPLETE')

print('Getting Camera controller')
initScr = scr.init()
#initCam.setVerbose()
scr_control = initScr.physical_Screen_Controller()
print('Getting Camera controller COMPLETE')



def set_magnets_and_wait(mag_names, mag_values, tolerance, timeout = 30):
    ''' assume dict is keys = mag_names, and values = si_value'''
    # set magnets
    global mag_control
    print('set_magnets_and_wait called, ')
    if len(mag_names) != len(mag_values):
        print('len(mag_names) != len(mag_values), ERROR ')
        return False
    else:
        print('Mag Names  = ', mag_names)
        print('Mag Values = ', mag_values)
        print('tolerance  = ', tolerance)
        print( )

        settled =  mag_control.setSI( mag_names, mag_values, tolerance,  timeout )
        print settled
        print mag_names

        if settled == mag_names:
            return True
        return False

    #     #
    #     # wait to see if they are set
    #     max_wait_time = time.time() + 45# MAGIC_NUMBER 45 second waiting time
    #     timeout = False
    #     while True:
    #         has_settled  = [False] * len(mag_names)
    #         for i, (magnet, value) in enumerate(zip(mag_names, mag_values)):
    #             has_settled[i] = mag_control.isRIequalVal(magnet, value, tolerance )
    #         if all(has_settled):
    #             break
    #         if time.time() > max_wait_time:
    #             timeout = True
    #             break
    #         time.sleep(0.1)
    # return not timeout



def open_shutter1():
    s = 'SHUT01' # MAGIC_STRING
    pil_control.openAndWait(s, 10) #MAGIC_NUMBER timout time
    return True




def close_shutter1():
    s = 'SHUT01' # MAGIC_STRING
    pil_control.closeAndWait(s,10) #
    return True



def screen_in(screen, timeout):
    print('Moving ',screen, ' YAG IN')
    t0 = time.time()
    scr_control.insertYAG(screen)
    waittime = time.time() + timeout
    has_timed_out = False
    while 1:
        if scr_control.isScreenIn(screen):
            break
        if time.time() > waittime:
            has_timed_out = True
            break
    print('Moving ' + screen + ' YAG IN took (s)', time.time() - t0,' seconds')
    return has_timed_out


def rf_cage_in(screen, timeout):
    print('Moving ', screen,' RF_CAGE IN')
    t0 = time.time()
    scr_control.moveScreenTo(screen, scr.SCREEN_STATE.V_RF)
    waittime = time.time() + timeout
    has_timed_out = False
    while 1:
        #print(scr_control.getScreenState(screen))
        if scr_control.isScreenInState(screen, scr.SCREEN_STATE.V_RF):
            print("RF CAGE IN")
            break
        if time.time() > waittime:
            has_timed_out = True
            break
    print('Moving RF_CAGE,' + screen + ' IN  took (s) ', time.time() - t0)
    return has_timed_out


def degauss(magnets):
    print('Degaussing ,', magnets)
    mag_control.degauss(magnets, True)

    t0 = time.time()
    time.sleep(2)
    while 1:
        #print(scr_control.getScreenState(screen))
        isdeglist =[False] * len(magnets)
        for i, magnet in enumerate(magnets):
            if mag_control.isDegaussing(magnet):
                print(magnet,' is degaussing')
                isdeglist[i] = True
            else:
                print(magnet, ' is NOT degaussing')
        if not any(isdeglist):
            break
    print('Degaussing took (s) ', time.time() - t0)
    return True



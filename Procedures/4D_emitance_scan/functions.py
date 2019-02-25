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


print('Getting Shutter controller')
initShut = shut.init()
#initShut.setVerbose()
shut_control = initShut.physical_PIL_Shutter_Controller()
print('Getting Shutter controller COMPLETE')


print('Getting Magnet controller')
maginit = mag.init()
#maginit.setVerbose()
mag_control = maginit.physical_CLARA_PH1_Magnet_Controller()
print('Getting Magnet controller COMPLETE')

print('Getting Camera controller')
initCam = cam.init()
initCam.setVerbose()
cam_control = initCam.physical_Camera_Controller()
print('Getting Camera controller COMPLETE')

print('Getting Screen controller')
initScr = scr.init()
#initScr.setVerbose()
scr_control = initScr.physical_Screen_Controller()
print('Getting Screen controller COMPLETE')


raw_input()
print('press key to continue')
raw_input()

def message(str, header = False):
    if header:
        print('')
        print('------------------------------')
        print(str)
        print('------------------------------')
        print('')
    else:
        print(str)

def wait_for_acquiring(cam, timeout):
    global cam_control
    message('wait_for_acquiring: Passed ' +  str(cam) + ', timeout = ' + str(timeout))
    if cam_control.isAcquiring(cam):
        return True
    if cam_control.startAcquiring(cam):
        message(cam + ' sent acquiring success')
    else:
        message(cam + ' sent acquiring failure')
    waittime = time.time() + timeout
    isAcquiring = False
    while 1:
        if cam_control.isAcquiring(cam):
            isAcquiring = True
            break
        elif time.time() > waittime:
            break
    return isAcquiring

def wait_for_collectAndSave(cam, num_images):
    global cam_control
    message('wait_for_collectAndSave: Passed ' +  str(cam) + ', numimages = ' + str(num_images))
    success = False
    if cam_control.isAcquiring(cam):
        cam_control.collectAndSave(cam, num_images)
        waittime = time.time() + 60 # MAGIC_NUMBER
        time.sleep(1)
        while 1:
            if cam_control.isCollectingOrSaving(cam):
                message(cam+ ' isBusy == TRUE')
                pass
            else:
                success = True
                message(cam+ ' isBusy == FALSE, wait_for_collectAndSave SUCCESS')
                break
            if time.time() > waittime:
                message('wait_for_collectAndSave timeout 60 seconds :(')
                break
            time.sleep(1)
    return success


def get_image(cam, num_images):
    global cam_control
    message('get_image: passed ' + str(cam) + ' ' + str(num_images))
    # what to return
    dirfn = 'FAILED'
    if wait_for_acquiring(cam, 60):
        if wait_for_collectAndSave(cam, num_images):
            dirfn = cam_control.getLatestDirectory(cam) +  cam_control.getLatestFilename(cam)
            message(cam + ' collected and saved to ' + dirfn)
    else:
        message('!!!FAILED!!! get_image: FALIED TO SET')
    return dirfn

def open_shutter1():
    global shut_control
    s = 'SHUT01' # MAGIC_STRING
    shut_control.openAndWait(s, 10) #MAGIC_NUMBER timout time
    return True

def close_shutter1():
    global shut_control
    s = 'SHUT01' # MAGIC_STRING
    shut_control.closeAndWait(s,10) #
    return True

# def screen_in(screen, timeout):
#     print('Moving ',screen, ' YAG IN')
#     t0 = time.time()
#     scr_control.insertYAG(screen)
#     waittime = time.time() + timeout
#     has_timed_out = False
#     while 1:
#         if scr_control.isScreenIn(screen):
#             break
#         if time.time() > waittime:
#             has_timed_out = True
#             break
#     print('Moving ' + screen + ' YAG IN took (s)', time.time() - t0,' seconds')
#     return has_timed_out


def set_magnets(mag_names, mag_values):
    ''' assume dict is keys = mag_names, and values = si_value'''
    # set magnets
    global mag_control
    print('set_magnets_and_wait called, ')
    if len(mag_names) != len(mag_values):
        print('len(mag_names) != len(mag_values), ERROR ')
        return False
    else:
        return mag_control.setSI( mag_names, mag_values)

def is_ri_steady(magnet, tol, numchecks = 5):
    ri_data = []
    while len(ri_data) < numchecks:
        ri_data.append(mag_control.getRI(magnet))
        time.sleep(0.11)# force this to be greater than the 10Hz magnet SI update
    # find the abs difference between values and mean vlaue
    ri_data[:] = [abs(x - sum(ri_data) / len(ri_data)) for x in ri_data]
    # return mean of abs difference <= tolerance
    return sum(ri_data) / len(ri_data) <= tol

def set_magnets_and_wait(mag_names, mag_values, tolerance, timeout=100):
    if set_magnets(mag_names=mag_names, mag_values=mag_values):
        settled = [False]*len(mag_names)
        waittime = time.time() + timeout
        while 1:
            for i, magnet in enumerate(mag_names):
                if is_ri_steady(magnet, tolerance):
                    message(magnet + ' is settled to tolerance =  '+  str(tolerance))
                    settled[i] = True
                    print settled
                else:
                    pass
            if all(settled):
                print('magnets settled ')
                return True
            elif time.time() > waittime:
                    break
            print('magnet settle loop ')
        return False


def rf_cage_in_and_wait(screen, timeout):
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

def degauss_and_wait(magnets):
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

def degauss(magnets):
    print('Degaussing ,', magnets)
    mag_control.degauss(magnets, True)

def wait_for_degaussing(magnets):
    while 1:
        isdeglist =[False] * len(magnets)
        for i, magnet in enumerate(magnets):
            if mag_control.isDegaussing(magnet):
                print(magnet,' is degaussing')
                isdeglist[i] = True
            else:
                print(magnet, ' is NOT degaussing')
        if not any(isdeglist):
            break
        time.sleep(2)
    print('Degaussing Finished ')
    return True


def screens_in(screens):
    global scr_control
    message('screens_in: Passed ' + ",".join(screens))
    for screen in screens:
        if scr_control.isScreenIn(screen):
            message('screens_in: ' + str(screen) + ' is already in.')
            pass
        else:
            message('screens_in: move ' + str(screen) + ' in')
            scr_control.insertYAG(screen)

def wait_for_screen_in(screens, timeout = 100):
    global scr_control
    t0 = time.time()
    waittime = t0 + timeout
    while 1:
        all_screens_in = True
        for screen in screens:
            if scr_control.isScreenIn(screen):
                message(screen + ' is IN')
                pass
            else:
                message(screen + ' is OUT')
                all_screens_in = False
                break
        if all_screens_in:
            message('All screens are IN ')
            break
        if time.time() > waittime:
            message('Timeout waiting for All screens to go IN ')
            all_screens_in = False
            break
        time.sleep(2)
    return all_screens_in


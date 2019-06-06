#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
import sys
import math
#sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\')
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\')

import VELA_CLARA_PILaser_Control as pil
import VELA_CLARA_Shutter_Control as shut
import VELA_CLARA_Screen_Control as scr
import VELA_CLARA_Camera_Control as cam
import VELA_CLARA_Magnet_Control as mag
import VELA_CLARA_General_Monitor

############################################################################
# MESSAGING & Logging
############################################################################
def message(str, header = False, log_file = ''):
    if header:
        to_write = '\n------------------------------\n'+str+'\n------------------------------\n'
    else:
        to_write=str
    print to_write
    if log_file != '':
        with open(log_file, 'a') as the_file:
            the_file.write(to_write)

############################################################################
############################################################################
# Open and Close Shutter
############################################################################
############################################################################
initShut = shut.init()
#initShut.setVerbose()
shut_control = initShut.physical_PIL_Shutter_Controller()
message('Getting Shutter controller COMPLETE')


def open_shutter1(timeout = 10):
    global shut_control
    return shut_control.openAndWait('SHUT01', timeout)

def close_shutter1(timeout = 10):
    global shut_control
    return shut_control.closeAndWait('SHUT01',timeout) #

############################################################################
############################################################################
# Open and Close Shutter
############################################################################
############################################################################
message('Getting Screen controller')
initScr = scr.init()
#initScr.setVerbose()
scr_control = initScr.physical_Screen_Controller()
message('Getting Screen controller COMPLETE')

def rf_cage_in_and_wait(screen, timeout = 90):
    global scr_control
    message('rf_cage_in_and_wait: Passed ' + screen)
    scr_control.moveScreenTo(screen, scr.SCREEN_STATE.V_RF)
    waittime = time.time() + timeout
    while 1:
        if scr_control.isScreenInState(screen, scr.SCREEN_STATE.V_RF):
            return True
        if time.time() > waittime:
            message('!!!ERROR!!! rf_cage_in_and_wait timed out', header=True)
            return False

def screens_in(screens):
    global scr_control
    message('screens_in: Passed ' + ",".join(screens))
    for screen in screens:
        if scr_control.isScreenIn(screen):
            #message('screens_in: ' + str(screen) + ' is already in.')
            pass
        else:
            #message('screens_in: move ' + str(screen) + ' in')
            scr_control.insertYAG(screen)

def wait_for_screens_in(screens, timeout = 90):
    message('wait_for_screen_in: Passed ' + ",".join(screens))
    global scr_control
    waittime = time.time() + timeout
    while 1:
        all_screens_in = True
        for screen in screens:
            if scr_control.isScreenIn(screen):
                pass
            else:
                all_screens_in = False
                break
        if all_screens_in:
            break
        if time.time() > waittime:
            message('!!!ERROR!!! wait_for_screen_in timed out', header=True)
            all_screens_in = False
            break
        time.sleep(2)
    return all_screens_in

############################################################################
############################################################################
# General Monitoring of he WCM trace, save every value ...
############################################################################
############################################################################
message('Getting General monitor  controller')
gen_mon = VELA_CLARA_General_Monitor.init()
#gen_mon.setVerbose()
message('Getting General monitor COMPLETE')

def start_WCM_bufffer(buffersize = 20000):
    global gen_mon
    message('start_WCM_bufffer', header=True)
    pv = 'CLA-S01-DIA-WCM-01:Q'
    id = gen_mon.connectPV(pv)
    if id == 'FAILED':
        message('!!!ERROR!!! FAILED TO CONNECT to ' +  pv)
        raw_input()
    else:
        message('CONNECTED to ' + pv)
    gen_mon.setBufferSize(id, buffersize)
    message('Buffersize = ', gen_mon.getBufferSize(id))
    return id

def get_WCM_BUFFER(id):
    global gen_mon
    return gen_mon.getBuffer(id)

def get_wcm_counter_and_value(id):
    global gen_mon
    return gen_mon.getCounterAndValue(id)

def get_wcm_value(id):
    global gen_mon
    return gen_mon.getValue(id)

def dump_wcm_data(id, log_file):
    message('dump_wcm_data (timestamp) : (value) ', header=True, log_file=log_file)
    buffer = get_WCM_BUFFER(id)
    for key, value in buffer.iteritems():
        message( key + ' : ' + str(value) , log_file=log_file)


############################################################################
############################################################################
# camera Image Acquisition ...
############################################################################
###########################################################################
message('Getting Camera controller')
initCam = cam.init()
#initCam.setVerbose()
cam_control = initCam.physical_Camera_Controller()
message('Getting Camera controller COMPLETE')

def wait_for_acquiring(cam, timeout = 10):
    global cam_control
    message('wait_for_acquiring: Passed ' +  str(cam) + ', timeout = ' + str(timeout))
    if cam_control.isAcquiring(cam):
        return True
    if cam_control.startAcquiring(cam):
        message(cam + ' sent acquiring success')
    else:
        message(cam + ' sent acquiring failure')
    waittime = time.time() + timeout
    while 1:
        if cam_control.isAcquiring(cam):
            return True
        elif time.time() > waittime:
            return False

def wait_for_collectAndSave(cam, num_images, timeout = 60):
    global cam_control
    message('wait_for_collectAndSave: Passed ' +  str(cam) + ', num_images = ' + str(num_images))
    if cam_control.isAcquiring(cam):
        cam_control.collectAndSave(cam, num_images)
        waittime = time.time() + timeout
        time.sleep(1)
        while 1:
            if cam_control.isCollectingOrSaving(cam):
                pass
            else:
                return True
            if time.time() > waittime:
                message('!!!ERROR!!! wait_for_collectAndSave timed out, cam = ' + str(cam),
                        header=True)
                return False
            time.sleep(1)
    message('!!!ERROR!!! wait_for_collectAndSave: isAcquiring(cam = ' + str(cam) + ') == False',
            header=True)
    return False

def get_image(cam, num_images, timout = 60):
    global cam_control
    message('get_image: Passed cam = ' + str(cam) + ', num_images =  ' + str(num_images))
    # what to return
    dirfn = 'FAILED'
    if wait_for_acquiring(cam, timeout = timout):
        if wait_for_collectAndSave(cam, num_images, timeout= timout):
            dirfn = cam_control.getLatestDirectory(cam) +  cam_control.getLatestFilename(cam)
            message(cam + ' collected and saved to ' + dirfn)
    else:
        message('!!!ERROR!!! get_image: failed to set get acquiring ')
        raw_input()
    return dirfn


def get_images(screen, num_beam_on_images, num_beam_off_images, log_file):
    if open_shutter1():
        message('get_images: Shutter open ', log_file=log_file)
    else:
        message('!!!ERROR!!! get_images: Failed to open shutter')
        raw_input()

    image_acquired = get_image(screen, num_beam_on_images)
    if image_acquired == 'FAILED':
        message('!!!ERROR!!! get_images: get_image Failed for screen = ' + str(screen))
        raw_input()
    message('get_quad_off_data: ' + screen + ' Beam ON Images = ' + str(image_acquired))

    # give the cam daq a breather ... :(
    time.sleep(5)

    if close_shutter1():
        message('get_images: Shutter closed ', log_file=log_file)
    else:
        message('!!!ERROR!!! get_images: Failed to close shutter')
        raw_input()
    # give the cam daq a breather ... :(
    time.sleep(5)

    image_acquired = get_image(screen, num_beam_off_images)
    if image_acquired == 'FAILED':
        message('!!!ERROR!!! get_images: get_image Failed for screen = ' + str(screen))
        raw_input()
    message('get_images: ' + screen + ' Beam OFF Images = ' + str(image_acquired),
            log_file=log_file)


def get_images_and_screen_out(screen, num_beam_on_images, num_beam_off_images, log_file):
    get_images(screen, num_beam_on_images, num_beam_off_images, log_file)
    if rf_cage_in_and_wait(screen, 60):
        message('get_images: ' + str(screen) + ' RF Cage in', log_file=log_file)
    else:
        message('!!!ERROR!!! get_images: rf_cage_in_and_wait Failed for ' + str(screen))
        raw_input()



############################################################################
############################################################################
# Magnet Control
############################################################################
###########################################################################
message('Getting Magnet controller')
maginit = mag.init()
#maginit.setVerbose()
mag_control = maginit.physical_CLARA_PH1_Magnet_Controller()
message('Getting Magnet controller COMPLETE')


def set_magnets(mag_names, mag_values):
    # set magnets
    global mag_control
    message('set_magnets: passed mag_names = '  + ','.join(mag_names) + ',' + ','.join(str(e) for e in mag_values))
    return mag_control.setSI( mag_names, mag_values)

def is_ri_steady(magnets_IN, tol, numchecks = 5):
    # if magnets is not a list make it so:
    if isinstance(magnets_IN,list):
        magnets = magnets_IN
    else:
        magnets = [magnets_IN]
    # ri_data will be a 2d array of RI for each magnet,
    # there will be len(magnets) columns and numchecks rows
    ri_data = []
    # get RI
    while len(ri_data) < numchecks:
        temp = []
        for magnet in magnets:
            temp.append(mag_control.getRI(magnet))
        ri_data.append(temp)
        time.sleep(0.11)# force this to be greater than the 10Hz magnet SI update
    # Transpose ri_data, each row is now aRI data fro a different magnet
    ri_data_T = zip(*ri_data)
    # loop over each magnet (i.e. row) in ri_data_T:
    for data in ri_data_T:
        # find the abs difference between values and mean value
        temp = [abs(x - sum(data) / len(data)) for x in data]
        # if abs differences is greater than tolerance, we have not settled
        if sum(temp) / len(temp) > tol:
            return False
    # if we get here then the magnet RI have settled to tolerance
    return True

def set_magnets_and_wait(mag_names, mag_values, tolerance, timeout=100):
    message('set_magnets_and_wait: Passed mag_names = '+','.join(mag_names) + ',' + ','.join(str(e) for e in
                                                                                    mag_values)+', tolerance = ' + str(tolerance))
    if set_magnets(mag_names=mag_names, mag_values=mag_values):
        waittime = time.time() + timeout
        while 1:
            if is_ri_steady(mag_names, tolerance):
                return True
            if time.time() > waittime:
                message('!!!ERROR!!! set_magnets_and_wait timed out',header=True)
                return False
    return False

def degauss(magnets):
    message('Degaussing ,' +','.join(magnets), True)
    mag_control.degauss(magnets, True)

def wait_for_degaussing(magnets, timeout = 120):
    waittime = time.time() + timeout
    while 1:
        isdeglist =[False] * len(magnets)
        for i, magnet in enumerate(magnets):
            if mag_control.isDegaussing(magnet):
                isdeglist[i] = True
        if not any(isdeglist):
            break
        if time.time() > waittime:
            message('!!!ERROR!!! wait_for_degaussing timed out',header=True)
            return False
        time.sleep(1)
    return True


def fast_degauss(magnets, num_steps =10):
    global mag_control
    values_now = mag_control.getSI(magnets)
    print('values_now ', values_now)
    degauss_max = [math.ceil(abs(x)) * math.copysign(1, x) for x in values_now]
    deg_values = []
    for value in degauss_max:
        temp = []
        for i in range(int(math.floor(num_steps / 2.0 )), 0, -1):
            # print(i)
            # print( float(i) / float(num_steps / 2.0)  )
            # print( (float(i) / float(num_steps / 2.0) )*value )
            #temp.append(  (i / num_steps / 2.0 )  )
            temp.append( round((float(i) / float(num_steps / 2.0) )*value,2) )
            temp.append( -1.0*round((float(i) / float(num_steps / 2.0) )*value,2) )
        # append zero
        temp.append( 0.0 ) # set reversepoalriies
        # flatten
        deg_values.append( temp )
    deg_values_T =  zip(*deg_values)

    for item in deg_values_T:
        set_magnets_and_wait(magnets, list(item), 0.01, 120)

    #print('Deg finished time taken = ', time.time() - tstart )



def scan_bucking_coil(screen, log_file):
    message('scan_bucking_coil called', header=True, log_file=log_file)
    global num_beam_on_images
    global num_beam_off_images
    for i,setting in enumerate(bc_values):
        message('scan_bucking_coil: Setting ' + str(i) + '/' +str(len(values)), log_file=log_file)
        if set_magnets_and_wait(mag_names='LRG-BSOL', mag_values=setting, tolerance=0.01,timeout=100):
            message('scan_bucking_coil: set_magnets_and_wait success')
            get_images(screen, num_beam_on_images, num_beam_off_images, log_file)
        else:
            message('!!!ERROR!!! main_loop: set_magnets_and_wait Failed')
            raw_input()









#
# def degauss_and_wait(magnets):
#     print('Degaussing ,', magnets)
#     mag_control.degauss(magnets, True)
#     t0 = time.time()
#     time.sleep(2)
#     while 1:
#         #print(scr_control.getScreenState(screen))
#         isdeglist =[False] * len(magnets)
#         for i, magnet in enumerate(magnets):
#             if mag_control.isDegaussing(magnet):
#                 print(magnet,' is degaussing')
#                 isdeglist[i] = True
#             else:
#                 print(magnet, ' is NOT degaussing')
#         if not any(isdeglist):
#             break
#     print('Degaussing took (s) ', time.time() - t0)
#     return True





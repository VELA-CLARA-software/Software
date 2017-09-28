#!python2
# -*- coding: utf-8 -*-

"""This is the 'model' component of the Cassis app. It runs a scan of the momentum, solenoid current and 
bucking coil current, and fetches the wall current monitor and beam loss monitor traces at each point, as well as 
the image on Screen 1. Use the cassis.py GUI to control this, or import it into your own program."""

import threading
import zmq
import os
from libtiff import TIFF
from time import time, sleep

context = zmq.Context()
socket = context.socket(zmq.PAIR)
socket.connect('tcp://cdsvbox1:5556')


class DarkCurrentScan(threading.Thread):
    def __init__(self, mag_controller, scope_controller, save_location):
        super(DarkCurrentScan, self).__init__()
        self.magnets = mag_controller
        self.scopes = scope_controller
        self.save_location = save_location
        self.cancel = False

    def startLoop(self, mom_range, sol_range, bc_range, callback):
        """Define the range of momentumm, solenoid and BC current to scan over, and begin a scan."""
        self.cancel = False
        self.mom_range = mom_range
        self.sol_range = sol_range
        self.bc_range = bc_range
        self.n_points = len(mom_range) * len(sol_range) * len(bc_range)
        self.run(callback)

    def stopLoop(self):
        self.cancel = True

    def run(self, callback):
        #TODO: get gun gradient
        sol_current = self.magnets.getSI('SOL')
        bc_current = self.magnets.getSI('BSOL')
        self.run_loop(callback)
        self.magnets.setSI('SOL', sol_current)
        self.magnets.setSI('BSOL', bc_current)

    def run_loop(self, callback):
        i = 0
        for mom in self.mom_range:
            #TODO: lookup momentum and set gun gradient accordingly
            for sol_current in self.parent.sol_range:
                self.magnets.setSI('SOL', sol_current)
                for bc_current in self.parent.bc_range:
                    self.magnets.setSI('BSOL', bc_current)

                    filename = '{}\\mom={:.1f}_sol={:.1f}_bc={.1f}.tif'.format(
                        self.save_location, mom, sol_current, bc_current)
                    traces, img = self.singleGrab(filename)
                    i += 1
                    callback((mom, sol_current, bc_current), traces, img, i / self.n_points)
                    if self.cancel:
                        return

    def singleGrab(self, filename):
        """Do a single dark current point."""
        wcm1 = self.scopes.getScopeTR1Buffer("WVF01")[0]
        wcm2 = self.scopes.getScopeTR2Buffer("WVF01")[0]
        blm1 = self.scopes.getScopeTR3Buffer("WVF01")[0]
        blm2 = self.scopes.getScopeTR4Buffer("WVF01")[0]
        # socket.send(filename)  # send a signal to cdsvbox1 to take an image, and save it
        # wait until file exists and is reasonable size
        start = time()
        while time() - start < 10:  # wait 10 secs
            try:
                if os.path.getsize(filename) > 2 * 2**20:  # at least 2MB, uncompressed TIFFs are more like 10MB
                    break
                sleep(0.1)
            except WindowsError:  # ignore "file not found"
                pass
        else:  # got to the end of the loop!
            raise FileNotFoundError('Timed out waiting for the file "{}" to be created.'.format(filename))
        img = TIFF.open(filename).read_image()
        # resave with compression (approx 3x smaller files!)
        TIFF.open(filename, mode='w').write_image(img, compression='lzw')
        return (wcm1, wcm2, blm1, blm2), img
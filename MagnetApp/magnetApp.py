#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys,logging,socket

import magnetAppGlobals as globals
import magnetAppController
import os

#BE SPECIFIC.... YOUR I.P. FOR YOUR VM
os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"
os.environ["EPICS_CA_SERVER_PORT"]="6000"




class magnetApp(QtGui.QApplication):
    def __init__(self,argv):
        # you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the magnetAppController
        self.controller = magnetAppController.magnetAppController(argv)

if __name__ == '__main__':
    logging.basicConfig(filename=globals.logfile, level=logging.INFO,format='%(asctime)s %(message)s')
    logging.info('Started on ' + socket.gethostname() )
    print "starting magnet app"
    app = magnetApp(sys.argv)
    sys.exit(app.exec_())
    logging.info('Finished on ' + socket.gethostname() )

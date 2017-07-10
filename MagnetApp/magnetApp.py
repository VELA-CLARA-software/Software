#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# Run this and everything follows
from PyQt4 import QtGui
import sys
import os
import logging
import socket
import magnetAppGlobals as globals
import magnetAppController

os.environ["EPICS_CA_SERVER_PORT"]="6000"


class magnetApp(QtGui.QApplication):
    def __init__(self,argv):
        # you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the magnetAppController
        self.controller = magnetAppController.magnetAppController(argv)

if __name__ == '__main__':
    logging.basicConfig(
        filename=globals.logfile,
        level=logging.INFO,
        format='%(asctime)s %(message)s')
    logging.info('Started on ' + socket.gethostname() )
    print "starting magnet app"
    app = magnetApp(sys.argv)
    sys.exit(app.exec_())
    logging.info('Finished on ' + socket.gethostname() )

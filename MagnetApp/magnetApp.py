#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys,logging,socket

import magnetAppController

class magnetApp(QtGui.QApplication):
    def __init__(self,argv):
        # you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the magnetAppController
        self.controller = magnetAppController.magnetAppController(argv)

if __name__ == '__main__':
    logging.basicConfig(filename='magnetTestLog.log', level=logging.INFO,format='%(asctime)s %(message)s')
    logging.info('Started on ' + socket.gethostname() )
    print "starting magnet app"
    app = magnetApp(sys.argv)
    sys.exit(app.exec_())
    logging.info('Finished on ' + socket.gethostname() )

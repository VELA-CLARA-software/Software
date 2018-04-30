#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PyQt4 import QtGui, QtCore
import sys,os,scopeWriterGlobals
import scopeWriterMasterController

class scopeWriterApp(QtGui.QApplication):
    def __init__(self,argv):
        # you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the magnetAppController
        self.controller = scopeWriterMasterController.scopeWriterMasterController(argv)

if __name__ == '__main__':
    print "starting scope writer"
    app = scopeWriterApp(sys.argv)
    sys.exit(app.exec_())

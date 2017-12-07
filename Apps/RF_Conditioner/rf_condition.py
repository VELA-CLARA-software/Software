# RF conditioning Script
# Version 3
# DJS
# This is the main filoe that creates the rf_condition object
# rf_ccondition owns all other objects and does nothing else
from PyQt4 import QtGui
import sys
import master



class rf_condition(QtGui.QApplication):
    def __init__(self,argv):
        # you need this init line here to instantiate a QTApplication
        QtGui.QApplication.__init__(self,argv)
        #QtGui.QWidget.__init__(self, argv)
        # Everything else is handled by the magnetAppController
        self.controller = master.master(argv,config_file = "test.config")

if __name__ == '__main__':
    print('Starting rf_condition Application')
    app = rf_condition(sys.argv)
    sys.exit( app.exec_() )

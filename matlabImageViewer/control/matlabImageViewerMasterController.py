import sys, os
from PyQt4 import QtGui, QtCore
from view.matlabImageLauncherView import matlabImageLauncherView
from view.emittanceMeasurementView import emittanceMeasurementView
from view.energySpreadView import energySpreadView
from control.matlabImageViewerController import matlabImageViewerController

# this class handles everything
class matlabImageViewerMasterController(object):
    def __init__(self):
        self.startLauncher = matlabImageLauncherView()
        self.startLauncher.show()
        self.startLauncher.launcherButton.clicked.connect( self.handle_startviewstartbutton )
        self.startLauncher.measurementTypeSignal.connect( self.handle_measurementTypeSignal ) # User inputs for the controller types
        self.startLauncher.destroyed.connect(self.startLauncher.close) # needed ??
        # initial choices for area and mode are None
        self.measurementType = None
        self.mainView = None
        # timer for mainView GUI update call
        self.widgetUpdateTimer = QtCore.QTimer()
        self.widgetTimerUpdateTime_ms = 200  # MAGIC_NUMBER

    def handle_measurementTypeSignal(self,r):
         self.measurementType = r

    # check to see if the a choice of area and mode has been made
    def areaAndModeSet(self):
        ret = False
        if self.measurementType is not None:
            ret = True
        return ret

    # pressing start, tries to launch a scope controller and build the main view
    def handle_startviewstartbutton(self):
        if self.areaAndModeSet():
            self.startLauncher.update()
            QtGui.QApplication.processEvents();
            # launch main view
            self.launchMainView()
            print "starting"
            self.controller = matlabImageViewerController( self.mainView )
            self.startLauncher.infoLabel.setText("Loading matlab image viewer")
            self.mainViewClose()
        else:
            self.startLauncher.infoLabel.setText("click a measurement type, idiot")

    def launchMainView(self):
        if self.measurementType == "Emittance":
            self.mainView = emittanceMeasurementView()
        elif self.measurementType == "Energy spread":
            self.mainView = energySpreadView()
        self.startLauncher.close()

    def mainViewClose(self):
        self.mainView.closing.connect(self.connectCloseEvents)

    def connectCloseEvents(self):
        self.mainView.close()

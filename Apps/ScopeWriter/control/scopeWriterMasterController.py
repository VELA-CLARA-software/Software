#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys,os,scopeWriterGlobals
import VELA_CLARA_Scope_Control as vcsc

from PyQt4 import QtGui, QtCore
import scopeWriterLauncherView
import scopeWriterView
import scopeWriterController
import scopeWriterLoadView
import scopeWriterSaveView

# this class handles everything
class scopeWriterMasterController(object):
    def __init__(self,argv):
        # initilaize the VELA_CLARA_Scope_Control,
        self.scopeInit = vcsc.init()
        #self.scopeInit.setVerbose()
        # startView and connections
        # the startView is where you select the machine mode and area
        self.startLauncher = scopeWriterLauncherView.scopeWriterLauncherView()
        self.startLauncher.show()
        self.startLauncher.launcherButton.clicked.connect( self.handle_startviewstartbutton )
        self.startLauncher.machineAreaSignal.connect( self.handle_machineAreaSignal ) # User inputs for the controller types
        self.startLauncher.machineModeSignal.connect( self.handle_machineModeSignal )
        self.startLauncher.destroyed.connect(self.startLauncher.close) # needed ??
        # initial choices for area and mode are None
        self.machineArea = None
        self.machineMode = None
        # init objects to none, these get changed depending on the flavour chosen in startView
        self.scopeController = None
        self.mainView = None
        # flag to say if we are connected to any epics, so we know how to handle
        # button presses with NO EPICS connection
        self.activeEPICS = False
        # timer for mainView GUI update call
        self.widgetUpdateTimer = QtCore.QTimer()
        self.widgetTimerUpdateTime_ms = 200  # MAGIC_NUMBER

        self.beamlines = {"VELA_INJ":  vcsc.MACHINE_AREA.VELA_INJ,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA1,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA2,
                          "CLARA_S01": vcsc.MACHINE_AREA.CLARA_S01}
        self.modes = {"Physical": vcsc.MACHINE_MODE.PHYSICAL,
                      "Virtual":  vcsc.MACHINE_MODE.VIRTUAL,
                      "Offline":  vcsc.MACHINE_MODE.OFFLINE}

#          __                 __             .__
#  _______/  |______ ________/  |_     ___  _|__| ______  _  __
# /  ___/\   __\__  \\_  __ \   __\    \  \/ /  |/ __ \ \/ \/ /
# \___ \  |  |  / __ \|  | \/|  |       \   /|  \  ___/\     /
#/____  > |__| (____  /__|   |__|        \_/ |__|\___  >\/\_/
#     \/            \/                               \/
    # these functions handle the start view signals
    # start view radio group 1
    def handle_machineAreaSignal(self,r):
         self.machineArea = r

    def handle_machineModeSignal(self,r):
        self.machineMode = r
        print self.machineMode

    # check to see if the a choice of area and mode has been made
    def areaAndModeSet(self):
        ret = False
        if self.machineArea is not None and self.machineMode is not None:
            ret = True
        return ret

    # pressing start, tries to launch a scope controller and build the main view
    def handle_startviewstartbutton(self):
        if self.areaAndModeSet():
            self.startLauncher.update()
            QtGui.QApplication.processEvents();
            # launch requested scope controller
            self.launchScopeController()
            # launch main view
            self.launchMainView()
            self.loadView = scopeWriterLoadView.scopeWriterLoadView("Load setup", scopeWriterGlobals.scopeSetupLocation)
            self.saveView = scopeWriterSaveView.scopeWriterSaveView()
            self.controller = scopeWriterController.scopeWriterController(self.mainView, self.scopeController, self.loadView, self.saveView)
            self.startLauncher.infoLabel.setText("Loading scope writer")
            self.mainViewClose()
        else:
            self.startLauncher.infoLabel.setText("click a beamline and machine mode, idiot")

    def handle_loadSettings(self):
        self.scopeWriterLoadView.show()
        self.scopeWriterLoadView.activateWindow()

    def launchMainView(self):
        self.mainView = scopeWriterView.scopeWriterView()
        self.mainView.show()
        self.startLauncher.close()

    def mainViewClose(self):
        self.mainView.closing.connect(self.connectCloseEvents)

    def connectCloseEvents(self):
        self.mainView.close()

    def launchScopeController(self):
        self.scopeController = self.scopeInit.getScopeController( self.machineMode, self.machineArea )
        if  self.machineMode is not vcsc.MACHINE_MODE.OFFLINE:
            self.activeEPICS = True

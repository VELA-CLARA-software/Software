#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
#get the magnet enums used to define magnet types and  PSU states
import magnetAppGlobals

import VELA_CLARA_MagnetControl as mag

from PyQt4 import QtGui, QtCore
from GUI_magnetAppStartup import GUI_magnetAppStartup
from GUI_magnetAppMainView import GUI_magnetAppMainView
from GUI_FileLoad import GUI_FileLoad
from GUI_FileSave import GUI_FileSave


dburtLocation = "\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Snapshots\\DBURT\\"
appIcon = 'magpic.jpg'
sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage\\')



# this class handles everything
class magnetAppController(object):
    def __init__(self,argv):
        # initilaize the VELA_CLARA_MagnetControl, from this object we can get all flavours of magnet controller
        self.magInit = mag.init()
        # startView and connections
        # the startView is where you select the machine mode and area
        self.startView = GUI_magnetAppStartup()
        self.startView.show()
        self.startView.startButton.clicked.connect( self.handle_startviewstartbutton )
        self.startView.cancelButton.clicked.connect( self.handle_startviewstartbutton )
        self.startView.machineAreaSignal.connect( self.handle_machineAreaSignal )
        self.startView.machineModeSignal.connect( self.handle_machineModeSignal )
        self.startView.destroyed.connect(self.startView.close) # needed ??
        # initial choices for area and mode
        self.machineArea = 'UNKNOWN'
        self.machineMode = 'UNKNOWN'
        # init objects to none, these get changed depending on the flavour chosen in startView
        self.localMagnetController = None
        self.mainView = None
        # hash table of all mag object references, filled when mainView is created
        self.allMagnetObjReferences = {}
        # flag to say if we are connected to any epics
        self.activeEPICS = False
        # timer for mainView GUI update call
        self.widgetUpdateTimer = QtCore.QTimer()
        # The dburtLoadView and dburtSaveView always exist, we 'show' and 'hide' them where necessary,
        # even calling close on them just hides them, until the mainView is closed
        # DBURT File Load Window
        global dburtLocation
        self.dburtLoadView = GUI_FileLoad("Load DBURT", dburtLocation )
        self.dburtLoadView.setWindowIcon(QtGui.QIcon( appIcon ) )
        self.dburtLoadView.selectButton.clicked.connect(self.handle_fileLoadSelect)
        # DBURT File Save Window
        self.dburtSaveView = GUI_FileSave()
        self.dburtSaveView.setWindowIcon(QtGui.QIcon(appIcon))
        self.dburtSaveView.saveNowButton_2.clicked.connect(self.handle_fileSaveNow)
#          __                 __             .__
#  _______/  |______ ________/  |_     ___  _|__| ______  _  __
# /  ___/\   __\__  \\_  __ \   __\    \  \/ /  |/ __ \ \/ \/ /
# \___ \  |  |  / __ \|  | \/|  |       \   /|  \  ___/\     /
# /____  > |__| (____  /__|   |__|        \_/ |__|\___  >\/\_/
#     \/            \/                               \/
    # these functions handle the start view signals
    # start view radio group
    def handle_machineAreaSignal(self,r):
         self.machineArea = r
    # start view radio group
    def handle_machineModeSignal(self,r):
         self.machineMode = r
    # check to see if the a choice of area and mode has been made
    def areaAndModeSet(self):
        ret = True
        if self.machineArea == 'UNKNOWN':
            ret = False
        if self.machineMode == 'UNKNOWN':
            ret = False
        return ret
    def handle_startviewstartbutton(self):
        if  self.areaAndModeSet():
            # forced update to the startup window showing choices
            self.startView.waitMessageLabel.setText("Building Main Window...Patience is a virtue")
            self.startView.update()
            QtGui.QApplication.processEvents();
            # launch requested magnet controller
            self.launchPythonMagnetController()
            # get magnet names, required to build main view
            # launch main view and add magnets
            self.launchMainView()
            #which magnets get added depends on what machine area you choose...
            self.addMagnetsToMainView()
        else:
            # forced update to the startup window showing error
            self.startView.waitMessageLabel.setText("<font color='red'>ERROR: You must select a Machine Area and Mode "
                                                    "first</font>")
            self.startView.waitMessageLabel.update()
#                .__                  .__
#  _____ _____  |__| ____      ___  _|__| ______  _  __
# /     \\__  \ |  |/    \     \  \/ /  |/ __ \ \/ \/ /
#|  Y Y  \/ __ \|  |   |  \     \   /|  \  ___/\     /
#|__|_|  (____  /__|___|  /      \_/ |__|\___  >\/\_/
#      \/     \/        \/                   \/
  #  # ... and then build the mainView
    def launchMainView(self):
        self.mainView = GUI_magnetAppMainView()
        # set mainView text depending on flavours and mode
        self.setMainViewHeaderText()
        self.mainView.show()
        self.startView.close()
        # connect button signals, some are connected in GUI_magnetAppMainView
        self.mainView.selectedOn.clicked.connect( self.handle_selectedOn )
        self.mainView.selectedOff.clicked.connect( self.handle_selectedOff )
        self.mainView.allOff.clicked.connect( self.handle_allOff )
        self.mainView.allOn.clicked.connect( self.handle_allOn )
        self.mainView.allZero.clicked.connect( self.handle_allZero )
        self.mainView.selectedDegauss.clicked.connect( self.handle_selectedDegauss )
        self.mainView.loadSettings.clicked.connect( self.handle_loadSettings )
        self.mainView.saveSettings.clicked.connect( self.handle_saveSettings )
        # the dburtSaveView needs to know what controller type we are using to write it to the save file
        self.dburtSaveView.controller_type = self.machineArea
        # connect the timer to mainViewUpdate, no threading in this app
        QtCore.QTimer.connect(self.widgetUpdateTimer, QtCore.SIGNAL("timeout()"), self.mainViewUpdate)
        # start timer for 200 ms
        self.widgetUpdateTimer.start(200)
    # update the  mainViewUpdate
    def mainViewUpdate(self):
        # conceivably the timer could restart this function before it completes so guard against that
        try:
            self.mainView.updateMagnetWidgets()
        finally:
            self.widgetUpdateTimer.start(200)
    # mainView buttons
    # some buttons are connected in the GUI_magnetAppMainView, ones tha trequire a magnet controller are handled here
    def handle_selectedOn(self):
        print 'handle_selectedOn'
        if self.activeEPICS:
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(self.mainView.getActiveNames())
            self.localMagnetController.switchONpsu(self.activeMags)
    def handle_selectedOff(self):
        print 'handle_selectedOn'
        if self.activeEPICS:
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(self.mainView.getActiveNames())
            self.localMagnetController.switchOFFpsu(self.activeMags)
    def handle_allOff(self):
        print 'handle_allOff'
        if self.activeEPICS:
            self.localMagnetController.switchOFFpsu(self.allMagNames)
    def handle_allZero(self):
        if self.activeEPICS:
            self.localMagnetController.setSIZero(self.allMagNames)
    def handle_allOn(self):
        print 'handle_allOn'
        if self.activeEPICS:
            self.localMagnetController.switchONpsu(self.allMagNames)
    def handle_selectedDegauss(self):
        print 'handle_selectedDegauss'
        if self.activeEPICS:
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(self.mainView.getActiveNames())
            print 'active magnet widgets'
            print self.activeMags
            self.localMagnetController.degauss(self.activeMags, True)
    def handle_saveSettings(self):
        # dburtSaveView filename is set by current time and date
        self.dburtSaveView.setFileName()
        self.dburtSaveView.show()
        self.dburtSaveView.activateWindow()
    def handle_loadSettings(self):
        self.dburtLoadView.show()
        self.dburtLoadView.activateWindow()
    # set mainview text depending on mode and area chosen in startview
    def setMainViewHeaderText(self):
        self.title = 'Magnet Control for '
        if self.machineArea == 'VELA_INJ':
            self.title += 'VELA Injector Magnets'
        elif self.machineArea == 'VELA_BA1':
            self.title += 'VELA BA1 Magnets'
        elif self.machineArea == 'VELA_BA2':
            self.title += 'VELA BA2 Magnets'
        elif self.machineArea == 'CLARA_INJ':
            self.title += 'CLARA Injector Magnets'
        if self.machineMode == 'physicalMode':
            self.title += ' Connected to the Physical Machine'
        elif self.machineMode == 'virtualMode':
            self.title += ' Connected to the Virtual Machine '
        elif self.machineMode == 'offlineMode':
            self.title += ' No EPICS Connection '
        self.mainView.titleLabel.setText( self.title )
    # more cancer below
    def addMagnetsToMainView(self):
        # get all magnet names
        self.allMagNames = self.localMagnetController.getMagnetNames()
        #iterate over all magnets, and add them to respective lists depending on their magnet type
        for i in self.allMagNames:
            self.allMagnetObjReferences[ i ] = self.localMagnetController.getMagObjConstRef( i )
            if self.localMagnetController.isAQuad( i ):
                self.mainView.addQuad( self.allMagnetObjReferences.get(i) )
                self.mainView.quadWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.quadWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isADip( i ):
                self.mainView.addDip( self.allMagnetObjReferences.get(i) )
                self.mainView.dipWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.dipWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isASol( i ):
                self.mainView.addSol( self.allMagnetObjReferences.get(i) )
                self.mainView.solWidgets[i].magRef.append(self.allMagnetObjReferences[ i ])
                self.mainView.solWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isABSol( i ):
                self.mainView.addSol( self.allMagnetObjReferences.get(i) )
                self.mainView.solWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.solWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isACor(i):
                self.mainView.addCor(self.allMagnetObjReferences.get(i))
                self.mainView.corWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.corWidgets[i].setDefaultOptions()
        self.mainView.mainResize()
        # now we have the mainView, we connect it's close function, this
        # ensures that when the main view is closed all the other views are closed too
        self.mainView.closing.connect(self.connectCloseEvents)
    # the 2 dburt windows can't be closed until this function is called,
    def connectCloseEvents(self):
        self.widgetUpdateTimer.stop()
        self.dburtLoadView.canWindowClose = True
        self.dburtLoadView.close()
        self.dburtSaveView.canWindowClose = True
        self.dburtSaveView.close()
        self.mainView.close()
        print 'Fin - magnetApp closed down'




    def setVM(self):
        os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
        os.environ["EPICS_CA_ADDR_LIST"] = "10.10.0.12"
        os.environ["EPICS_CA_MAX_ARRAY_BYTES"] = "10000000"

    # i hate the way the below few functions work, ... cancer
    def launchPythonMagnetController(self):
        if self.machineMode == 'physicalMode':
            self.launchPhysical()
            self.activeEPICS = True
        elif self.machineMode == 'virtualMode':
            self.setVM()
            self.launchVirtual()
            self.activeEPICS = True
        elif self.machineMode == 'offlineMode':
            self.launchOffline()
        else:
            print 'magnetAppController launchPythonMagnetController ERROR'
    def launchPhysical(self):
        if self.machineArea == 'VELA_INJ':
            self.localMagnetController = self.magInit.physical_VELA_INJ_Magnet_Controller()
        elif self.machineArea == 'VELA_BA1':
            self.localMagnetController = self.magInit.physical_VELA_BA1_Magnet_Controller()
        elif self.machineArea == 'VELA_BA2':
            self.localMagnetController = self.magInit.physical_VELA_BA2_Magnet_Controller()
        elif self.machineArea == 'CLARA_INJ':
            self.localMagnetController = self.magInit.physical_CLARA_INJ_Magnet_Controller()
    def launchVirtual(self):
        if self.machineArea == 'VELA_INJ':
            self.localMagnetController = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        elif self.machineArea == 'VELA_BA1':
            self.localMagnetController = self.magInit.virtual_VELA_BA1_Magnet_Controller()
        elif self.machineArea == 'VELA_BA2':
            self.localMagnetController = self.magInit.virtual_VELA_BA2_Magnet_Controller()
        elif self.machineArea == 'CLARA_INJ':
            self.localMagnetController = self.magInit.virtual_CLARA_INJ_Magnet_Controller()
    def launchOffline(self):
        if self.machineArea == 'VELA_INJ':
            self.localMagnetController = self.magInit.offline_VELA_INJ_Magnet_Controller()
        elif self.machineArea == 'VELA_BA1':
            self.localMagnetController = self.magInit.offline_VELA_BA1_Magnet_Controller()
        elif self.machineArea == 'VELA_BA2':
            self.localMagnetController = self.magInit.offline_VELA_BA2_Magnet_Controller()
        elif self.machineArea == 'CLARA_INJ':
            self.localMagnetController = self.magInit.offline_CLARA_INJ_Magnet_Controller()



    def handle_fileSaveNow(self):
        self.fn = str(self.dburtSaveView.file_name_entry.text())
        self.comments = str(self.dburtSaveView.commentsSection.toPlainText())
        self.keywords = self.dburtSaveView.getComboBoxEntries()
        self.localMagnetController.writeDBURT(self.fn, self.comments, self.keywords)
        self.dburtSaveView.hide()




    def handle_fileLoadSelect(self):
        if self.haveDBurtAndNotInOfflineMode():
            if self.dburtLoadView.dburtType == self.dburtLoadView.allMagnets:
                self.localMagnetController.applyDBURT(self.dburtLoadView.dburtFile)
            elif self.dburtLoadView.dburtType == self.dburtLoadView.quadMagnets:
                self.localMagnetController.applyDBURTQuadOnly(self.dburtLoadView.dburtFile)
            elif self.dburtLoadView.dburtType == self.dburtLoadView.corrMagnets:
                self.localMagnetController.applyDBURTCorOnly(self.dburtLoadView.dburtFile)
        self.dburtLoadView.hide()
        self.dburtLoadView.hide()
        # reset the loadfile
        self.dburtLoadView.dburtFile = ""


    def haveDBurtAndNotInOfflineMode(self):
        self.ret = True
        if self.machineMode == 'offlineMode':
            self.ret = False
        if self.dburtLoadView.dburtFile == "":
            self.ret = False
        return self.ret


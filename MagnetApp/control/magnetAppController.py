#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of MagtnetApp
import os
import VELA_CLARA_Magnet_Control as mag
import magnetAppGlobals as globals
from PyQt4 import QtGui, QtCore
from GUI.GUI_magnetAppStartup import GUI_magnetAppStartup
from GUI.GUI_magnetAppMainView import GUI_magnetAppMainView
from GUI.GUI_FileLoad import GUI_FileLoad
from GUI.GUI_FileSave import GUI_FileSave

# this class handles everything
class magnetAppController(object):
    def __init__(self,argv):
        # initilaize the VELA_CLARA_MagnetControl,
        # from this object we can get all flavours of magnet controller
        self.magInit = mag.init()
        #self.magInit.setVerbose()
        # startView and connections
        # the startView is where you select the machine mode and area
        self.startView = GUI_magnetAppStartup()
        self.startView.show()
        self.startView.startButton.clicked.connect(self.handle_startviewstartbutton)
        self.startView.cancelButton.clicked.connect(self.handle_startviewcancelbutton )
        self.startView.machineAreaSignal.connect(self.handle_machineAreaSignal)
        self.startView.machineModeSignal.connect(self.handle_machineModeSignal)
        self.startView.destroyed.connect(self.startView.close) # needed ??
        # initial choices for area and mode are None
        self.machineArea = None
        self.machineMode = None
        # init objects to none, these get changed depending on the flavour chosen in startView
        self.localMagnetController = None
        self.mainView = None
        # hash table (python dict) of all magobject refs, filled when mainView created
        self.allMagnetObjReferences = {}
        # flag to say if we are connected to any epics, so we know how to handle
        # button presses with NO EPICS connection
        self.activeEPICS = False
        # timer for mainView GUI update call
        self.widgetUpdateTimer = QtCore.QTimer()
        self.widgetTimerUpdateTime_ms = 200  # MAGIC_NUMBER
        # The dburtLoadView and dburtSaveView always exist,
        # we 'show' and 'hide' them where necessary
        # even calling close on them just hides them, until the mainView is closed
        # DBURT File Load Window
        self.dburtLoadView = None
        # self.dburtLoadView = GUI_FileLoad("Load DBURT", globals.dburtLocation2)
        # self.dburtLoadView.setWindowIcon(QtGui.QIcon(globals.appIcon))
        # self.dburtLoadView.selectButton.clicked.connect(self.handle_fileLoadSelect)
        # DBURT File Save Window
        self.dburtSaveView = GUI_FileSave()
        self.dburtSaveView.setWindowIcon(QtGui.QIcon(globals.appIcon))
        self.dburtSaveView.saveNowButton_2.clicked.connect(self.handle_fileSaveNow)
        # this map is used a few places, sodefined here
        # I think there is a c++ method to get this, but the documentation is... meh...
        self.Area_ENUM_to_Text ={
            mag.MACHINE_AREA.VELA_BA1:'VELA_BA1',
            mag.MACHINE_AREA.VELA_BA2:'VELA_BA2',
            mag.MACHINE_AREA.VELA_INJ:'VELA_Injector',
            mag.MACHINE_AREA.CLARA_PH1:'CLARA_PH1'
            # mag.MACHINE_AREA.CLARA_PHASE_1:'CLARA PHASE 1 Magnets',
            }
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
    # start view radio group 2
    def handle_machineModeSignal(self,r):
        self.machineMode = r
    # check to see if the a choice of area and mode has been made
    def areaAndModeSet(self):
        ret = False
        if self.machineArea is not None and self.machineMode is not None:
            ret = True
        return ret
    # pressing start, tries to lanuch a magcontroller and build the main view
    def handle_startviewstartbutton(self):
        if self.areaAndModeSet():
            # forced update to the startup window showing choices
            self.startView.waitMessageLabel.setText(
                "Building Main Window...Patience is a virtue")
            self.startView.update()
            QtGui.QApplication.processEvents()
            # launch requested magnet controller
            self.launchPythonMagnetController()
            # get magnet names, required to build main view
            # launch main view and add magnets
            self.launchMainView()
            #which magnets get added depends on what machine area you choose...
            self.addMagnetsToMainView()
        else:
            # forced update to the startup window showing error
            self.startView.waitMessageLabel.setText(
                "<font color='red'>ERROR: You must select a Machine Area and Mode first</font>")
            self.startView.waitMessageLabel.update()
    # quit from start-up-screen
    def handle_startviewcancelbutton(self):
        QtCore.QCoreApplication.instance().quit()
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
        self.mainView.selectedOn.clicked.connect(self.handle_selectedOn)
        self.mainView.selectedOff.clicked.connect(self.handle_selectedOff)
        self.mainView.allOff.clicked.connect(self.handle_allOff)
        self.mainView.allOn.clicked.connect(self.handle_allOn)
        self.mainView.allZero.clicked.connect(self.handle_allZero)
        self.mainView.selectedDegauss.clicked.connect(self.handle_selectedDegauss)
        self.mainView.selectedDegaussToZero.clicked.connect(
            self.handle_selectedDegaussToZero)
        self.mainView.loadSettings.clicked.connect(self.handle_loadSettings)
        self.mainView.saveSettings.clicked.connect(self.handle_saveSettings)
        # the dburtSaveView needs to know what controller
        # type we are using to write it to the save file
        self.dburtSaveView.controller_type = \
            self.Area_ENUM_to_Text[self.machineArea]
        # connect the timer to mainViewUpdate, no threading in this app
        QtCore.QTimer.connect(self.widgetUpdateTimer,
                              QtCore.SIGNAL("timeout()"),
                              self.mainViewUpdate)
        # start timer for 200 ms
        self.widgetUpdateTimer.start(self.widgetTimerUpdateTime_ms)
    # update the  mainViewUpdate
    def mainViewUpdate(self):
        # conceivably the timer could restart this function before it completes
        # so guard against that
        try:
            self.mainView.updateMagnetWidgets()
        finally:
            self.widgetUpdateTimer.start(self.widgetTimerUpdateTime_ms)
    # mainView buttons
    # 'simple' buttons are connected in the GUI_magnetAppMainView
    # ones that require a magnet controller are handled here
    def handle_selectedOn(self):
        if self.activeEPICS:
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(self.mainView.getActiveNames())
            self.localMagnetController.switchONpsu(self.activeMags)

    def handle_selectedOff(self):
        if self.activeEPICS:
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(self.mainView.getActiveNames())
            self.localMagnetController.switchOFFpsu(self.activeMags)

    def handle_allOff(self):
        if self.activeEPICS:
            self.localMagnetController.switchOFFpsu(self.allMagNames)

    def handle_allZero(self):
        if self.activeEPICS:
            self.localMagnetController.setSIZero(self.allMagNames)

    def handle_allOn(self):
        if self.activeEPICS:
            self.localMagnetController.switchONpsu(self.allMagNames)

    def handle_selectedDegauss(self):
        self.handle_Degauss(False)

    def handle_selectedDegaussToZero(self):
        self.handle_Degauss(True)

    def handle_Degauss(self,tozero):
        if self.activeEPICS:
            activeMags = self.mainView.getActiveNames()
            solmags = []
            mags = []
            for mag in activeMags:
                if self.localMagnetController.isASol(mag):
                    solmags.append(mag)
                else:
                    mags.append(mag)
            if len(solmags) > 0:
                self.localMagnetController.degauss(solmags,tozero)
            self.localMagnetController.degauss(mags,tozero)


    def handle_saveSettings(self):
        # dburtSaveView filename is set by current time and date
        self.dburtSaveView.setFileName()
        self.dburtSaveView.show()
        self.dburtSaveView.activateWindow()

    def handle_loadSettings(self):
        self.dburtLoadView = GUI_FileLoad("Load DBURT", globals.dburtLocation2)
        self.dburtLoadView.setWindowIcon(QtGui.QIcon(globals.appIcon))
        self.dburtLoadView.selectButton.clicked.connect(self.handle_fileLoadSelect)

        self.dburtLoadView.show()
        self.dburtLoadView.activateWindow()
    # set mainview text depending on mode and area chosen in startview
    def setMainViewHeaderText(self):
        self.Mode_Text = {
            mag.MACHINE_MODE.OFFLINE :' No EPICS Connection ',
            mag.MACHINE_MODE.PHYSICAL:' Connected to the Physical Machine',
            mag.MACHINE_MODE.VIRTUAL :' Connected to the Virtual Machine'
            }
        self.title = 'Magnet Control for '
        self.title +=  self.Area_ENUM_to_Text[self.machineArea]
        self.title +=  ' Magnets '
        self.title +=  self.Mode_Text[self.machineMode]
        self.mainView.titleLabel.setText(self.title)
    # more cancer below, but i think i have to live with this...
    def addMagnetsToMainView(self):
        # get all magnet names
        self.allMagNames = self.localMagnetController.getMagnetNames()
        # iterate over all magnets, and add them to respective lists depending
        # on their magnet type
        for i in self.allMagNames:
            # get a reference to the HWC magnet object with name i and put it in the list
            # self.allMagnetObjReferences
            self.allMagnetObjReferences[i] = self.localMagnetController.getMagObjConstRef(i)
            if self.localMagnetController.isAQuad(i):
                # if i is a quad, then add to the main view quads list,
                self.mainView.addQuad( self.allMagnetObjReferences.get(i) )
                # pass to mainView the reference,
                # (which then gets passed to the GUI_magnetWidget from mainView)
                self.mainView.quadWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                # set the default options in GUI_magnetWidget (i.e. the name, max.min RI etc)
                self.mainView.quadWidgets[i].setDefaultOptions()
            # do the same for dipoles, correctors and sols
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
        # resize the main view
        self.mainView.mainResize()
        # now we have built the mainView, we connect it's close function, this
        # ensures that when the main view is closed all the other views (saveview nad loadView) are closed too
        self.mainView.closing.connect(self.connectCloseEvents)
    # the load and save dburt windows can't be closed until this function is called
    def connectCloseEvents(self):
        self.widgetUpdateTimer.stop()
        #self.dburtLoadView.canWindowClose = True
        #self.dburtLoadView.close()
        self.dburtSaveView.canWindowClose = True
        self.dburtSaveView.close()
        self.mainView.close()
        print 'Fin - magnetApp closed down, goodbye.'

    def handle_fileSaveNow(self):
        self.fn = str(self.dburtSaveView.file_name_entry.text())
        self.comments = str(self.dburtSaveView.commentsSection.toPlainText())
        self.keywords = self.dburtSaveView.getComboBoxEntries()
        self.localMagnetController.writeDBURT(self.fn, self.comments, self.keywords)
        self.dburtSaveView.hide()

    def handle_fileLoadSelect(self):
        if self.haveDBurtAndNotInOfflineMode():
            if self.dburtLoadView.dburtType == self.dburtLoadView.allMagnets:
                self.localMagnetController.applyDBURT(self.dburtLoadView.selectedFile)
            elif self.dburtLoadView.dburtType == self.dburtLoadView.quadMagnets:
                self.localMagnetController.applyDBURTQuadOnly(self.dburtLoadView.selectedFile)
            elif self.dburtLoadView.dburtType == self.dburtLoadView.corrMagnets:
                self.localMagnetController.applyDBURTCorOnly(self.dburtLoadView.selectedFile)
        self.dburtLoadView.done(1)

    def haveDBurtAndNotInOfflineMode(self):
        self.ret = True
        if self.machineMode == mag.MACHINE_MODE.OFFLINE:
            self.ret = False
        if self.dburtLoadView.selectedFile == "":
            self.ret = False
        return self.ret

    def launchPythonMagnetController(self):
        print os.environ["EPICS_CA_ADDR_LIST"]
        if self.machineMode == mag.MACHINE_MODE.VIRTUAL:
            os.environ["EPICS_CA_SERVER_PORT"] = "6000"
        self.localMagnetController = \
            self.magInit.getMagnetController( self.machineMode, self.machineArea)
        if self.machineMode is not mag.MACHINE_MODE.OFFLINE:
            self.activeEPICS = True



#    _____    __________               .__            .___
#   /  _  \   \______   \ ____   _____ |__| ____    __| _/___________
#  /  /_\  \   |       _// __ \ /     \|  |/    \  / __ |/ __ \_  __ \
# /    |    \  |    |   \  ___/|  Y Y  \  |   |  \/ /_/ \  ___/|  | \/
# \____|__  /  |____|_  /\___  >__|_|  /__|___|  /\____ |\___  >__|
#         \/          \/     \/      \/        \/      \/    \/
#
# A REMINDER OF WHAT PYTHON CANCER CAN LOOK LIKE
    #def launchPythonMagnetController(self):
        #self.localMagnetController
        # if self.machineMode == 'physicalMode':
        #     self.launchPhysical()
        #     self.activeEPICS = True
        # elif self.machineMode == 'virtualMode':
        #     #self.setVM()
        #     self.launchVirtual()
        #     self.activeEPICS = True
        # elif self.machineMode == 'offlineMode':
        #     self.launchOffline()
        # else:
        #     print 'magnetAppController launchPythonMagnetController ERROR'
    # def launchPhysical(self):
    #     if self.machineArea == 'VELA_INJ':
    #         self.localMagnetController = self.magInit.physical_VELA_INJ_Magnet_Controller()
    #     elif self.machineArea == 'VELA_BA1':
    #         self.localMagnetController = self.magInit.physical_VELA_BA1_Magnet_Controller()
    #     elif self.machineArea == 'VELA_BA2':
    #         self.localMagnetController = self.magInit.physical_VELA_BA2_Magnet_Controller()
    #     elif self.machineArea == 'CLARA_INJ':
    #         self.localMagnetController = self.magInit.physical_CLARA_INJ_Magnet_Controller()
    # def launchVirtual(self):
    #     if self.machineArea == 'VELA_INJ':
    #         self.localMagnetController = self.magInit.virtual_VELA_INJ_Magnet_Controller()
    #     elif self.machineArea == 'VELA_BA1':
    #         self.localMagnetController = self.magInit.virtual_VELA_BA1_Magnet_Controller()
    #     elif self.machineArea == 'VELA_BA2':
    #         self.localMagnetController = self.magInit.virtual_VELA_BA2_Magnet_Controller()
    #     elif self.machineArea == 'CLARA_INJ':
    #         self.localMagnetController = self.magInit.virtual_CLARA_INJ_Magnet_Controller()
    # def launchOffline(self):
    #     if self.machineArea == 'VELA_INJ':
    #         self.localMagnetController = self.magInit.offline_VELA_INJ_Magnet_Controller()
    #     elif self.machineArea == 'VELA_BA1':
    #         self.localMagnetController = self.magInit.offline_VELA_BA1_Magnet_Controller()
    #     elif self.machineArea == 'VELA_BA2':
    #         self.localMagnetController = self.magInit.offline_VELA_BA2_Magnet_Controller()
    #     elif self.machineArea == 'CLARA_INJ':
    #         self.localMagnetController = self.magInit.offline_CLARA_INJ_Magnet_Controller()
        # def setMainViewHeaderText(self):
            # self.VELA_BA2.objectName(): MACHINE_AREA.VELA_BA2,
            # self.VELA_BA1.objectName(): MACHINE_AREA.VELA_BA1,
            # self.VELA_INJ.objectName(): MACHINE_AREA.VELA_INJ
            # #self.CLARA_PHASE_1.objectName(): MACHINE_AREA.CLARA_PHASE_1,
            # #self.CLARA_2_VELA.objectName(): MACHINE_AREA.CLARA_2_VELA
            # }
            # self.radioModeTo_ENUM = {self.virtualMode.objectName(): MACHINE_MODE.VIRTUAL,
            # self.physicalMode.objectName(): MACHINE_MODE.PHYSICAL,
            # self.offlineMode.objectName(): MACHINE_MODE.OFFLINE
            # # self.CLARA_PHASE_1.objectName(): MACHINE_AREA.CLARA_PHASE_1,
            # # self.CLARA_2_VELA.objectName(): MACHINE_AREA.CLARA_2_VELA
            # }
            #
            #
            # self.title = 'Magnet Control for '
            # self.area_to_title ={}
            #
            # if self.machineArea == 'VELA_INJ':
            #     self.title += 'VELA Injector Magnets'
            # elif self.machineArea == 'VELA_BA1':
            #     self.title += 'VELA BA1 Magnets'
            # elif self.machineArea == 'VELA_BA2':
            #     self.title += 'VELA BA2 Magnets'
            # elif self.machineArea == 'CLARA_INJ':
            #     self.title += 'CLARA Injector Magnets'
            # if self.machineMode == 'physicalMode':
            #     self.title += ' Connected to the Physical Machine'
            # elif self.machineMode == 'virtualMode':
            #     self.title += ' Connected to the Virtual Machine '
            # elif self.machineMode == 'offlineMode':
            #     self.title += ' No EPICS Connection '
            # self.mainView.titleLabel.setText( self.title )
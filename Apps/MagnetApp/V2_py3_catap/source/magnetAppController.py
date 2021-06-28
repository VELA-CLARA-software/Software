'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:    DJS
//  Created:   01-04-2020
//  Last edit:   01-04-2020
//  FileName:    magnetAppController.py
//  Description: controller or magnet app
//
//
//*/
'''
# part of MagtnetApp
import sys
import os

# catap_path = os.path.join('C:\\Users', 'djs56', 'Documents', 'catapillar-build',
#                           'PythonInterface','Release')

# catap_path = os.path.join('C:\\Users', 'djs56', 'GitHub', 'CATAP','caterpillar-build',
#                           'PythonInterface','Release')

catap_path = os.path.join('\\\\claraserv3.dl.ac.uk', 'claranet', 'packages', 'CATAP','bin')

resource_path = os.path.join('resources','magnetApp')
sys.path.append(os.path.join(sys.path[0],resource_path))
sys.path.append(catap_path)

for item in sys.path:
    print(item)



from CATAP.GlobalTypes import TYPE
from CATAP.GlobalStates import STATE
from CATAP.HardwareFactory import *


#print(TYPE.LLRF_TYPE)

# import VELA_CLARA_Magnet_Control as mag
import magnetAppGlobals as globals
# from PyQt4 import QtGui, QtCore
from .gui.GUI_magnetAppStartup import GUI_magnetAppStartup
from .gui.GUI_magnetAppMainView import GUI_magnetAppMainView
from .gui.GUI_FileLoad import GUI_FileLoad
from .gui.GUI_FileSave import GUI_FileSave
# from operator import itemgetter
# import time
# import sys

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication

# this class handles everything
class magnetAppController(object):
    def __init__(self,argv):
        print("show")
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
        self.widgetUpdateTimer = QTimer()
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
        self.dburtSaveView.setWindowIcon(QIcon(globals.appIcon))
        self.dburtSaveView.saveNowButton_2.clicked.connect(self.handle_fileSaveNow)
        # this map is used a few places, sodefined here
        # I think there is a c++ method to get this, but the documentation is... meh...
        self.Area_ENUM_to_Text ={
            TYPE.BA1:'BA1',
            TYPE.BA2:'BA2',
            TYPE.VELA:'VELA_Injector',
            TYPE.CLARA_PH1:'CLARA_PH1',
            TYPE.CLARA_2_BA1_BA2:'CLARA_2_BA1_BA2',
            TYPE.CLARA_2_BA1:'CLARA_2_BA1'
            #mag.MACHINE_AREA.CLARA_PHASE_1:'CLARA PHASE 1 Magnets',
            }

#        for i in sys.path:
#            print i
#          __                 __             .__
#  _______/  |______ ________/  |_     ___  _|__| ______  _  __
# /  ___/\   __\__  \\_  __ \   __\    \  \/ /  |/ __ \ \/ \/ /
# \___ \  |  |  / __ \|  | \/|  |       \   /|  \  ___/\     /
#/____  > |__| (____  /__|   |__|        \_/ |__|\___  >\/\_/
#     \/            \/                               \/
    # these functions handle the start view signals4
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
        print("handle_startviewstartbutton")
        if self.areaAndModeSet():
            # forced update to the startup window showing choices
            self.startView.waitMessageLabel.setText(
                "Building Main Window...Patience is a virtue")
            self.startView.update()
            QApplication.processEvents()

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
        print("FIN")
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
        self.widgetUpdateTimer.timeout.connect(self.mainViewUpdate)
        # start timer for 200 ms
        self.widgetUpdateTimer.start(self.widgetTimerUpdateTime_ms)




    # update the  mainViewUpdate
    def mainViewUpdate(self):
        # conceivably the timer could restart this function before it completes
        # so guard against that
        try:
            self.mainView.updateMagnetWidgets()
            #self.mainView.updateMagnetDegaussButton()
        finally:
            self.widgetUpdateTimer.start(self.widgetTimerUpdateTime_ms)
    # mainView buttons
    # 'simple' buttons are connected in the GUI_magnetAppMainView
    # ones that require a magnet controller are handled here
    def handle_selectedOn(self):
        if self.activeEPICS:
            self.activeMags = self.mainView.getActiveNames()
            print( type(self.activeMags ) )
            print( type(self.activeMags ) )
            print( type(self.activeMags[0] ) )
            print( type(self.activeMags[0] ) )
            self.localMagnetController.swtichOn(self.activeMags)

    def handle_selectedOff(self):
        if self.activeEPICS:
            self.activeMags = self.mainView.getActiveNames()
            print( type(self.activeMags ))
            print( type(self.activeMags ))
            print( type(self.activeMags[0] ))
            print( type(self.activeMags[0] ))
            print( self.activeMags[0])
            print( self.activeMags[0])
            for i in self.activeMags:
                print(i)
            self.localMagnetController.swtichOff(self.activeMags)

    def handle_allOff(self):
        if self.activeEPICS:
            self.localMagnetController.switchOffAll()

    def handle_allZero(self):
        if self.activeEPICS:
            self.localMagnetController.SETIAllZero()

    def handle_allOn(self):
        if self.activeEPICS:
            self.localMagnetController.switchOnAll()

    def handle_selectedDegauss(self):
        self.handle_Degauss(False)

    def handle_selectedDegaussToZero(self):
        self.handle_Degauss(True)

    def handle_Degauss(self,tozero):
        print("handle_Degauss")
        if self.activeEPICS:
            self.mainView.selectedDegauss.setStyleSheet("background-color: red")
            self.mainView.DEGAUSS_PREP = True
            QApplication.processEvents()

            activeMags = self.mainView.getActiveNames()
            LOCAL_solmags = []
            LOCAL_mags = []
            print("2")
            # if self.machineArea == TYPE.VELA_INJ:
            #     for magnet in activeMags:
            #         if self.localMagnetController.isASol(magnet):
            #             LOCAL_solmags.append(magnet)
            #         else:
            #             LOCAL_mags.append(magnet)
            # else:
            #
            LOCAL_mags = activeMags

            # if len(LOCAL_solmags) > 0:
            #     self.localMagnetController.degauss(LOCAL_solmags, tozero)



            if len(LOCAL_mags) > 0:
                for magnet_NAME in LOCAL_mags:
                    print('DEGAUSSING ', magnet_NAME)
                # hack to stop degaussing gun solenoids
                try:
                    LOCAL_mags.remove('CLA-LRG1-MAG-SOL-01')
                    print("LRG-SOL is a GUN solenoid , NOT degaussing")
                except:
                    pass
                try:
                    LOCAL_mags.remove('CLA-GUN-MAG-SOL-02')
                    print("LRG-SOL is a GUN solenoid , NOT degaussing")
                except:
                    pass
                try:
                    LOCAL_mags.remove("LRG-SOL")
                    print("LRG-SOL is a GUN solenoid , NOT degaussing")
                except:
                    pass
                # hack to stop degaussing gun solenoids
                try:
                    LOCAL_mags.remove("LRG-SOL02")
                    print("LRG-SOL is a GUN solenoid , NOT degaussing")
                except:
                    pass
                try:
                    LOCAL_mags.remove("LRG-BSOL")
                    print("LRG-BSOL is a GUN solenoid , NOT degaussing")
                except:
                    pass
                # disable degaussing correctors
                corr_list = []
                for magnet in LOCAL_mags:
                    if self.localMagnetController.isACor(magnet):
                        print(magnet, ' as a corrector, NOT degaussing')
                        corr_list.append(magnet)
                LOCAL_mags = [e for e in LOCAL_mags if e not in corr_list]

                # disable degaussing BA1 magnets
                BA1_list = []
                for magnet in LOCAL_mags:
                    if 'BA1' in magnet:
                        print(magnet, ' as a BA1 magnet, NOT degaussing')
                        BA1_list.append(magnet)
                LOCAL_mags = [e for e in LOCAL_mags if e not in BA1_list]


                if len(LOCAL_mags) > 0:
                    self.localMagnetController.degauss(LOCAL_mags, tozero)
                self.mainView.DEGAUSS_PREP = False
                QApplication.processEvents()


    def handle_saveSettings(self):

        print(self.mainView.getActiveNames())

        # dburtSaveView filename is set by current time and date
        self.dburtSaveView.setFileName()
        #self.dburtSaveView.addComboKeywords(self.Area_ENUM_to_Text[self.machineArea])
        self.dburtSaveView.show()
        self.dburtSaveView.activateWindow()

    def handle_loadSettings(self):
        print("handle_loadSettings 1")
        self.dburtLoadView = GUI_FileLoad("Load DBURT", root = globals.dburtLocation2)
        print("handle_loadSettings 2")
        self.dburtLoadView.setWindowIcon(QIcon(globals.appIcon))
        print("handle_loadSettings 3")
        self.dburtLoadView.selectButton.clicked.connect(self.handle_fileLoadSelect)
        print("handle_loadSettings 4")
        self.dburtLoadView.show()
        print("handle_loadSettings 5")
        self.dburtLoadView.activateWindow()

    # set mainview text depending on mode and area chosen in startview
    def setMainViewHeaderText(self):
        self.Mode_Text = {
            STATE.OFFLINE :' No EPICS Connection ',
            STATE.PHYSICAL:' Connected to the Physical Machine',
            STATE.VIRTUAL :' Connected to the Virtual Machine'
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

        print("addMagnetsToMainView 1")
        self.magnet_names_to_canonical_order()
        # iterate over all magnets, and add them to respective lists depending
        # on their magnet type
        print("addMagnetsToMainView 3")
        for i in self.allMagNames:
            # get a reference to the HWC magnet object with name i and put it in the list
            # self.allMagnetObjReferences
            self.allMagnetObjReferences[i] = self.localMagnetController.getMagnet(i)
            if self.localMagnetController.isAQuad(i):
                print(i, "is a quad")
                # if i is a quad, then add to the main view quads list,
                self.mainView.addQuad( self.allMagnetObjReferences.get(i) )
                # pass to mainView the reference,
                # (which then gets passed to the GUI_magnetWidget from mainView)
                self.mainView.quadWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                # set the default options in GUI_magnetWidget (i.e. the name, max.min RI etc)
                self.mainView.quadWidgets[i].setDefaultOptions()
            # do the same for dipoles, correctors and sols
            elif self.localMagnetController.isADip( i ):
                print(i, "is a dip")
                self.mainView.addDip( self.allMagnetObjReferences.get(i) )
                self.mainView.dipWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.dipWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isASol( i ):
                print(i, "is a Bsol")
                self.mainView.addSol( self.allMagnetObjReferences.get(i) )
                self.mainView.solWidgets[i].magRef.append(self.allMagnetObjReferences[ i ])
                self.mainView.solWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isABSol( i ):
                print(i, "is a sol")
                self.mainView.addSol( self.allMagnetObjReferences.get(i) )
                self.mainView.solWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.solWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isACor(i):
                print(i, "is a cor")
                self.mainView.addCor(self.allMagnetObjReferences.get(i))
                self.mainView.corWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.corWidgets[i].setDefaultOptions()
            print(i, "FIN")
        # resize the main view
            print(i, "3")

        self.mainView.mainResize()
        # now we have built the mainView, we connect it's close function, this
        # ensures that when the main view is closed all the other views (saveview nad loadView) are closed too
        self.mainView.closing.connect(self.connectCloseEvents)
    # the load and save dburt windows can't be closed until this function is called

    def magnet_names_to_canonical_order(self):

        canon_order = ['LRG','GUN','S01','L01','S02','C2V','INJ','BA1','BA2']
        order = []
        for name in self.allMagNames:
            i = 0
            for area in canon_order:
                if area in name:
                    order.append([i,name])
                else:
                    i += 1
        import operator
        self.allMagNames = [x[1] for x in sorted(order, key=operator.itemgetter(0))]

    def connectCloseEvents(self):
        self.widgetUpdateTimer.stop()
        #self.dburtLoadView.canWindowClose = True
        #self.dburtLoadView.close()
        self.dburtSaveView.canWindowClose = True
        self.dburtSaveView.close()
        for window in self.dburtLoadView.textWindowList:
            window.close()
        self.dburtLoadView.close()
        self.mainView.close()
        print( 'Fin - magnetApp closed down, goodbye.')

    def handle_fileSaveNow(self):
        self.fn = str(self.dburtSaveView.file_name_entry.text())
        self.path = str(self.dburtSaveView.path_name_entry.text())
        self.comments = str(self.dburtSaveView.commentsSection.toPlainText())
        #self.keywords = self.dburtSaveView.getComboBoxEntries()
        self.localMagnetController.writeDBURT(self.path,  self.fn, self.comments)
        self.dburtSaveView.hide()

    def handle_fileLoadSelect(self):
        print("handle_fileLoadSelect")
        burt_applied = False
        if self.haveDBurtAndNotInOfflineMode():
            print( "self.haveDBurtAndNotInOfflineMode() is TRUE")
            if self.dburtLoadView.dburtType == self.dburtLoadView.allMagnets:
                print("all")
                print("self.dburtLoadView.selectedFilePath = ", self.dburtLoadView.selectedFilePath)
                print("self.dburtLoadView.selectedFile = ", self.dburtLoadView.selectedFile)
                burt_applied = self.localMagnetController.applyDBURT(
                        self.dburtLoadView.selectedFilePath,
                        self.dburtLoadView.selectedFile)
            elif self.dburtLoadView.dburtType == self.dburtLoadView.quadMagnets:
                burt_applied = self.localMagnetController.applyDBURTQuadOnly(
                    self.dburtLoadView.selectedFilePath, self.dburtLoadView.selectedFile)
            elif self.dburtLoadView.dburtType == self.dburtLoadView.corrMagnets:
                burt_applied = self.localMagnetController.applyDBURTCorOnly(
                    self.dburtLoadView.selectedFilePath,self.dburtLoadView.selectedFile)

        else:
            print( "self.haveDBurtAndNotInOfflineMode() is FALSE")

        if burt_applied:
            print( 'burt load success')
            self.dburtLoadView.burtLoadSuccess()
            #time.sleep(2)
            self.dburtLoadView.done(1)
        else:
            print( 'burt load failed')
            # cancer
            failed = self.localMagnetController.getLastFailedSet()
            #flattened_list = [y for x in failed for y in x]
            f3 = ', '.join(str(e) for e in failed)
            print( f3)
            self.dburtLoadView.burtLoadFailed(text=f3)


    def haveDBurtAndNotInOfflineMode(self):
        print("haveDBurtAndNotInOfflineMode")
        print("self.machineMode  = ", self.machineMode )
        ret = True
        if self.machineMode == STATE.OFFLINE:
            print("MODE == OFFLINE")
            ret = False
        if self.dburtLoadView.selectedFile == "":
            print("self.dburtLoadView.selectedFile == blank ")
            ret = False
        print("ret = ", ret)
        return ret

    def launchPythonMagnetController(self):
        print("macheinMode = ", self.machineMode)
        if self.machineMode == STATE.VIRTUAL:
            print("Applying Virtual EPCIS environment variables ")
            os.environ["EPICS_CA_SERVER_PORT"] = "6000"
            os.environ["EPICS_CA_AUTO_ADDR_LIST"] = "NO"
            os.environ['EPICS_CA_ADDR_LIST'] = "10.10.0.12"

        # we can't create a magnet controler intil we know what machein mode to use
        # initilaize the VELA_CLARA_MagnetControl,
        # from this object we can get all flavours of magnet controller
        #self.magInit = mag.init()
        self.HF = HardwareFactory( self.machineMode )
        # # input()
        # MF = self.HF.getMagnetFactory()
        #
        #self.magInit.setVerbose()
        self.localMagnetController = self.HF.getMagnetFactory( )
        if self.machineMode is not STATE.OFFLINE:
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
import sys, os
#get the magnet enums used to define magnet types and  PSU states
#We should probably create magnet module to make importing stuff easier  
#sys.path.append('D:\\VELA\\GIT Projects\\VELA-CLARA-Controllers\\bin\\Release')

dburtLocation = "\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Snapshots\\DBURT\\"
appIcon = 'magpic.jpg'

import VELA_CLARA_MagnetControl as mag

from PyQt4 import QtGui, QtCore
from GUI_magnetAppStartup import GUI_magnetAppStartup
from GUI_magnetAppMainView import GUI_magnetAppMainView
from GUI_FileLoad import GUI_FileLoad

class magnetAppController(object):
    def __init__(self,argv):
        self.magInit = mag.init()   # initilaize the VELA_CLARA_MagnetControl
        # startup veiw and connections
        self.startView = GUI_magnetAppStartup()
        self.startView.show()
        self.startView.startButton.clicked.connect( self.handle_startviewstartbutton )
        self.startView.cancelButton.clicked.connect( self.handle_startviewstartbutton )
        self.startView.machineAreaSignal.connect( self.handle_machineAreaSignal )
        self.startView.machineModeSignal.connect( self.handle_machineModeSignal )
        # init choices for different modes
        self.machineArea = 'UNKNOWN'
        self.machineMode = 'UNKNOWN'
        # init objects
        self.localMagnetController = None
        self.mainView = None
        self.allMagnetObjReferences = {}
        # self.allMagNames = []
        self.burtType = None
        # flag to say if we are connected to any epics
        self.activeEPICS = False
        # timer for GUI update call
        self.widgetUpdateTimer = QtCore.QTimer()
        # File Load Window
        self.dburtLoadView = None
        self.dburtSaveView = None

    def handle_saveSettings(self):
        self.dburtLoad = GUI_FileBrowser()
        self.fb.show()
        self.dburtLoadView.selectButton.clicked.connect(self.handle_fileLoadCancel)
        self.dburtLoadView.cancelButton.clicked.connect(self.handle_fileLoadSelect)

    def handle_loadSettings(self):
        self.fb = GUI_FileLoad("Load DBURT",dburtLocation )
        self.fb.setWindowIcon(QtGui.QIcon( appIcon ) )
        self.fb.show()

    def handle_fileLoadCancel(self):
        self.dburtLoadView.close()
    def handle_fileLoadSelect(self):

        if self.dburtLoad.dburtType  == self.dburtLoad.allMagnets:
            self.localMagnetController.applyDBURT( self.dburtLoadView.dburtFile )
        elif self.dburtLoad.dburtType  == self.dburtLoad.quadMagnets:
            self.localMagnetController.applyDBURTQuadOnly( self.dburtLoadView.dburtFile )
        elif self.dburtLoad.dburtType == self.dburtLoad.corrMagnets:
            self.localMagnetController.applyDBURTCorOnly(self.dburtLoadView.dburtFile)
        self.dburtLoadView.close()


    def setLoadFile(self,r):
        self.loadfile = r
        if fileName:
            print fileName
        print 'handle_loadSettings'
        self.loadView.show()
        #QtGui.QFileDialog


    # these fucntions updatet the GUI and (re)start the timer
    def startMainViewUpdateTimer(self):
        self.widgetUpdateTimer = QtCore.QTimer()
        QtCore.QTimer.connect(self.widgetUpdateTimer, QtCore.SIGNAL("timeout()"), self.mainViewUpdate )
        self.widgetUpdateTimer.start(100)
    def mainViewUpdate(self):
        # conceivably the timer could restart this function before it complete - so guard against that
        try:
            self.mainView.updateMagnetWidgets()
        finally:
            self.widgetUpdateTimer.start(100)

    # these functions handle the start view signals
    def handle_machineAreaSignal(self,r):
         self.machineArea = r
    def handle_machineModeSignal(self,r):
         self.machineMode = r
    def handle_startviewstartbutton(self):
        if  self.areaAndModeSet():
            # forced update to the startup window showing choices
            self.startView.waitMessageLabel.setText("Building Main Window...Patience is a virtue")
            self.startView.update()
            QtGui.QApplication.processEvents();
            # launch requested magnet controller
            self.launchPythonMagnetController()
            # get magnet names, required to build main view
            # launch main view and add magnets (whihc magnets get added depends on what machine area you choose...)
            self.launchMainView()
            self.addMagnetsToMainView()
        else:
            # forced update to the startup window showing error
            self.startView.waitMessageLabel.setText("<font color='red'>ERROR: You must select a Machine Area and Mode "
                                                    "first</font>")
            self.startView.waitMessageLabel.update()
    # ... and then build the mainView
    def launchMainView(self):
        self.mainView = GUI_magnetAppMainView()
        self.setMainViewHeaderText()
        self.mainView.show()
        self.startView.close()
        # connect signals
        self.mainView.selectedOn.clicked.connect( self.handle_selectedOn )
        self.mainView.allOff.clicked.connect( self.handle_allOff )
        self.mainView.selectedDegauss.clicked.connect( self.handle_selectedDegauss )
        self.mainView.loadSettings.clicked.connect( self.handle_loadSettings )
        self.mainView.saveSettings.clicked.connect( self.handle_saveSettings )
        self.startMainViewUpdateTimer()

    def areaAndModeSet(self):
        ret = True
        if self.machineArea == 'UNKNOWN':
            ret = False
        if self.machineMode == 'UNKNOWN':
            ret = False
        return ret


    # set mainview text depending on mode and area chosen in startview
    def setMainViewHeaderText(self):
        self.title = 'Magnet Control for '
        if self.machineArea == 'VELA_INJ_Magnets':
            self.title += 'VELA Injector Magnets'
        elif self.machineArea == 'VELA_BA1_Magnets':
            self.title += 'VELA BA1 Magnets'
        elif self.machineArea == 'VELA_BA2_Magnets':
            self.title += 'VELA BA2 Magnets'
        elif self.machineArea == 'CLARA_INJ_Magnets':
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
        self.allMagNames = self.localMagnetController.getMagnetNames()
        for i in self.allMagNames:
            self.allMagnetObjReferences[ i ] = self.localMagnetController.getMagObjConstRef( i )
            if self.localMagnetController.isAQuad( i ):
                self.mainView.addQuad( self.allMagnetObjReferences.get(i) )
                self.mainView.quadWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.quadWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isADip( i ):
                #print 'ADDING DIP'
                self.mainView.addDip( self.allMagnetObjReferences.get(i) )
                self.mainView.dipWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.dipWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isASol( i ):
                self.mainView.addSol( self.allMagnetObjReferences.get(i) )
                self.mainView.solWidgets[i].magRef.append(self.allMagnetObjReferences[ i ])
                self.mainView.solWidgets[i].setDefaultOptions()
                #print 'ADDING SOL'
            elif self.localMagnetController.isABSol( i ):
                self.mainView.addSol( self.allMagnetObjReferences.get(i) )
                self.mainView.solWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.solWidgets[i].setDefaultOptions()
            elif self.localMagnetController.isACor(i):
                self.mainView.addCor(self.allMagnetObjReferences.get(i))
                self.mainView.corWidgets[i].magRef.append(self.allMagnetObjReferences[i])
                self.mainView.corWidgets[i].setDefaultOptions()
                #print 'ADDING BSOL'
        self.mainView.mainResize()
#        self.mainView.updateGUI()


    def handle_mainSelectAll(self):
        print 'handle_mainSelectAll'


    def handle_selectNone(self):
        print 'handle_selectNone'

    def handle_selectedOn(self):
        print 'handle_selectedOn'
        if self.activeEPICS:
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(   self.mainView.getActiveNames() )
            print self.activeMags
            self.localMagnetController.switchONpsu( self.activeMags )

    def handle_allOff(self):
        print 'handle_allOff'
        if self.activeEPICS:
            print 'epics active'
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(   self.mainView.getActiveNames() )
            print self.activeMags
            self.localMagnetController.switchOFFpsu( self.allMagNames )

    def handle_selectedDegauss(self):
        print 'handle_selectedDegauss'
        if self.activeEPICS:
            self.activeMags = mag.std_vector_string()
            self.activeMags.extend(   self.mainView.getActiveNames() )
            print 'active magnet widgets'
            print self.activeMags
            self.localMagnetController.degauss( self.activeMags, True )



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
        if self.machineArea == 'VELA_INJ_Magnets':
            self.localMagnetController = self.magInit.physical_VELA_INJ_Magnet_Controller()
        elif self.machineArea == 'VELA_BA1_Magnets':
            self.localMagnetController = self.magInit.physical_VELA_BA1_Magnet_Controller()
        elif self.machineArea == 'VELA_BA2_Magnets':
            self.localMagnetController = self.magInit.physical_VELA_BA2_Magnet_Controller()
        elif self.machineArea == 'CLARA_INJ_Magnets':
            self.localMagnetController = self.magInit.physical_CLARA_INJ_Magnet_Controller()
    def launchVirtual(self):
        if self.machineArea == 'VELA_INJ_Magnets':
            self.localMagnetController = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        elif self.machineArea == 'VELA_BA1_Magnets':
            self.localMagnetController = self.magInit.virtual_VELA_BA1_Magnet_Controller()
        elif self.machineArea == 'VELA_BA2_Magnets':
            self.localMagnetController = self.magInit.virtual_VELA_BA2_Magnet_Controller()
        elif self.machineArea == 'CLARA_INJ_Magnets':
            self.localMagnetController = self.magInit.virtual_CLARA_INJ_Magnet_Controller()
    def launchOffline(self):
        if self.machineArea == 'VELA_INJ_Magnets':
            self.localMagnetController = self.magInit.offline_VELA_INJ_Magnet_Controller()
        elif self.machineArea == 'VELA_BA1_Magnets':
            self.localMagnetController = self.magInit.offline_VELA_BA1_Magnet_Controller()
        elif self.machineArea == 'VELA_BA2_Magnets':
            self.localMagnetController = self.magInit.offline_VELA_BA2_Magnet_Controller()
        elif self.machineArea == 'CLARA_INJ_Magnets':
            self.localMagnetController = self.magInit.offline_CLARA_INJ_Magnet_Controller()



























    # VELA_BA2_Magnets
    # CLAR_INJ_Magnets
    # VELA_BA1_Magnets
    # VELA_INJ_Magnets
        # self.view = view
        # self.view.selectAllSignal.connect( self.handle_selectAll )
        # self.view.selectedDegaussSignal.connect( self.handle_selectedDegauss )
        # self.view.loadSettingsSignal.connect( self.handle_loadSettings )
        # self.view.saveSettingsSignal.connect( self.handle_saveSettings )
        # self.view.allOffSignal.connect( self.handle_allOff )
        # self.view.selectNoneSignal.connect( self.handle_selectNone )
        # self.maginit = mag.init()
        # self.magControl = self.maginit.virtual_VELA_INJ_Magnet_Controller_NOEPICS()
        # self.allQuadNames = self.magControl.getQuadNames()
        # self.allDipNames  = self.magControl.getDipNames()
        # self.allSolNames  = self.magControl.getSolNames()
        # self.allHCorNames = self.magControl.getHCorNames()
        # self.allVCorNames = self.magControl.getVCorNames()
        # self.allMagNames  = self.magControl.getMagnetNames()
        # get a dictionary of magnet objects references keyed by the magnet name
        # these point to all the magnet data we have access to
        # self.allMagnetObjReferences = {}
        # for i in self.allMagNames:
        #     self.allMagnetObjReferences[ i ] = self.magControl.getMagObjConstRef( i )
        #     if self.magControl.isAQuad( i ):
        #         self.view.addQuadrupole( self.allMagnetObjReferences[ i ] )
        #     elif self.magControl.isADip( i ):
        #         self.view.addSolOrDip( self.allMagnetObjReferences[ i ] )
        #     elif self.magControl.isASol( i ):
        #         self.view.addSolOrDip( self.allMagnetObjReferences[ i ] )
        #
        #     print 'added ' + i
        # self.view.updateGUI()



    def setViewSols():
        self.allSolNames  = self.magControl.getSolNames()































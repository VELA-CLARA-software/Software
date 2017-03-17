from PyQt4 import QtGui, QtCore
from Ui_magnetAppStartup import Ui_magnetAppStartup
import magnetAppGlobals as globals
from VELA_CLARA_MagnetControl import MACHINE_MODE, MACHINE_AREA

class GUI_magnetAppStartup(QtGui.QMainWindow, Ui_magnetAppStartup):
    # static signals to emit when radioButtons are pressed
    machineAreaSignal = QtCore.pyqtSignal(MACHINE_AREA)
    machineModeSignal = QtCore.pyqtSignal(MACHINE_MODE)
    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        # I can't find a *good* way to get the toggled radio button, apart from emitting signals and
        # interpreting them later... meh
        self.VELA_BA2.toggled.connect(lambda:self.handle_areaRadio(self.VELA_BA2))
        self.VELA_BA1.toggled.connect(lambda:self.handle_areaRadio(self.VELA_BA1))
        self.VELA_INJ.toggled.connect(lambda:self.handle_areaRadio(self.VELA_INJ))
        self.CLARA_PHASE_1.toggled.connect(lambda:self.handle_areaRadio(self.CLARA_PHASE_1))
        self.virtualMode.toggled.connect(lambda:self.handle_modeRadio(self.virtualMode))
        self.physicalMode.toggled.connect(lambda:self.handle_modeRadio(self.physicalMode))
        self.offlineMode.toggled.connect(lambda:self.handle_modeRadio(self.offlineMode))
        self.appPixMap = QtGui.QPixmap(globals.appIcon)
        self.iconLabel.setPixmap(self.appPixMap)
        self.setWindowTitle("VELA - CLARA Magnet App")
        self.logo  = QtGui.QPixmap(globals.claraIcon)
        self.scaledLogo =  self.logo.scaled(self.logoLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.logoLabel.setPixmap(self.scaledLogo)
        self.setWindowIcon(QtGui.QIcon(globals.appIcon))
        self.waitMessageLabel.setText("")
        self.radioAreaTo_ENUM ={ self.VELA_BA2.objectName(): MACHINE_AREA.VELA_BA2,
        self.VELA_BA1.objectName(): MACHINE_AREA.VELA_BA1,
        self.VELA_INJ.objectName(): MACHINE_AREA.VELA_INJ
        #self.CLARA_PHASE_1.objectName(): MACHINE_AREA.CLARA_PHASE_1,
        #self.CLARA_2_VELA.objectName(): MACHINE_AREA.CLARA_2_VELA
        }
        self.radioModeTo_ENUM = {self.virtualMode.objectName(): MACHINE_MODE.VIRTUAL,
        self.physicalMode.objectName(): MACHINE_MODE.PHYSICAL,
        self.offlineMode.objectName(): MACHINE_MODE.OFFLINE
        # self.CLARA_PHASE_1.objectName(): MACHINE_AREA.CLARA_PHASE_1,
        # self.CLARA_2_VELA.objectName(): MACHINE_AREA.CLARA_2_VELA
        }
    # the radio buttones emit a MACHINE_MODE or MACHINE_AREA enum
    # this is then set as a variable in the  magnetAppController
    def handle_areaRadio(self,r):
        if r.isChecked() == True:
            self.machineAreaSignal.emit(self.radioAreaTo_ENUM[r.objectName()])
    def handle_modeRadio(self,r):
        if r.isChecked() == True:
            self.machineModeSignal.emit(self.radioModeTo_ENUM[r.objectName()])



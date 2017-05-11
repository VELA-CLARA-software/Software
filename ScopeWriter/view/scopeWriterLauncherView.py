from PyQt4 import QtGui, QtCore
import scopeWriterLauncherUI
import VELA_CLARA_Scope_Control as vcsc

class scopeWriterLauncherView(QtGui.QMainWindow, scopeWriterLauncherUI.scopeWriterLauncherUI):
    # static signals to emit when radioButtons are pressed
    machineAreaSignal = QtCore.pyqtSignal(vcsc.MACHINE_AREA)
    machineModeSignal = QtCore.pyqtSignal(vcsc.MACHINE_MODE)
    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        self.beamlineTypesComboBox.currentIndexChanged['QString'].connect(self.handle_areaRadio)
        self.controllerTypesComboBox.currentIndexChanged['QString'].connect(self.handle_modeRadio)
        self.setWindowTitle("Scope writer launcher")

        self.beamlines = {"VELA_INJ":  vcsc.MACHINE_AREA.VELA_INJ,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA1,
                          "VELA_BA1":  vcsc.MACHINE_AREA.VELA_BA2,
                          "CLARA_S01": vcsc.MACHINE_AREA.CLARA_S01}
        self.modes = {"Physical": vcsc.MACHINE_MODE.PHYSICAL,
                      "Virtual":  vcsc.MACHINE_MODE.VIRTUAL,
                      "Offline":  vcsc.MACHINE_MODE.OFFLINE}

    def handle_areaRadio(self):
        self.machineAreaSignal.emit(self.beamlines[str(self.beamlineTypesComboBox.currentText())])

    def handle_modeRadio(self):
        self.machineModeSignal.emit(self.modes[str(self.controllerTypesComboBox.currentText())])

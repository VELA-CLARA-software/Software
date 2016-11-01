from PyQt4 import QtGui, QtCore
from Ui_magnetAppStartup import Ui_magnetAppStartup


class GUI_magnetAppStartup(QtGui.QMainWindow, Ui_magnetAppStartup):
    # static signals to emit when radioButtons are pressed
    machineAreaSignal = QtCore.pyqtSignal(str)
    machineModeSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        # I can't find a *good* way to get the toggled radio button, apart from emitting signals and
        # interpreting them later... meh
        self.VELA_BA2_Magnets.toggled.connect(lambda:self.handle_areaRadio(self.VELA_BA2_Magnets))
        self.VELA_BA1_Magnets.toggled.connect(lambda:self.handle_areaRadio(self.VELA_BA1_Magnets))
        self.VELA_INJ_Magnets.toggled.connect(lambda:self.handle_areaRadio(self.VELA_INJ_Magnets))
        self.CLAR_INJ_Magnets.toggled.connect(lambda:self.handle_areaRadio(self.CLAR_INJ_Magnets))
        self.virtualMode.toggled.connect(lambda:self.handle_modeRadio(self.virtualMode))
        self.physicalMode.toggled.connect(lambda:self.handle_modeRadio(self.physicalMode))
        self.offlineMode.toggled.connect(lambda:self.handle_modeRadio(self.offlineMode))
        self.appPixMap = QtGui.QPixmap('magpic.jpg')
        self.iconLabel.setPixmap(self.appPixMap)
        self.setWindowTitle("VELA - CLARA Magnet App")
        self.logo  = QtGui.QPixmap('CLARA5.bmp')
        self.scaledLogo =  self.logo.scaled(self.logoLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.logoLabel.setPixmap(self.scaledLogo)
        self.setWindowIcon(QtGui.QIcon('magpic.jpg'))
        self.waitMessageLabel.setText("")


    def handle_areaRadio(self,r):
        if r.isChecked() == True:
            self.machineAreaSignal.emit(r.objectName())
    def handle_modeRadio(self,r):
        if r.isChecked() == True:
            self.machineModeSignal.emit(r.objectName())



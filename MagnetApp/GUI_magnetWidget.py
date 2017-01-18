from PyQt4 import QtGui, QtCore
from Ui_magnetWidget import Ui_magnetWidget
import sys

# this class needs to know the magnet enums
from VELA_CLARA_MagnetControl import MAG_PSU_STATE, MAG_TYPE, MAG_REV_TYPE

class GUI_magnetWidget(QtGui.QMainWindow, Ui_magnetWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        # holds the reference to the c++ magnet Object data,
        # set in  addMagnetsToMainView in the magnetAppController
        self.magRef = []
        self.SIValue.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.isActive = False       # active magnets have their check button checked
        self.mag_Active.stateChanged.connect( self.setActiveState ) # check button connection
        self.riMeterScalefactor = 1000;#MAGIC_NUMBER
    # called after the magnet
    def setDefaultOptions(self):
        self.name.setText( self.magRef[0].name )
        self.rimin =  min(self.magRef[0].degValues) * self.riMeterScalefactor
        self.rimax =  max(self.magRef[0].degValues) * self.riMeterScalefactor
        self.RIMeter.setRange(  self.rimin, self.rimax  )
    #active magnets are those with the check box checked
    def setActiveState(self):
        self.isActive = self.mag_Active.checkState()
    # we use the reference to the magnet object contained in the list self.magRef to get the
    # latest magnet object values to update the gui with
    def updateMagWidget(self):
        #print 'update ' + self.localName
        self.SIValue.setValue( self.magRef[0].siWithPol )
        self.updatePSUButton(  self.magRef[0].psuState, self.Mag_PSU_State_Button)
        if self.magRef[0].magRevType == MAG_REV_TYPE.NR:
            self.updatePSUButton(self.magRef[0].nPSU.psuState, self.PSU_N_State_Button)
            self.updatePSUButton(self.magRef[0].rPSU.psuState, self.PSU_R_State_Button)
        self.RIMeter.setValue( self.magRef[0].riWithPol * self.riMeterScalefactor )
        self.Mag_PSU_State_Button.setText( "{:.3f}".format(self.magRef[0].riWithPol)  )
    # set the PSU button colors based on their state
    def updatePSUButton(self, psuState, button):
        if psuState == MAG_PSU_STATE.MAG_PSU_OFF:
            button.setStyleSheet("background-color: red")
        elif psuState == MAG_PSU_STATE.MAG_PSU_ON:
            button.setStyleSheet("background-color: green")
        elif psuState == MAG_PSU_STATE.MAG_PSU_TIMING:
            button.setStyleSheet("background-color: yellow")
        elif psuState == MAG_PSU_STATE.MAG_PSU_ERROR:
            button.setStyleSheet("background-color: magenta")
        elif psuState == MAG_PSU_STATE.MAG_PSU_NONE:
            button.setStyleSheet("background-color: black")
        else:
            print 'ERROR with ' + self.localName



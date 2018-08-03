import sys,os

from PyQt4 import QtGui, QtCore
from draftguizero import Ui_MainWindow
from rfalign import gunrfaligner
#from aligncontroller import alignAppController



class draftappgui(QtGui.QMainWindow, Ui_MainWindow):
# static signals to emit when radioButtons are pressed
#    machineAreaSignal = QtCore.pyqtSignal(str)
#    machineModeSignal = QtCore.pyqtSignal(str)
    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)
        # I can't find a *good* way to get the toggled radio button, apart from emitting signals and
		# interpreting them later... meh
        #self.dorfalign.clicked.connect(self.falign)
        #print "Hello world frank1"
        self.rfphi2box_4.setMaximum(999)	
		
    def falign(self):
	    print "Hello world"
		
        

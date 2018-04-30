from PyQt4 import QtGui, QtCore
import scopeWriterUI
import scopeWriterGlobals
import scopeWriterLoadView,scopeWriterSaveView
from VELA_CLARA_Scope_Control import MACHINE_MODE, MACHINE_AREA

class scopeWriterView(QtGui.QMainWindow, scopeWriterUI.scopeWriterUi):
    # static signals to emit when radioButtons are pressed
    closing = QtCore.pyqtSignal()
    def __init__(self):
        print 'create startup window'
        QtGui.QWidget.__init__(self)
        self.setupUi(self)

    def closeEvent(self,event):
        self.closing.emit()
	

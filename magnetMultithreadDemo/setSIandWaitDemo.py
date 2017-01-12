# this sort of works, but not as nicely as i would like
# the gui freezes for a few seconds and then becomes responsizve, while the loop is still running
# i presume we can improve on this

import sys
sys.path.append('\\\\fed.cclrc.ac.uk\\org\\NLab\\ASTeC\\Projects\\VELA\\Software\\VELA_CLARA_PYDs\\bin\\stage\\')

import VELA_CLARA_MagnetControl as mag

from PyQt4 import QtGui, QtCore
import sys, time
from  design import GUI
class mainController():

    def __init__(self):
        #super(self.__class__, self).__init__()
        # instantiate the controller
        self.magInit = mag.init()
        self.mc = self.magInit.virtual_VELA_INJ_Magnet_Controller()
        # ... then the gui
        self.view = GUI()
        self.view.show()
        self.view.btn_start.clicked.connect(self.printMessage)
        self.view.btn_setSI.clicked.connect(self.setSIandWait)
        # some varibles
        self.counter = 0
        self.mag = "QUAD01"

    def printMessage(self):
        self.counter +=1
        self.view.list_submissions.addItem("GUI responds : " + str(self.counter))

    def setSIandWait(self):
        # first disconnect the button just pressed, otherwsie clicking it while this function runs will confuse things
        self.view.btn_setSI.setEnabled(False)

        # our dummy procedure, flip a magnet from -10 to 10 etc.
        self.tolerance = 0.1
        if self.mc.getRI(self.mag) < 0:
            self.newValue = 10.0
        else:
            self.newValue = -10.0
        self.message = "Setting SI to " +  str(self.newValue) + ", with tolerance = " +  str(self.tolerance)
        self.view.list_submissions.addItem(self.message)

        QtCore.QCoreApplication.processEvents()
        self.mc.setSI(self.mag,self.newValue)

        # set times for timeout checking
        self.startTime = time.time()
        self.timeouttime = self.startTime + 30
        self.timedout = False

        time.sleep(0.1)
        # the while loop waiting for the RI to reach SI value (within tolerance)
        while not self.mc.isRIequalVal( self.mag, self.newValue,self.tolerance  ):
            QtCore.QCoreApplication.processEvents()
            if time.time() > self.timeouttime:
                self.view.list_submissions.addItem("TIMEOUT")
                self.timedout = True
                break
            time.sleep(0.01)

        if not self.timedout:
            self.view.list_submissions.addItem("SI SET success")

        self.view.btn_setSI.setEnabled(True)

class App(QtGui.QApplication):
    def __init__(self,argv):
        # seems you need this init line here to instantiate a QTApplication
        QtGui.QWidget.__init__(self,argv)
        # Everything else is handled by the controller
        self.controller = mainController()

if __name__ == '__main__':
    print 'set SI and wait demo'
    app = App(sys.argv)
    sys.exit(app.exec_())


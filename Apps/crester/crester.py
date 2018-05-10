import sys, os
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import pyqtgraph as pg
import numpy as np
from cresting import *

pg.setConfigOptions(antialias=True)
pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'k')

class crester(QMainWindow):
    def __init__(self, parent = None):
        super(crester, self).__init__(parent)
        self.acc = accelerator()

        stdicon = self.style().standardIcon
        style = QStyle
        self.setWindowTitle("RF Cavity Cresting Application")

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)
        fileMenu.addAction(exitAction)

        self.layout = QGridLayout()
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        self.newButton = QPushButton('Reset')
        self.newButton.clicked.connect(self.newAcc)

        self.BFieldWidget = labeledWidget(QLineEdit(),'B Field:')
        self.BFieldWidget.widget.setValidator(QDoubleValidator())
        self.acc.newBfield.connect(lambda x: self.BFieldWidget.widget.setText(str(x)))

        self.pWidget = labeledWidget(QLineEdit(),'Momentum:')
        self.pWidget.widget.setValidator(QDoubleValidator())
        self.acc.newP.connect(lambda x: self.pWidget.widget.setText(str(x/1e6)))

        self.tabs = QTabWidget()
        for i in range(1):
            self.tabs.addTab(cavityCrester(i, self.acc),'Cavity '+str(i+1))
        self.layout.addWidget(self.newButton,0,0)
        self.layout.addWidget(self.BFieldWidget,0,1)
        self.layout.addWidget(self.pWidget,0,2)
        self.layout.addWidget(self.tabs,1,0,6,6)

        self.newAcc()

    def newAcc(self):
        for i in range(1):
            self.acc.cavityNumber = i
            self.acc.crest = 360.0*np.random.random()
            self.acc.turnOffCavity()
            self.tabs.widget(i).reset()
        self.acc.cavityNumber = 0
        self.acc.B = 0.1
        self.acc.reset()

class cavityCrester(QWidget):
    def __init__(self, cavityNumber=0, acc=None, parent = None):
        super(cavityCrester, self).__init__(parent)
        self.cavityNumber = cavityNumber
        self.acc = acc
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        self.crestButton = QPushButton('Crest')
        self.crestButton.clicked.connect(self.autocrest)
        self.gradientWidget = labeledWidget(QLineEdit(), 'Gradient:')
        self.gradientWidget.widget.setReadOnly(True)
        self.calculatedCrestWidget = labeledWidget(QLineEdit(), 'Computed Crest Phase:')
        self.calculatedCrestWidget.widget.setReadOnly(True)
        self.crestWidget = labeledWidget(QLineEdit(), 'Crest Phase:')
        self.crestWidget.widget.setReadOnly(False)
        self.crestWidget.widget.editingFinished.connect(self.setCrest)
        self.acc.newGradient.connect(self.check_autocrest)

        self.controlLayout = QHBoxLayout()
        self.controlLayout.addWidget(self.crestButton)
        self.controlLayout.addWidget(self.gradientWidget)
        self.controlLayout.addWidget(self.crestWidget)
        self.controlLayout.addWidget(self.calculatedCrestWidget)

        self.plotWidget = crestingPlot(cavity=self.cavityNumber)
        self.acc.newBPMReading.connect(self.plotWidget.newBPMReading)
        self.layout.addLayout(self.controlLayout)
        self.layout.addWidget(self.plotWidget)

        self.timer = QTimer()
        self.timer.timeout.connect(self.acc.step)

    def reset(self):
        self.crestWidget.widget.setText(str(self.acc.crest))
        self.plotWidget.reset()

    def changeCavity(self):
        self.acc.cavityNumber = self.cavityNumber
        self.crestWidget.widget.setText(str(self.acc.crest))

    def setCrest(self):
        self.acc.crest = float(str(self.crestWidget.text()))

    def autocrest(self):
        self.crestButton.clicked.disconnect(self.autocrest)
        self.crestButton.clicked.connect(self.stopCrest)
        self.acc.cavityNumber = self.cavityNumber
        self.plotWidget.data = np.empty((0,2),int)
        self.acc.turnOnCavity()
        self.acc.reset()
        self.acc.findCrest(self.acc.phase)
        self.crestButton.setText('Stop')
        self.timer.start(25)

    def check_autocrest(self, cavityNumber, phasesign, gradient):
        if cavityNumber == self.cavityNumber:
            self.gradientWidget.widget.setText(str(gradient))
            fitting_params = self.acc.calculate_crest()
            self.calculatedCrestWidget.widget.setText(str(self.acc.crest - np.mod(fitting_params[2],360)))
            self.plotWidget.newFittedReading(self.acc.fittedData())
            if not phasesign * gradient > -1:
                self.stopCrest()
                self.acc.set_on_phase(self.acc.calculated_crest)
                print ('final values = ', self.acc.crest - self.acc.phase)

    def stopCrest(self):
        self.timer.stop()
        self.crestButton.setText('Crest')
        self.crestButton.clicked.disconnect(self.stopCrest)
        self.crestButton.clicked.connect(self.autocrest)

class crestingPlot(pg.PlotWidget):
    def __init__(self, parent=None, cavity=0):
        super(crestingPlot, self).__init__(parent)
        self.cavity = cavity
        self.plotItem = self.getPlotItem()
        self.data = np.empty((0,2),int)
        self.bpmPlot = self.plotItem.plot(symbol='+', symbolPen='r')
        self.fittedPlot = self.plotItem.plot(pen='b')
        self.plotItem.showGrid(x=True, y=True)

    def reset(self):
        self.data = np.empty((0,2),int)
        self.bpmPlot.clear()
        self.fittedPlot.clear()

    def newBPMReading(self, cavityNumber, data):
        if cavityNumber == self.cavity:
            self.data = np.append(self.data, [data], axis=0)
            self.bpmPlot.setData(self.data)

    def newFittedReading(self, data):
        self.fittedPlot.setData(np.array(data))


def main():
   app = QApplication(sys.argv)
   ex = crester()
   ex.show()
   # ex.testSleep()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()

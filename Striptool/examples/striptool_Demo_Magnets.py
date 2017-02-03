import sys, time, os
sys.path.append("..")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore, QtGui
import pyqtgraph as pg
import striptool as striptool
import numpy as np
''' Load loggerWidget library (comment out if not available) '''
sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
import loggerWidget as lw
import logging
logger = logging.getLogger(__name__)

import striptoolSignalTable as stable

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]

class timeButton(QPushButton):
    def __init__(self, mainForm):
        super(timeButton, self).__init__()
        self.__mainForm = mainForm
        self.connect(self, SIGNAL("clicked ()"), self.buttonPushed)

    def buttonPushed(self):
        # send signal to MainForm class, self.__comboID is actually row number, ind is what is selected
        self.__mainForm.emit(SIGNAL("timeButtonPushed(int)"), convert_to_seconds(str(self.text())))


class striptool_Demo_Magnets(QMainWindow):
    def __init__(self, parent = None):
        super(striptool_Demo_Magnets, self).__init__(parent)

        self.setWindowTitle("striptool_Demo_Magnets")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)

        ''' Initiate logger (requires loggerWidget - comment out if not available)'''
        self.logwidget1 = lw.loggerWidget([logger,striptool.logger])

        ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ''' initialise an instance of the stripPlot Widget '''
        self.sp = striptool.stripPlot(plotRateBar=False)

        ''' Here we create a tab layout widget, and put the 3 stripplots into a grid layout in one of the tabs
            In the second tab we put the first stripplot. NB: the stripplot "sp" can only exist in one place at a time!
            Comment out line 83 to see the difference. '''
        self.tab = QTabWidget()
        self.GUISplitter = QtGui.QSplitter()
        self.GUISplitter.setHandleWidth(14)
        self.GUISplitter.setOrientation(Qt.Vertical)
        self.GUISplitter.setStyleSheet("QSplitter::handle{background-color:transparent;}");
        self.GUISplitter.addWidget(stable.signalTable(self.sp))
        self.timeButton10 = self.createTimeButton('10s')
        self.timeButton60 = self.createTimeButton('1m')
        self.timeButton600 = self.createTimeButton('10m')
        self.connect(self, SIGNAL("timeButtonPushed(int)"), self.changePlotScales)
        self.timeButtonLayout = QHBoxLayout()
        self.timeButtonWidget = QWidget()
        self.timeButtonWidget.setMaximumHeight(100)
        self.timeButtonLayout.addWidget(self.timeButton10)
        self.timeButtonLayout.addWidget(self.timeButton60)
        self.timeButtonLayout.addWidget(self.timeButton600)
        self.timeButtonWidget.setLayout(self.timeButtonLayout)
        self.spTimeButtonsLayout = QVBoxLayout()
        self.spTimeButtonsWidget = QWidget()
        self.spTimeButtonsLayout.addWidget(self.sp,10)
        self.spTimeButtonsLayout.addWidget(self.timeButtonWidget,1)
        self.spTimeButtonsWidget.setLayout(self.spTimeButtonsLayout)
        self.GUISplitter.addWidget(self.sp)
        self.GUISplitter.addWidget(self.timeButtonWidget)

        handle = self.GUISplitter.handle(1)
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitterbutton = [1,2,3]
        self.splitterbuttonArrows = [1,2,3]

        self.splitterbutton[0] = QtGui.QToolButton(handle)
        self.splitterbutton[0].setArrowType(QtCore.Qt.DownArrow)
        self.splitterbuttonArrows[0] = [QtCore.Qt.UpArrow,QtCore.Qt.DownArrow]
        self.splitterbutton[0].clicked.connect(
            lambda: self.handleSplitterButton(no=0,closed=False))
        self.GUISplitter.splitterMoved.connect(lambda x: self.handleSplitterButtonArrow(no=0, pos=x))
        layout.addWidget(self.splitterbutton[0])
        handle.setLayout(layout)

        handle = self.GUISplitter.handle(2)
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitterbutton[2] = QtGui.QToolButton(handle)
        self.splitterbutton[2].setArrowType(QtCore.Qt.DownArrow)
        self.splitterbuttonArrows[2] = [QtCore.Qt.DownArrow, QtCore.Qt.UpArrow]
        self.splitterbutton[2].clicked.connect(
            lambda: self.handleSplitterButton(no=2,closed=False))
        self.GUISplitter.splitterMoved.connect(lambda x: self.handleSplitterButtonArrow(no=2, pos=x))
        layout.addWidget(self.splitterbutton[2])
        handle.setLayout(layout)

        self.GUISplitter.setStretchFactor(0,1)
        self.GUISplitter.setStretchFactor(1,4)
        self.GUISplitter.setStretchFactor(2,1)
        self.GUIsizes = [100, 1000, 100]
        self.handleSplitterButton(no=0,closed=True)
        self.handleSplitterButton(no=2,closed=True)


        self.tab.addTab(self.GUISplitter,"Strip Plot")
        ''' Here we connect the QTabWidget signal "currentChanged" to a function defined above. This will pause plots not currently visible
            whenever the tabs are changed. This reduces the load as only visible plots are updated. '''
        self.tab.currentChanged.connect(lambda x: self.pausePlots(self.tab))

        ''' Add loggerWidget Tab (requires loggerWidget - comment out if not available)'''
        self.tab.addTab(self.logwidget1,"Log")

        ''' This starts the plotting timer (by default at 1 Hz) '''
        self.sp.start()

        ''' modify the plot scale to 10 secs '''
        self.sp.setPlotScale(60)

        ''' Display the Qt App '''
        self.setCentralWidget(self.tab)

        self.sp.plotWidget.statusChanged.connect(self.updateStatusBar)

    def handleSplitterButton(self, no=0, closed=True):
        sizes = self.GUISplitter.sizes()
        if closed:
            self.GUISplitter.setStretchFactor(no,0)
            self.GUIsizes[no] = 0
        elif sizes[no] == 0:
            self.GUISplitter.setStretchFactor(no,1)
            self.GUIsizes[no] = 100
        else:
            self.GUISplitter.setStretchFactor(no,0)
            self.GUIsizes[no] = 0
        self.GUISplitter.setSizes(self.GUIsizes)
        self.handleSplitterButtonArrow(no=no)

    def handleSplitterButtonArrow(self, no=0, pos=0):
        sizes = self.GUISplitter.sizes()
        if sizes[no] > 0:
            self.splitterbutton[no].setArrowType(self.splitterbuttonArrows[no][0])
        else:
            self.splitterbutton[no].setArrowType(self.splitterbuttonArrows[no][1])

    def pausePlots(self, parentwidget):
        widgets = parentwidget.findChildren((striptool.stripPlot))
        for widget in widgets:
            if widget.isVisible():
                widget.pausePlotting(False)
                widget.plotUpdate()
            else:
                widget.pausePlotting(True)

    def updateStatusBar(self,text):
        self.statusBar.clearMessage()
    	self.statusBar.showMessage(text,2000)

    def createTimeButton(self,label):
        button = timeButton(self)
        button.setText(label)
        return button

    def changePlotScales(self, time):
        print 'time = ', time
        for plot in self.findChildren((striptool.stripPlot)):
            plot.setPlotScale(time)

def main():
   app = QApplication(sys.argv)
   ex = striptool_Demo_Magnets()
   ex.show()
   ex.pausePlots(ex.tab)
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()

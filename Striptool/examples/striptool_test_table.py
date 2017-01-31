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
        self.GUISplitter.addWidget(self.sp)
        handle = self.GUISplitter.handle(1)
        layout = QtGui.QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.splitterbutton = QtGui.QToolButton(handle)
        self.splitterbutton.setArrowType(QtCore.Qt.DownArrow)
        self.splitterbutton.clicked.connect(
            lambda: self.handleSplitterButton(False))
        self.GUISplitter.splitterMoved.connect(self.handleSplitterButtonArrow)
        layout.addWidget(self.splitterbutton)
        handle.setLayout(layout)
        self.GUISplitter.setStretchFactor(0,1)
        self.GUISplitter.setStretchFactor(1,4)
        self.handleSplitterButton(up=True)


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

    def handleSplitterButton(self, up=True):
        # width = self.GUISplitter.size().width()
        if up:
            self.GUISplitter.setStretchFactor(0,0)
            self.GUISplitter.setStretchFactor(1,1)
            self.GUISplitter.setSizes([0,1])
        elif not all(self.GUISplitter.sizes()):
            self.GUISplitter.setStretchFactor(0,1)
            self.GUISplitter.setStretchFactor(1,4)
            self.GUISplitter.setSizes([1,1000])
        else:
            self.GUISplitter.setStretchFactor(0,0)
            self.GUISplitter.setStretchFactor(1,1)
            self.GUISplitter.setSizes([0,1])
        self.handleSplitterButtonArrow()

    def handleSplitterButtonArrow(self):
        sizes = self.GUISplitter.sizes()
        if self.GUISplitter.sizes()[0] > 0:
            self.splitterbutton.setArrowType(QtCore.Qt.UpArrow)
        else:
            self.splitterbutton.setArrowType(QtCore.Qt.DownArrow)

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

def main():
   app = QApplication(sys.argv)
   ex = striptool_Demo_Magnets()
   ex.show()
   ex.pausePlots(ex.tab)
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()

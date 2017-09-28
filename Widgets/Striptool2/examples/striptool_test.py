import sys, time, os
sys.path.append(".")
sys.path.append("..")
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
import pyqtgraph as pg
import striptool as striptool
import scatterPlot as scatterplot
import numpy as np
''' Load loggerWidget library (comment out if not available) '''
# sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
# import loggerWidget as lw
# import logging
# logger = logging.getLogger(__name__)

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]

class timeButton(QPushButton):

    timeButtonPushed = pyqtSignal('int')

    def __init__(self, label):
        super(timeButton, self).__init__()
        self.setText(label)
        self.clicked.connect(self.buttonPushed)

    def buttonPushed(self):
        self.timeButtonPushed.emit(convert_to_seconds(str(self.text())))

class striptool_Demo(QMainWindow):
    def __init__(self, parent = None):
        super(striptool_Demo, self).__init__(parent)

        stdicon = self.style().standardIcon
        style = QStyle
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qApp.quit)

        self.setWindowTitle("striptool_Demo")
        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAction)

        ''' Initiate logger (requires loggerWidget - comment out if not available)'''
        # self.logwidget1 = lw.loggerWidget([logger,striptool.logger])

        ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ''' initialise an instance of the stripPlot Widget '''
        self.sp = striptool.stripPlot(plotRateBar=True)
        self.sp2 = striptool.stripPlot(plotRateBar=True)
        self.sp3 = scatterplot.scatterPlot(stripplot=self.sp2, plotRateBar=True)

        ''' Add some signals to the striptool - note they call our signal generator at a frequency of 1/timer (100 Hz and 10 Hz in these cases).
            The 'pen' argument sets the color of the curves
                - see <http://www.pyqtgraph.org/documentation/style.html>'''
        self.sp.addSignal(name='signal1',pen='r', timer=1.0/10.0, function=self.createRandomSignal, arg=[0.5])
        self.sp2.addSignal(name='signal3',pen='g', timer=1.0/10.0, function=self.createRandomSignal, arg=[100,10])
        self.sp2.addSignal(name='signal2',pen='r', timer=1.0/10.0, function=self.createRandomSignal, arg=[1e-8, 1e-9], logScale=True, verticalRange=[1e-10, 1e-7])
        self.sp2.addSignal(name='signal4',pen='b', timer=1.0/10.0, function=self.createRandomSignal, arg=[1e4, 1e1], logScale=True, verticalRange=[1e3, 1e5])
        self.sp2.addSignal(name='signal5',pen='c', timer=1.0/10.0, function=self.createRandomSignal, arg=[1])
        self.sp2.addSignal(name='signal6',pen='m', timer=1.0/10.0, function=self.createRandomSignal, arg=[3])
        self.sp2.addSignal(name='signal7',pen='y', timer=1.0/10.0, function=self.createRandomSignal, arg=[5])
        # self.sp3.addSignal(name='signal8',pen='b', timer=1.0/10.0, function=self.createRandomSignal, arg=[0.5])

        ''' this adds pre-data to the signal '''
        # ,'signal3':-3,'signal4':-1,'signal5':1,'signal6':3,'signal7':5
        # for name, moffset in {'signal3':[100,10]}.items():
        #     testdata = []
        #     t = time.time()
        #     n = 10000
        #     for i in range(n):
        #         self.sp2.records[name]['signal'].dataReady.emit([t-(n/10)+i/10.0,self.createRandomSignal(moffset[0],moffset[1],t-(n/10)+i/10.0)])
        #

        ''' To remove a signal, reference it by name or use the in-built controls'''
        # sp.removeSignal(name='signal1')
        # sp.removeSignal(name='signal2')

        ''' Here we create a tab layout widget, and put the 3 stripplots into a grid layout in one of the tabs
            In the second tab we put the first stripplot. NB: the stripplot "sp" can only exist in one place at a time!
        '''
        self.tab = QTabWidget()
        self.plotLayout = QVBoxLayout()
        self.splitter = QSplitter()
        self.splitter.setOrientation(Qt.Vertical)
        self.splitter.addWidget(self.sp2)
        self.splitter.addWidget(self.sp3)
        self.plotLayout.addWidget(self.splitter)
        self.timeButtonList = []
        self.timeButton10 = self.createTimeButton('10s')
        self.timeButton60 = self.createTimeButton('1m')
        self.timeButton600 = self.createTimeButton('10m')
        self.timeButton6000 = self.createTimeButton('100m')
        self.timeButton60000 = self.createTimeButton('1000m')
        self.timeButtonWidget = QWidget()
        self.timeButtonLayout = QHBoxLayout()
        self.timeButtonLayout.addWidget(self.timeButton10)
        self.timeButtonLayout.addWidget(self.timeButton60)
        self.timeButtonLayout.addWidget(self.timeButton600)
        self.timeButtonLayout.addWidget(self.timeButton6000)
        self.timeButtonLayout.addWidget(self.timeButton60000)
        self.plotLayout.addLayout(self.timeButtonLayout)
        self.plotWidget = QFrame()
        self.plotWidget.setLayout(self.plotLayout)
        self.tab.addTab(self.plotWidget,"Strip Plot")
        self.tab.addTab(self.sp,"Strip Plot 1")
        ''' Here we connect the QTabWidget signal "currentChanged" to a function defined above. This will pause plots not currently visible
            whenever the tabs are changed. This reduces the load as only visible plots are updated. '''
        self.tab.currentChanged.connect(lambda x: self.pausePlots(self.tab))

        ''' Add loggerWidget Tab (requires loggerWidget - comment out if not available)'''
        # self.tab.addTab(self.logwidget1,"Log")

        ''' This starts the plotting timer (by default at 1 Hz) '''
        self.sp.start()
        self.sp2.start()
        self.sp3.start()

        ''' modify the plot scale to 10 secs '''
        self.sp.setPlotScale(600)
        self.sp2.setPlotScale(60*1)
        # self.sp3.setPlotScale(600)

        # self.sp2.setPlotType(FFT=True)
        # self.sp3.setPlotType(FFT=False)
        self.sp.setPlotRate(10)
        self.sp2.setPlotRate(1)
        # self.sp3.setPlotRate(10)

        ''' Display the Qt App '''
        self.setCentralWidget(self.tab)

        # self.sp.plotWidget.statusChanged.connect(self.updateStatusBar)
        # self.sp2.plotWidget.statusChanged.connect(self.updateStatusBar)
        # self.sp3.plotWidget.statusChanged.connect(self.updateStatusBar)
    ''' This is a signal generator. It could easily read a magnet current using the hardware controllers
        The signal should have peaks at 5 Hz and 10 Hz, which should be seen on the FFT plot assuming the
        sample rate is high enough
    '''
    def createRandomSignal(self, mean=0, sigma=1, t=None):
        if t == None:
            t = time.time()
        signalValue = np.random.normal(mean, sigma)
        return signalValue

    def pausePlots(self, parentwidget):
        widgets = parentwidget.findChildren((striptool.stripPlot))
        for widget in widgets:
            if widget.isVisible():
                widget.pausePlotting(False)
                widget.plotUpdate()
            else:
                widget.pausePlotting(True)

    def createTimeButton(self,label):
        button = timeButton(label)
        button.timeButtonPushed.connect(self.changePlotScales)
        return button

    def changePlotScales(self, time):
        print( 'time = ', time)
        for plot in self.findChildren((striptool.stripPlot)):
            plot.setPlotScale(time)

    def updateStatusBar(self,text):
        self.statusBar.clearMessage()
        self.statusBar.showMessage(text,2000)

    def testSleep(self):
        import time
        for i in range(100):
            self.sp.setPlotScale((i+1)*60)
            self.sp2.setPlotScale((i+1)*60)
            self.sp3.setPlotScale((i+1)*60)
            QtTest.QTest.qWait(1000*60)
        exit()

    def closeEvent(self, event):
        for plot in self.findChildren((striptool.stripPlot)):
            plot.close()

def main():
   app = QApplication(sys.argv)
   # app.setStyle(QStyleFactory.create("plastique"))
   ex = striptool_Demo()
   ex.show()
   # ex.testSleep()
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()

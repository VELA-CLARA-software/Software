import sys, time, os
if getattr(sys, 'frozen', False):
    print( 'frozen!')
else:
    print( 'Not frozen!')
    sys.path.append("../../Widgets/Striptool2")
# from PyQt4.QtCore import pyqtSignal, Qt
# from PyQt4.QtGui import QFileDialog, QWidget, QPushButton, QMainWindow, QApplication, QStyle, QAction, qApp, QStatusBar, QTabWidget, QHBoxLayout, QPixmap, QSplashScreen, QDesktopWidget, QIcon
try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
    import qt4icons
except ImportError:
    print ('importing PyQt5')
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *
    import qt5icons
from pyqtgraph.dockarea import *

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

        scatterPlotAction = QAction('+Scatter', self)
        scatterPlotAction.setStatusTip('Add Scatter Plot')
        scatterPlotAction.triggered.connect(self.addScatterPlot)

        fftPlotAction = QAction('+FFT', self)
        fftPlotAction.setStatusTip('Add FFT Plot')
        fftPlotAction.triggered.connect(self.addFFTPlot)

        self.setWindowTitle("striptool_Demo")
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')

        ''' Initiate logger (requires loggerWidget - comment out if not available)'''
        # self.logwidget1 = lw.loggerWidget([logger,striptool.logger])

        ''' These are some options for pyqtgraph that make the graph black-on-white, and turn on antialiasing, which is nicer on the eye '''
        pg.setConfigOptions(antialias=False)
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')

        ''' initialise an instance of the stripPlot Widget '''
        self.generalplot = generalplot.generalPlot()
        self.scrollingplot = self.generalplot.scrollingPlot()
        self.fftplot = self.generalplot.fftPlot()
        self.histogramplot = self.generalplot.histogramPlot()
        self.scatterplot = self.generalplot.scatterPlot()
        self.legend = self.generalplot.legend()
        self.signaltable = signaltable.signalTable(parent=self.generalplot)#, VELAMagnetController=Vmagnets, CLARAMagnetController=Cmagnets, BPMController=bpms, GeneralController=general)

        reloadSettingsAction = QAction('Reload Settings', self)
        reloadSettingsAction.setStatusTip('Reload Settings YAML File')
        reloadSettingsAction.triggered.connect(self.signaltable.reloadSettings)
        fileMenu.addAction(reloadSettingsAction)

        saveAllDataAction = QAction('Save Data', self)
        saveAllDataAction.setStatusTip('Save All Data')
        saveAllDataAction.triggered.connect(self.generalplot.saveAllData)
        fileMenu.addAction(saveAllDataAction)
        fileMenu.addAction(exitAction)

        self.enabledPlotNames = []
        self.legend.tree.legendselectionchanged.connect(self.addSignalToFFTHistogramPlots)

        ''' Create some common axes to plot similar signals with '''
        # self.generalplot.createAxis(name='logsmall', color='k',logMode=True, verticalRange=[1e-10, 1e-7])
        # self.generalplot.createAxis(name='logbig', color='b', logMode=True, verticalRange=[1e3, 1e5])
        # self.generalplot.createAxis(name='smallnumbers', color='g', logMode=False, verticalRange=[-5,10])

        ''' Add some signals to the striptool - note they call our signal generator at a frequency of 1/timer (100 Hz and 10 Hz in these cases).
            The 'pen' argument sets the color of the curves
                - see <http://www.pyqtgraph.org/documentation/style.html>'''
        self.generalplot.addSignal(name='signal1', pen='g', timer=1.0/50.0, function=self.createRandomSignal, args=[100,10,2.3347])
        self.generalplot.addSignal(name='signal2', pen='r', timer=1.0/10.0, function=self.createRandomSignal, args=[1e-8, 1e-9,4.005], logScale=False)
        # self.generalplot.addSignal(name='signal3', pen='b', timer=1.0/10.0, function=self.createRandomSignal, args=[1e4, 1e1, 2])
        # self.generalplot.addSignal(name='signal4', pen='c', timer=1.0/20.0, function=self.createRandomSignal, args=[1,0.5,7.8])
        # self.generalplot.addSignal(name='signal5', pen='m', timer=1.0/10.0, function=self.createRandomSignal, args=[3,2,0.87])
        # self.generalplot.addSignal(name='signal6', pen='y', timer=1.0/10.0, function=self.createRandomSignal, args=[5,2,2.35])


        # self.fftplot.addPlot('signal2')

        ''' this adds pre-data to the signal '''
        # ,'signal3':-3,'signal4':-1,'signal5':1,'signal6':3,'signal7':5
        # for name, moffset in {'signal3':[1e4, 1e1, 2]}.items():
        #     testdata = []
        #     t = time.time()
        #     n = 10000
        #     for i in range(n):
        #         self.generalplot.records[name]['signal'].timer.dataReady.emit([t-(n/10)+i/10.0,self.createRandomSignal(moffset[0], moffset[1], moffset[2],t-(n/10)+i/10.0)])

        ''' To remove a signal, reference it by name or use the in-built controls'''
        # sp.removeSignal(name='signal1')
        # sp.removeSignal(name='signal2')

        ''' Here we create a tab layout widget, and put the 3 stripplots into a grid layout in one of the tabs
            In the second tab we put the first stripplot. NB: the stripplot "sp" can only exist in one place at a time!
        '''
        self.tab = QTabWidget()
        self.area = DockArea()
        d1 = Dock("Scrolling Plot")
        d2 = Dock("Plot Legend")
        d3 = Dock("FFT Plot")
        d4 = Dock("Scatter Plot")
        d5 = Dock("Histogram Plot")
        d1.addWidget(self.scrollingplot)
        d2.addWidget(self.legend)
        d3.addWidget(self.fftplot)
        d4.addWidget(self.scatterplot)
        d5.addWidget(self.histogramplot)
        self.area.addDock(d1, position='top')
        self.area.addDock(d2, position='right', relativeTo=d1)
        self.area.addDock(d3,'bottom')
        self.area.addDock(d4, position='right', relativeTo=d3)
        self.area.addDock(d5, position='right', relativeTo=d4)

        ''' Make QSPlitter '''
        self.plotLayout = splitterWithHandles()
        self.plotLayout.setOrientation(Qt.Vertical)
        self.plotLayout.addWidget(self.signaltable)
        self.plotLayout.addWidget(self.area)
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
        self.timeButtonWidget.setLayout(self.timeButtonLayout)
        self.plotLayout.addWidget(self.timeButtonWidget)
        ''' Style QSplitter Handles '''
        self.plotLayout.setHandleWidth(14)
        self.plotLayout.setStyleSheet("QSplitter::handle{background-color:transparent;}");
        self.plotLayout.handle(1).setLocation('top','Add Signal')
        self.plotLayout.handle(2).setLocation('bottom','Set Timebase')
        self.plotLayout.handle(1).setClosed()
        self.plotLayout.handle(2).setClosed()

        ''' Make Frame Widget '''
        # self.plotWidget = QFrame()
        # self.plotWidget.setLayout(self.plotLayout)
        # self.tab.addTab(self.plotWidget,"Strip Plot")

        ''' Add loggerWidget Tab (requires loggerWidget - comment out if not available)'''
        # self.tab.addTab(self.logwidget1,"Log")

        ''' This starts the plotting timer (by default at 1 Hz) '''
        self.generalplot.start()
        self.scrollingplot.start(100)
        self.fftplot.start()
        # self.scatterplot.start()
        self.histogramplot.start()

        ''' modify the plot scale to 10 secs '''
        self.scrollingplot.setPlotScale(60)

        ''' Display the Qt App '''
        self.setCentralWidget(self.plotLayout)


    ''' This is a signal generator. It could easily read a magnet current using the hardware controllers
        The signal should have peaks at 5 Hz and 10 Hz, which should be seen on the FFT plot assuming the
        sample rate is high enough
    '''
    def createRandomSignal(self, mean=0, sigma=1, freq=1.682, t=None):
        if t == None:
            t = time.time()
        signalValue = mean+sigma*np.sin(2*freq*np.pi*t+0.05)+0.5*np.random.normal(mean, sigma)#+np.sin(1.384*2*np.pi*t-0.1)+0.5*np.random.normal(mean, sigma)
        return signalValue

    def addScatterPlot(self):
        d = Dock("Scatter Plot")
        scatterplot = self.generalplot.scatterPlot()
        d.addWidget(scatterplot)
        self.area.addDock(d, position='right', relativeTo="Scatter Plot")

    def addFFTPlot(self):
        d = Dock("FFT Plot")
        fftplot = self.generalplot.fftPlot()
        d.addWidget(fftplot)
        self.area.addDock(d, position='right', relativeTo="FFT Plot")

    def addSignalToFFTHistogramPlots(self,names):
        for name in names:
            if name not in self.enabledPlotNames:
                self.enabledPlotNames.append(name)
            self.fftplot.selectionChange(name, True)
            self.histogramplot.selectionChange(name, True)
        for name in self.enabledPlotNames:
            if name not in names:
                self.fftplot.selectionChange(name, self.legend.tree.isFFTEnabled(name))
                self.histogramplot.selectionChange(name, self.legend.tree.isHistogramEnabled(name))

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
        for plot in self.findChildren((scrollingplot.scrollingPlot)):
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
        for plot in self.findChildren((scrollingplot.scrollingPlot)):
            plot.close()

def main():
   app = QApplication(sys.argv)
   app_icon = QIcon(':/striptool.ico')
   app.setWindowIcon(app_icon)
   # app.setStyle(QStyleFactory.create("plastique"))
   splash_pix = QPixmap(':/striptool.png')
   splash = QSplashScreen(splash_pix)
   print('here?')
   splash.setWindowFlags(Qt.FramelessWindowHint)
   splash.setEnabled(False)
   splash.show()
   splash.showMessage("<h1><font color='#6BBAFD'>Striptool Initialising...</font></h1>", Qt.AlignTop | Qt.AlignCenter, Qt.black)
   global pg, generalplot, scrollingplot, signaltable, np, splitterWithHandles
   import pyqtgraph as pg
   import generalPlot as generalplot
   import scrollingPlot as scrollingplot
   import signalTable as signaltable
   import numpy as np
   from splitterWithHandles import splitterWithHandles
   ex = striptool_Demo()
   ex.show()
   splash.finish(ex)
   sys.exit(app.exec_())

if __name__ == '__main__':
   main()

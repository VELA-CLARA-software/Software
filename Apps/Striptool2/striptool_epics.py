import sys, time, os
if getattr(sys, 'frozen', True):
    print 'Frozen!'
    sys.path.append("../../Widgets/Striptool2")
sys.path.append("../../../")
import Software.Procedures.qt as qt
from pyqtgraph.dockarea import DockArea, Dock
import VELA_CLARA_Magnet_Control as vmag
import VELA_CLARA_BPM_Control as vbpmc
import  VELA_CLARA_General_Monitor as vgen

''' Load loggerWidget library (comment out if not available) '''
# sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\..\\..\\loggerWidget\\')
# import loggerWidget as lw
# import logging
# logger = logging.getLogger(__name__)

seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800}

def convert_to_seconds(s):
    return int(s[:-1]) * seconds_per_unit[s[-1]]

class timeButton(qt.QPushButton):

    timeButtonPushed = qt.pyqtSignal('int')

    def __init__(self, label):
        super(timeButton, self).__init__()
        self.setText(label)
        self.clicked.connect(self.buttonPushed)

    def buttonPushed(self):
        self.timeButtonPushed.emit(convert_to_seconds(str(self.text())))

class striptool_Demo(qt.QMainWindow):
    def __init__(self, parent = None):
        super(striptool_Demo, self).__init__(parent)

        stdicon = self.style().standardIcon
        style = qt.QStyle
        exitAction = qt.QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(qt.qApp.quit)

        scatterPlotAction = qt.QAction('+Scatter', self)
        scatterPlotAction.setStatusTip('Add Scatter Plot')
        scatterPlotAction.triggered.connect(self.addScatterPlot)

        fftPlotAction = qt.QAction('+FFT', self)
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
        self.signaltable = signaltable.signalTable(parent=self.generalplot,
        VELAMagnetController=Vmagnets,
        CLARAMagnetController=Cmagnets,
        VELABPMController=Vbpms,
        CLARABPMController=Cbpms,
        GeneralController=general)

        reloadSettingsAction = qt.QAction('Reload Settings', self)
        reloadSettingsAction.setStatusTip('Reload Settings YAML File')
        reloadSettingsAction.triggered.connect(self.signaltable.reloadSettings)
        fileMenu.addAction(reloadSettingsAction)

        saveAllDataAction = qt.QAction('Save Data', self)
        saveAllDataAction.setStatusTip('Save All Data')
        saveAllDataAction.triggered.connect(self.generalplot.saveAllData)
        fileMenu.addAction(saveAllDataAction)
        fileMenu.addAction(exitAction)

        self.enabledPlotNames = []
        self.legend.tree.legendselectionchanged.connect(self.addSignalToFFTHistogramPlots)

        ''' Here we create a DockArea layout widget, and put the 4 types of plot into a grid layout
            We place all of it in a modified QSPlitter (with Handles)
        '''
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
        self.plotLayout.setOrientation(qt.Qt.Vertical)
        self.plotLayout.addWidget(self.signaltable)
        self.plotLayout.addWidget(self.area)
        self.timeButtonList = []
        self.timeButton10 = self.createTimeButton('10s')
        self.timeButton60 = self.createTimeButton('1m')
        self.timeButton600 = self.createTimeButton('10m')
        self.timeButton6000 = self.createTimeButton('100m')
        self.timeButton60000 = self.createTimeButton('1000m')
        self.timeButtonWidget = qt.QWidget()
        self.timeButtonLayout = qt.QHBoxLayout()
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
        ''' Set up the Handles with labels '''
        self.plotLayout.handle(1).setLocation('top','Add Signal')
        self.plotLayout.handle(2).setLocation('bottom','Set Timebase')
        ''' Default the Handles to closed '''
        self.plotLayout.handle(1).setClosed()
        self.plotLayout.handle(2).setClosed()

        ''' This starts the plotting timer (by default at 1 Hz) '''
        self.generalplot.start()
        self.scrollingplot.start()
        self.fftplot.start()
        self.scatterplot.start()
        self.histogramplot.start()

        ''' modify the plot scale to 60 secs '''
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
            qt.QtTest.QTest.qWait(1000*60)
        exit()

    def closeEvent(self, event):
        for plot in self.findChildren((scrollingplot.scrollingPlot)):
            plot.close()

def main():
    app = qt.QApplication(sys.argv)
    app_icon = qt.QIcon(':/striptool.ico')
    app.setWindowIcon(app_icon)
    # app.setStyle(QStyleFactory.create("plastique"))
    splash_pix = qt.QPixmap(':/striptool.png')
    splash = qt.QSplashScreen(qt.QDesktopWidget().screen(), splash_pix)
    splash.setWindowFlags(qt.Qt.FramelessWindowHint)
    splash.setEnabled(False)
    splash.show()
    splash.showMessage("<h1><font color='#6BBAFD'>Striptool Initialising...</font></h1>", qt.Qt.AlignTop | qt.Qt.AlignCenter, qt.Qt.black)
    global pg, generalplot, scrollingplot, signaltable, np, splitterWithHandles
    import pyqtgraph as pg
    import generalPlot as generalplot
    import scrollingPlot as scrollingplot
    import signalTable as signaltable
    import numpy as np
    from splitterWithHandles import splitterWithHandles
    maginit = vmag.init()
    bpms = vbpmc.init()
    global Vmagnets, Cmagnets, Vbpms, Cbpms, general
    Vmagnets = maginit.physical_VELA_INJ_Magnet_Controller()
    Cmagnets = maginit.physical_CLARA_PH1_Magnet_Controller()
    Vbpms = bpms.physical_VELA_INJ_BPM_Controller()
    Cbpms = bpms.physical_CLARA_PH1_BPM_Controller()
    general = vgen.init()
    ex = striptool_Demo()
    ex.show()
    splash.finish(ex)
    sys.exit(app.exec_())

if __name__ == '__main__':
   main()

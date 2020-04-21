import sys, time, os, datetime, math
import pyqtgraph as pg
import collections
import numpy as np
sys.path.append("../../../")
import Software.Procedures.qt as qt
import colours as colours

''' This class is a PyQtGraph axis which modifies the data points from "seconds before the current time" into Hours:Mins:Secs format.
We only want to do this for linear plots, so it is turned off in the FFT and Histogram plots. Also, if we turn "autoscroll" off, the
time is relative to the moment we switched it off.
'''
class HAxisTime(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(HAxisTime, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.dateTicksOn = True
        self.autoscroll = True

    def updateTimeOffset(self,time):
        self.timeOffset = time
        self.resizeEvent()
        self.update()

    def tickStrings(self, values, scale, spacing):
        if not hasattr(self, 'fixedtimepoint'):
            self.fixedtimepoint = round(time.time(),2)
        if self.dateTicksOn:
            if self.autoscroll:
                reftime = round(time.time(),2)
            else:
                reftime = self.fixedtimepoint
            try:
                ticks = [time.strftime("%H:%M:%S", time.localtime(x)) for x in values]
            except:
                ticks = []
            return ticks
        else:
            places = max(0, np.ceil(-np.log10(spacing*scale)))
            strings = []
            for v in values:
                vs = v * scale
                if abs(vs) < .001 or abs(vs) >= 10000:
                    vstr = "%g" % vs
                else:
                    vstr = ("%%0.%df" % places) % vs
                strings.append(vstr)
            return strings

class VAxis(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(VAxis, self).__init__(parent=parent, orientation=orientation, linkView=linkView)

    def logTickStrings(self, values, scale, spacing):
        return ["%0.1g"%abs(x) for x in 10 ** np.array(values).astype(float)]

class MenuBox(pg.GraphicsObject):
    """
    This class draws a rectangular area. Right-clicking inside the area will
    raise a custom context menu which also includes the context menus of
    its parents.
    """
    def __init__(self, name):
        self.name = name
        self.pen = pg.mkPen('r')

        # menu creation is deferred because it is expensive and often
        # the user will never see the menu anyway.
        self.menu = None

        # note that the use of super() is often avoided because Qt does not
        # allow to inherit from multiple QObject subclasses.
        pg.GraphicsObject.__init__(self)


    # All graphics items must have paint() and boundingRect() defined.
    def boundingRect(self):
        return qt.QRectF(0, 0, 10, 10)

    def paint(self, p, *args):
        p.setPen(self.pen)
        p.drawRect(self.boundingRect())


    # On right-click, raise the context menu
    def mouseClickEvent(self, ev):
        if ev.button() == qt.Qt.RightButton:
            if self.raiseContextMenu(ev):
                ev.accept()

    def raiseContextMenu(self, ev):
        menu = self.getContextMenus()

        # Let the scene add on to the end of our context menu
        # (this is optional)
        menu = self.scene().addParentContextMenus(self, menu, ev)

        pos = ev.screenPos()
        menu.popup(qt.Qt.QPoint(pos.x(), pos.y()))
        return True

    # This method will be called when this item's _children_ want to raise
    # a context menu that includes their parents' menus.
    def getContextMenus(self, event=None):
        if self.menu is None:
            self.menu = qt.QMenu()
            self.menu.setTitle(self.name+ " options..")

            green = qt.QAction("Turn green", self.menu)
            green.triggered.connect(self.setGreen)
            self.menu.addAction(green)
            self.menu.green = green

            blue = qt.QAction("Turn blue", self.menu)
            blue.triggered.connect(self.setBlue)
            self.menu.addAction(blue)
            self.menu.green = blue

            alpha = qt.QWidgetAction(self.menu)
            alphaSlider = qt.QSlider()
            alphaSlider.setOrientation(qt.Qt.Horizontal)
            alphaSlider.setMaximum(255)
            alphaSlider.setValue(255)
            alphaSlider.valueChanged.connect(self.setAlpha)
            alpha.setDefaultWidget(alphaSlider)
            self.menu.addAction(alpha)
            self.menu.alpha = alpha
            self.menu.alphaSlider = alphaSlider
        return self.menu

    # Define context menu callbacks
    def setGreen(self):
        self.pen = pg.mkPen('g')
        # inform Qt that this item must be redrawn.
        self.update()

    def setBlue(self):
        self.pen = pg.mkPen('b')
        self.update()

    def setAlpha(self, a):
        self.setOpacity(a/255.)

class scrollingPlot(qt.QWidget):

    doCurveUpdate = qt.pyqtSignal()
    timeChangeSignal = qt.pyqtSignal('float')

    def __init__(self, generalplot, parent=None, plotRateBar=False, color=0):
        super(scrollingPlot, self).__init__(parent)
        self.pg = pg
        self.paused = False
        self.plotrate = 1
        ''' create the scatterPlot as a grid layout '''
        self.scrollingPlot = qt.QVBoxLayout()
        self.plotThread = qt.QTimer()
        self.paused = False
        self.generalPlot = generalplot
        self.records = self.generalPlot.records
        ''' Create generalPlot object '''
        self.scrollingPlotPlot = scrollingPlotPlot(self)
        ''' set-up plot rate slider '''
        self.setupPlotRateSlider()
        self.scrollingPlot.addWidget(self.scrollingPlotPlot.plotWidget, 5)
        if plotRateBar:
            self.setupPlotRateSlider()
            self.scrollingPlot.addLayout(self.plotRateLayout)
        self.setLayout(self.scrollingPlot)

        self.generalPlot.signalAdded.connect(self.addSignal)
        self.generalPlot.signalRemoved.connect(self.removeSignal)

    def addSignal(self, name):
        name = str(name)
        self.records[name].scrollingplot = self.scrollingPlotPlot
        curve = self.scrollingPlotPlot.addCurve(name)
        self.records[name].curve = curve

    def removeSignal(self, name):
        # print 'removing signal = ', name
        self.scrollingPlotPlot.removeCurve(name)

    def setupPlotRateSlider(self):
        self.plotRateLayout = qt.QHBoxLayout()
        self.plotRateLabel = qt.QLabel()
        self.plotRateLabel.setText('Plot Update Rate ['+str(self.plotrate)+' Hz]:')
        self.plotRateLabel.setAlignment(qt.Qt.AlignCenter)
        self.plotRateSlider = qt.QSlider()
        self.plotRateSlider.setOrientation(qt.Qt.Horizontal)
        self.plotRateSlider.setInvertedAppearance(False)
        self.plotRateSlider.setInvertedControls(False)
        self.plotRateSlider.setMinimum(1)
        self.plotRateSlider.setMaximum(50)
        self.plotRateSlider.setValue(self.plotrate)
        self.plotRateSlider.valueChanged.connect(self.setPlotRate)
        self.plotRateLayout.addWidget(self.plotRateLabel)
        self.plotRateLayout.addWidget(self.plotRateSlider)

    def setPlotRate(self, value):
        self.plotrate = value
        self.plotRateLabel.setText('Plot Update Rate [' + str(self.plotrate) + ' Hz]:')
        self.plotThread.setInterval(1000 * 1 / value)

    def start(self, timer=1000):
        self.plotUpdate()
        self.plotThread.start(timer)
        self.lastplottime = round(time.time(),2)
        self.plotThread.timeout.connect(self.plotUpdate)

    def plotUpdate(self):
        if self.isVisible():
            if not self.paused:
                self.doCurveUpdate.emit()
                lastplottime = round(time.time(),2)
                self.timeOffset = lastplottime-self.lastplottime
                for name in self.records:
                    self.records[name].curve.clearCurve()
                self.scrollingPlotPlot.plot.vb.disableAutoRange(axis='x')
                self.scrollingPlotPlot.plot.vb.translateBy(x=self.timeOffset)
                for name in self.records:
                    self.records[name].curve.drawCurve()
                self.timeChangeSignal.emit(self.timeOffset)
                self.lastplottime = lastplottime

    def pausePlotting(self, value=True):
        self.paused = value
        # self.plotWidget.togglePause(self.paused)

    def setPlotScale(self, timescale):
        self.timescale = timescale
        self.scrollingPlotPlot.setPlotScale([time.time()+(-1.025*timescale),time.time()+(0.025*timescale)])

    def createAxis(self, *args, **kwargs):
        self.scrollingPlotPlot.createAxis(*args, **kwargs)


    def setYRange(self, min, max):
        self.scrollingPlotPlot.setYRange(min, max)

class scrollingPlotPlot(qt.QWidget):

    plotUpdated = qt.pyqtSignal()
    newaxis = qt.pyqtSignal()
    yAxisScaled = qt.pyqtSignal(float, float)

    def __init__(self, scrollingplot, parent = None):
        super(scrollingPlotPlot, self).__init__(parent=parent)
        self.scrollingPlot = scrollingplot
        self.records = self.scrollingPlot.records
        self.paused = False
        self.doingPlot = False
        self.paused = False
        self.plotWidget = pg.GraphicsLayoutWidget()
        self.threads = {}
        self.workers = {}
        self.namedaxes = {}
        self.createPlot()
        self.yScale = 1
        self.yPos = 1

    ''' This creates a PyQtGraph plot object (self.plot) and instantiates the bottom axis to be a CAxisTime axis '''
    def createPlot(self):
        self.date_axis = HAxisTime(orientation = 'bottom')
        self.scrollingPlot.timeChangeSignal.connect(self.date_axis.updateTimeOffset)
        self.leftaxis = pg.AxisItem("left")
        self.plot = self.plotWidget.addPlot(row=0,col=50, autoDownsample=True, clipToView=True, antialias=False, downsampleMethod='subsample', axisItems={'bottom':self.date_axis})
        self.plot.vb.setMouseEnabled()
        axiszero = self.plot.vb.menu.addAction('Set Axes to 0')
        axiszero.triggered.connect(self.setAxesToZero)
        self.plot.vb.sigYRangeChanged.connect(self.vbYRangeChanged)
        self.plot.disableAutoRange(False)
        self.plot.setRange(xRange=[-0.5,1.5])
        self.plot.showAxis('left', False)
        self.plot.mouseOver = False
        self.plot.showGrid(x=True, y=True)

    def setAxesToZero(self):
        for a in self.namedaxes.iteritems():
            axis, vb = a[1]
            vb.enableAutoRange(y=False)
            currentrange = vb.viewRange()
            vb.setYRange(0, currentrange[1][1], padding=0)

    def setYRange(self, *args, **kwargs):
        for a in self.namedaxes.iteritems():
            axis, vb = a[1]
            vb.enableAutoRange(y=False)
            vb.setYRange(*args, **kwargs)


    def setAxisToZero(self, vb):
        vb.enableAutoRange(y=False)
        currentrange = vb.viewRange()
        vb.setYRange(0, currentrange[1][1], padding=0)

    def vbYRangeChanged(self,x,y):
        pos = (y[1]+y[0])/2 - self.yPos
        scale = (y[1]-y[0])/self.yScale
        self.yAxisScaled.emit(scale, pos)
        self.yScale = (y[1]-y[0])
        self.yPos = (y[1]+y[0])/2

    ''' Sets the timescale of the plotting data '''
    def setPlotScale(self, timescale, padding=0.0):
        self.plotRange = timescale
        self.globalPlotRange = list(timescale)
        self.plot.vb.setRange(xRange=self.globalPlotRange, padding=0)

    ''' Function to update timescale if the viewbox range changes - i.e. via mouse interaction or autoscale'''
    def updatePlotScale(self, padding=0.0):
        vbPlotRange = self.vb.viewRange()[0]
        self.globalPlotRange = self.vb.viewRange()[0]
        self.plotRange = self.globalPlotRange

    ''' Toggles autoscroll on the plot '''
    def toggleAutoScroll(self, value):
        self.autoscroll = value
        if not value:
            self.currenttime = self.currentPlotTime
            self.fixedtimepoint = self.currentPlotTime

    def createAxis(self, name='', color='k', logMode=False, verticalRange=None):
        axis = pg.AxisItem("left")
        labelStyle = {'color': '#'+pg.colorStr(pg.mkColor(color))[0:-2]}
        axis.setLabel(name,**labelStyle)
        viewbox = pg.ViewBox()
        axis.linkToView(viewbox)
        viewbox.setXLink(self.plot.vb)
        # viewbox.setYLink(self.plot.vb)
        axiszero = viewbox.menu.addAction('Set Axis to 0')
        axiszero.triggered.connect(lambda: self.setAxisToZero(viewbox))
        self.namedaxes[name] = [axis, viewbox]
        if not verticalRange == None:
            viewbox.setRange(yRange=verticalRange, disableAutoRange=True)
        col = self.findFirstEmptyColumnInGraphicsLayout()
        self.plotWidget.ci.addItem(axis, row = 0, col = col,  rowspan=1, colspan=1)
        self.plotWidget.ci.addItem(viewbox, row=0, col=50)
        axis.setLogMode(logMode)
        # self.newaxis.emit()
        return axis, viewbox

    def getAxes(self):
        return self.namedaxes.keys()

    def changeAxis(self, name, axisname):
        record = self.records
        axis, viewbox = self.namedaxes[axisname]
        record[name].viewbox = viewbox
        record[name].axis = axis
        record[name].logScale = axis.logMode
        record[name].curve.changeViewbox(viewbox)

    ''' Helper function to add a curve to the plot '''
    def addCurve(self, name):
        # Create New Axis
        record = self.records
        if record[name].axisname == None:
            axis, viewbox = self.createAxis(name=name, color=record[name].pen, logMode=record[name].logScale, verticalRange=record[name].verticalRange)
            record[name].axisname = name
        elif record[name].axisname in  self.namedaxes:
            axis, viewbox = self.namedaxes[record[name].axisname]
        else:
            axis, viewbox = self.createAxis(name=record[name].axisname, color=record[name].pen, logMode=record[name].logScale,verticalRange=record[name].verticalRange)
        record[name].viewbox = viewbox
        record[name].axis = axis
        axis.setLogMode(record[name].logScale)
        # record[name]['logScale'] = axis.logMode
        self.threads[name] = qt.QThread(self.scrollingPlot)
        self.workers[name] = curveRecordWorker(self, name)
        self.workers[name].moveToThread(self.threads[name])
        self.threads[name].start()
        # print 'adding curve[',name,'] = ', self.workers[name].curve
        return self.workers[name].curve

    def removeCurve(self, name):
        record = self.records
        name = str(name)
        # print 'removing stripplot signal = ', name
        axisname = record[name].axisname
        axis, viewbox = self.namedaxes[record[name].axisname]
        self.threads[name].quit()
        self.plotWidget.ci.removeItem(axis)
        try:
            self.plotWidget.ci.removeItem(viewbox)
        except:
            pass
        # print 'removing curve[',name,'] = ', self.workers[name].curve
        self.workers[name].curve.stop()
        self.workers[name].curve.deleteLater()
        self.workers[name].deleteLater()


    # def toggleAxis(self, name, visible):
    #     axis, viewbox = self.namedaxes[self.records[name]['axisname']]
    #     axis.setVisible(visible)

    def findFirstEmptyColumnInGraphicsLayout(self):
        rowsfilled =  self.plotWidget.ci.rows.get(0, {}).keys()
        for i in range(49):
            if not i in rowsfilled:
                return i

class curveRecordWorker(qt.QObject):
    def __init__(self, plot, name):
        qt.QObject.__init__(self)
        self.curve = curve(plot, name)

''' This is the curve class which enables plotting on a plotting object. Making it a class eases control of the different options for multiple curves'''
class curve(qt.QObject):
    def __init__(self, plot, name):
        qt.QObject.__init__(self)
        self.plot = plot
        self.records = self.plot.records
        self.name = name
        self.vb = self.records[name].viewbox
        self.logMode = self.records[name].logScale
        # print 'self.logMode = ', self.logMode
        self.plot.yAxisScaled.connect(self.scaleYAxis)
        self.curve = pg.PlotDataItem(autoDownsample=True,clipToView=True)
        self.curve.setPen(pg.mkPen(self.records[self.name].pen))
        self.curve10 = pg.PlotDataItem(autoDownsample=True,clipToView=True)
        self.curve10.setPen(pg.mkPen(**{'color': self.records[self.name].pen, 'dash': [2,2], 'width': 2}))
        self.curve100 = pg.PlotDataItem(autoDownsample=True,clipToView=True)
        self.curve100.setPen(pg.mkPen(**{'color': self.records[self.name].pen, 'dash': [2,2], 'width': 3}))
        self.curve1000 = pg.PlotDataItem(autoDownsample=True,clipToView=True)
        self.curve1000.setPen(pg.mkPen(**{'color': self.records[self.name].pen, 'dash': [3,3], 'width': 4}))
        self.vb.addItem(self.curve)
        self.vb.addItem(self.curve10)
        self.vb.addItem(self.curve100)
        self.vb.addItem(self.curve1000)
        self.points = collections.deque(maxlen=self.records[name].maxlength)
        self.points10 = collections.deque(maxlen=self.records[name].maxlength)
        self.points100 = collections.deque(maxlen=self.records[name].maxlength)
        self.points1000 = collections.deque(maxlen=self.records[name].maxlength)
        self.visibility = {'curve': True, 'curve10': False, 'curve100': False, 'curve1000': False}
        self.plot.records[name].worker.recordLatestValueSignal.connect(lambda x: self.updateData(x, self.points))
        self.plot.records[name].worker.recordMean10Signal.connect(lambda x: self.updateData(x, self.points10))
        self.plot.records[name].worker.recordMean100Signal.connect(lambda x: self.updateData(x, self.points100))
        self.plot.records[name].worker.recordMean1000Signal.connect(lambda x: self.updateData(x, self.points1000))
        self.drawCurve()

    def scaleYAxis(self, scale, pos):
        newpos = self.vb.state['viewRange'][1]
        newscale = newpos[1] - newpos[0]
        # self.vb.translateBy(y=pos*newscale)
        self.vb.scaleBy(y=scale, center=self.points1000[-1])

    def stop(self):
        try:
            self.plot.scrollingPlot.timeChangeSignal.disconnect(self.updateTimeOffset)
        except:
            pass
        self.plot.records[self.name].worker.recordLatestValueSignal.disconnect()
        self.plot.records[self.name].worker.recordMean10Signal.disconnect()
        self.plot.records[self.name].worker.recordMean100Signal.disconnect()
        self.plot.records[self.name].worker.recordMean1000Signal.disconnect()

    def setVisibility(self, linename, visible):
        self.visibility[linename] = visible
        # if linename is 'curve':
        #     if visible is False:
        #         for k in self.visibility.keys():
        #             getattr(self, k).setVisible(False)
        #     else:
        #         for k,v in self.visibility.iteritems():
        #             getattr(self, k).setVisible(self.visibility[k])
        # else:
        if linename in self.visibility:
            self.visibility[linename] = visible
            getattr(self, linename).setVisible(visible)


    def changeViewbox(self, viewbox):
        name = self.name
        self.vb = self.records[name].viewbox
        self.lineOn = False

    def clearCurve(self):
        pass

    def drawCurve(self):
        self.redrawLines(self.points, self.curve, 'curve', {'color': self.records[self.name].pen})
        self.redrawLines(self.points10, self.curve10, 'curve10', {'color': self.records[self.name].pen, 'dash': [2,2], 'width': 2})
        self.redrawLines(self.points100, self.curve100, 'curve100', {'color': self.records[self.name].pen, 'dash': [2,2], 'width': 3})
        self.redrawLines(self.points1000, self.curve1000, 'curve1000', {'color': self.records[self.name].pen, 'dash': [3,3], 'width': 4})

    def setLogMode(self, mode):
        # print 'change log mode = ', self.records['signal2']['axis'].logMode
        self.records[self.name].logScale = mode
        currentRange = self.vb.state['viewRange'][1]
        self.plot.records[self.name].axis.setLogMode(mode)
        self.curve.setLogMode(False, mode)
        self.curve10.setLogMode(False, mode)
        self.curve100.setLogMode(False, mode)
        self.curve1000.setLogMode(False, mode)
        self.vb.enableAutoRange(y=True)
        # if not self.logMode and mode and not currentRange[0] == 0.0 and isinstance(currentRange[0], (float, int)):
        #     print ('entering log mode, currentRange = ', currentRange, ' == ', [np.log10(i) for i in currentRange])
        #     if currentRange[0] <= 0:
        #         newRange = [0,0]
        #         newRange[1] = np.log10(currentRange[1])
        #         newRange[0] = newRange[1] - np.log10(currentRange[1]-currentRange[0])
        #     else:
        #         newRange = [np.log10(i) for i in currentRange]
        #     if (not newRange[0] == 0.0) and isinstance(newRange[0], (float, int)) and not np.isnan(newRange[0]):
        #         print ('newRange = ', newRange)
        #         self.vb.setYRange(*newRange, padding=0)
        # else:
        #     # print 'leaving log mode, currentRange = ', currentRange, ' == ', [10**i for i in currentRange]
        #     newRange = [10**i for i in currentRange]
        #     self.vb.setYRange(*newRange, padding=0)
        # print 'change log mode 2 = ', self.records['signal2']['axis'].logMode
        self.logMode = mode


    def redrawLines(self, points, curve, curvename, pen):
        if curve.isVisible() and self.visibility[curvename] is True and len(points) > 1:
            curve.setData(np.array(points))

    def changePenColour(self):
        self.curve.setPen(pg.mkPen(color=self.records[self.name].pen))
        self.curve10.setPen(pg.mkPen(color=self.records[self.name].pen, dash=[1,1], width=2))
        self.curve100.setPen(pg.mkPen(color=self.records[self.name].pen, dash=[2,2], width=3))
        self.curve1000.setPen(pg.mkPen(color=self.records[self.name].pen, dash=[3,3], width=4))

    ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
    def updateData(self, data, points):
        # if hasattr(self, 'lastVal'):
        #     val = data[0] - self.lastVal #if not self.records[self.name]['logScale'] else math.log(data[1],10)
        # else:
        #     val = 0
        # self.lastVal = data[0]
        newpoint = data#(data[0], val)
        points.append(newpoint)

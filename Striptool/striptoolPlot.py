import sys, time, os, datetime
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import numpy as np
from bisect import bisect_left, bisect_right
import peakutils
from itertools import compress
import win32clipboard
import itertools
import colours as colours

def takeClosestPosition(xvalues, myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    if len(myList) < 1 or myNumber < xvalues[0]:
        return [0,(0,0)]
    pos = bisect_left(xvalues, myNumber)
    if pos == 0:
        return [0,myList[0]]
    if pos == len(myList):
        return [-1,myList[-1]]
    before = myList[pos-1]
    after = myList[pos]
    if abs(after[0] - myNumber) < abs(myNumber - before[0]):
       return [pos,after]
    else:
       return [pos-1,before]

class TextItem(pg.GraphicsObject):
    """
    GraphicsItem displaying unscaled text (the text will always appear normal even inside a scaled ViewBox).
    """
    def __init__(self, text='', color=(200,200,200), html=None, anchor=(0,0),
                 border=None, fill=None, angle=0, rotateAxis=None):
        """
        ==============  =================================================================================
        **Arguments:**
        *text*          The text to display
        *color*         The color of the text (any format accepted by pg.mkColor)
        *html*          If specified, this overrides both *text* and *color*
        *anchor*        A QPointF or (x,y) sequence indicating what region of the text box will
                        be anchored to the item's position. A value of (0,0) sets the upper-left corner
                        of the text box to be at the position specified by setPos(), while a value of (1,1)
                        sets the lower-right corner.
        *border*        A pen to use when drawing the border
        *fill*          A brush to use when filling within the border
        *angle*         Angle in degrees to rotate text. Default is 0; text will be displayed upright.
        *rotateAxis*    If None, then a text angle of 0 always points along the +x axis of the scene.
                        If a QPointF or (x,y) sequence is given, then it represents a vector direction
                        in the parent's coordinate system that the 0-degree line will be aligned to. This
                        Allows text to follow both the position and orientation of its parent while still
                        discarding any scale and shear factors.
        ==============  =================================================================================
        The effects of the `rotateAxis` and `angle` arguments are added independently. So for example:
        * rotateAxis=None, angle=0 -> normal horizontal text
        * rotateAxis=None, angle=90 -> normal vertical text
        * rotateAxis=(1, 0), angle=0 -> text aligned with x axis of its parent
        * rotateAxis=(0, 1), angle=0 -> text aligned with y axis of its parent
        * rotateAxis=(1, 0), angle=90 -> text orthogonal to x axis of its parent
        """

        self.anchor = pg.Point(anchor)
        self.rotateAxis = None if rotateAxis is None else pg.Point(rotateAxis)
        #self.angle = 0
        pg.GraphicsObject.__init__(self)
        self.textItem = QtGui.QGraphicsTextItem()
        self.textItem.setParentItem(self)
        self._lastTransform = None
        self._lastScene = None
        self._bounds = QtCore.QRectF()
        if html is None:
            self.setColor(color)
            self.setText(text)
        else:
            self.setHtml(html)
        self.fill = pg.functions.mkBrush(fill)
        self.border = pg.functions.mkPen(border)
        self.setAngle(angle)

    def setText(self, text, color=None):
        """
        Set the text of this item.

        This method sets the plain text of the item; see also setHtml().
        """
        if color is not None:
            self.setColor(color)
        self.textItem.setPlainText(text)
        self.updateTextPos()

    def setPlainText(self, *args):
        """
        Set the plain text to be rendered by this item.

        See QtGui.QGraphicsTextItem.setPlainText().
        """
        self.textItem.setPlainText(*args)
        self.updateTextPos()

    def setHtml(self, *args):
        """
        Set the HTML code to be rendered by this item.

        See QtGui.QGraphicsTextItem.setHtml().
        """
        self.textItem.setHtml(*args)
        self.updateTextPos()

    def setTextWidth(self, *args):
        """
        Set the width of the text.

        If the text requires more space than the width limit, then it will be
        wrapped into multiple lines.

        See QtGui.QGraphicsTextItem.setTextWidth().
        """
        self.textItem.setTextWidth(*args)
        self.updateTextPos()

    def setFont(self, *args):
        """
        Set the font for this text.

        See QtGui.QGraphicsTextItem.setFont().
        """
        self.textItem.setFont(*args)
        self.updateTextPos()

    def setAngle(self, angle):
        self.angle = angle
        self.updateTransform()

    def setAnchor(self, anchor):
        self.anchor = pg.Point(anchor)
        self.updateTextPos()

    def setColor(self, color):
        """
        Set the color for this text.

        See QtGui.QGraphicsItem.setDefaultTextColor().
        """
        self.color = pg.functions.mkColor(color)
        self.textItem.setDefaultTextColor(self.color)

    def updateTextPos(self):
        # update text position to obey anchor
        r = self.textItem.boundingRect()
        tl = self.textItem.mapToParent(r.topLeft())
        br = self.textItem.mapToParent(r.bottomRight())
        offset = (br - tl) * self.anchor
        self.textItem.setPos(-offset)

        ### Needed to maintain font size when rendering to image with increased resolution
        #self.textItem.resetTransform()
        ##self.textItem.rotate(self.angle)
        #if self._exportOpts is not False and 'resolutionScale' in self._exportOpts:
            #s = self._exportOpts['resolutionScale']
            #self.textItem.scale(s, s)

    def boundingRect(self):
        return self.textItem.mapToParent(self.textItem.boundingRect()).boundingRect()

    def viewTransformChanged(self):
        # called whenever view transform has changed.
        # Do this here to avoid double-updates when view changes.
        self.updateTransform()

    def paint(self, p, *args):
        # this is not ideal because it requires the transform to be updated at every draw.
        # ideally, we would have a sceneTransformChanged event to react to..
        s = self.scene()
        ls = self._lastScene
        if s is not ls:
            if ls is not None:
                ls.sigPrepareForPaint.disconnect(self.updateTransform)
            self._lastScene = s
            if s is not None:
                s.sigPrepareForPaint.connect(self.updateTransform)
            self.updateTransform()
            p.setTransform(self.sceneTransform())

        if self.border.style() != QtCore.Qt.NoPen or self.fill.style() != QtCore.Qt.NoBrush:
            p.setPen(self.border)
            p.setBrush(self.fill)
            p.setRenderHint(p.Antialiasing, True)
            p.drawPolygon(self.textItem.mapToParent(self.textItem.boundingRect()))

    def updateTransform(self):
        # update transform such that this item has the correct orientation
        # and scaling relative to the scene, but inherits its position from its
        # parent.
        # This is similar to setting ItemIgnoresTransformations = True, but
        # does not break mouse interaction and collision detection.
        p = self.parentItem()
        if p is None:
            pt = QtGui.QTransform()
        else:
            pt = p.sceneTransform()

        if pt == self._lastTransform:
            return

        t = pt.inverted()[0]
        # reset translation
        t.setMatrix(t.m11(), t.m12(), t.m13(), t.m21(), t.m22(), t.m23(), 0, 0, t.m33())

        # apply rotation
        angle = -self.angle
        if self.rotateAxis is not None:
            d = pt.map(self.rotateAxis) - pt.map(pg.Point(0, 0))
            a = np.arctan2(d.y(), d.x()) * 180 / np.pi
            angle += a
        t.rotate(angle)

        self.setTransform(t)

        self._lastTransform = pt

        self.updateTextPos()

''' This class is a PyQtGraph axis which modifies the data points from "seconds before the current time" into Hours:Mins:Secs format.
We only want to do this for linear plots, so it is turned off in the FFT and Histogram plots. Also, if we turn "autoscroll" off, the
time is relative to the moment we switched it off.
'''
class CAxisTime(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(CAxisTime, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.dateTicksOn = True
        self.autoscroll = True
        self.fixedtimepoint = round(time.time(),2)

    def tickStrings(self, values, scale, spacing):
        if self.dateTicksOn:
            if self.autoscroll:
                reftime = round(time.time(),2)
            else:
                reftime = self.fixedtimepoint
            return [time.strftime("%H:%M:%S", time.localtime(reftime+x)) for x in values]
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


''' Basic plotting class, providing Linear, Histogram and FFT plots in a PyQtGraph PlotWidget '''
class generalPlot(pg.PlotWidget):
    changePlotScale = pyqtSignal('PyQt_PyObject')
    plotUpdated = pyqtSignal()
    statusChanged = pyqtSignal(str)
    crosshairsChanged = pyqtSignal('PyQt_PyObject')
    signalValuesUnderCrosshairs = pyqtSignal('PyQt_PyObject')


    def __init__(self, stripplot, crosshairs=True, parent = None):
        super(generalPlot, self).__init__(parent=parent)
        self.parent=parent
        self.stripplot = stripplot
        self.paused = True
        self.linearPlot = True
        self.histogramPlot = False
        self.FFTPlot = False
        self.scatterPlot = False
        self.doingPlot = False
        self.usePlotRange = True
        self.autoscroll = True
        self.decimateScale = 5000
        self.legend = pg.LegendItem(size=(100,100))
        self.legend.setParentItem(None)
        self.globalPlotRange = [-10,0]
        self.currentPlotTime = round(time.time(),2)
        self.plotWidget = pg.GraphicsLayoutWidget()
        # self.label = pg.LabelItem(justify='right')
        # self.plotWidget.addItem(self.label)
        self.numberBins = 50
        self.crosshairs = crosshairs
        self.crosshairsadded = False

    ''' This creates a PyQtGraph plot object (self.plot) and instantiates the bottom axis to be a CAxisTime axis '''
    def createPlot(self):
        self.plot = self.plotWidget.addPlot(row=0,col=0, autoDownsample=True, clipToView=True)
        self.date_axis = CAxisTime(orientation = 'bottom', parent=self.plot)
        self.log_axis = pg.AxisItem('right', parent=self.plot)
        self.log_axis.setLogMode(True)
        self.plot.mouseOver = False
        # self.plot.scene().installEventFilter(self)

        nontimeaxisItems = {'bottom': self.plot.axes['bottom']['item'], 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.plot.axes['right']['item']}
        axisItems = {'bottom': self.date_axis, 'top': self.plot.axes['top']['item'], 'left': self.plot.axes['left']['item'], 'right': self.log_axis}
        self.plot.axes = {}
        for k, pos in (('top', (1,1)), ('bottom', (3,1)), ('left', (2,0)), ('right', (2,2))):
            if k in axisItems:
                axis = axisItems[k]
                axis.linkToView(self.plot.vb)
                self.plot.axes[k] = {'item': axis, 'pos': pos}
                self.plot.layout.removeItem(self.plot.layout.itemAt(*pos))
                self.plot.layout.addItem(axis, *pos)
                axis.setZValue(-1000)
                axis.setFlag(axis.ItemNegativeZStacksBehindParent)
        self.plot.showGrid(x=True, y=True)
        self.vb = self.plot.vb
        if self.crosshairs:
            ''' Here we create the two lines that form the crosshairs '''
            self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('r'))
            self.vLine.setZValue(1000)
            self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('r'))
            self.hLine.setZValue(1000)
            ''' this is a line label for the vertical crosshair line. We modify the horizontal position in the signal functions '''
            self.hvLineText = TextItem() #pg.InfLineLabel(self.vLine, color='r', fill=(200,200,200,130))
            self.hvLineText.setZValue(1000)
            self.hvr = self.hLine.viewRect()
            self.vvr = self.vLine.viewRect()
            self.plot.addItem(self.vLine, ignoreBounds=True)
            self.plot.addItem(self.hLine, ignoreBounds=True)
            # self.plot.addItem(self.hvLineText, ignoreBounds=True)
            ''' define some parameters and instantiate the crosshair signals. We change the crosshairs whenever the sigMouseMoved is triggered,
            whilst we must update the vertical axis if the plot autoscales, and also we must also update the horizontal axis if the time changes under the crosshairs'''
            self.mousePos = QtCore.QPointF(0.01, 0.01)
            self.proxyMouseMoved = pg.SignalProxy(self.plot.scene().sigMouseMoved, rateLimit=10, slot=self.mouseMoved)
            self.proxyAxisChanged = pg.SignalProxy(self.plot.vb.sigYRangeChanged, rateLimit=1, slot=self.axisChanged)
            self.proxyTimeChanged = pg.SignalProxy(self.plotUpdated, rateLimit=1, slot=self.timeAxisChanged)
        return self.plot

    ''' This defines a general eventFilter for the self.plot object that we use to update the crosshairs'''
    def eventFilter(self, object, event):
        ''' This just allows me to confirm which plot we are in, in case there are many '''
        if event.type() == QtCore.QEvent.GraphicsSceneMouseMove and self.plot.scene() == object:
            self.mouseMoved(event)
            # print 'mouse over'
        # else:
            # self.plot.mouseOver = False
        ''' this will copy the crosshairs location to the clipboard '''
        if event.type() == QtCore.QEvent.GraphicsSceneMousePress:
            try:
                win32clipboard.OpenClipboard()
                win32clipboard.EmptyClipboard()
                win32clipboard.SetClipboardText(self.statusTextClipboard)
                win32clipboard.CloseClipboard()
            except:
                pass
        # self.showCrosshairs()
        return False

    def showCrosshairs(self):
        try:
            if self.plot.sceneBoundingRect().contains(self.mousePos):
                if not self.crosshairsadded:
                    self.plot.addItem(self.vLine, ignoreBounds=True)
                    self.plot.addItem(self.hLine, ignoreBounds=True)
                    self.plot.addItem(self.hvLineText, ignoreBounds=True)
                    self.crosshairsadded = True
            elif self.crosshairsadded:
                self.plot.removeItem(self.vLine)
                self.plot.removeItem(self.hLine)
                self.plot.removeItem(self.hvLineText)
                self.crosshairsadded = False
        except:
            pass

    ''' This is used to update the location of the crosshair lines as well as the accompanyng text'''
    def updateLines(self):
            self.vLine.setValue(self.mousePoint.x())
            self.hLine.setValue(self.mousePoint.y())
            self.crosshairsChanged.emit(self.mousePoint.x())
            self.hvLineText.setHtml('<span style="color: black; background-color: rgba(255, 0, 0, 100); opacity: 0.1;">'+self.statusText+'</span>')
            if self.hvr is not None:
                if self.hvr.center().y() > 0:
                    if self.vvr.center().y() > 0:
                        self.hvLineText.setAnchor((1, 1.0))
                    else:
                        self.hvLineText.setAnchor((0, 1.0))
                else:
                    if self.vvr.center().y() > 0:
                        self.hvLineText.setAnchor((1, 0))
                    else:
                        self.hvLineText.setAnchor((-0.1, 0))
            self.hvLineText.setPos(self.mousePoint.x(),self.mousePoint.y())
            self.showCrosshairs()

    ''' This is the event handler for a sigMouseMoved event for the viewbox '''
    def mouseMoved(self, evt):
        self.mousePos = evt[0]
        self.mousePoint = self.vb.mapSceneToView(self.mousePos)
        self.timeAxisChanged()
        self.updateLines()
        if self.plot.mouseOver:
            self.statusChanged.emit(self.statusTextClipboard)
        self.showCrosshairs()

    ''' This is the event handler for if the vertical axis autoscales '''
    def axisChanged(self, evt):
        if self.plot.sceneBoundingRect().contains(self.mousePos):
            self.mousePoint = self.vb.mapSceneToView(self.mousePos)
            self.timeAxisChanged()
            self.updateLines()
        self.showCrosshairs()

    ''' This is the event handler for when the horizontal axis time changes during "autoscroll" '''
    def timeAxisChanged(self):
        self.mousePoint = self.vb.mapSceneToView(self.mousePos)
        if self.linearPlot:
            if self.autoscroll:
                reftime = round(time.time(),2)
            else:
                reftime = self.fixedtimepoint
            self.statusTextX = time.strftime("%H:%M:%S", time.localtime(reftime + self.mousePoint.x()))
            self.statusTextY = "%0.3f" % (self.mousePoint.y())
            self.statusTextLogY = "%04.03e" % (np.power(10,self.mousePoint.y()))
            self.statusText = "&nbsp;"+self.statusTextX+", "+self.statusTextY+"("+self.statusTextLogY+")&nbsp;"
            self.statusTextClipboard = "{\""+self.statusTextX+"\", "+self.statusTextY+"}"
        else:
            self.statusTextX = "%0.3f" % (self.mousePoint.x())
            self.statusTextY = "%0.3f" % (self.mousePoint.y())
            self.statusTextClipboard = self.statusText = "{"+self.statusTextX+", "+self.statusTextY+"}"
        self.updateLines()
        self.showCrosshairs()

    ''' Helper function to add a curve to the plot '''
    def addCurve(self, record, plot, name):
        curve = self.curve(record, plot, name)
        return curve

    ''' Sets the timescale of the plotting data '''
    def setPlotScale(self, timescale, padding=0.0):
        self.plotRange = timescale
        self.globalPlotRange = list(timescale)
        if self.linearPlot:
            self.plot.vb.setRange(xRange=self.globalPlotRange, padding=0)
        self.changePlotScale.emit(self.globalPlotRange)

    ''' Function to update timescale if the viewbox range changes - i.e. via mouse interaction or autoscale'''
    def updatePlotScale(self, padding=0.0):
        if self.linearPlot:
            vbPlotRange = self.plot.vb.viewRange()[0]
            if vbPlotRange != [0,1]:
                self.globalPlotRange = self.plot.vb.viewRange()[0]
            self.plotRange = self.globalPlotRange
        self.changePlotScale.emit(self.globalPlotRange)

    ''' Wrapper '''
    def show(self):
        self.plotWidget.show()

    ''' Wrapper '''
    def togglePause(self, value):
        self.paused = value

    ''' Toggles autoscroll on the plot '''
    def toggleAutoScroll(self, value):
        self.autoscroll = value
        if not value:
            self.currenttime = self.currentPlotTime
            self.date_axis.fixedtimepoint = self.currentPlotTime
            self.fixedtimepoint = self.currentPlotTime

    ''' This is the curve class which enables plotting on a plotting object. Making it a class eases control of the different options for multiple curves'''
    class curve(QObject):
        def __init__(self, record, plot, name):
            QObject.__init__(self)
            self.records = record
            self.name = name
            self.plotScale = None
            self.plot = plot
            # self.globalPlotRange = self.plot.globalPlotRange
            self.doingPlot = False
            self.curve = self.plot.plot.plot()
            self.lines = self.MultiLine(np.array([[0]]),np.array([[0]]),pen='w')
            self.fftTextLabels = []
            # self.plot.crosshairsChanged.connect(self.emitSignalValue)

        def signalValueAtX(self, xvalue):
            return (self.name,takeClosestPosition(self.plotData[:,0],self.plotData,xvalue)[1][1])

        def addCurve(self):
            return self.curve

        ''' This updates the curve points based on the plot type and using the data from the timefilter function '''
        def updateData(self, data, pen):
            self.VerticalScale = self.records[self.name]['VerticalScale']
            self.VerticalOffset = self.records[self.name]['VerticalOffset']
            self.verticalMeanSubtraction = self.records[self.name]['verticalMeanSubtraction']
            self.logscale = self.records[self.name]['logscale']
            if len(data) > 1 and not self.plot.scatterPlot:
                x,y = np.transpose(data)
                if not self.VerticalScale == 1 or not self.VerticalOffset == 0:
                    y = (self.VerticalScale * y) + self.VerticalOffset
                if self.verticalMeanSubtraction or self.plot.stripplot.subtractMean:
                    meany = np.mean(y)
                    y = y - meany
                if self.logscale:
                    y = np.log10(np.abs(y))
                if self.plot.histogramPlot:
                    y2,x2 = np.histogram(y, bins=self.plot.numberBins)
                    self.curve.setData({'x': x2, 'y': y2}, pen=pen, stepMode=True, fillLevel=0, fillBrush=pen)
                elif self.plot.FFTPlot:
                    self.curve.setData({'x': x, 'y': y}, pen=pen, stepMode=False, fillLevel=None)
                    if(len(self.curve.yDisp) > 0):
                        indexes = peakutils.indexes(self.curve.yDisp, thres=0.75, min_dist=20)
                        if len(indexes) < 5:
                            for index in indexes:
                                fftTextlabel=pg.TextItem(html='<span style="color: '+pg.mkColor(pen).name()+';">'+str(round(self.curve.xDisp[index],2))+'</span>',anchor=(-0.7,1.2), angle=0)
                                fftTextlabel.setPos(self.curve.xDisp[index],self.curve.yDisp[index])
                                fftTextArrow=pg.ArrowItem(pos=(self.curve.xDisp[index],self.curve.yDisp[index]), angle=-45, pen=pen, brush=pg.mkBrush(pen))
                                self.fftTextLabels.append([fftTextlabel, fftTextArrow])
                                self.plot.plot.addItem(fftTextlabel)
                                self.plot.plot.addItem(fftTextArrow)
                    self.plot.updateSpectrumMode(True)
                else:
                    if len(x) > self.plot.decimateScale:
                        decimationfactor = int(np.floor(len(x)/self.plot.decimateScale))
                        self.lines = self.MultiLine(x[::decimationfactor],y[::decimationfactor],pen=pen, log=self.logscale)
                    else:
                        self.lines = self.MultiLine(x, y, pen=pen, log=self.logscale)
                    self.plot.plot.addItem(self.lines)

        ''' This filters the data based on the plotrange of the current viewbox. For small datasets this is ~pointless, but for moderately large datasets
        and bigger it makes a noticeable speed up, despite the functions built in to PyQtGraph'''
        def timeFilter(self, datain, timescale=None):
            datain = np.array(datain)
            if len(datain) > 0:
                if (datain[0][0] > (self.currenttime+self.plot.globalPlotRange[0]) and datain[-1][0] <=  (self.currenttime+self.plot.globalPlotRange[1])):
                    return datain
                else:
                    if datain[-1][0] <=  (self.currenttime+self.plot.globalPlotRange[1]):
                        datain = datain[bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[0])-1:-1]
                    else:
                        if datain[0][0] >= (self.currenttime+self.plot.globalPlotRange[0]):
                            datain = datain[0:bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[1])+1]
                        else:
                            datain = datain[bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[0])-1:bisect_left(datain[:,0], self.currenttime+self.plot.globalPlotRange[1])+1]
                    return datain
            else:
                return datain

        ''' helper function to clear a curves points '''
        def clear(self):
            self.plot.plot.removeItem(self.lines)
            self.curve.clear()

        ''' Wrapper function which calls timefilter and updateData'''
        def update(self):
            self.plot.plot.removeItem(self.lines)
            for i in range(len(self.fftTextLabels)):
                for j in range(len(self.fftTextLabels[i])):
                    self.plot.plot.removeItem(self.fftTextLabels[i][j])
            self.fftTextLabels = []
            if not self.plot.paused and not self.doingPlot:
                self.doingPlot = True
                if self.records[self.name]['ploton']:
                    self.plotData = self.timeFilter(self.records[self.name]['data'], self.plot.globalPlotRange)
                    if len(self.plotData) > 0:
                        self.plotData[:,0] = self.plotData[:,0] - self.currenttime
                        self.updateData(self.plotData, self.records[self.name]['pen'])
                else:
                    # self.clear()
                    pass
                self.doingPlot = False
            self.plot.plotUpdated.emit()

        class MultiLine(pg.QtGui.QGraphicsPathItem):
            def __init__(self, x, y, pen, log=False):
                """x and y are 1D arrays of shape (Nplots, Nsamples)"""
                # connect = np.ones(x.shape, dtype=bool)
                # connect[:,-1] = 0 # don't draw the segment between each trace
                self.path = pg.arrayToQPath(x, y)
                pg.QtGui.QGraphicsPathItem.__init__(self, self.path)
                if log:
                    self.setPen(pg.mkPen(pen,width=3))
                else:
                    self.setPen(pg.mkPen(pen,width=1))
            def shape(self): # override because QGraphicsPathItem.shape is too expensive.
                return pg.QtGui.QGraphicsItem.shape(self)
            def boundingRect(self):
                return self.path.boundingRect()

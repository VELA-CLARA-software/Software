import numpy as np
import pyqtgraph as pg

class HAxisRF(pg.AxisItem):
    def __init__(self, orientation=None, pen=None, linkView=None, parent=None, maxTickLength=-5, showValues=True):
        super(HAxisRF, self).__init__(parent=parent, orientation=orientation, linkView=linkView)
        self.setTickSpacing(major=20, minor=5)

    def tickStrings(self, values, scale, spacing):
        """Return the strings that should be placed next to ticks. This method is called
        when redrawing the axis and is a good method to override in subclasses.
        The method is called with a list of tick values, a scaling factor (see below), and the
        spacing between ticks (this is required since, in some instances, there may be only
        one tick and thus no other way to determine the tick spacing)

        The scale argument is used when the axis label is displaying units which may have an SI scaling prefix.
        When determining the text to display, use value*scale to correctly account for this prefix.
        For example, if the axis label's units are set to 'V', then a tick value of 0.001 might
        be accompanied by a scale value of 1000. This indicates that the label is displaying 'mV', and
        thus the tick should display 0.001 * 1000 = 1.
        """
        if self.logMode:
            return self.logTickStrings(values, scale, spacing)

        places = max(0, np.ceil(-np.log10(spacing*scale)))
        strings = []
        for v in values:
            vs = np.mod(v * scale + 180, 360) - 180
            if abs(vs) < .001 or abs(vs) >= 10000:
                vstr = "%g" % vs
            else:
                vstr = ("%%0.%df" % places) % vs
            strings.append(vstr)
        return strings

class plotWidgets(pg.GraphicsView):

    def __init__(self, cavity):
        super(plotWidgets, self).__init__()
        self.cavity = cavity
        self.layout = pg.GraphicsLayout(border=(100,100,100))
        self.setCentralItem(self.layout)
        self.subPlots = {}

        p1, p1e, p1f, p2, p2e, p2f = self.createMultiAxisPlot('Linac Parameters', 'Linac Set Point', 'r', 'C2V BPM', 'b', errors=[False, True])
        self.subPlots['setpoint'] = {}
        self.subPlots['bpmpos'] = {}
        self.subPlots['setpoint']['data'] = p1
        self.subPlots['bpmpos']['data'] = p2
        self.subPlots['setpoint']['error'] = p1e
        self.subPlots['bpmpos']['error'] = p2e
        self.subPlots['setpoint']['fit'] = p1f
        self.subPlots['bpmpos']['fit'] = p2f
        self.layout.nextRow()
        # x = np.array([1,2,3])
        # y = np.array([100,200,300])
        # y2 = np.array([30,20,10])
        # p1.setData(x=x, y=y)
        # p1e.setData(x=x, y=y, height=y/10.)
        # p2.setData(x=x, y=y2)
        # p2e.setData(x=x, y=y2, height=y2/3.)
        p1, p1e, p1f, p2, p2e, p2f = self.createMultiAxisPlot('CTR Parameters', 'CTR Signal', [212, 219, 7], 'WCM Q', [34, 122, 7])
        self.subPlots['ctrsignal'] = {}
        self.subPlots['wcmq'] = {}
        self.subPlots['ctrsignal']['data'] = p1
        self.subPlots['wcmq']['data'] = p2
        self.subPlots['ctrsignal']['error'] = p1e
        self.subPlots['wcmq']['error'] = p2e
        self.subPlots['ctrsignal']['fit'] = p1f
        self.subPlots['wcmq']['fit'] = p2f

    def createMultiAxisPlot(self, title="", leftLabel="", leftColor='k', rightLabel="", rightColor='k', errors=[True,True]):
        p1 = pg.PlotItem(title=title)
        self.layout.addItem(p1)
        p1c = p1.plot(pen=pg.mkPen(leftColor, width=3))
        p1f = p1.plot(pen=pg.mkPen(leftColor, width=5))
        p1.getAxis('left').setLabel(leftLabel, color='#'+pg.colorStr(pg.mkColor(leftColor))[:-2])
        if errors[0]:
            p1e = pg.ErrorBarItem(x=np.array([]), y=np.array([]), height=np.array([]), beam=None, pen={'color': leftColor, 'width':2})
            p1.addItem(p1e)
        else:
            p1e = None
        p2 = pg.ViewBox()
        p1.showAxis('right')
        p1.scene().addItem(p2)
        p1.getAxis('right').linkToView(p2)
        p2.setXLink(p1)
        p1.getAxis('right').setLabel(rightLabel, color='#'+pg.colorStr(pg.mkColor(rightColor))[:-2])
        p2c = pg.PlotDataItem(pen=pg.mkPen(rightColor, width=3))
        p2f = pg.PlotDataItem(pen=pg.mkPen(rightColor, width=5))
        p2.addItem(p2c)
        p2.addItem(p2f)
        if errors[1]:
            p2e = pg.ErrorBarItem(x=np.array([]), y=np.array([]), height=np.array([]), beam=None, pen={'color': rightColor, 'width':2})
            p2.addItem(p2e)
        else:
            p2e = None
        self.updateViews(p1,p2)
        p1.vb.sigResized.connect(lambda: self.updateViews(p1, p2))
        return p1c, p1e, p1f, p2c, p2e, p2f

    def updateViews(self, p1, p2):
        p2.setGeometry(p1.vb.sceneBoundingRect())
        p2.linkedViewChanged(p1.vb, p2.XAxis)

    def newData(self, cavity, actuator, data):
        actuator = str(actuator)
        try:
            if str(cavity) == self.cavity:
                if 'xData' in data and 'yData' in data and 'yStd' in data:
                    # newdata = zip(data['xData'], data['yData'], data['yStd'])
                    # xdata, ydata, stddata = [np.array(a) for a in zip(*[a for a in newdata if a[1] is not float('nan')])]
                    xdata, ydata, stddata = [np.array(a) for a in [data['xData'], data['yData'], data['yStd']]]
                    self.subPlots[actuator]['data'].setData(x=xdata, y=ydata)
                    self.subPlots[actuator]['error'].setData(x=xdata, y=ydata, height=stddata)
                if 'xFit' in data and 'yFit' in data:
                    self.subPlots[actuator]['fit'].setData(x=data['xFit'], y=data['yFit'])
        except:
            pass

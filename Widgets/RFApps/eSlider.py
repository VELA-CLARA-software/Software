from PyQt4.QtCore import *
from PyQt4.QtGui import *
from epicsQt import epicsQt
from epicsQt import css
import PyQt4.Qt as QtQt

class eSlider(QSlider):
    def __init__(self, parent=None, pvName=None, min=-10, max=10, sliderorientation=Qt.Horizontal, factor=100):
        QSlider.__init__(self, parent)
        self.factor = factor
        self.min = min*self.factor
        self.max = max*self.factor
        self.setOrientation(sliderorientation)
        self.setValue(0)
        self.setFixedWidth(70)
        self.setEnabled(False)
        if pvName is not None:
            self.setPV(pvName)

    def setPV(self, pv):
        if isinstance(pv, str):
            self.pv = epicsQt(pv)
        else:
            self.pv = pv
        if self.pv.inited:
            self.setEnabled(True)
            self.controlInfo()
            self.valueChanged()
        self.connect(self.pv, QtQt.SIGNAL('connectionChanged(bool)'), self.connectionChanged)
        self.connect(self.pv, QtQt.SIGNAL('valueChanged()'), self.valueChanged)
        self.connect(self.pv, QtQt.SIGNAL('controlInfo()'), self.controlInfo)

    def getPvName(self):
        return self.pv.name()

    def setPvName(self, name):
        self.setPV(str(name))

    pvName = QtQt.pyqtProperty("QString", getPvName, setPvName)

    def editingFinished(self, value):
        self.pv.array_put(self.value())

    def controlInfo(self):
        lolim = None; uplim = None
        if hasattr(self.pv, 'pv_loctrllim'):
            lolim = self.pv.pv_loctrllim
            self.setMinimum(lolim)
        if hasattr(self.pv, 'pv_upctrllim'):
            uplim = self.pv.pv_upctrllim
            self.setMaximum(uplim)

        # to avoid stupid lazy developers who put lowlim=uplim=0.0
        if lolim == uplim:
            print 'lazy'
            self.setRange(self.min, self.max)

        if not hasattr(self.pv, 'pv_precision'): prec = 13
        else: prec = self.pv.pv_precision

        # if hasattr(self.pv, 'pv_units'):
        #     self.setSuffix(' ' + self.pv.pv_units)

    def valueChanged(self):
        if self.pv.pv_severity == 0: self.setStyleSheet(css.normal)
        elif self.pv.pv_severity == 1: self.setStyleSheet(css.warn)
        elif self.pv.pv_severity == 2: self.setStyleSheet(css.alarm)
        elif self.pv.pv_severity == 3: self.setStyleSheet(css.invalid)
        # avoid infinite loop
        self.disconnect(self, QtQt.SIGNAL('valueChanged(double)'), self.editingFinished)
        self.setValue(self.pv.pv_value)
        self.connect(self, QtQt.SIGNAL('valueChanged(double)'), self.editingFinished)

    def connectionChanged(self, connected):
        if connected:
            self.setEnabled(True)
        else:
            self.setEnabled(False)
            self.setStyleSheet(css.disabled)

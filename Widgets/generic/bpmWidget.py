from pv import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from positionWidget import *
from intensityWidget import *
from phaseWidget import *
from collections import OrderedDict

class bpmWidget(QWidget):
    def __init__(self, bpm=None, parent=None):
        super(bpmWidget, self).__init__(parent)
        self.name = bpm
        self.setMinimumSize(250,600)
        self._x = 0
        self._y = 0
        self._x_ref = 0
        self._y_ref = 0
        self._I = 0
        self._I_ref = 1
        self._ph = 0
        self.resize(250,600)
        self.positionWidget = positionWidget()
        self.phaseWidget = phaseWidget()
        self.intensityWidget = intensityWidget()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel(self.name)
        f = self.label.font()
        f.setPointSize(14)
        f.setBold(True)
        self.label.setFont(f)
        self.label.setAlignment(Qt.AlignHCenter| Qt.AlignTop)
        self.label.setMaximumHeight(25)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.positionWidget,2)
        self.layout.addWidget(self.phaseWidget,2)
        self.layout.addWidget(self.intensityWidget,1)

    def setColor(self, color):
        self.positionWidget.color = color
        self.phaseWidget.color = color
        self.intensityWidget.color = color

    def setReferenceColor(self, color):
        self.positionWidget.ref_color = color
        self.phaseWidget.ref_color = color
        self.intensityWidget.ref_color = color

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self.updatePosition()
    def set_x(self, time, value):
        self._x = value
        self.updatePosition()
    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self.updatePosition()
    def set_y(self, time, value):
        self._y = value
        self.updatePosition()
    @property
    def x_ref(self):
        return self._x_ref
    @x_ref.setter
    def x_ref(self, value):
        self._x_ref = value
        self.updateReferencePosition()
    def set_x_ref(self, time, value):
        self._x_ref = value
        self.updateReferencePosition()
    @property
    def y_ref(self):
        return self._y_ref
    @y_ref.setter
    def y_ref(self, value):
        self._y_ref = value
        self.updateReferencePosition()
    def set_y_ref(self, time, value):
        self._y_ref = value
        self.updateReferencePosition()

    def updatePosition(self):
        self.positionWidget.setValue([self.x, self.y])
        self.positionWidget.update()
    def updateReferencePosition(self):
        self.positionWidget.setReferenceValue([self.x_ref, self.y_ref])
        self.positionWidget.update()

    def setPositionScale(self, scale):
        self.positionWidget.setScale(scale)

    @property
    def I(self):
        return self._I
    @I.setter
    def I(self, value):
        self._I = value
        self.updateIntensity()
    def set_I(self, time, value):
        self._I = value
        self.updateIntensity()

    def updateIntensity(self):
        self.intensityWidget.setValue(self.I)
        self.intensityWidget.update()

    @property
    def I_ref(self):
        return self._I_ref
    @I_ref.setter
    def I_ref(self, value):
        self._I_ref = value
        self.updateReferenceIntensity()
    def set_I_ref(self, time, value):
        self._I_ref = value
        self.updateReferenceIntensity()

    def updateReferenceIntensity(self):
        self.intensityWidget.setReferenceValue(self.I_ref)
        self.intensityWidget.update()

    @property
    def phase(self):
        return self._ph
    @phase.setter
    def phase(self, value):
        self._ph = value
        self.updatePhase()
    def set_phase(self, time, value):
        self._ph = value
        self.updatePhase()

    def updatePhase(self):
        self.phaseWidget.setValue(self.phase)
        self.phaseWidget.update()

    @property
    def phase_ref(self):
        return self._ph_ref
    @phase_ref.setter
    def phase_ref(self, value):
        self._ph_ref = value
        self.updateReferencePhase()
    def set_phase_ref(self, time, value):
        self._ph_ref = value
        self.updateReferencePhase()

    def updateReferencePhase(self):
        self.phaseWidget.setReferenceValue(self.phase_ref)
        self.phaseWidget.update()

class bpmTable(QWidget):
    def __init__(self, bpmList=[], parent=None):
        super(bpmTable, self).__init__(parent)
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)

        self.bpmWidgets = OrderedDict([])

        for bpm in bpmList:
            w = bpmWidget(bpm)
            self.bpmWidgets[bpm] = w
            self.layout.addWidget(w)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mw = QMainWindow()
    # mw.resize(1.25*250,1.25*600)
    bpm = bpmTable(['BPM 1','BPM 2','BPM 3','BPM 4','BPM 5','BPM 6','BPM 7'])
    mw.setCentralWidget(bpm)
    mw.show()
    sys.exit(app.exec_())

from PyQt5.QtCore import QPoint, Qt, QTime, QTimer, QRectF
from PyQt5.QtGui import QColor, QPainter, QPolygon, QPen
from PyQt5.QtWidgets import QApplication, QWidget
import random

class intensityWidget(QWidget):

    bgcolor = QColor(200, 200, 200)
    color = QColor(139, 177, 239)
    ref_color = QColor(63, 82, 114)

    def __init__(self, parent=None):
        super(intensityWidget, self).__init__(parent)
        self.resize(100, 150)
        self.value = 0.0
        self.ref_value = 1.0

    def setValue(self, value):
        self.value = value

    def setReferenceValue(self, value):
        self.ref_value = value

    def paintEvent(self, event=None):
        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(self.width() / 500.0, self.height() / 150.0)

        painter.setBrush(self.bgcolor)
        painter.setPen(self.bgcolor)

        painter.drawRect(-70,-90, 70, 2*90)
        painter.drawRect(0,-90, 70, 2*90)

        painter.setBrush(self.ref_color)
        painter.setPen(self.ref_color)
        painter.drawRect(0, 90, 68, -1.0*2*90)

        painter.setBrush(self.color)
        painter.setPen(self.color)
        painter.drawRect(-70, 90, 68, -1.0*(self.value/self.ref_value)*2*90)

def spin(*args, **kwargs):
    spinValue = random.random()
    pw.setValue(spinValue)
    pw.update()

if __name__ == '__main__':
    import sys
    global pw
    app = QApplication(sys.argv)
    pw = intensityWidget()
    pw.setValue(0.76)
    pw.show()
    timer = QTimer()
    timer.timeout.connect(spin)
    timer.start(10)
    sys.exit(app.exec_())

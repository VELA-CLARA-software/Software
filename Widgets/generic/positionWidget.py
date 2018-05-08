from PyQt5.QtCore import QPoint, Qt, QTime, QTimer, QRectF
from PyQt5.QtGui import QColor, QPainter, QPolygon, QPen
from PyQt5.QtWidgets import QApplication, QWidget
import random

class positionWidget(QWidget):

    color = QColor(139, 177, 239)
    ref_color = QColor(63, 82, 114)

    def __init__(self, parent=None):
        super(positionWidget, self).__init__(parent)
        self.resize(200, 200)
        self.pointWidth = 5
        self.value = [0, 0]
        self.refValue = [0,0]
        self.scale_x = [-10,10]
        self.scale_y = [-10,10]

    def setValue(self, value):
        self.value = value

    def setReferenceValue(self, value):
        self.refValue = value

    def setScale(self, scale):
        if isinstance(scale, (list, tuple)):
            self.scale_x = scale
            self.scale_y = scale
        else:
            self.scale_x = [-1*scale, scale]
            self.scale_y = [-1*scale, scale]

    def setScaleX(self, scale):
        if isinstance(scale, (list, tuple)):
            self.scale_x = scale
        else:
            self.scale_x = [-1*scale, scale]

    def setScaleY(self, scale):
        if isinstance(scale, (list, tuple)):
            self.scale_y = scale
        else:
            self.scale_y = [-1*scale, scale]

    @property
    def range_x(self):
        return self.scale_x[1] - self.scale_x[0]
    @property
    def range_y(self):
        return self.scale_y[1] - self.scale_y[0]

    def paintEvent(self, event=None):
        side = min(self.width(), self.height())
        pos = self.value
        ref_pos = self.refValue

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2 + 10, self.height() / 2)
        painter.scale(side / 230.0, side / 230.0)

        painter.setBrush(Qt.NoBrush)
        painter.setPen(QColor(0, 0, 0))

        painter.drawRect(-100,-100, 2*100, 2*100)

        for i in range(20):
            x = -100 + i * 10
            painter.drawLine(x,100,x,98)
            painter.drawLine(x,-100,x,-98)
            painter.drawLine(-100,x,-98,x)
            painter.drawLine(100,x,98,x)

        painter.drawLine(-100,0,100,0)
        painter.drawLine(-100,50,100,50)
        painter.drawLine(-100,-50,100,-50)
        painter.drawLine(-50,-100,-50, 100)
        painter.drawLine(50, 100,50, -100)
        painter.drawLine(0,-100, 0, 100)

        painter.setBrush(self.ref_color)
        painter.setPen(self.ref_color)
        painter.drawEllipse((ref_pos[0] * (100/self.range_x)) - self.pointWidth, (ref_pos[1] * -(100/self.range_y)) - self.pointWidth,
        2.1*self.pointWidth, 2.1*self.pointWidth)

        painter.setBrush(self.color)
        painter.drawEllipse((pos[0] * (100/self.range_x)) - self.pointWidth, (pos[1] * -(100/self.range_y)) - self.pointWidth,
        2*self.pointWidth, 2*self.pointWidth)

#        painter.save()
#        painter.setPen(QColor(0,0,0))
#        painter.rotate(180)
#        for i in range(2):
#            painter.drawLine(-1*((pos[0] * (100/self.scale)) - self.pointWidth/2), -1*((pos[1] * -(100/self.scale)) - self.pointWidth/2),
#            -1*((pos[0] * (100/self.scale)) + self.pointWidth/2), -1*((pos[1] * -(100/self.scale)) + self.pointWidth/2))
#            painter.rotate(180)
#        painter.restore()

        painter.setPen(QColor(0,0,0))
        font = painter.font()
        font.setPointSize(font.pointSize() * 1.2)
        painter.setFont(font)

        painter.drawText(QRectF(-107, 102, 30, 20), str(self.scale_x[0]))
        painter.drawText(QRectF(90, 102, 30, 20), str(1*self.scale_x[1]))

        painter.drawText(QRectF(-130, 90, 30, 20), str(self.scale_y[0]))
        painter.drawText(QRectF(-125, -105, 30, 20), str(1*self.scale_y[1]))

def spin(*args, **kwargs):
    spinValue = [20*random.random() - 10, 20*random.random() - 10]
    pw.setValue(0, list(spinValue))
    pw.update()

if __name__ == '__main__':
    import sys
    global pw
    app = QApplication(sys.argv)
    pw = positionWidget()
    pw.setValue(0, [0, 5])
    pw.show()
    timer = QTimer()
    timer.timeout.connect(spin)
    timer.start(10)
    sys.exit(app.exec_())

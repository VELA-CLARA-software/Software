from PyQt5.QtCore import QPoint, Qt, QTime, QTimer, QRectF
from PyQt5.QtGui import QColor, QPainter, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget


class phaseWidget(QWidget):
    hand = QPolygon([
        QPoint(4, 7),
        QPoint(0, 14),
        QPoint(-4, 7),
        QPoint(-1, -80),
        QPoint(1, -80)
    ])

    color = QColor(139, 177, 239)
    ref_color = QColor(63, 82, 114)

    def __init__(self, parent=None):
        super(phaseWidget, self).__init__(parent)
        self.resize(200, 200)
        self.value = 0
        self.refValue = 180

    def setValue(self, value):
        self.value = value

    def setReferenceValue(self, value):
        self.refValue = value

    def paintEvent(self, event):
        side = 0.8 * min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2 / 0.95)
        painter.scale(side / 200.0 * 0.95, side / 200.0 * 0.95)

        painter.setPen(Qt.NoPen)

        painter.setBrush(self.ref_color)
        painter.save()
        painter.rotate(self.refValue)
        painter.drawConvexPolygon(self.hand)
        painter.restore()

        painter.setBrush(self.color)
        painter.save()
        painter.rotate(self.value - self.refValue)
        painter.drawConvexPolygon(self.hand)
        painter.restore()

        painter.save()
        painter.setPen(QColor(0,0,0))

        for i in range(27):
            painter.drawLine(88, 0, 92, 0)
            painter.rotate(15)

        painter.restore()
        painter.save()
        painter.setPen(QColor(0,0,0))
        painter.rotate(0.0)
        for i in range(9):
            painter.drawLine(88, 0, 96, 0)
            painter.rotate(45.0)

        painter.restore()

        painter.setPen(QColor(0,0,0))
        font = painter.font()
        font.setPointSize(font.pointSize() * 1.2)
        painter.setFont(font)
        painter.drawText(QRectF(-7.5, 100, 30, 20), '180°')
        painter.drawText(QRectF(-5, -110, 35, 20), '0°')
        painter.drawText(QRectF(-125, -5, 30, 20), '270°')
        painter.drawText(QRectF(105, -5, 35, 20), '90°')


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    pw = phaseWidget()
    pw.setValue(0, 168)
    pw.show()
    sys.exit(app.exec_())

from PyQt4.QtGui import QLabel, QPainter, QWidget
from PyQt4.QtCore import QSize
from PyQt4 import QtCore, QtGui

class vertical_label(QLabel):
    def __init__(self, *args):
		QLabel.__init__(self, *args)
		self.count = 0
		
    def paintEvent(self, event):
		print("paintEvent",self.count)
		self.count +=1
		#QLabel.paintEvent(self, event)
		painter = QPainter(self)
		#painter.begin(self);
		painter.translate(0, self.height()-1)
		painter.rotate(-90)
		self.setGeometry(self.x(), self.y(), self.height(), self.width())
		#QLabel.render(self, painter)
		#painter.drawText(50,50, self.text() )
		#QLabel.update(self)
		#painter.end()
		
		
		
    # def __init__(self, *args):
        # QLabel.__init__(self, *args)

    # def paintEvent(self, event):
        # QLabel.paintEvent(self, event)
        # painter = QPainter(self)
        # painter.translate(0, self.height()-1)
        # painter.rotate(-90)
        # self.setGeometry(self.x(), self.y(), self.height(), self.width())
        # #QLabel.render(self, painter)

    # def minimumSizeHint(self):
        # size = QLabel.minimumSizeHint(self)
        # return QSize(size.height(), size.width())

    # def sizeHint(self):
        # size = QLabel.sizeHint(self)
        # return QSize(size.height(), size.width())
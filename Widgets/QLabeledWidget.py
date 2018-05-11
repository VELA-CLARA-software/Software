try:
    from PyQt4.QtCore import *
    from PyQt4.QtGui import *
except ImportError:
    from PyQt5.QtCore import *
    from PyQt5.QtGui import *
    from PyQt5.QtWidgets import *

class QLabeledWidget(QWidget):
    def __init__(self, widget, label, parent=None):
        super(QLabeledWidget, self).__init__(parent)
        self.widget = widget
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.label = QLabel(label)
        self.label.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.widget)

    def setText(self, text):
        self.label.setText(text)

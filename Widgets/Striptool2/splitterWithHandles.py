# from PyQt5.QtCore import QTimer, pyqtSignal, pyqtSlot, Qt
# from PyQt5.QtGui import QHBoxLayout
# from PyQt5.QtWidgets import QSplitter, QToolButton, QSplitterHandle, QLabel
from PyQt4 import QtCore, QtGui

class splitterWithHandles(QtGui.QSplitter):

    def __init__(self, parent = None):
        super(splitterWithHandles, self).__init__(parent)
        self.splitterMoved.connect(self.handleSplitterMoved)

    def createHandle(self):
        return splitterHandle(self.orientation(), self)

    def handleSplitterMoved(self, pos, index):
        widgetIndex = 0 if index is 1 else 2
        if self.orientation() == QtCore.Qt.Horizontal:
            self.handle(index).setState(self.widget(widgetIndex).size().width())
        else:
            self.handle(index).setState(self.widget(widgetIndex).size().height())

class QDoubleClickToolButton(QtGui.QToolButton):
    doubleClicked = QtCore.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QDoubleClickToolButton, self).__init__(*args, **kwargs)
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.checkDoubleClick)

    @QtCore.pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)

class splitterHandle(QtGui.QSplitterHandle):

    def __init__(self, orientation=QtCore.Qt.Horizontal, parent = None):
        super(splitterHandle, self).__init__(orientation, parent)
        self.orientation = orientation
        self.open = True

    def setLocation(self, location='top', label=None):
        self.location = location
        self.label = label
        if self.orientation == QtCore.Qt.Vertical:
            self.layout = QtGui.QHBoxLayout()
            self.openArrow = QtCore.Qt.UpArrow if location is 'top' else QtCore.Qt.DownArrow
            self.closedArrow = QtCore.Qt.DownArrow if location is 'top' else QtCore.Qt.UpArrow
        else:
            self.layout = QtGui.QVBoxLayout()
            self.openArrow = QtCore.Qt.LeftArrow if location is 'top' else QtCore.Qt.RightArrow
            self.closedArrow = QtCore.Qt.RightArrow if location is 'top' else QtCore.Qt.LeftArrow
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.button = QDoubleClickToolButton(self)
        self.button.doubleClicked.connect(self.handleButtonClick)
        self.button.setArrowType(self.openArrow)
        self.layout.addStretch()
        self.layout.addWidget(self.button)
        if self.label is not None:
            self.labelWidget = QtGui.QLabel(self.label)
            self.layout.addWidget(self.labelWidget)
        self.layout.addStretch()
        self.setLayout(self.layout)
        self.originalPosition = self.getCurrentPosition()

    def handleButtonClick(self):
        if self.open:
            self.setClosed()
        else:
            self.setOpen()

    def setClosed(self):
        self.originalPosition = self.getCurrentPosition()
        self.open = False
        self.setClosedArrow()
        self.labelWidget.setVisible(True)
        self.moveSplitter(self.getClosedPosition())

    def setOpen(self):
        self.open = True
        self.setOpenArrow()
        self.labelWidget.setVisible(False)
        if self.originalPosition < 0:
            self.moveSplitter(self.splitter().size().height()+self.originalPosition)
        else:
            self.moveSplitter(self.originalPosition)

    def getClosedPosition(self):
        if self.location is 'top' or self.location is 'left':
            return 0
        else:
            if self.orientation == QtCore.Qt.Horizontal:
                return self.splitter().size().width()
            else:
                return self.splitter().size().height()

    def getCurrentPosition(self):
        if self.orientation == QtCore.Qt.Horizontal:
            if self.location is 'left':
                if not self.isVisible():
                    return  self.splitter().widget(0).sizeHint().width()
                else:
                    return self.pos().x()
            else:
                if not self.isVisible():
                    return -1*self.splitter().widget(2).sizeHint().width()
                else:
                    return self.pos().x() - self.splitter().size().width()
        else:
            if self.location is 'top':
                if not self.isVisible():
                    return  self.splitter().widget(0).sizeHint().height()
                else:
                    return self.pos().y()
            else:
                if not self.isVisible():
                    return -1*self.splitter().widget(2).sizeHint().height()
                else:
                    return self.pos().y() - self.splitter().size().height()

    def setState(self, size):
        if size is 0:
            self.setClosedArrow()
        else:
            self.setOpenArrow()

    def setOpenArrow(self):
        self.open = True
        self.button.setArrowType(self.openArrow)

    def setClosedArrow(self):
        self.open = False
        self.button.setArrowType(self.closedArrow)

import sys
sys.path.append("../../../")
import Software.Procedures.qt as qt

class splitterWithHandles(qt.QSplitter):

    def __init__(self, parent = None):
        super(splitterWithHandles, self).__init__(parent)
        self.splitterMoved.connect(self.handleSplitterMoved)

    def createHandle(self):
        return splitterHandle(self.orientation(), self)

    def handleSplitterMoved(self, pos, index):
        widgetIndex = 0 if index is 1 else 2
        if self.orientation() == qt.Qt.Horizontal:
            self.handle(index).setState(self.widget(widgetIndex).size().width())
        else:
            self.handle(index).setState(self.widget(widgetIndex).size().height())

class QDoubleClickToolButton(qt.QToolButton):
    doubleClicked = qt.pyqtSignal()

    def __init__(self, *args, **kwargs):
        super(QDoubleClickToolButton, self).__init__(*args, **kwargs)
        self.timer = qt.QTimer()
        self.timer.setSingleShot(True)
        self.clicked.connect(self.checkDoubleClick)

    @qt.pyqtSlot()
    def checkDoubleClick(self):
        if self.timer.isActive():
            self.doubleClicked.emit()
            self.timer.stop()
        else:
            self.timer.start(250)

class splitterHandle(qt.QSplitterHandle):

    def __init__(self, orientation=qt.Qt.Horizontal, parent = None):
        super(splitterHandle, self).__init__(orientation, parent)
        self.orientation = orientation
        self.open = True

    def setLocation(self, location='top', label=None):
        self.location = location
        self.label = label
        if self.orientation == qt.Qt.Vertical:
            self.layout = qt.QHBoxLayout()
            self.openArrow = qt.Qt.UpArrow if location is 'top' else qt.Qt.DownArrow
            self.closedArrow = qt.Qt.DownArrow if location is 'top' else qt.Qt.UpArrow
        else:
            self.layout = qt.QVBoxLayout()
            self.openArrow = qt.Qt.LeftArrow if location is 'top' else qt.Qt.RightArrow
            self.closedArrow = qt.Qt.RightArrow if location is 'top' else qt.Qt.LeftArrow
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.button = QDoubleClickToolButton(self)
        self.button.doubleClicked.connect(self.handleButtonClick)
        self.button.setArrowType(self.openArrow)
        self.layout.addStretch()
        self.layout.addWidget(self.button)
        if self.label is not None:
            self.labelWidget = qt.QLabel(self.label)
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
            if self.orientation == qt.Qt.Horizontal:
                return self.splitter().size().width()
            else:
                return self.splitter().size().height()

    def getCurrentPosition(self):
        if self.orientation == qt.Qt.Horizontal:
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

import sys
import time, math
from PyQt5.QtCore import QObject, QUrl, Qt, pyqtProperty, pyqtSignal, QTimer
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLineEdit
from PyQt5.QtQml import QQmlApplicationEngine, qmlRegisterType, QQmlEngine, QQmlComponent
from PyQt5 import QtCore, QtGui
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQuickWidgets import QQuickWidget

class gauge(QWidget):
    def __init__(self, parent = None):
        super(gauge, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.gaugeWidget = QQuickWidget()
        self.gaugeWidget.setSource(QUrl('full_gauge.qml'))
        self.gauge = self.gaugeWidget.rootObject().findChild(QObject, 'test_gauge')
        self.gauge.setProperty('gauge_value',0)
        self.layout.addWidget(self.gaugeWidget)

<<<<<<< HEAD
    def setValue(self, value):
=======
    def setValue(self, time, value):
>>>>>>> parent of 903bfae1... Added handle_update_individual_trace button to NO-ARCv2 GUI that toggles the updating of individual traces between passive and 10Hz.
        #print ('guage value = ', value)
        self.gauge.setProperty('gauge_value',value)

class mainWindow(QMainWindow):
    def __init__(self, parent = None):
        super(mainWindow, self).__init__(parent)
        self.widget = gauge(self)
        self.setCentralWidget(self.widget)
        self.spinValue = 0

    def spinBaby(self):
        self.timer = QTimer()
        self.timer.timeout.connect(self.spin)
        self.timer.start(500)

    def spin(self):
        self.spinValue += 30
        self.widget.setValue(self.spinValue % 360)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = mainWindow()
    window.show()
    window.spinBaby()
    sys.exit(app.exec_())

from PyQt4 import QtGui
import sys


class MainWindow(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Main Window")


class FirstWindow(QtGui.QDialog):

    def __init__(self, parent=None):
        super(FirstWindow, self).__init__(parent)

        self.createWindow()

    def createWindow(self):
        btn = QtGui.QPushButton('Open New Window', self)
        btn.move(10, 10)

        self.openNewWindow = MainWindow(self)
        btn.clicked.connect(self.openMainWin)

        self.setGeometry(250,250, 150,50)
        self.setWindowTitle("First Window")
        self.show()

    def openMainWin(self):
        self.openNewWindow.show()


if __name__ == "__main__":

    app = QtGui.QApplication(sys.argv)
    firstwin = FirstWindow()
    sys.exit(app.exec_())

from conditioning_gui import Ui_MainWindow
from PyQt4.QtGui import *
import sys

app = QApplication(sys.argv)


class test_view(QMainWindow, Ui_MainWindow):
    pass

        #
    # other attributes will be initialised in base-class
    def __init__(self, columnwidth = 80):
        QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)


# Create the QML user interface.
view = test_view()
view.show()

#app.exec_()

#view.mean_start.update()

#QApplication.processEvents()

raw_input()
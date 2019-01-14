

from src.gui.designer_MainWindow import Ui_MainWindow
from PyQt4.QtGui import QMainWindow


class gui(QMainWindow, Ui_MainWindow): # do we ''need'' to inhereit from a main windOw?


    def __init__(self):
        QMainWindow.__init__(self)
        self.my_name = 'gui'

    def show_gui(self):
        self.setupUi(self)



    def hello(self):
        print(self.my_name + ' says hello')
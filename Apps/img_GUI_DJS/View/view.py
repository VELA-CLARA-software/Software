from PyQt5.QtWidgets import QMainWindow
from procedure.procedure import procedure
from .img_gui_view import Ui_MainWindow


class view(QMainWindow, Ui_MainWindow ):
    # custom close signal to send to controller
    #closing = QtCore.pyqtSignal()

    valves = {}

    # create a procedure object to access static data
    procedure = procedure()
    data = procedure.img_values

    def __init__(self):
        QMainWindow.__init__(self)
        self.my_name = 'view'
        self.setupUi(self)

        # this dict just links the widgesets the valve names
        self.img_name_to_widget = {}
        self.connect_widget()


    def update_gui(self):
        print("update_gui")
        for img_name, value in view.data.items():
            self.img_name_to_widget[img_name].display( value )




    def connect_widget(self):
        self.img_name_to_widget['EBT-INJ-VAC-IMG-01'] = self.IMG01_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-02'] = self.IMG02_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-03'] = self.IMG03_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-04'] = self.IMG04_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-05'] = self.IMG05_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-06'] = self.IMG06_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-07'] = self.IMG07_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-08'] = self.IMG08_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-09'] = self.IMG09_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-10'] = self.IMG10_lcdNumber
        self.img_name_to_widget['EBT-INJ-VAC-IMG-11'] = self.IMG11_lcdNumber

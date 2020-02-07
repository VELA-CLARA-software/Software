'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify     //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Software is distributed in the hope that it will be useful,          //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   11-01-2019
//  FileName:    gui.oy
//  Description: template for class for gui class in generic High Level Application
//
//
//*/
'''
from src.main_windows_source import Ui_mainWindow
from src.data import data
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QLabel
from PyQt4.QtCore import QString
from PyQt4.QtGui import QDoubleSpinBox
from PyQt4.QtGui import QComboBox
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QPalette


class gui(QMainWindow, Ui_mainWindow):  # do we ''need'' to inhereit from a main windOw?
    """
        gui class for BA1-easy-stage, this class inherits from a programamtically created QT designer classs
        it requires the BA1-easy-stage data class to work
    """
    def __init__(self):
        # init base class
        QMainWindow.__init__(self)

        # for setting colors of widgets define some hex-color-codes
        self.white = "#ffffff"
        self.red = "#ff5733"
        self.green = "#75ff33"
        #
        # startup
        self.setupUi(self)
        #
        # the data is held in a data class, make a reference to values for convenience
        self.data = data()
        self.values = self.data.values
        #
        # connect gui widgets to items in data.value, for convenience we keep references to widgets in some handy dicts
        # Thse dicts allow us easy access to the widgets we want via stage name, they are set up in set_widget_dicts()
        self.stage_name = {}
        self.read_device = {}
        self.set_device = {}
        self.move_to_dev = {}
        self.read_pos = {}
        self.set_pos_read = {}
        self.new_set_pos = {}
        self.min_pos = {}
        self.max_pos = {}
        self.device_stage = {}
        self.set_widget_dicts()

    def update(self):
        """
            update the gui widgets, this function is called from a timer in the controller
        """
        for stage, widget in self.read_pos.iteritems():
            widget.setValue(self.values[self.data.read_pos][stage])
            if self.values[self.data.is_moving][stage]:
                self.toggle_moving(widget)
            else:
                self.set_default_style(widget)
        for stage, widget in self.set_pos_read.iteritems():
            widget.setValue(self.values[self.data.set_pos][stage])
        if all(v is True for v in self.values[data.is_clear_for_beam].values()):
            self.set_clear_for_beam()
        else:
            self.set_not_clear_for_beam()

    def set_clear_for_beam(self):
        """
            set widget style when all stages are clear_for_beam
        """
        self.clear_for_beam_button.setStyleSheet("color: black; background-color: " + self.green)
        self.clear_for_beam_button.setText("All CLEAR FOR BEAM")

    def set_not_clear_for_beam(self):
        """
            set widget style when all stages are clear_for_beam
        """
        self.clear_for_beam_button.setStyleSheet("color: black; background-color: " + self.red)
        self.clear_for_beam_button.setText("PRESS TO MOVE ALL TO CLEAR FOR BEAM")

    def toggle_moving(self, widget):
        """
            change the widget color depending on the current color
        :param widget: which widget to change colo0r of
        """
        color = str(widget.palette().color(QPalette.Window).name())
        if color == self.red:
            widget.setStyleSheet("color: black; background-color: " + self.green)
        elif color == self.green:
            widget.setStyleSheet("color: black; background-color: " + self.red)
        else:
            widget.setStyleSheet("color: black; background-color: " + self.green)

    def set_default_style(self, widget):
        """
            set default widget style (white)
        :param widget: to change
        """
        if str(widget.palette().color(QPalette.Window).name()) != self.white:
            widget.setStyleSheet("background-color: white; color: black")

    def set_widget_dicts(self):
        """
        This function sets up a dictionary for each widget type, for each stage
        there is a dictionary for each type of widget:
        all the widgets have a common name then _1, _2, ... _9 for the stage number
        :return: nothing
        """
        # WE have hardcoded in 9 stages, they all have the same widgets,
        # they are numbered 1 to 9
        # iterate over each stage number, and get the name (as defined in config) we have 9 stages iterate over each
        # one, if it is active set up it's widgets, if it is not active disable it's widgets
        # We loop over each stage and set its widgets depending on if it is "ACTIVE" or not
        for stage_number in range(1, 10):
            if stage_number in self.values[data.active_stage_numbers]:
                self.set_active(stage_number)
            else:
                self.set_not_active(stage_number)
        for stage_name, widget in self.min_pos.iteritems():
            widget.setValue(self.values[data.min_pos][stage_name])
        for stage_name, widget in self.max_pos.iteritems():
            widget.setValue(self.values[data.max_pos][stage_name])
        for stage_name, widget in self.stage_name.iteritems():
            widget.setText(stage_name)
        for stage_name, widget in self.device_stage.iteritems():
            widget.addItems(self.values[self.data.stage_devices][stage_name])


    def set_active(self, stage_number):
        """
            set the widgets for stage_number to active, adds the widget to convenience dicts, and sets some default
            values and style options
        :param stage_number: which stage we are updating
        """
        # these base strings, are the base names of the widgets, each stage has its number appended to teh end of
        # these names
        name_label_base = "name_stage"
        move2dev_stage_base = "move2dev_stage"
        device_stage_base = "device_stage"
        read_pos_stage_base = "read_pos_stage"
        min_pos_stage_base = "min_pos_stage"
        max_pos_stage_base = "max_pos_stage"
        set_pos_stage_base = "set_pos_stage"
        read_set_pos_stage_base = "read_set_pos_stage"

        stage_name = self.data.stage_number_to_name[stage_number]
        print(__name__, " adding widgets for stage = ", stage_name, stage_number)

        # this is the suffix to add to each base name,
        suffix = "_" + str(stage_number)

        self.stage_name[stage_name] = self.findChild(QLabel, QString(name_label_base + suffix))
        self.device_stage[stage_name] = self.findChild(QComboBox, device_stage_base + suffix)
        self.move_to_dev[stage_name] = self.findChild(QPushButton, move2dev_stage_base + suffix)

        self.min_pos[stage_name] = self.findChild(QDoubleSpinBox, QString(min_pos_stage_base + suffix))
        self.min_pos[stage_name].setDecimals(self.values[data.precision][stage_name])
        self.min_pos[stage_name].setEnabled(False)
        self.set_default_style(self.min_pos[stage_name])

        self.max_pos[stage_name] = self.findChild(QDoubleSpinBox, max_pos_stage_base + suffix)
        self.max_pos[stage_name].setDecimals(self.values[data.precision][stage_name])
        self.max_pos[stage_name].setEnabled(False)
        self.set_default_style(self.max_pos[stage_name])

        self.read_pos[stage_name] = self.findChild(QDoubleSpinBox, read_pos_stage_base + suffix)
        self.read_pos[stage_name].setDecimals(self.values[data.precision][stage_name])
        self.read_pos[stage_name].setEnabled(False)
        self.set_default_style(self.read_pos[stage_name])
        self.read_pos[stage_name].setValue(self.values[self.data.read_pos][stage_name])


        self.set_pos_read[stage_name] = self.findChild(QDoubleSpinBox, read_set_pos_stage_base + suffix)
        self.set_pos_read[stage_name].setDecimals(self.values[data.precision][stage_name])
        self.set_pos_read[stage_name].setEnabled(False)
        self.set_default_style(self.set_pos_read[stage_name])

        self.new_set_pos[stage_name] = self.findChild(QDoubleSpinBox, set_pos_stage_base + suffix)
        self.new_set_pos[stage_name].setRange(self.values[data.min_pos][stage_name],
                                              self.values[data.max_pos][stage_name])
        self.new_set_pos[stage_name].setDecimals(self.values[data.precision][stage_name])
        self.new_set_pos[stage_name].setKeyboardTracking(False)
        self.set_default_style(self.new_set_pos[stage_name])
        self.new_set_pos[stage_name].setValue(self.values[data.set_pos][stage_name])


    # def set_up_widget(self, widget, stage_name):
    #     self.set_pos_read[stage_name] = self.findChild(QDoubleSpinBox, read_set_pos_stage_base + suffix)
    #     widget.setDecimals(self.values[data.precision][stage_name])
    #     self.set_pos_read[stage_name].setEnabled(False)
    #     self.set_default_style(self.set_pos_read[stage_name])


    def set_not_active(self, stage_number):
        move2dev_stage_base = "move2dev_stage"
        device_stage_base = "device_stage"
        read_pos_stage_base = "read_pos_stage"
        set_pos_stage_base = "set_pos_stage"
        min_pos_stage_base = "min_pos_stage"
        max_pos_stage_base = "max_pos_stage"

        read_set_pos_stage_base = "read_set_pos_stage"

        print(__name__, " adding widgets for stage = ", stage_number)
        suffix = "_" + str(stage_number)

        widget = self.findChild(QDoubleSpinBox, set_pos_stage_base + suffix)
        widget.setDisabled(True)

        widget = self.findChild(QComboBox, device_stage_base + suffix)
        widget.setDisabled(True)

        widget = self.findChild(QDoubleSpinBox, min_pos_stage_base + suffix)
        widget.setDisabled(True)

        widget = self.findChild(QDoubleSpinBox, max_pos_stage_base + suffix)
        widget.setDisabled(True)

        widget = self.findChild(QPushButton, move2dev_stage_base + suffix)
        widget.setDisabled(True)

        widget = self.findChild(QDoubleSpinBox, read_set_pos_stage_base + suffix)
        widget.setDisabled(True)

        widget = self.findChild(QDoubleSpinBox, read_pos_stage_base + suffix)
        widget.setDisabled(True)


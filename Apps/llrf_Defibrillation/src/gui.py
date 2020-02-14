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
//  FileName:    gui_source.oy
//  Description: template for class for gui_source class in generic High Level Application
//
//
//*/
'''
from src.gui_source.rf_defib_view import Ui_MainWindow
import data
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QIcon


class gui(QMainWindow, Ui_MainWindow): # do we ''need'' to inhereit from a main windOw?

    data = data.data()

    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.setWindowIcon(QIcon('.\\resources\\llrf_defibrillator\\defib.ico'))

        self.linac_value.setEnabled(False)
        self.gun_value.setEnabled(False)
        self.linac_is_keeping_alive.setEnabled(False)
        self.gun_is_keeping_alive.setEnabled(False)

        self.red = "#ff5733"
        self.green = "#75ff33"
        self.data = gui.data
        self.values = self.data.values


    def show_gui(self):
        self.show()


    def toggle_button(self, widget,  value):
        widget.setText(str(value))
        color = str(widget.palette().color(QPalette.Window).name())
        if color == self.red:
            widget.setStyleSheet("color: black; background-color: " + self.green)
        else:
            widget.setStyleSheet("color: black; background-color: " + self.red)


    def update(self):

        if self.values[self.data.should_keep_linac_alive]:
            self.linac_is_keeping_alive.setChecked(True)
        else:
            self.linac_is_keeping_alive.setChecked(False)

        if self.values[self.data.should_keep_gun_alive]:
            self.gun_is_keeping_alive.setChecked(True)
        else:
            self.gun_is_keeping_alive.setChecked(False)



        # for key, value in self.values.iteritems():
        #     print("gui", key, "=", value)

        if self.values[self.data.linac_keep_alive_value] != self.values[self.data.old_linac_keep_alive_value]:
            print("Linac CHANGED")
            self.toggle_button(self.linac_value, self.values[self.data.linac_keep_alive_value])
        # else:
        #     print("Linac NOT")


        if self.values[self.data.gun_keep_alive_value] != self.values[self.data.old_gun_keep_alive_value]:
            print("Gun CHANGED")
            self.toggle_button(self.gun_value, self.values[self.data.gun_keep_alive_value])
        # else:
        #     print("Gun NOT")






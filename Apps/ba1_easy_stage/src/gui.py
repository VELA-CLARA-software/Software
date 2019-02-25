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
from src.main_windows_source import Ui_MainWindow
from src.data  import data
from PyQt4.QtGui import QMainWindow


class gui(QMainWindow, Ui_MainWindow): # do we ''need'' to inhereit from a main windOw?


    def __init__(self):
        QMainWindow.__init__(self)
        #
        # startup
        self.setupUi(self)
        self.my_name = 'gui'
        self.data = data()
        self.values= self.data.values

        # to be neater each row should be a widget, that we set values to .... instead of this
        # cancer ...
        # see magnet App, for example ...




        self.widget_to_dataname = {}
        self.set_widget_dicts()

    def init_gui(self):
        self.values


    def show_gui(self):
        self.show()

    def hello(self):
        print(self.my_name + ' says hello')


    def update(self):
        for stage, widget in self.read_labels.iteritems():
            widget.setText( str(self.values[self.data.stage_positions][stage] ) )
        for stage, widget in self.set_labels.iteritems():
            widget.setValue( self.values[self.data.stage_set_positions][stage]  )



    def set_widget_dicts(self):

        self.name_labels = {}
        self.device_labels = {}
        self.read_labels = {}
        self.set_labels = {}
        self.move_buttons= {}
        self.dev_move_buttons = {}


        name_labels = [self.s1_name,self.s2_name,self.s3_name,self.s4_name,self.s5_name,
                            self.s6_name]
        device_labels = [self.s1_dev,self.s2_dev,self.s3_dev,self.s4_dev,self.s5_dev,
                            self.s6_dev]
        read_labels = [self.s1_read,self.s2_read,self.s3_read,self.s4_read,self.s5_read,
                            self.s6_read]
        set_labels = [self.s1_set,self.s2_set,self.s3_set,self.s4_set,self.s5_set,
                            self.s6_set]
        move_buttons= [self.s1_move2set,self.s2_move2set,self.s3_move2set,self.s4_move2set,self.s5_move2set,
                            self.s6_move2set]
        dev_move_buttons= [self.s1_move2dev,self.s2_move2dev,self.s3_move2dev,self.s4_move2dev,
                             self.s5_move2dev, self.s6_move2dev]


        for i, name in enumerate(self.values[self.data.stage_names]):
            print('name = ', name)
            name_labels[i].setText(name)
            self.name_labels[name] = name_labels[i].setText(name)

            print('dev = ', self.values[self.data.stage_devices][name])
            device_labels[i].addItems(self.values[self.data.stage_devices][name])
            self.device_labels[name] =  device_labels[i]
            self.read_labels[name] = read_labels[i]
            self.set_labels[name] = set_labels[i]
            self.move_buttons[move_buttons[i]] = name
            self.dev_move_buttons[dev_move_buttons[i]] = name







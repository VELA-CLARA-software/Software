"""
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
//  Last edit:   07-02-2020
//  FileName:    controller.py
//  Description: Controller for BA1 easy stage app
//
//
//*/
"""
from PyQt4 import QtCore
from src.data import data
from src.procedure import procedure
from src.gui import gui


class controller(object):  # inherit of an python object
    """
        This is the main controller that handles all objects, adn signals for the app
    """
    def __init__(self, argv):
        object.__init__(self)
        self.argv = argv
        print(__name__,' created with these arguments: ', self.argv)
        # create the main objects used in this design, FIRST data
        self.data = data()
        # second procedure
        self.procedure = procedure()
        # Then the GUI
        self.gui = gui()
        self.gui.setWindowTitle('BA1 Easy Stage')
        self.connect_gui_widgets()
        self.gui.show()
        self.gui.activateWindow()


        # Then the gui update timer
        self.start_count = 0
        self.timer = QtCore.QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(500)

    def connect_gui_widgets(self):
        for stage_name, widget in self.gui.new_set_pos.iteritems():
            # connect to a lambda, so we can pass the stage_name at the same time,
            # this pattern binds the stage_name on this lambda
            # https://www.mfitzp.com/article/qt-transmit-extra-data-with-signals/
            # !!WARNINBG!! there are subtleties in how you name the objects either side of the equals sign,
            widget.valueChanged.connect(lambda checked, stage_name=stage_name: self.move(stage_name=stage_name))
        for stage_name, widget in self.gui.move_to_dev.iteritems():
            widget.clicked.connect(lambda checked, stage_name=stage_name: self.move_to_device(stage_name))

        self.gui.clear_for_beam_button.clicked.connect(self.set_clear_for_beam)

    def set_clear_for_beam(self):
        self.procedure.set_clear_for_beam()

    def move(self, stage_name):
        print("move", stage_name, self.gui.new_set_pos[stage_name].value())
        self.procedure.move(stage_name, self.gui.new_set_pos[stage_name].value())

    def move_to_device(self, stage_name):
        device = str(self.gui.device_stage[stage_name].currentText())
        self.procedure.move_device(stage_name, device)

    def update_gui(self):
        self.procedure.update_values()
        self.gui.update()

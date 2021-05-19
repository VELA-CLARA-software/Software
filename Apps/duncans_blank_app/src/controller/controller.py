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
//  FileName:    controller.py
//  Description: template for class for controller in generic High Level Application
//
//
//*/
'''


from src.data.data import data
from src.procedure.procedure import procedure
from src.gui.gui import gui
import sys

sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\packages\\vcc\\bin\\Stage\\')
try:
    import VELA_CLARA_PILaser_Control as pil
except Exception as  e:
    print("FAILED TO LOAD VELA_CLARA_PILaser_Control")
    print(e)

class controller(object):# inherit of an python object


    def __init__(self, argv):
        object.__init__(self)
        self.my_name = "controller"
        self.argv = argv
        print('controller created with these arguments: ',self.argv)

        # create the main objects used in this design
        self.data = data()
        self.proccedure = procedure()
        self.gui = gui()
        self.hello()
        self.gui.show_gui()
        self.connect_gui_widgets()


    def connect_gui_widgets(self):
        self.gui.pushButton.clicked.connect(self.handle_pushButton)


    def handle_pushButton(self):
        print("HI")


    def hello(self):
        print(self.my_name+ ' says hello')
        self.data.hello()
        self.proccedure.hello()
        self.gui.hello()

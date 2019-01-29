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
//               qt help: http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
//
//*/
'''


from src.data.data import data
from src.procedure.procedure import procedure
from src.gui.gui import gui


class controller(object):

    def __init__(self, argv):
        object.__init__(self)
        self.my_name = "controller"
        self.argv = argv
        print('controller created with these arguments: ',self.argv)

        # create the objects used in th edesign
        self.data = data()

        self.procedure = procedure()
        # pass the message function to the proceudre
        self.function_dict = {}
        self.function_dict["message"] = self.message
        self.procedure.message = self.function_dict["message"]

        self.gui = gui()
        self.hello()
        self.gui.show_gui()
        self.connect_gui_widgets()
#f
## https://stackoverflow.com/questions/21071448/redirecting-stdout-and-stderr-to-a-pyqt4-qtextedit-from-a-secondary-thread


    def connect_gui_widgets(self):
        '''
            connect up the gui widget buttons to functions
        :return:
        '''
        self.gui.close_button.clicked.connect(self.handle_close)
        self.gui.do_something_button.clicked.connect(self.handle_do_something)
        self.gui.test_button.clicked.connect(self.handle_test)


    def handle_close(self):
        self.message(self.my_name + " handle_close called")
        self.message("close button clicked")


    def handle_do_something(self):
        self.message(self.my_name + " handle_do_something called")
        self.message("controller is executing self.procedure.do_something() ")
        self.procedure.do_something()
        self.message("self.procedure.do_something() FIN")


    def handle_test(self):
        self.message(self.my_name + " handle_test called")


    def message(self, message, priority = 0):
        '''
            all message get routed through here so they can get printed to message_pad
            as well as stdout
        :return:
        '''
        self.gui.new_message(message, priority)


    def hello(self):
        print(self.my_name+ ' says hello')
        self.data.hello()
        self.procedure.hello()
        self.gui.hello()

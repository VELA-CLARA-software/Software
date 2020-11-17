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
//  Last edit:   16-11-2020
//  FileName:    Valve_Status.py
//  Description: Generic template for __main__ for general High Level Application. This one is
//               also used in the valve status app
//
//
//*/
'''
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from src.control.control import control
import sys
import ctypes

# meh playing with icon robustness
myappid = 'stfc.clara_apps.valve_status.1'  # arbitrary string
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)


class App(QApplication):
    '''
        small wrapper class to hold the control in
    '''
    def __init__(self, sys_argv):
        QWidget.__init__(self, sys_argv)
        print('Creating Controller')
        self.control = control(sys_argv)
        print('Running')


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

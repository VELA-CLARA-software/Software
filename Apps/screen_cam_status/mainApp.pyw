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
//  FileName:    mainApp.oy
//  Description: screen_and_cam_status app, simple way to move screens in/out following correct
//               procedure, start stp cams, take HDF5 images, enable disable LEDs
//
//
//*/
'''
import sys
from PyQt5 import QtGui, QtCore
from src.control import control
import ctypes

class App(QtGui.QApplication):
    # https://stackoverflow.com/questions/1551605/how-to-set-applications-taskbar-icon-in-windows-7/1552105#1552105
    myappid = u'CLARA.cam_and_screen_status.1'  # arbitrary string
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

    def __init__(self, sys_argv):
        QtGui.QWidget.__init__(self, sys_argv)
        print('Creating Controller')
        self.control = control(sys_argv)
        print('Running')

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

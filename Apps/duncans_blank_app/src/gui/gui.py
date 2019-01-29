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
from src.gui.designer_MainWindow import Ui_MainWindow
from PyQt4.QtGui import QMainWindow


class gui(QMainWindow, Ui_MainWindow): # do we ''need'' to inhereit from a main windOw?


    def __init__(self):
        QMainWindow.__init__(self)
        self.my_name = 'gui'
        self.setupUi(self)

    def show_gui(self):
        self.show()

    def hello(self):
        print(self.my_name + ' says hello')
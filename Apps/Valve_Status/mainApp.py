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
//  Last edit:   05-06-2018
//  FileName:    mainApp.oy
//  Description: Generic template for __main__ for general High Level Application
//
//
//*/
'''
import sys
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\Release\\')
# for i in sys.path:
#     print i
from PyQt4.QtGui import QApplication
from PyQt4.QtGui import QWidget
from control.control import control
from procedure.procedure import procedure as procedure
from view.view import view as view


class App(QApplication):
    def __init__(self, sys_argv):
        QWidget.__init__(self, sys_argv)
        self.procedure = procedure()
        self.view = view()
        print 'Creating Controller'
        self.control = control(sys_argv, view = self.view, procedure= self.procedure)
        print 'Running'


if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

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
//  Created:   01-04-2020
//  Last edit:   05-06-2018
//  FileName:    magnetApp.py
//  Description: magnet app main source file, run this one to run the app
//                THIS IS UPDATED AND WORKING on 24-06-2021, beware solenoid degaussing, solenoid names, and  check
                   magnets get loaded properly
                   FOR FULL CATAP VERISON TAKE CARE!
//
//*/
'''
'''******** Import modules *********'''
import sys
import os
''' 
QApplication is the top-level class we create, 
'''
from PyQt5.QtWidgets import QApplication
'''
Import the controller class, everything specific to this app starts from there 
'''
from source.magnetAppController import magnetAppController
#import magnetAppGlobals as globals
sys.path.append(os.path.join(sys.path[0],'GUI'))
sys.path.append(os.path.join(sys.path[0],'control'))



class magnetApp(QApplication):
    def __init__(self,argv):
        # you need this init line here to instantiate a QTApplication
        QApplication.__init__(self,argv)
        # Everything else is handled by the magnetAppController
        self.controller = magnetAppController(argv)

if __name__ == '__main__':
    print("starting magnetApp")
    app = magnetApp(sys.argv)
    sys.exit(app.exec_())

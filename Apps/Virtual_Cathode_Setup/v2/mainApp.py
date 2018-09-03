#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Controllers is free software: you can redistribute it and/or modify  //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   03-07-2018
//  FileName:    controller.py
//  Description: The controller for the virtual cathode operator application
//
//
//
//
//*/
'''
import time
import sys,os
sys.path.append('\\\\apclara1\\ControlRoomApps\\Controllers\\bin\\stage\\')
#os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin' \
#                                      '\\Release\\'
#os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin
# \\stage\\'
#os.environ['PATH']=os.environ['PATH']+';\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin
# \\Release\\root_v5.34.34\\bin\\'
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\model')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\controller')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view')
#sys.path.append(str(os.path.dirname(os.path.abspath(__file__)))+'\\view\\viewSource')
# for i in sys.path:
#     print "hi"
#     print i
from PyQt4 import QtGui
from controller.controller import controller
from model.model import model
from view.mainView import mainView as view


class App(QtGui.QApplication):
    def __init__(self, sys_argv):
        QtGui.QWidget.__init__(self, sys_argv)
        self.model = model()

        #time.sleep(1000)

        print 'creating view'
        print 'creating view'
        print 'creating view'

        #time.sleep(20)
        #self.view = view()
        print 'Creating Controller'
        self.control = controller(sys_argv, model= self.model)
        #self.control = controller(sys_argv, view = self.view, model= self.model)
        #self.view.show()
        print 'Running'

if __name__ == '__main__':
    app = App(sys.argv)
    sys.exit(app.exec_())

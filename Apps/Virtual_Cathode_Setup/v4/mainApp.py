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
//  FileName:    virtual_cathode_controller.py
//  Description: The controller for the virtual cathode operator application
//
//
//
//
//*/
'''
import sys
# meh  https://stackoverflow.com/questions/11953618/pyinstaller-importerror-no-module-named
# -pyinstaller
sys.path.append('.')
import time
from PyQt4 import QtGui
from src.virtual_cathode_controller import virtual_cathode_controller


class App(QtGui.QApplication):
	# use sys_argv to pass in arguments
	def __init__(self, sys_argv):
		QtGui.QApplication.__init__(self, sys_argv)
		self.control = virtual_cathode_controller(sys_argv)
		self.control.view.setWindowIcon(
			QtGui.QIcon('resources\\Virtual_Cathode_App\\Virtual_Cathode_App.ico'))


if __name__ == '__main__':
	app = App(sys.argv)
	sys.exit(app.exec_())

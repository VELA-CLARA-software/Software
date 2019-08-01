#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify  //
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
//  Last edit:   03-07-2019
//  FileName:    rf_condition_view.py
//  Description: The rf_condition_view is the main gui
//
//
//
//
//*/
'''
#from PyQt4.QtGui import QApplication
#from PyQt4.QtCore import QTimer
#from controller_base import controller_base
#from src.gui.gui_conditioning import gui_conditioning
#import src.data.rf_condition_data_base as dat
#from src.data.state import state
import sys
import time
import os
from PyQt4.QtGui import QMainWindow
from rf_condition_view_base import Ui_rf_condition_mainWindow
from PyQt4.QtGui import *

from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QTextCursor
from PyQt4.QtCore import QTimer

class OutLog:

    initial_stdout = sys.stdout


    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        """
        here we are providing a new "write" method for the stdout
        https://docs.python.org/2/library/sys.html#module-sys
        sys.stdin
        sys.stdout
        sys.stderr
        File objects corresponding to the interpreter’s standard input, output and error streams.
        stdin is used for all interpreter input except for scripts but including calls to input()
        and raw_input(). stdout is used for the output of print and expression statements and for
        the prompts of input() and raw_input(). The interpreter’s own prompts and (almost all of)
        its error messages go to stderr. stdout and stderr needn’t be built-in file objects: any
        object is acceptable as long as it has a write() method that takes a string argument. (
        Changing these objects doesn’t affect the standard I/O streams of processes executed by
        os.popen(), os.system() or the exec*() family of functions in the os module.)
        :param m: the string to be written
        :return:
        """
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        self.edit.moveCursor(QTextCursor.End)
        self.edit.insertPlainText( m )

        if self.out:
            self.out.write(m)

        # also write message to the initial standard out
        OutLog.initial_stdout.write(m)


    #class main_controller(controller_base):
class rf_condition_view(QMainWindow, Ui_rf_condition_mainWindow):
    pass

        #
    # other attributes will be initialised in base-class
    def __init__(self, columnwidth = 80):
        QMainWindow.__init__(self)
        Ui_rf_condition_mainWindow.__init__(self)
        self.setupUi(self)
        self.message_pad.setLineWrapColumnOrWidth(columnwidth )

        self.config = None
        self.data = None
        self.values = None

        self.pixmap = QPixmap('resources\\rf_conditioning\\fine.png')
        self.label.setScaledContents(True)
        # self.label.setPixmap(self.pixmap.scaled(self.label.size()))
        self.label.setPixmap(self.pixmap)
        # redirect PYTHON std out ...
        sys.stdout = OutLog(edit=self.message_pad)
        #sys.stderr = OutLog(edit=self.message_pad, color=QColor(255, 0, 0))


    def start_gui_update(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(self.config.raw_config_data[self.config.GUI_UPDATE_TIME])

    # main update gui function, loop over all widgets, and if values is new update gui with new
    # value
    def update_gui(self):
        print("update_gui")
        QApplication.processEvents()
        # for key, val in self.widget.iteritems():
        #     if self.value_is_new(key, base.data.values[key]):
        #         self.update_widget(key, base.data.values[key], val)

    def normal_output_writer(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.message_pad.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.message_pad.setTextCursor(cursor)
        self.message_pad.ensureCursorVisible()

    def error_output_writer(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.message_pad.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.message_pad.setTextCursor(cursor)
        self.message_pad.ensureCursorVisible()
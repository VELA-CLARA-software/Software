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
//  Author:    DJS
//  Created:   02-04-2020
//  Last edit:   02-04-2020
//  FileName:    GUI_FileSave.py
//  Description: file save  window for  magnet settings
//*/
'''
# part of MagtnetApp

from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from .ui_source.Ui_FileSave import Ui_FileSave
import datetime
import magnetAppGlobals as globals


class GUI_FileSave(QMainWindow, Ui_FileSave):
    def __init__(self  ):
        QMainWindow.__init__(self)
        # startup crap
        self.setupUi(self)
        self.setWindowIcon(QIcon(globals.appIcon))
        self.appPixMap = QPixmap(globals.appIcon)
        self.commentsSection.appendPlainText("Some Interesting Comments...")
        self.now = datetime.datetime.now()
        #type(self.now.month)
        self.controller_type = ""
        self.cancelButton_2.clicked.connect(self.handle_fileSaveCancel)
        self.canWindowClose = False

    def setFileName(self):
        self.now = datetime.datetime.now()
        self.filename = globals.dburtLocation2 + \
                        self.controller_type + "_" + \
                        str(self.now.year)  + '-' + \
                        '{:02d}'.format(self.now.month) + '-' + \
                        '{:02d}'.format(self.now.day  ) + '-' + \
                        '{:02d}'.format(self.now.hour ) + \
                        '{:02d}'.format(self.now.minute)+ \
                        '.dburt'
        self.file_name_entry.setText(self.filename)
        #print 'SAVE FIILENAME = ' + self.filename

    def getComboBoxEntries(self):
        self.keywords = str(self.areaCombo.currentText()) + '\t' +\
                        str(self.comboBox1.currentText()) + '\t' +\
                        str(self.comboBox2.currentText()) + '\t' +\
                        str(self.comboBox3.currentText()) + '\t'
        return self.keywords
    # this event is inherited and we overload it so the GUI_FileSave
    # is never deleted, (until we call close on the entire program)
    def closeEvent(self, evnt):
        if self.canWindowClose:
            super(GUI_FileSave, self).closeEvent(evnt)
        else:
            evnt.ignore()
            self.hide()
    # cancel button
    def handle_fileSaveCancel(self):
        self.hide()
    # when we decide keywords we'll add more here...
    def addComboKeywords(self,controller_type):
        list1 = [
            self.tr(controller_type),
            self.tr('AREA   51'),
            self.tr('Cheyenne ')]
        self.areaCombo.addItems(list1)





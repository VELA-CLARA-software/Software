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
//               qt help: http://pyqt.sourceforge.net/Docs/PyQt4/classes.html
//
//*/
'''
from src.gui.designer_MainWindow import Ui_MainWindow
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QPalette
from PyQt4.QtGui import QLabel
from PyQt4.QtGui import QVBoxLayout


class gui(QMainWindow, Ui_MainWindow): # do we ''need'' to inhereit from a main windOw?


    def __init__(self):
        QMainWindow.__init__(self)
        self.my_name = 'gui'
        self.setupUi(self)
        # make some cosmetic changes for fun
        self.scroll_area.setBackgroundRole(QPalette.Dark)

        # add labels to the scroll_area in which to write text
        num_text_labels = 50
        self.labels = {}
        vbox = QVBoxLayout()
        vbox.addStretch(1)
        self.scrollAreaWidgetContents.setLayout(vbox)

        for i in range(0, num_text_labels):
            name = "label_" + str(i)
            print('New label, name = ', name)
            self.labels[i] = QLabel()
            vbox.addWidget(self.labels[i])
            self.labels[i].setObjectName(name)
            self.labels[i].setText(name)
            #self.scrollAreaWidgetContents
        self.current_label = 0

    def show_gui(self):
        self.show()


    def hello(self):
        print(self.my_name + ' says hello')


    def new_message(self, message, priority):
        self.labels[self.current_label % len(self.labels) ].setText(message)
        self.current_label += 1
        print message

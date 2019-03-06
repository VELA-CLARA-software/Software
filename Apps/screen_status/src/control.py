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
//  Description: Generic template for control class for general High Level Application
//
//
//*/
'''
from PyQt4.QtCore import QTimer

import view as view
import procedure as procedure
import data as data
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QAction


class control(object):
    # we don;t need to pass these things in !!
    def __init__(self,sys_argv = None):
        self.my_name = 'control'
        self.sys_argv = sys_argv
        '''define model and view'''
        self.data = data.data()
        self.procedure = procedure.procedure()

        self.view = view.view()


        #raw_input()

        # update gui with this:
        print('controller, starting timer')
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

        # show view
        self.view.show()
        self.set_up_gui()
        # update gui with this:
        self.start_gui_update()
        # show view
        self.view.show()
        print(self.my_name + ', class initiliazed')
        self.last_scr = ''

        self.gui_enabled_moving = []


    def set_up_gui(self):
        # connect main buttons to functions
        self.view.allout_Button.clicked.connect(self.handle_all_out)
        self.view.checkDevices_Button.clicked.connect(self.handle_checkDevices_Button)
        self.view.add_screens()

        # for name in self.procedure.scr_names:
        #     self.view.add_context(name, self.procedure.get_screen_devices(name))
            #self.button.customContextMenuRequested.connect(self.on_context_menu)

        # connect individual valve buttons to functions
        for name, widget in self.view.screens.iteritems():
            widget.clicked.connect(self.handle_in_out)
            self.view.add_context(name)
            widget.customContextMenuRequested.connect(self.on_context_menu)


    def on_context_menu(self, point):
        s = self.view.sender()
        scr = str(s.objectName())
        self.last_scr = scr

        popMenu = QMenu(s)

        if scr in self.gui_enabled_moving:
            a = QAction('CANCEL_MOVING', self.view.screens[scr])
            a.setObjectName('CANCEL_MOVING')
            popMenu.addAction(a)
        else:
            print(scr, " Context Menu" )
            devices = self.procedure.get_screen_devices(scr)
            for device in devices:
                print("Added device ",device)
                a = QAction(device, self.view.screens[scr])
                a.setObjectName(device)
                print("TEST ", a.objectName())
                popMenu.addAction(a)
                #x = popMenu.addAction(QAction(device, self.contextMenuChoice))
                #x.connect(self.contextMenuChoice(x.text()))
            #'popMenu.exec_(button.mapToGlobal())
        popMenu.triggered.connect(self.contextMenuChoice)
        popMenu.setStyleSheet("background-color: gray")
        popMenu.exec_(s.mapToGlobal(point))

    def contextMenuChoice(self, passed):
        device = str(passed.objectName())
        if device == 'CANCEL_MOVING':
            self.gui_enabled_moving.remove(self.last_scr)
        else:
            self.procedure.move_screen_to(self.last_scr,device)
            self.gui_enabled_moving.append(self.last_scr)


    def handle_checkDevices_Button(self):
        self.procedure.make_read_equal_set_all()


    def handle_screen_in(self):
        self.procedure.screen_in()

    def handle_all_out(self):
        self.procedure.all_out()

    def handle_in_out(self):
        sender = self.view.sender()
        self.procedure.in_out(str(sender.objectName()))

    def start_gui_update(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

    def update_gui(self):
        '''
            generic function that updates values from the procedure and then updates the gui
        '''
        self.procedure.update_states()

        # check states with self.gui_enabled_moving
        # magic && cancer
        to_delete = []
        for item in self.gui_enabled_moving:
            #print("Checking gui clicked for ", item)
            if self.procedure.is_moving(item):
                to_delete.append(item)
            elif self.procedure.set_state_equal_read_state(item):
                to_delete.append(item)
        for item in to_delete:
            self.gui_enabled_moving.remove(item)







        self.view.update_gui()
        #print('update_gui')




#!/usr/bin/env python
# -*- coding: utf-8 -*-
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
//  FileName:    view.oy
//  Description: Screen Status GUI
//
//
//*/
'''
#from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from PyQt4.QtGui import QMenu
from PyQt4.QtGui import QAction
from PyQt4 import QtCore
# view source, as generated in QT designer
from viewSource.Ui_screen_status_view import Ui_screen_status_view
# We need the SCREEN.STATE enum
import sys,os
sys.path.append('\\\\apclara1.dl.ac.uk\\ControlRoomApps\\Controllers\\bin\\Release\\')
from VELA_CLARA_Screen_Control import SCREEN_STATE
import data as data
from operator import itemgetter
import ctypes

class view(QMainWindow, Ui_screen_status_view ):
    # custom close signal to send to controller
    # closing = QtCore.pyqtSignal()

    # static data class
    data = data.data()

    def __init__(self):
        QWidget.__init__(self)

        self.red = "#ff5733"
        self.green = "#75ff33"

        self.setupUi(self)
        self.setWindowIcon(QIcon('.\\resources\\screen_status\\screen_status_icon.ico'))

        # ref. to static data class, to help others with readability
        self.data = view.data

        print('gui __init__ ', self.data.screen_names)
        #raw_input()
        self.screens = {}

    def add_screens(self):
        print('add_screens ', self.data.screen_names)
        self.vbox = QVBoxLayout()
        # Order the anmes
        # this type of ordering should be pushed down to the HWC
        canon_order = ['LRG','S01','L01','S02','C2V','INJ','BA1','BA2']
        order = []
        for name in self.data.screen_names:
            print('name = ', name)
            i = 0
            for area in canon_order:
                if area in name:
                    order.append([i,name])
                else:
                    i += 1
        orderd_names =  [x[1] for x in sorted(order, key=itemgetter(0))]
        # print("ORDER")
        # for n in orderd_names:
        #     print n


        for name in orderd_names:
            self.screens[name] = QPushButton(self.widget)
            self.screens[name].setObjectName(name)
            self.screens[name].setText(name)
            self.vbox.addWidget(self.screens[name])
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)

    def add_context(self, name):
        self.screens[name].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
       # create context menu


    def set_clara_led_is_on(self):
        self.clara_led_button.setStyleSheet("background-color: " + self.green)
        self.clara_led_button.setText('SWITCH CLARA LED OFF')


    def set_clara_led_is_off(self):
        self.clara_led_button.setStyleSheet("background-color: " + self.red)
        self.clara_led_button.setText('SWITCH CLARA LED ON')

    def set_vela_led_is_on(self):
        self.vela_led_button.setStyleSheet("background-color: " + self.green)
        self.vela_led_button.setText('SWITCH VELA LED OFF')

    def set_vela_led_is_off(self):
        self.vela_led_button.setStyleSheet("background-color: " + self.red)
        self.vela_led_button.setText('SWITCH VELA LED ON')

    def update_gui(self):
        for name, state in self.data.states.iteritems():
            if self.data.move_attempted[name][0]:
                self.set_clicked(self.screens[name])
            # the order we check things matters for how the GUI looks
            elif self.data.v_enabled[name]:
                self.set_moving(self.screens[name])
                #print(name," v is enabled")
            elif self.data.h_enabled[name]:
                self.set_moving(self.screens[name])
                #print(name, " h is enabled")
            else:
                self.update_widget(self.screens[name], state)


    def set_clicked(self, widget):
        widget.setStyleSheet("background-color: purple")
        widget.setText(widget.objectName() + ' CLICKED')


    def set_moving(self, widget):
        widget.setStyleSheet("background-color: yellow")
        widget.setText(widget.objectName() + ' MOVING')


    def update_widget(self,widget,state):


        if self.data.clara_led_state:
            self.set_clara_led_is_on()
        else:
            self.set_clara_led_is_off()

        if self.data.vela_led_state:
            self.set_vela_led_is_on()
        else:
            self.set_vela_led_is_off()

        # now we have to handle the horrible case of clicked, but not yet moving
        # and not got to where we want to ...

        if state == SCREEN_STATE.SCREEN_MOVING:
            widget.setStyleSheet("background-color: yellow")
            widget.setText( widget.objectName() + ' MOVING' )
        elif state == SCREEN_STATE.V_MAX:#1
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' V-MAX' )
        elif state == SCREEN_STATE.H_MAX:#2
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' H -MAX' )
        elif state == SCREEN_STATE.V_MIRROR:#3
            widget.setStyleSheet("background-color: light gray")
            widget.setText( widget.objectName() + ' V-MIRROR' )
        elif state == SCREEN_STATE.V_GRAT:#4
            widget.setStyleSheet("background-color: cyan")
            widget.setText( widget.objectName() + ' V-GRATICULE' )
        elif state == SCREEN_STATE.YAG:#5
            widget.setStyleSheet("background-color: " + self.green)
            widget.setText( widget.objectName() + ' YAG' )
        elif state == SCREEN_STATE.V_YAG:#6
            widget.setStyleSheet("background-color: " + self.green)
            widget.setText( widget.objectName()+ ' YAG' )
        elif state == SCREEN_STATE.V_RF:
            widget.setStyleSheet("background-color: " + self.red)
            widget.setText( widget.objectName() + ' RF' )
        elif state == SCREEN_STATE.V_COL:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' V-COL' )
        elif state == SCREEN_STATE.H_RETRACTED:
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' H-RETRACTED' )
        elif state == SCREEN_STATE.V_RETRACTED:
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' V-RETRACTED' )
        elif state == SCREEN_STATE.RETRACTED:
            widget.setStyleSheet("background-color: " + self.red)
            widget.setText( widget.objectName() + ' RETRACTED (RF)' )
        elif state == SCREEN_STATE.V_SLIT_1:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' SLIT' )
        elif state == SCREEN_STATE.H_SLIT_1:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' SLIT' )
        elif state == SCREEN_STATE.H_SLIT_2:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' SLIT' )
        elif state == SCREEN_STATE.H_SLIT_3:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' SLIT' )
        elif state == SCREEN_STATE.H_APT_1:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' H_APT_1' )
        elif state == SCREEN_STATE.H_APT_2:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' H_APT_2' )
        elif state == SCREEN_STATE.H_APT_3:
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' H_APT_3' )
        else:
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' ERRRR' )

        # if state == 'CLICKED':
        #     widget.setStyleSheet("background-color: purple")
        #     widget.setText( widget.objectName() + ' CLICKED' )







        # elif state == 'CLICKED':
        #     widget.setStyleSheet("background-color: orange")
        #     widget.setText( widget.objectName() + ' CLICKED' )

        #
        # .value("H_RETRACTED",     screenStructs::SCREEN_STATE::H_RETRACTED)
        # .value("H_SLIT_1",        screenStructs::SCREEN_STATE::H_SLIT_1)
        # .value("H_SLIT_2",        screenStructs::SCREEN_STATE::H_SLIT_2)
        # .value("H_SLIT_3",        screenStructs::SCREEN_STATE::H_SLIT_3)
        # .value("H_APT_1",         screenStructs::SCREEN_STATE::H_APT_1)
        # .value("H_APT_2",         screenStructs::SCREEN_STATE::H_APT_2)
        # .value("H_APT_3",         screenStructs::SCREEN_STATE::H_APT_3)
        # .value("V_RETRACTED",     screenStructs::SCREEN_STATE::V_RETRACTED)
        # .value("V_SLIT_1",        screenStructs::SCREEN_STATE::V_SLIT_1)
        # .value("V_MAX",           screenStructs::SCREEN_STATE::V_MAX)
        # .value("V_RF",            screenStructs::SCREEN_STATE::V_RF)
        # .value("V_MIRROR",        screenStructs::SCREEN_STATE::V_MIRROR)
        # .value("V_YAG",           screenStructs::SCREEN_STATE::V_YAG)
        # .value("V_GRAT",          screenStructs::SCREEN_STATE::V_GRAT )
        # .value("V_COL",           screenStructs::SCREEN_STATE::V_COL )
        # .value("RETRACTED",       screenStructs::SCREEN_STATE::YAG )
        # .value("YAG",             screenStructs::SCREEN_STATE::RETRACTED )
        # .value("UNKNOWN_POSITION",screenStructs::SCREEN_STATE::UNKNOWN_POSITION )

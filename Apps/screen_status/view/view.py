#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
#from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton

from viewSource.Ui_view import Ui_CamState
from procedure.procedure import procedure
from VELA_CLARA_Screen_Control import SCREEN_STATE

class view(QMainWindow, Ui_CamState ):
    # custom close signal to send to controller
    # closing = QtCore.pyqtSignal()

    # dictionary for each camera
    screens = {}

    # create a procedure object to access static data
    procedure = procedure()
    data = procedure.states

    def __init__(self):
        QWidget.__init__(self)
        self.my_name = 'view'
        self.setupUi(self)
        self.setWindowIcon(QIcon('resources\\cam_status\\moview.ico'))

    def add_cams(self,names):
        self.vbox = QVBoxLayout()
        for name in names:
            view.screens[name] = QPushButton(self.widget)
            view.screens[name].setObjectName(name)
            view.screens[name].setText(name)
            self.vbox.addWidget(view.screens[name])
        self.vbox.addStretch(1)
        self.groupBox.setLayout(self.vbox)

    def update_gui(self):
        for name, state in view.data.iteritems():
            self.update_widget(view.screens[name],state)

    def update_widget(self,widget,state):
        if state == SCREEN_STATE.RETRACTED:
            widget.setStyleSheet("background-color: green")
            widget.setText( widget.objectName() + ' SCREEN-OUT' )
        elif state == SCREEN_STATE.V_RETRACTED:
            widget.setStyleSheet("background-color: green")
            widget.setText( widget.objectName() + ' SCREEN-OUT' )
        elif state == SCREEN_STATE.H_RETRACTED:
            widget.setStyleSheet("background-color: green")
            widget.setText( widget.objectName() + ' SCREEN-OUT' )
        elif state == SCREEN_STATE.YAG:
            widget.setStyleSheet("background-color: red")
            widget.setText( widget.objectName() + ' SCREEN-IN' )
        elif state == SCREEN_STATE.V_YAG:
            widget.setStyleSheet("background-color: red")
            widget.setText( widget.objectName()+ ' SCREEN-IN' )
        elif state == SCREEN_STATE.V_RF:
            widget.setStyleSheet("background-color: green")
            widget.setText( widget.objectName() + ' RF' )
        elif state == SCREEN_STATE.SCREEN_MOVING:
            widget.setStyleSheet("background-color: yellow")
            widget.setText( widget.objectName() + ' MOVING' )

        elif state == 'CLICKED':
            widget.setStyleSheet("background-color: orange")
            widget.setText( widget.objectName() + ' CLICKED' )
        else:
            widget.setStyleSheet("background-color: magenta")
            widget.setText( widget.objectName() + ' ERRRR' )
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

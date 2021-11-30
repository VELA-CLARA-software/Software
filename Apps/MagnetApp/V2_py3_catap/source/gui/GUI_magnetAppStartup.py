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
//  Created:   01-04-2020
//  Last edit:   01-04-2020
//  FileName:    magnetAppController.py
//  Description: controller or magnet app
//
//
//*/
'''

import sys
import os
catap_path = os.path.join('C:\\Users', 'djs56', 'Documents', 'catapillar-build',
                          'PythonInterface','Release')
sys.path.append(catap_path)
resource_path = os.path.join('resources','magnetApp')
sys.path.append(os.path.join(sys.path[0],resource_path))
from CATAP.GlobalTypes import TYPE
from CATAP.GlobalStates import STATE
from PyQt5 import QtGui, QtCore, QtWidgets
from .ui_source.Ui_magnetAppStartup import Ui_magnetAppStartup
import magnetAppGlobals as globals
#from VELA_CLARA_Magnet_Control import MACHINE_MODE
#from VELA_CLARA_Magnet_Control import MACHINE_AREA


class GUI_magnetAppStartup(QtWidgets.QMainWindow, Ui_magnetAppStartup):
    # static signals to emit when radioButtons are pressed
    machineAreaSignal = QtCore.pyqtSignal(TYPE)
    machineModeSignal = QtCore.pyqtSignal(STATE)
    def __init__(self):
        print('create startup window')
        QtWidgets.QWidget.__init__(self)
        self.setupUi(self)
        # I can't find a *good* way to get the toggled radio button, apart from emitting signals and
        # interpreting them later... meh
        try:
            self.VELA_BA2.toggled.connect(lambda:self.handle_areaRadio(self.VELA_BA2))
        except:
            pass
        try:
            self.VELA_BA1.toggled.connect(lambda:self.handle_areaRadio(self.VELA_BA1))
        except:
            pass
        try:
            self.VELA_INJ.toggled.connect(lambda:self.handle_areaRadio(self.VELA_INJ))
        except:
            pass
        try:
            self.CLARA_PHASE_1.toggled.connect(lambda:self.handle_areaRadio(self.CLARA_PHASE_1))
        except:
            pass
        try:
            self.CLARA_2_BA1.toggled.connect(lambda:self.handle_areaRadio(self.CLARA_2_BA1))
        except:
            pass
        try:
            self.CLARA_2_BA2.toggled.connect(lambda:self.handle_areaRadio(self.CLARA_2_BA2))
        except:
            pass
        try:
            self.CLARA_2_BA1_BA2.toggled.connect(lambda:self.handle_areaRadio(self.CLARA_2_BA1_BA2))
        except:
            pass

        self.virtualMode.toggled.connect(lambda:self.handle_modeRadio(self.virtualMode))
        self.physicalMode.toggled.connect(lambda:self.handle_modeRadio(self.physicalMode))
        self.offlineMode.toggled.connect(lambda:self.handle_modeRadio(self.offlineMode))
        self.appPixMap = QtGui.QPixmap(globals.appIcon)
        self.iconLabel.setPixmap(self.appPixMap)
        self.setWindowTitle("VELA - CLARA Magnet App")
        self.logo = QtGui.QPixmap(globals.claraIcon)
        self.scaledLogo = self.logo.scaled(self.logoLabel.size(), QtCore.Qt.KeepAspectRatio)
        self.logoLabel.setPixmap(self.scaledLogo)
        self.setWindowIcon(QtGui.QIcon('magpic.jpg'))
        self.waitMessageLabel.setText("")
        # This dict needs updating when you add in different machine areas
        self.radioAreaTo_ENUM ={
            #self.VELA_BA2.objectName(): MACHINE_AREA.VELA_BA2,
            #self.VELA_BA1.objectName(): MACHINE_AREA.VELA_BA1,
            self.VELA_INJ.objectName(): TYPE.VELA,
            #self.CLARA_PHASE_1.objectName(): MACHINE_AREA.CLARA_PH1,
            #self.CLARA_2_BA1.objectName(): MACHINE_AREA.CLARA_2_BA1,
            self.CLARA_2_BA1_BA2.objectName(): TYPE.CLARA_2_BA1_BA2
            #self.CLARA_2_VELA.objectName(): MACHINE_AREA.CLARA_2_VELA
        }

        self.radioModeTo_ENUM = {
            self.virtualMode.objectName(): STATE.VIRTUAL,
            self.physicalMode.objectName(): STATE.PHYSICAL,
            self.offlineMode.objectName(): STATE.OFFLINE
        }

    # the radio buttones emit a MACHINE_MODE or MACHINE_AREA enum
    # this is then set as a variable in the  magnetAppController
    def handle_areaRadio(self,r):
        if r.isChecked() == True:
            print(self.radioAreaTo_ENUM[r.objectName()])
            self.machineAreaSignal.emit(self.radioAreaTo_ENUM[r.objectName()])
        # wow this is bad ...
        if r == self.VELA_INJ:
            self.CLARA_2_BA1_BA2.setChecked(False)
        if r == self.CLARA_2_BA1_BA2:
            self.VELA_INJ.setChecked(False)


    def handle_modeRadio(self,r):
        if r.isChecked() == True:
            self.machineModeSignal.emit(self.radioModeTo_ENUM[r.objectName()])



#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
# part of MagtnetApp
from PyQt5 import QtCore, QtGui, QtWidgets
from .ui_source.Ui_magnetWidget import Ui_magnetWidget
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


# class MyPopup(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#
#     def paintEvent(self, e):
#         dc = QPainter(self)
#         dc.drawLine(0, 0, 100, 100)
#         dc.drawLine(100, 0, 0, 100)


class GUI_magnetWidget(QtWidgets.QMainWindow, Ui_magnetWidget):
    # we know there will be many instances of this class,
    # so lets try and be more efficent with our memory
    # class variables (sort of static),
    # we only need one copy for each instance of this class
    psuStateColors = {STATE.OFF   : "background-color: red",
                      STATE.ON    : "background-color: green",
                      # Lost in new magnet scheme
                      #MAG_PSU_STATE.MAG_PSU_TIMING: "background-color: yellow",
                      STATE.ERR : "background-color: magenta"
        #,STATE.MAG_PSU_NONE  : "background-color: black"
                      }
    # the meter is *1000 to give 3 decimal places precision
    riMeterScalefactor = 1000  # MAGIC_NUMBER

    has_focus = None

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setupUi(self)
        # holds the reference to the c++ Magnet Object Data,
        # this ***MUST*** be in a list otherwise the reference won't update
        # maybe it could be a dict, or set,
        # in fact i think it **MUST** be in a mutable container
        # set in  addMagnetsToMainView in the magnetAppController
        self.magRef = []
        #self.SIValue.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        # active magnets have their check button checked
        self.isActive = False
        self.mag_Active.toggled.connect( self.setActiveState ) # check button connection

        self.SIValue.setDecimals(3)
        # custom context menu
        # https://wiki.python.org/moin/PyQt/Handling%20context%20menus
        self.SIValue.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.SIValue.customContextMenuRequested.connect(self.showMenu)

        self.Mag_PSU_State_Button.clicked.connect(self.psu_pressed)

        self.SI_default_style_sheet = self.SIValue.styleSheet()
        self.SIValue.installEventFilter(self)

        self.menu = QtWidgets.QTableWidget(1,2)
        self.menu.setItem(0, 0, QtWidgets.QTableWidgetItem("SI Step"))
        #
        self.isDegaussing = None


    def showMenu(self,position):
        print('show menu')
        # self.menu.setItem(0, 1, QTableWidgetItem(self.SIValue.singleStep()))
        #
        # self.menu.move(self.SIValue.mapToGlobal(position))
        # self.menu.show()
        # menu = QTableWidget()
        # menu.setRowCount(1)
        # menu.setColumnCount(2)
        # menu.setItem(0, 0, QTableWidgetItem("Si Step = "))

        # menu = QMenu()
        # quitAction = menu.addAction("Quit")
        # I = menu.addAction("Set Step")
        # menu.exec_(self.SIValue.mapToGlobal(position))
        # if action == I:
        #      print("HELLO")
        # elif action == quitAction:
        #      print("setSI step")

    def eventFilter(self, qobject, qevent):
        if isinstance(qobject , QtWidgets.QDoubleSpinBox):
            if isinstance(qevent, QtGui.QFocusEvent):
                 if qevent.gotFocus():
                    self.has_focus = True
                    print('gotFocus')
                    self.SIValue.setStyleSheet(" border: 3px solid black")
                 elif qevent.lostFocus():
                    self.has_focus = False
                    print('lostFocus')
                    self.SIValue.setStyleSheet(self.SI_default_style_sheet)
        return False



    def clearSelection(self):
        self.setCurrentIndex(-1)

    def updatePSUButton(self, psuState, button):
        button.setStyleSheet(GUI_magnetWidget.psuStateColors.get(psuState, "background-color: black"))

    # called after the magnet
    def setDefaultOptions(self):
        #self.name.setText(self.magRef[0].name)

        # the long name is too long, so remove MAG, EBT and CLA
        long_name = self.magRef[0].name.split("-")
        long_name.remove("MAG")
        if "EBT" in long_name:
            long_name.remove("EBT")
        if "CLA" in long_name:
            long_name.remove("CLA")
        short_name = "-".join(long_name)
        self.name.setText(short_name)

        rimin =  self.magRef[0].min_i * GUI_magnetWidget.riMeterScalefactor
        rimax =  self.magRef[0].max_i * GUI_magnetWidget.riMeterScalefactor
        self.RIMeter.setRange(rimin, rimax)

    #active magnets are those with the check box checked
    def setActiveState(self):
        self.isActive = self.mag_Active.isChecked()
    # we use the reference to the magnet object contained in the list self.magRef to get the
    # latest magnet object values to update the gui with
    def updateMagWidget(self):
        #print 'update ' + self.localName
        if self.has_focus:
            pass
        else:
            self.SIValue.setValue( self.magRef[0].getSETI() )

        # if self.magRef[0].name == "EBT-INJ-MAG-DIP-02":
        #     print("psu_state = ", self.magRef[0].psu_state)

        self.updatePSUButton(self.magRef[0].psu_state, self.Mag_PSU_State_Button)
        # if self.magRef[0].revType == MAG_REV_TYPE.NR:
        #     self.updatePSUButton(self.magRef[0].nPSU.psuState, self.PSU_N_State_Button)
        #     self.updatePSUButton(self.magRef[0].rPSU.psuState, self.PSU_R_State_Button)
        self.RIMeter.setValue(self.magRef[0].READI * self.riMeterScalefactor)
        self.Mag_PSU_State_Button.setText("{:.3f}".format(self.magRef[0].READI))
        self.isDegaussing = self.magRef[0].is_degaussing


    def psu_pressed(self):
        print('psu pressed')
        if self.magRef[0].psu_state == STATE.ON:
            self.magRef[0].psu_state = STATE.OFF
        elif self.magRef[0].psu_state == STATE.OFF:
            self.magRef[0].psu_state = STATE.ON

    # set the PSU button colors based on their state
    # CANCER, but it's been refactored out and i'm leaving this here to remind
    # myself how NOT to do things...
    # def updatePSUButton_OLD(self, psuState, button):
    #     if psuState == MAG_PSU_STATE.MAG_PSU_OFF:
    #         button.setStyleSheet("background-color: red")
    #     elif psuState == MAG_PSU_STATE.MAG_PSU_ON:
    #         button.setStyleSheet("background-color: green")
    #     elif psuState == MAG_PSU_STATE.MAG_PSU_TIMING:
    #         button.setStyleSheet("background-color: yellow")
    #     elif psuState == MAG_PSU_STATE.MAG_PSU_ERROR:
    #         button.setStyleSheet("background-color: magenta")
    #     elif psuState == MAG_PSU_STATE.MAG_PSU_NONE:
    #         button.setStyleSheet("background-color: black")
    #     else:
    #         print 'ERROR with ' + self.localName



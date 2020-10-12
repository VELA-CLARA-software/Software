#!/usr/bin/env python
# -*- coding: utf-8 -*-
# DJS 2017
#from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QWidget
from PyQt4.QtGui import QMainWindow
from PyQt4.QtGui import QIcon
from PyQt4.QtGui import QFocusEvent
from PyQt4.QtGui import QDoubleSpinBox
from PyQt4.QtGui import QDoubleValidator
from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QVBoxLayout
from PyQt4.QtGui import QPushButton
from VELA_CLARA_Magnet_Control import MAG_PSU_STATE
from viewSource.Ui_view import Ui_SolAdjuster
from procedure.procedure import procedure


class view(QMainWindow, Ui_SolAdjuster ):
    # custom close signal to send to controller
    # closing = QtCore.pyqtSignal()

    # create a procedure object to access static data
    procedure = procedure()

    def __init__(self):
        QWidget.__init__(self)
        self.my_name = 'view'
        self.setupUi(self)
        self.red = "#ff5733"
        self.green = "#75ff33"
        self.setWindowIcon(QIcon('resources\\cam_status\\moview.ico'))

        self.bsol_stepsize.setValue(1.00)
        self.sol_stepsize.setValue(1.00)

        self.bsol_seti.installEventFilter(self)
        self.sol_seti.installEventFilter(self)
        self.sol_seti_name = self.sol_seti.objectName()
        self.bsol_seti_name = self.bsol_seti.objectName()
        self.bsol_seti_has_focus = False
        self.sol_seti_has_focus = False

        self.degauss_default_style = self.degauss_sol_0.styleSheet()
        self.spin_style_sheet = self.bsol_seti.styleSheet()

        self.rf_prot_state.setEnabled(False)

        self.psuStateColors = {MAG_PSU_STATE.MAG_PSU_OFF   : "color: black; background-color: " +
                                                        self.red,
                          MAG_PSU_STATE.MAG_PSU_ON    : "color: black; background-color: " + self.green,
                          # Lost in new magnet scheme
                          #MAG_PSU_STATE.MAG_PSU_TIMING: "background-color: yellow",
                          MAG_PSU_STATE.MAG_PSU_ERROR : "background-color: magenta",
                          MAG_PSU_STATE.MAG_PSU_NONE  : "background-color: black"}


    def eventFilter(self, qobject, qevent):
        if isinstance(qobject , QDoubleSpinBox):
            if isinstance(qevent, QFocusEvent):
                if qobject.objectName() == self.sol_seti_name:
                    if qevent.gotFocus():
                        self.sol_seti_has_focus = True
                        self.sol_seti.setStyleSheet(" border: 3px solid black")
                    elif qevent.lostFocus():
                        self.sol_seti_has_focus = False
                        self.sol_seti.setStyleSheet(self.spin_style_sheet)

                if qobject.objectName() == self.bsol_seti_name:
                    if qevent.gotFocus():
                        self.bsol_seti_has_focus = True
                        self.bsol_seti.setStyleSheet(" border: 3px solid black")
                    elif qevent.lostFocus():
                        self.bsol_seti_has_focus = False
                        self.bsol_seti.setStyleSheet(self.spin_style_sheet)

            #
            # if isinstance(qevent, QFocusEvent):
            #     print("event filter = ", str(qobject.objectName()))
            #     elif qobject.objectName() == self.bsol_seti_name:
            #         self.bsol_seti_has_focus = True
            #         self.bsol_seti.setStyleSheet(" border: 3px solid black")
            #         print("self.bsol_seti_has_focus = True ")
            #     else:
            #         self.bsol_seti_has_focus = False
            #         self.sol_seti_has_focus = False
            #         self.sol_seti.setStyleSheet(self.spin_style_sheet)
            #         self.bsol_seti.setStyleSheet(self.spin_style_sheet)
        return False





    def update_gui(self):
        self.sol_seti.setValue(procedure.data["sol_seti"])
        self.bsol_seti.setValue(procedure.data["bsol_seti"])

        self.BSol_PSU_State.setText("{:.3f}".format(procedure.data["bsol_readi"]))
        self.Sol_PSU_State.setText("{:.3f}".format(procedure.data["sol_readi"]))


        self.BSol_PSU_State.setStyleSheet(self.psuStateColors[procedure.data["bsol_psu"]] )
        self.Sol_PSU_State.setStyleSheet(self.psuStateColors[procedure.data["sol_psu"]] )

       # print("procedure.data[rf_prot] = ",procedure.data["rf_prot"])

        if procedure.data["rf_prot"]:
            self.rf_prot_state.setStyleSheet("color: black; background-color: " + self.green)
        else:
            self.rf_prot_state.setStyleSheet("color: black; background-color: " + self.red)

        if procedure.data["can_degauss"]:
            self.degauss_sol_0.setEnabled(True)
            self.degauss_bsol_0.setEnabled(True)
            self.degauss_sol.setEnabled(True)
            self.degauss_bsol.setEnabled(True)
        else:
            self.degauss_sol_0.setEnabled(False)
            self.degauss_bsol_0.setEnabled(False)
            self.degauss_sol.setEnabled(False)
            self.degauss_bsol.setEnabled(False)

        if procedure.data["sol_is_degaussing"]:
            self.degauss_sol_0.setStyleSheet("color: black; background-color: " + self.red)
            self.degauss_sol.setStyleSheet("color: black; background-color: " + self.red)
            self.degauss_sol_0.setEnabled(False)
            self.degauss_sol.setEnabled(False)
        else:
            self.degauss_sol_0.setStyleSheet(self.degauss_default_style)
            self.degauss_sol.setStyleSheet(self.degauss_default_style)

        if procedure.data["bsol_is_degaussing"]:
            self.degauss_bsol_0.setStyleSheet("color: black; background-color: " + self.red)
            self.degauss_bsol.setStyleSheet("color: black; background-color: " + self.red)
            self.degauss_bsol_0.setEnabled(False)
            self.degauss_bsol.setEnabled(False)
        else:
            self.degauss_bsol_0.setStyleSheet(self.degauss_default_style)
            self.degauss_bsol.setStyleSheet(self.degauss_default_style)

        if self.bsol_seti_has_focus:
            pass
        else:
            #print("set bsol val = ", procedure.data["bsol_seti"])
            self.bsol_seti.setValue(procedure.data["bsol_seti"])

        if self.sol_seti_has_focus:
            pass
        else:
            #print("set sol val = ", procedure.data["sol_seti"])
            self.sol_seti.setValue(procedure.data["sol_seti"])


        # else:
        #     self.sol_seti.setStyleSheet(self.spin_style_sheet)
        #     self.sol_seti.setValue(procedure.data["sol_seti"])
        #
        # if procedure.data["bsol_seti_has_focus"]:
        #     self.bsol_seti.setStyleSheet(" border: 3px solid black")
        # else:
        #     self.bsol_seti.setStyleSheet(self.spin_style_sheet)
        #     self.bsol_seti.setValue(procedure.data["bsol_seti"])



        # procedure.data["sol_readi"] = procedure.magnets["sol"].readi
        # procedure.data["sol_psu"] = procedure.magnets["sol"].psuState
        # procedure.data["sol_is_degaussing"] = procedure.magnets["sol"].isDegaussing
        #
        # procedure.data["bsol_seti"] = procedure.magnets["bsol"].seti
        # procedure.data["bsol_readi"] = procedure.magnets["bsol"].readi
        # procedure.data["bsol_psu"] = procedure.magnets["sol"].psuState
        # procedure.data["bsol_is_degaussing"] = procedure.magnets["sol"].isDegaussing




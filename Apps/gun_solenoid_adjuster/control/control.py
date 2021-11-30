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
from PyQt4.QtGui import QApplication

import view.view as view
import procedure.procedure as procedure


class control(object):
    procedure = None
    view  = None
    def __init__(self,sys_argv = None,view = None, procedure= None):
        self.my_name = 'control'
        '''define procedure  and view'''
        control.procedure = procedure
        control.view = view

        # update gui with this:
        print('controller, starting timer')
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

        # show view
        self.view.show()
        print("show view")

        self.set_up_gui()
        # update gui with this:
        self.start_gui_update()
        # show view
        print(self.my_name + ', class initiliazed')


    def set_up_gui(self):
        # connect main buttons to functions
        self.view.degauss_sol_0.clicked.connect(self.handle_degauss_sol_0)
        self.view.degauss_bsol_0.clicked.connect(self.handle_degauss_bsol_0)
        self.view.degauss_sol.clicked.connect(self.handle_degauss_sol)
        self.view.degauss_bsol.clicked.connect(self.handle_degauss_bsol)
        self.view.BSol_PSU_State.clicked.connect(self.handle_BSol_PSU_State)
        self.view.Sol_PSU_State.clicked.connect(self.handle_Sol_PSU_State)
        self.view.bsol_stepsize.valueChanged.connect(self.handle_bsol_step)
        self.view.sol_stepsize.valueChanged.connect(self.handle_sol_step)
        self.view.bsol_seti.valueChanged.connect(self.handle_bsol_seti)
        self.view.sol_seti.valueChanged.connect(self.handle_sol_seti)

        tip_text = "min = {}\nmax = {}".format(self.procedure.min_sol,self.procedure.max_sol)

        self.view.sol_seti.setToolTip(tip_text)

        tip_text = "min = {}\nmax = {}".format(self.procedure.min_bsol,self.procedure.max_bsol)
        self.view.bsol_seti.setToolTip(tip_text)



        self.handle_bsol_step()
        self.handle_sol_step()

    def handle_BSol_PSU_State(self):
        print(__name__," handle_BSol_PSU_State")
        control.procedure.toggle_psu("bsol")

    def handle_Sol_PSU_State(self):
        print(__name__," handle_Sol_PSU_State")
        control.procedure.toggle_psu("sol")

    def handle_sol_step(self):
        print(__name__," handle_sol_step, ",self.view.sol_stepsize.value())
        self.view.sol_seti.setSingleStep(self.view.sol_stepsize.value())
        print("sol_seti step = ", self.view.sol_seti.singleStep())


    def handle_bsol_step(self):
        print(__name__," handle_bsol_step, ",self.view.bsol_stepsize.value())
        self.view.bsol_seti.setSingleStep(self.view.bsol_stepsize.value())
        print("bsol_seti step = ", self.view.bsol_seti.value())

    def handle_bsol_seti(self):
        print(__name__," handle_bsol_seti")
        if self.view.bsol_seti_has_focus:
            control.procedure.bsol_seti(self.view.bsol_seti.value())

        #self.view.sol_seti.setSingleStep(self.view.sol_stepsize.value())

    def handle_sol_seti(self):
        print(__name__," handle_sol_seti, ",self.view.sol_seti.value())
        if self.view.sol_seti_has_focus:
            control.procedure.sol_seti(self.view.sol_seti.value())


    def handle_degauss_sol_0(self):
        print(__name__," handle_degauss_sol_0")
        control.procedure.degauss("LRG-SOL", to_zero=True)


    def handle_degauss_bsol_0(self):
        print(__name__," handle_degauss_bsol_0")
        control.procedure.degauss("LRG-BSOL", to_zero=True)

    def handle_degauss_sol(self):
        print(__name__," handle_degauss_sol")
        control.procedure.degauss("LRG-SOL", to_zero=False)


    def handle_degauss_bsol(self):
        print(__name__," handle_degauss_bsol")
        control.procedure.degauss("LRG-BSOL", to_zero=False)

    def start_gui_update(self):
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(100)

    def update_gui(self):
        '''
            generic function that updates values from the procedure and then updates the gui
        '''
        control.procedure.update_data()
        control.view.update_gui()
        #print('update_gui')
        QApplication.processEvents()




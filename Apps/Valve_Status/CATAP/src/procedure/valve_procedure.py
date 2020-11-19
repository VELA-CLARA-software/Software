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
//  Last edit:   16-11-2020
//  FileName:    valve status valve_procedure.oy
//  Description: Procedure for simple valve status app
//
//*/
'''
import sys
sys.path.append('\\\\claraserv3\\claranet\\test\\CATAP\\bin\\')
sys.path.append('\\\\claraserv3.dl.ac.uk\\claranet\\test\\CATAP\\bin\\')
from CATAP.HardwareFactory import *


class valve_procedure(object):
    '''
        A procedure class. This class is the 'model' in teh Model-View_controle paradigm.  it
        instantiates and interfaces to  the CATAP valve factory from which you can interrogate
        the valves status and send commands to the valves.
        Commands flow from the gui -> control -> procedure
        The control class owns this class.
        All functions in this lcass shoudl be called externally
        This class knows NOTHING about the view, its is completely independent  of the view for
        this app. This means this procedures can be re-used with a different gui with no refactoring
        (maybe only extensioms, maybe  done with inheritance).
        There is very little error checking in this class. For example, if you pass in a valve
        name that does not exist things may nto work as expected. See CATAP docs for more info.
    '''
    #  create a hardware factory for PHYSICAL CLARA
    HF = HardwareFactory(STATE.PHYSICAL)
    # diaable messages
    HF.messagesOff()
    HF.debugMessagesOff()
    # create valve factor
    vv = HF.getValveFactory()
    # get names of all valves in valvefactory
    valve_names = vv.getAllValveNames()
    # empty dict to store latest state in
    valve_states = {}

    def __init__(self):
        print(__name__ + ', class initialized')

    def update_states(self):
        '''
            Get the state for each valve in valve_names. Called externally (e.g. control) to
            update states
        '''
        for name in valve_procedure.valve_names:
            valve_procedure.valve_states[name] = valve_procedure.vv.getValveState(name)


    def open_or_close(self,name):
        '''
            Toggle a avle to open or close
        :param name: name of valve to open
        '''
        if valve_procedure.valve_states[name] == STATE.VALVE_OPEN:
            self.close(name)
        elif valve_procedure.valve_states[name] == STATE.VALVE_CLOSED:
            self.open(name)

    def open(self, name):
        '''
            open a valve by its name
        :param name: name of valve to open
        '''
        valve_procedure.vv.open(name)

    def close(self, name):
        '''
            close a valve by its name
        :param name: name of valve to open
        '''
        valve_procedure.vv.close(name)

    def open_all(self):
        '''
            open all valves in valvefactory
        '''
        for name in valve_procedure.valve_names:
            valve_procedure.vv.open(name)

    def close_all(self):
        '''
            clas  all valves in valvefactory
        '''
        for name in valve_procedure.valve_names:
            valve_procedure.vv.close(name)
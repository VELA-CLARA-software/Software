#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
/*
//              This file is part of VELA-CLARA-Software.                             //
//------------------------------------------------------------------------------------//
//    VELA-CLARA-Software is free software: you can redistribute it and/or modify  //
//    it under the terms of the GNU General Public License as published by            //
//    the Free Software Foundation, either version 3 of the License, or               //
//    (at your option) any later version.                                             //
//    VELA-CLARA-Controllers is distributed in the hope that it will be useful,       //
//    but WITHOUT ANY WARRANTY; without even the implied warranty of                  //
//    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the                   //
//    GNU General Public License for more details.                                    //
//                                                                                    //
//    You should have received a copy of the GNU General Public License               //
//    along with VELA-CLARA-Software.  If not, see <http://www.gnu.org/licenses/>.    //
//
//  Author:      DJS
//  Last edit:   03-07-2018
//  FileName:    state.py
//  Description: enum state class, https://docs.python.org/3/library/enum.html
//
//
//*/
'''
from enum import Enum, unique


@unique
class state(Enum):
    '''
        flags states for different monitors
    '''
    BAD = 0
    GOOD = 1
    UNKNOWN = 2
    INIT = 3
    NEW_BAD = 4
    NEW_GOOD = 5
    TIMING = 6
    ERROR = 7
    INTERLOCK = 8
    STANDBY = 9

    statename = { BAD: 'BAD', GOOD: 'GOOD', UNKNOWN:'UNKNOWN', INIT:'INIT', NEW_BAD:'NEW_BAD',NEW_GOOD:'NEW_GOOD',
                  TIMING:'TIMING', ERROR: 'ERROR', INTERLOCK:'INTERLOCK', STANDBY:'STANDBY'}


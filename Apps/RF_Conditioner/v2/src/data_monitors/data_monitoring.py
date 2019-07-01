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
//  FileName:    data_monitoring.py
//  Description: The hardware_control_hub, creates and holds all CATAP hardware controllers,
//                they get passed to where they are needed
//
//*/
'''

from VELA_CLARA_enums import MACHINE_MODE
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_enums import CONTROLLER_TYPE
from VELA_CLARA_LLRF_Control import LLRF_TYPE
import VELA_CLARA_LLRF_Control
import VELA_CLARA_Vac_Valve_Control
import VELA_CLARA_RF_Modulator_Control
import VELA_CLARA_RF_Protection_Control
import VELA_CLARA_Magnet_Control
import VELA_CLARA_General_Monitor
import subprocess
from collections import defaultdict

from src.data import config
from src.data import rf_conditioning_logger


class data_monitoring(object):
    """
    This class creates and holds all the data monitoring classes
    """



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
//    You should have received a copy of the GNU General Public License               //(*x value that gives a certain percentage of power required*)
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

    statename = {BAD: 'BAD', GOOD: 'GOOD', UNKNOWN: 'UNKNOWN', INIT: 'INIT', NEW_BAD: 'NEW_BAD', NEW_GOOD: 'NEW_GOOD', TIMING: 'TIMING',
                 ERROR: 'ERROR', INTERLOCK: 'INTERLOCK', STANDBY: 'STANDBY'}


def is_good_or_new_good(s):
    if s == state.GOOD:
        return True
    if s == state.NEW_GOOD:
        return True
    return False

def is_bad_or_new_bad(s):
    if s == state.BAD:
        return True
    if s == state.NEW_BAD:
        return True
    return False


def is_new_good(snew, sold):
    '''
        checks to see if snew is a new_good (verbose, and by going through different outcomes)
    '''
    if snew == state.GOOD:
        if sold == state.GOOD:
            return False
        if sold == state.NEW_GOOD:
            return False
        return True
    return False

def is_new_bad(snew, sold):
    '''
        compares new state to old state, and returns new_bad if  old != bad
    '''
    if snew == state.BAD:
        if sold == state.BAD:
            return False
        if sold == state.NEW_BAD:
            return False
        return True
    return False

def compare_states(snew, sold):
    if is_new_good(snew, sold):
        return state.NEW_GOOD
    elif is_new_bad(snew, sold):
        return state.NEW_BAD
    return snew



@unique
class ramp_method(Enum):
    '''
        flags states for different monitors
        DEFAULT__TOO_FEW_BINS: Default amp_sp increase used. The TOTAL number of bins with amp_sp less than current amp_sp is < num_sp_to_fit + 1
        DEFAULT__ENOUGH_BINS__ZERO_IN_LIST__NOT_ENOUGH_NON_ZERO: Default amp_sp increase used. There are not enough non-zero bins to satisfy num_sp_to_fit + 1
        FIT__ENOUGH_BINS__ZERO_IN_LIST__ENOUGH_NON_ZERO: Fitting function engaged. Zero(s) in list so used the highest value non-zero amp_sp bins to fit
        FIT_ENOUGH_BINS__ALL_NON_ZERO: Fitting function engaged. Enough bins and they are all non-zero, so use the previous num_sp_to_fit + 1 to use with
                                       the fitting function.
    '''
    UNKNOWN = 0
    DEFAULT__TOO_FEW_BINS = 1
    DEFAULT__ENOUGH_BINS__ZERO_IN_LIST__NOT_ENOUGH_NON_ZERO = 2
    PREDICTED_SP_GRTRTHN_CURRENT_SP = 3
    DEFAULT__DELTA_GTRTHN_MAX = 4
    PREDICTED_SP_LSSTHN_CURRENT_SP = 5
    DEFAULT__NEG_RAMP = 6
    DEFAULT__FLAT_RAMP = 7
    FIT = 8



    # others include: but the new sp  was too big, etc ...
    statename = {UNKNOWN: 'UNKNOWN', DEFAULT__TOO_FEW_BINS: 'DEFAULT__TOO_FEW_BINS', DEFAULT__ENOUGH_BINS__ZERO_IN_LIST__NOT_ENOUGH_NON_ZERO:
        'DEFAULT__ENOUGH_BINS__ZERO_IN_LIST__NOT_ENOUGH_NON_ZERO', PREDICTED_SP_LSSTHN_CURRENT_SP: 'PREDICTED_SP_LSSTHN_CURRENT_SP',
        DEFAULT__DELTA_GTRTHN_MAX:'DEFAULT__DELTA_GTRTHN_MAX', PREDICTED_SP_GRTRTHN_CURRENT_SP: 'PREDICTED_SP_GRTRTHN_CURRENT_SP',
        DEFAULT__NEG_RAMP: 'DEFAULT__NEG_RAMP', DEFAULT__FLAT_RAMP: 'DEFAULT__FLAT_RAMP',FIT: 'FIT'}



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
//  Last edit:   27-06-2019
//  FileName:    config.py
//  Description: The config reader for RF Conditioning VERSION 2.0
//
//*/
'''
import yaml
from collections import defaultdict
# Future warning:
# CATAP 2.0 is probably going to put all these into a general enum name space to be included first
from VELA_CLARA_enums import MACHINE_AREA
from VELA_CLARA_LLRF_Control import LLRF_TYPE
from VELA_CLARA_RF_Protection_Control import RF_PROT_TYPE
import sys


class config(object):
    '''
    This class reads in the configuration file(yaml) and then puts the information in various
    static dictionaries for each hardware type, these dictionaries are used by the different
    classes in the programme to configure conditioning
    It fairly obvious, non-standard things are:
    the general_monitoring parameters, defined at run-time, so have to be searached for
    The traces to monitor are checked for "full names" as used in CATAP
    moar static variables are defined at the end of this class definition
    '''
    # whoami
    my_name = 'rf_conditioning_config'
    #
    have_config = False
    _config_file = None
    #
    llrf_type = LLRF_TYPE.UNKNOWN_TYPE
    raw_config_data = None
    raw_config_read = False
    # see end for more static variables

    # useful dictionaries, with default values or unknown keys
    # TODO:  maybe put these in a generic utilities space
    get_llrf_type = {"CLARA_HRRG": LLRF_TYPE.CLARA_HRRG, "CLARA_LRRG": LLRF_TYPE.CLARA_LRRG,
                     "VELA_HRRG": LLRF_TYPE.VELA_HRRG, "VELA_LRRG": LLRF_TYPE.VELA_LRRG,
                     "L01": LLRF_TYPE.L01 }
    get_llrf_type = defaultdict(lambda: LLRF_TYPE.UNKNOWN_TYPE, get_llrf_type)

    # TODO:  maybe put these in a generic utilities space
    get_rf_prot_type = {"CLARA_HRRG": RF_PROT_TYPE.CLARA_HRRG,
                        "CLARA_LRRG": RF_PROT_TYPE.CLARA_LRRG,
                        "VELA_HRRG": RF_PROT_TYPE.VELA_HRRG,
                        "VELA_LRRG": RF_PROT_TYPE.VELA_LRRG, "L01": RF_PROT_TYPE.L01,
                        LLRF_TYPE.CLARA_HRRG: RF_PROT_TYPE.CLARA_HRRG,
                        LLRF_TYPE.CLARA_LRRG: RF_PROT_TYPE.CLARA_LRRG,
                        LLRF_TYPE.VELA_HRRG: RF_PROT_TYPE.VELA_HRRG,
                        LLRF_TYPE.VELA_LRRG: RF_PROT_TYPE.VELA_LRRG,
                        LLRF_TYPE.L01: RF_PROT_TYPE.L01}
    get_rf_prot_type = defaultdict(lambda: RF_PROT_TYPE.NOT_KNOWN, get_rf_prot_type)

    get_machine_area = {'S01': MACHINE_AREA.CLARA_S01, 'VELA_INJ': MACHINE_AREA.VELA_INJ,
        'ALL_VELA_CLARA': MACHINE_AREA.ALL_VELA_CLARA, 'CLARA_PH1': MACHINE_AREA.CLARA_PH1, }
    get_machine_area = defaultdict(lambda: MACHINE_AREA.UNKNOWN_AREA, get_machine_area)


    def __init__(self):
        pass

    # get and set the config file
    @property
    def config_file(self):
        return config._config_file

    @config_file.setter
    def config_file(self, value):
        config._config_file = value

    def read_config(self):
        '''
        reads in the config file and places items in static config dictionary
        :return: success or failure
        '''
        try:
            with open(config._config_file) as f:
                # use safe_load instead load
                config.raw_config_data = yaml.safe_load(f)
            config.raw_config_read = True
            # add config filename to raw_config_data
            config.raw_config_data[config.CONFIG_FILE] = config._config_file

        except Exception:
            print("ERROR Failed To Read " + config._config_file + " suspect YAML formatting error")
            raise
        # if config.raw_config_data:
        #     print('Raw Config Data')
        #     for item in config.raw_config_data.iteritems():
        #         print item
        # else:
        #     print('Raw Config Data not Found')

        '''
        parse the config dictionary into individual dictionaries for main components of the
        application. This may not actually be necessary (!) In theory we could live with one 
        giant dictionary, 
        '''
        config.vac_config = self.split_raw_config(config.vac_keywords)
        config.DC_config = self.split_raw_config(config.dc_keywords)
        config.log_config = self.split_raw_config(config.log_keywords)
        config.vac_valve_config = self.split_raw_config(config.vac_valve_keywords)
        config.water_temp_config = self.split_raw_config(config.water_temp_keywords)
        config.cavity_temp_config = self.split_raw_config(config.cavity_temp_keywords)
        config.llrf_config = self.split_raw_config(config.llrf_keywords)
        config.breakdown_config = self.split_raw_config(config.breakdown_keywords)
        config.mod_config = self.split_raw_config(config.modulator_keywords)
        config.rfprot_config = self.split_raw_config(config.rfprot_keywords)
        config.gui_config = self.split_raw_config(config.gui_keywords)
        config.sol_config = self.split_raw_config(config.solenoid_keywords)

        # general monitor parameters are unknown at run time, we must search for them
        self.find_general_monitor_parameter()
        config.monitor_config = self.split_raw_config(config.gmonitor_keywords)

        # run final sanity checks and return result
        return self.sanity_checks()

    def split_raw_config(self, keywords):
        '''
        returns a dictionary of elements from config filled with keywords
        :return: new dictionary with keywords in config that match passed keywords or None
        '''
        return_dictionary = {}
        # Check if the KEYWORDS DEFINED IN THIS CLASS EXIST IN THE CONFIG
        try:
            for word in keywords:
                if word in config.raw_config_data:
                    return_dictionary[word] = config.raw_config_data[word]
                else:
                    raise NameError("Error, Config file missing keyword = " + word)
        except Exception:
            # yep, we force a crash if a keyword is not found
            raise
        if len(return_dictionary) > 0:
            return return_dictionary
        else:
            return None

    def find_general_monitor_parameter(self):
        """
        this picks up any extra PVs that are logged to file, but NOT displayed to the MAIN GUI it's
        going to look for any keys in the config that have the suffix given by the value for
        keyword = 'GMON_SUFFIX'  (TYPICALLY THIS SHOULD BE '_GMON', but i made it a variable)
        GMON_SUFFIX is one of the few hardcoded keywords that does not need to be used in the
        config file. IF NO GMON is configured, we need to know that
        :return: no return
        """
        # get the suffix, and iterate over all keywords in raw_config_data, looking for a matching
        # suffix, adding that keyword (with the suffix removed) to raw_config_data AND monitor_config
        general_monSuffix = config.raw_config_data.get(config.GMON_SUFFIX, None)
        if general_monSuffix:
            for key, value in config.raw_config_data.iteritems():
                if key.endswith(general_monSuffix):
                    if config.monitor_config == None:
                        config.monitor_config = {}
                    config.monitor_config[key.replace(general_monSuffix, '')] = value
            for key, value in config.monitor_config.iteritems():
                config.raw_config_data[key] = value
        else:
            print('WARNING GMON_SUFFIX not found in config file ')

    def which_cavity(self, trace):
        if self.llrf_type == LLRF_TYPE.CLARA_HRRG:
            return trace.replace("CAVITY", "CAVITY")
        elif self.llrf_type == LLRF_TYPE.CLARA_LRRG:
            return trace.replace("CAVITY", "CAVITY")
        elif self.llrf_type == LLRF_TYPE.VELA_LRRG:
            return trace.replace("CAVITY", "CAVITY")
        elif self.llrf_type == LLRF_TYPE.VELA_HRRG:
            return trace.replace("CAVITY", "CAVITY")
        elif self.llrf_type == LLRF_TYPE.L01:
            return trace.replace("CAVITY", "L01_CAVITY")
        else:
            return "error"

    """not used since """
    # def get_traces_to_monitor(self, traces_to_monitor):
    #     """
    #     Since we updated the LLRF and now have all traces in a single array (PV) we now always
    #     monitor everything
    #     :param traces_to_monitor: Trace specified in config file
    #     :return: the CATAP name of the traces to monitor
    #     """
    #     # print 'get_traces_to_monitor'
    #     traces = []
    #     for trace in traces_to_monitor.split(','):
    #         if "CAVITY" in trace and "PROBE" not in trace:  # MAGIC_STRING
    #             traces.append(self.which_cavity(trace))
    #         else:
    #             traces.append(trace)  # print('NEW TRACE To Monitor',traces[-1])
    #     return traces

    def sanity_checks(self):
        """
        perform any sanity checks on the config data here, failing sanity checks should terminate
        the application
        his is uglyaf must be a more elegant way to refactor this cancer
        :return: config.have_config
        """
        # print all data (pass to logger)
        for key, value in config.all_config.iteritems():
            if value:
                for key2, value2 in value.iteritems():
                    print(key2, value2)
        # We NEED an RF Structure type
        try:
            config.llrf_type = config.get_llrf_type[config.raw_config_data[config.RF_STRUCTURE]]
            if config.llrf_type != LLRF_TYPE.UNKNOWN_TYPE:
                pass
            else:
                raise NameError("Error, config entry RF_STRUCTURE " + config.raw_config_data[
                    config.RF_STRUCTURE] + " is unknown")
            # use the CATAP type instead of string
            config.raw_config_data[config.RF_STRUCTURE] = config.llrf_type
            valve_area = config.get_machine_area[config.raw_config_data[config.VAC_VALVE_AREA]]
            if valve_area != MACHINE_AREA.UNKNOWN_AREA:
                # use the CATAp type instead of string
                config.raw_config_data[config.VAC_VALVE_AREA] = valve_area
            else:
                raise NameError("Error, config entry VAC_VALVE_AREA = " + config.raw_config_data[
                    config.VAC_VALVE_AREA] + " is unknown")
            magnet_area = config.get_machine_area[config.raw_config_data[
                                                      config.MAGNET_MACHINE_AREA]]
            if magnet_area != MACHINE_AREA.UNKNOWN_AREA:
                # use the CATAp type instead of string
                config.raw_config_data[config.MAGNET_MACHINE_AREA] = magnet_area
            else:
                raise NameError("Error, config entry MAGNET_MACHINE_AREA " + config.raw_config_data[
                    config.MAGNET_MACHINE_AREA] + " is unknown")
        except Exception:
                raise




        # CHECK TH EVERACITY OF THE CONFIG FILE - SOMEHOW

        # WE ONLY CHECK THE

        num_keywords_found = len(config.DC_config) + \
        len(config.log_config) + \
        len(config.vac_config) + \
        len(config.vac_valve_config ) + \
        len(config.water_temp_config ) + \
        len(config.cavity_temp_config)  +\
        len(config.llrf_config ) + \
        len(config.breakdown_config) +\
        len(config.mod_config ) + \
        len(config.rfprot_config)  +\
        len(config.gui_config)  + \
        len(config.sol_config)  + \
        len(config.monitor_config)

        print(num_keywords_found, len(config.raw_config_data))

        # HERE we check if the keywords in the config file are as expected
        bad_keys = []
        for key in config.raw_config_data.keys():
            print("Checking: ",key)
            # If the key is Defined in all_config_keywords good,
            if key in config.all_config_keywords:
                print(key, " expected")
            # If the key is a _GMON key, then good (these are designed to be configurable from
            # the config file
            elif "_GMON" in key:
                print(key, " pass")
            # otherwise there MUST be an ERROR so stop
            else:
                bad_keys.append(key)

        # try:
        #     if len(bad_keys) == 0:
        #         pass
        #     else:
        #         bad_key_string = ", ".join(bad_keys)
        #         raise NameError("!!ERROR!! Unexpected key(s) found in config file (",
        #                         config.config_file, "), KEY(S) = " + bad_key_string)
        # except Exception:
        #     raise
        # TODO:  add in more exceptions for cross checking data-types
        #
        # so far ...  no sanity check!
        config.have_config = True
        return config.have_config

    # TODO: we KNOW all the possible values that keywords can take and should check them

    # The below variables are static,
    # They are defined at the bottom of the file to keep them out the way
    #

    """
    The Config FILE MUST contain the same keywords that are given below
    Adding extra keywords is easy, but must happen 
    them
    
    """
    # TODO: get rid of all the sperate configs and just have one mega-config for all
    # a global MODE that can be set to DEBUG or OPERTAIONAL

    MODE = 'MODE'

    ## Config File Keyword Defintitions
    MINIMUM_COOLDOWN_TIME = 'MINIMUM_COOLDOWN_TIME'

    # vacuum keywords
    VAC_NUM_SAMPLES_TO_AVERAGE = 'VAC_NUM_SAMPLES_TO_AVERAGE'
    VAC_ROLLING_SUM_NUM_SAMPLES = 'VAC_ROLLING_SUM_NUM_SAMPLES'
    VAC_SPIKE_DECAY_LEVEL = 'VAC_SPIKE_DECAY_LEVEL'
    VAC_SPIKE_DECAY_TIME = 'VAC_SPIKE_DECAY_TIME'
    VAC_SHOULD_DROP_AMP = 'VAC_SHOULD_DROP_AMP'
    VAC_SPIKE_DROP_AMP = 'VAC_SPIKE_DROP_AMP'
    WHEN_VAC_HI_DISABLE_RAMP = 'WHEN_VAC_HI_DISABLE_RAMP'
    VAC_SPIKE_DELTA = 'VAC_SPIKE_DELTA'
    VAC_DECAY_MODE = 'VAC_DECAY_MODE'
    VAC_CHECK_TIME = 'VAC_CHECK_TIME'
    VAC_MAX_LEVEL = 'VAC_MAX_LEVEL'
    VAC_PV = 'VAC_PV'
    vac_keywords = [WHEN_VAC_HI_DISABLE_RAMP,VAC_NUM_SAMPLES_TO_AVERAGE, VAC_SPIKE_DECAY_LEVEL,
                    VAC_SPIKE_DECAY_TIME,VAC_ROLLING_SUM_NUM_SAMPLES,
                    VAC_SHOULD_DROP_AMP, VAC_SPIKE_DROP_AMP,  # VAC_MAX_AMP_DROP,
                    VAC_SPIKE_DELTA, VAC_CHECK_TIME, VAC_DECAY_MODE, VAC_MAX_LEVEL, VAC_PV,
                    MINIMUM_COOLDOWN_TIME]

    DC_PV = 'DC_PV'
    DC_DECAY_MODE = 'DC_DECAY_MODE'
    DC_SPIKE_DECAY_LEVEL = 'DC_SPIKE_DECAY_LEVEL'
    DC_SPIKE_DELTA = 'DC_SPIKE_DELTA'
    DC_SPIKE_DROP_AMP = 'DC_SPIKE_DROP_AMP'
    DC_NUM_SAMPLES_TO_AVERAGE = 'DC_NUM_SAMPLES_TO_AVERAGE'
    DC_SPIKE_DECAY_TIME = 'DC_SPIKE_DECAY_TIME'
    DC_CHECK_TIME = 'DC_CHECK_TIME'
    #OUTSIDE_MASK_COOLDOWN_TIME = 'OUTSIDE_MASK_COOLDOWN_TIME'
    DC_SHOULD_DROP_AMP = 'DC_SHOULD_DROP_AMP'
    dc_keywords = [DC_PV, DC_DECAY_MODE, DC_SPIKE_DECAY_LEVEL, DC_SPIKE_DELTA, DC_SPIKE_DROP_AMP,
                   DC_NUM_SAMPLES_TO_AVERAGE, DC_SPIKE_DECAY_TIME, DC_CHECK_TIME,
                    DC_SHOULD_DROP_AMP]

    # data-logging parameters
    CONFIG_FILE = 'CONFIG_FILE'
    TEXT_LOG_FILENAME = 'TEXT_LOG_FILENAME'
    LOG_DIRECTORY = 'LOG_DIRECTORY'
    BINARY_DATA_LOG_FILENAME = 'BINARY_DATA_LOG_FILENAME'
    OUTSIDE_MASK_FORWARD_FILENAME = 'OUTSIDE_MASK_FORWARD_FILENAME'
    OUTSIDE_MASK_REVERSE_FILENAME = 'OUTSIDE_MASK_REVERSE_FILENAME'
    OUTSIDE_MASK_PROBE_FILENAME = 'OUTSIDE_MASK_PROBE_FILENAME'
    PULSE_COUNT_BREAKDOWN_LOG_FILENAME = 'PULSE_COUNT_BREAKDOWN_LOG_FILENAME'
    KFPOW_AMPSP_RUNNING_STATS_LOG_FILENAME = 'KFPOW_AMPSP_RUNNING_STATS_LOG_FILENAME'
    BINARY_DATA_LOG_TIME = 'BINARY_DATA_LOG_TIME'
    AMP_PWR_LOG_TIME = 'AMP_PWR_LOG_TIME'
    log_keywords = [TEXT_LOG_FILENAME, LOG_DIRECTORY, BINARY_DATA_LOG_FILENAME, OUTSIDE_MASK_FORWARD_FILENAME, OUTSIDE_MASK_REVERSE_FILENAME,
                    OUTSIDE_MASK_PROBE_FILENAME, PULSE_COUNT_BREAKDOWN_LOG_FILENAME, PULSE_COUNT_BREAKDOWN_LOG_FILENAME,
                    KFPOW_AMPSP_RUNNING_STATS_LOG_FILENAME, BINARY_DATA_LOG_TIME, AMP_PWR_LOG_TIME]
    #
    # vac_valve_parameter(self):
    VAC_VALVE = 'VAC_VALVE'
    VAC_VALVE_AREA = 'VAC_VALVE_AREA'
    VAC_VALVE_CHECK_TIME = 'VAC_VALVE_CHECK_TIME'
    KEEP_VALVE_OPEN = 'KEEP_VALVE_OPEN'
    vac_valve_keywords = [VAC_VALVE, VAC_VALVE_AREA, VAC_VALVE_CHECK_TIME, KEEP_VALVE_OPEN]
    #
    # water temp keywords
    WATER_TEMPERATURE_PV_COUNT = 'WATER_TEMPERATURE_PV_COUNT'
    WATER_TEMPERATURE_PV = 'WATER_TEMPERATURE_PV'
    WATER_TEMPERATURE_CHECK_TIME = 'WATER_TEMPERATURE_CHECK_TIME'
    water_temp_keywords = [WATER_TEMPERATURE_PV, WATER_TEMPERATURE_CHECK_TIME, WATER_TEMPERATURE_PV_COUNT]
    #
    # cavity temp keywords
    CAVITY_TEMPERATURE_PV_COUNT = 'CAVITY_TEMPERATURE_PV_COUNT'
    CAVITY_TEMPERATURE_PV = 'CAVITY_TEMPERATURE_PV'
    CAVITY_TEMPERATURE_CHECK_TIME = 'CAVITY_TEMPERATURE_CHECK_TIME'
    cavity_temp_keywords = [CAVITY_TEMPERATURE_PV, CAVITY_TEMPERATURE_CHECK_TIME, CAVITY_TEMPERATURE_PV_COUNT]
    #
    # solenoid keywords
    MAGNET_MACHINE_AREA = 'MAGNET_MACHINE_AREA'
    SOL_NAMES = 'SOL_NAMES'
    SOL_COUNT = 'SOL_COUNT'
    SOL_CHECK_TIME = 'SOL_CHECK_TIME'
    SHOULD_SOL_WOBBLE = 'SHOULD_SOL_WOBBLE'
    SOL_WOBBLE_HI = 'SOL_WOBBLE_HI'
    SOL_WOBBLE_LO = 'SOL_WOBBLE_LO'
    SOL_WOBBLE_OSCILLATION_TIME = 'SOL_WOBBLE_OSCILLATION_TIME'
    SOL_WOBBLE_OSCILLATION_POINTS = 'SOL_WOBBLE_OSCILLATION_POINTS'
    solenoid_keywords = [MAGNET_MACHINE_AREA, SOL_NAMES, SOL_CHECK_TIME, SHOULD_SOL_WOBBLE,
                         SOL_WOBBLE_HI, SOL_WOBBLE_LO,SOL_COUNT,
                         SOL_WOBBLE_OSCILLATION_TIME,SOL_WOBBLE_OSCILLATION_POINTS]
    #
    # llrf keywords
    RF_STRUCTURE = 'RF_STRUCTURE'
    # TIME_BETWEEN_RF_INCREASES = 'TIME_BETWEEN_RF_INCREASES'
    DEFAULT_RF_INCREASE_LEVEL = 'DEFAULT_RF_INCREASE_LEVEL'
    RF_REPETITION_RATE = 'RF_REPETITION_RATE'
    RF_REPETITION_RATE_ERROR = 'RF_REPETITION_RATE_ERROR'
    BREAKDOWN_RATE_AIM = 'BREAKDOWN_RATE_AIM'
    LLRF_CHECK_TIME = 'LLRF_CHECK_TIME'
    # NORMAL_POWER_INCREASE = 'NORMAL_POWER_INCREASE'
    # LOW_POWER_INCREASE = 'LOW_POWER_INCREASE'
    # LOW_POWER_INCREASE_RATE_LIMIT = 'LOW_POWER_INCREASE_RATE_LIMIT'
    NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY = 'NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY'
    VAC_SPIKE_TRACES_TO_SAVE = 'VAC_SPIKE_TRACES_TO_SAVE'
    EXTRA_TRACES_ON_BREAKDOWN = 'EXTRA_TRACES_ON_BREAKDOWN'
    NUM_BUFFER_TRACES = 'NUM_BUFFER_TRACES'
    DEFAULT_PULSE_COUNT = 'DEFAULT_PULSE_COUNT'
    MAX_DELTA_AMP_SP = 'MAX_DELTA_AMP_SP'
    NUM_SET_POINTS_TO_FIT = 'NUM_SET_POINTS_TO_FIT'
    TRACES_TO_SAVE = 'TRACES_TO_SAVE'
    MEAN_TRACES = 'MEAN_TRACES'
    # MEAN_TIME_TO_AVERAGE = 'MEAN_TIME_TO_AVERAGE'
    # RF_INCREASE_LEVEL = 'RF_INCREASE_LEVEL'
    # RF_INCREASE_RATE = 'RF_INCREASE_RATE'
    # POWER_AIM = 'POWER_AIM'
    PULSE_LENGTH = 'PULSE_LENGTH'
    PULSE_LENGTH_ERROR = 'PULSE_LENGTH_ERROR'
    KLY_PWR_FOR_ACTIVE_PULSE = 'KLY_PWR_FOR_ACTIVE_PULSE'
    KFPOW_MEAN_START = 'KFPOW_MEAN_START'
    KFPOW_MEAN_END = 'KFPOW_MEAN_END'
    KRPOW_MEAN_START = 'KRPOW_MEAN_START'
    KRPOW_MEAN_END = 'KRPOW_MEAN_END'
    KFPHA_MEAN_START = 'KFPHA_MEAN_START'
    KFPHA_MEAN_END = 'KFPHA_MEAN_END'
    KRPHA_MEAN_START = 'KRPHA_MEAN_START'
    KRPHA_MEAN_END = 'KRPHA_MEAN_END'
    CFPOW_MEAN_START = 'CFPOW_MEAN_START'
    CFPOW_MEAN_END = 'CFPOW_MEAN_END'
    CPPOW_MEAN_START = 'CPPOW_MEAN_START'
    CPPOW_MEAN_END = 'CPPOW_MEAN_END'
    CRPOW_MEAN_START = 'CRPOW_MEAN_START'
    CRPOW_MEAN_END = 'CRPOW_MEAN_END'
    CFPHA_MEAN_START = 'CFPHA_MEAN_START'
    CFPHA_MEAN_END = 'CFPHA_MEAN_END'
    CRPHA_MEAN_START = 'CRPHA_MEAN_START'
    CRPHA_MEAN_END = 'CRPHA_MEAN_END'
    CPPHA_MEAN_START = 'CPPHA_MEAN_START'
    CPPHA_MEAN_END = 'CPPHA_MEAN_END'
    llrf_keywords = [RF_STRUCTURE, DEFAULT_RF_INCREASE_LEVEL, RF_REPETITION_RATE,
                     RF_REPETITION_RATE_ERROR, BREAKDOWN_RATE_AIM, LLRF_CHECK_TIME,
                     # LOW_POWER_INCREASE,
                     # LOW_POWER_INCREASE_RATE_LIMIT,
                     NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY, VAC_SPIKE_TRACES_TO_SAVE,
                     EXTRA_TRACES_ON_BREAKDOWN, NUM_BUFFER_TRACES, DEFAULT_PULSE_COUNT,
                     MAX_DELTA_AMP_SP, NUM_SET_POINTS_TO_FIT, TRACES_TO_SAVE, MEAN_TRACES,
                     # MEAN_TIME_TO_AVERAGE,
                     # RF_INCREASE_LEVEL,
                     # RF_INCREASE_RATE,
                     # POWER_AIM,
                     # THESE WILL BE USED FOR CHECKING THE PULSE LENGTH, AND, MAYBE ONE DAY
                     # CHANGING IT AUTOMATICALLY
                     PULSE_LENGTH,
                     PULSE_LENGTH_ERROR,
                     KLY_PWR_FOR_ACTIVE_PULSE, KFPOW_MEAN_START, KFPOW_MEAN_END, KRPOW_MEAN_START,
                     KRPOW_MEAN_END, KFPHA_MEAN_START, KFPHA_MEAN_END, KRPHA_MEAN_START,
                     KRPHA_MEAN_END, CFPOW_MEAN_START, CFPOW_MEAN_END, CRPOW_MEAN_START,
                     CRPOW_MEAN_END, CFPHA_MEAN_START, CFPHA_MEAN_END, CRPHA_MEAN_START,
                     CRPHA_MEAN_END, CPPHA_MEAN_START, CPPHA_MEAN_END,  # TIME_BETWEEN_RF_INCREASES
                     CPPOW_MEAN_START, CPPOW_MEAN_END
                     # NORMAL_POWER_INCREASE
                     ]
    #



    #OUTSIDE_MASK_COOLDOWN_TIME = 'OUTSIDE_MASK_COOLDOWN_TIME'

    # breakdown keywords
    CFPOW_AUTO_SET = 'CFPOW_AUTO_SET'
    CRPOW_AUTO_SET = 'CRPOW_AUTO_SET'
    CPPOW_AUTO_SET = 'CPPOW_AUTO_SET'
    KFPOW_AUTO_SET = 'KFPOW_AUTO_SET'
    KRPOW_AUTO_SET = 'KRPOW_AUTO_SET'
    CFPHA_AUTO_SET = 'CFPHA_AUTO_SET'
    CRPHA_AUTO_SET = 'CRPHA_AUTO_SET'
    CPPHA_AUTO_SET = 'CPPHA_AUTO_SET'
    KFPHA_AUTO_SET = 'KFPHA_AUTO_SET'
    KRPHA_AUTO_SET = 'KRPHA_AUTO_SET'
    CFPOW_DROP_AMP = 'CFPOW_DROP_AMP'
    CRPOW_DROP_AMP = 'CRPOW_DROP_AMP'
    CPPOW_DROP_AMP = 'CPPOW_DROP_AMP'
    KFPOW_DROP_AMP = 'KFPOW_DROP_AMP'
    KRPOW_DROP_AMP = 'KRPOW_DROP_AMP'
    CFPHA_DROP_AMP = 'CFPHA_DROP_AMP'
    CRPHA_DROP_AMP = 'CRPHA_DROP_AMP'
    CPPHA_DROP_AMP = 'CPPHA_DROP_AMP'
    KFPHA_DROP_AMP = 'KFPHA_DROP_AMP'
    KRPHA_DROP_AMP = 'KRPHA_DROP_AMP'
    BREAKDOWN_TRACES = 'BREAKDOWN_TRACES'
    VAC_SPIKE_TRACES_TO_SAVE = 'VAC_SPIKE_TRACES_TO_SAVE'
    CFPOW_MASK_ABS_MIN = 'CFPOW_MASK_ABS_MIN'
    CRPOW_MASK_ABS_MIN = 'CRPOW_MASK_ABS_MIN'
    CPPOW_MASK_ABS_MIN = 'CPPOW_MASK_ABS_MIN'
    KFPOW_MASK_ABS_MIN = 'KFPOW_MASK_ABS_MIN'
    KRPOW_MASK_ABS_MIN = 'KRPOW_MASK_ABS_MIN'
    CFPHA_MASK_ABS_MIN = 'CFPHA_MASK_ABS_MIN'
    CRPHA_MASK_ABS_MIN = 'CRPHA_MASK_ABS_MIN'
    CPPHA_MASK_ABS_MIN = 'CPPHA_MASK_ABS_MIN'
    KFPHA_MASK_ABS_MIN = 'KFPHA_MASK_ABS_MIN'
    KRPHA_MASK_ABS_MIN = 'KRPHA_MASK_ABS_MIN'
    CFPOW_MASK_LEVEL = 'CFPOW_MASK_LEVEL'
    CRPOW_MASK_LEVEL = 'CRPOW_MASK_LEVEL'
    CPPOW_MASK_LEVEL = 'CPPOW_MASK_LEVEL'
    KFPOW_MASK_LEVEL = 'KFPOW_MASK_LEVEL'
    KRPOW_MASK_LEVEL = 'KRPOW_MASK_LEVEL'
    CFPHA_MASK_LEVEL = 'CFPHA_MASK_LEVEL'
    CRPHA_MASK_LEVEL = 'CRPHA_MASK_LEVEL'
    CPPHA_MASK_LEVEL = 'CPPHA_MASK_LEVEL'
    KFPHA_MASK_LEVEL = 'KFPHA_MASK_LEVEL'
    KRPHA_MASK_LEVEL = 'KRPHA_MASK_LEVEL'
    CFPOW_CHECK_STREAK = 'CFPOW_CHECK_STREAK'
    CRPOW_CHECK_STREAK = 'CRPOW_CHECK_STREAK'
    CPPOW_CHECK_STREAK = 'CPPOW_CHECK_STREAK'
    KFPOW_CHECK_STREAK = 'KFPOW_CHECK_STREAK'
    KRPOW_CHECK_STREAK = 'KRPOW_CHECK_STREAK'
    CFPHA_CHECK_STREAK = 'CFPHA_CHECK_STREAK'
    CRPHA_CHECK_STREAK = 'CRPHA_CHECK_STREAK'
    CPPHA_CHECK_STREAK = 'CPPHA_CHECK_STREAK'
    KFPHA_CHECK_STREAK = 'KFPHA_CHECK_STREAK'
    KRPHA_CHECK_STREAK = 'KRPHA_CHECK_STREAK'
    CFPOW_MASK_FLOOR = 'CFPOW_MASK_FLOOR'
    CRPOW_MASK_FLOOR = 'CRPOW_MASK_FLOOR'
    CPPOW_MASK_FLOOR = 'CPPOW_MASK_FLOOR'
    KFPOW_MASK_FLOOR = 'KFPOW_MASK_FLOOR'
    KRPOW_MASK_FLOOR = 'KRPOW_MASK_FLOOR'
    CFPHA_MASK_FLOOR = 'CFPHA_MASK_FLOOR'
    CRPHA_MASK_FLOOR = 'CRPHA_MASK_FLOOR'
    CPPHA_MASK_FLOOR = 'CPPHA_MASK_FLOOR'
    KFPHA_MASK_FLOOR = 'KFPHA_MASK_FLOOR'
    KRPHA_MASK_FLOOR = 'KRPHA_MASK_FLOOR'
    CFPOW_NUM_AVERAGE_TRACES = 'CFPOW_NUM_AVERAGE_TRACES'
    CRPOW_NUM_AVERAGE_TRACES = 'CRPOW_NUM_AVERAGE_TRACES'
    CPPOW_NUM_AVERAGE_TRACES = 'CPPOW_NUM_AVERAGE_TRACES'
    KFPOW_NUM_AVERAGE_TRACES = 'KFPOW_NUM_AVERAGE_TRACES'
    KRPOW_NUM_AVERAGE_TRACES = 'KRPOW_NUM_AVERAGE_TRACES'
    CFPHA_NUM_AVERAGE_TRACES = 'CFPHA_NUM_AVERAGE_TRACES'
    CRPHA_NUM_AVERAGE_TRACES = 'CRPHA_NUM_AVERAGE_TRACES'
    CPPHA_NUM_AVERAGE_TRACES = 'CPPHA_NUM_AVERAGE_TRACES'
    KFPHA_NUM_AVERAGE_TRACES = 'KFPHA_NUM_AVERAGE_TRACES'
    KRPHA_NUM_AVERAGE_TRACES = 'KRPHA_NUM_AVERAGE_TRACES'
    CPPOW_DROP_AMP_VALUE = 'CPPOW_DROP_AMP_VALUE'
    KFPOW_DROP_AMP_VALUE = 'KFPOW_DROP_AMP_VALUE'
    CRPOW_DROP_AMP_VALUE = 'CRPOW_DROP_AMP_VALUE'
    KRPOW_DROP_AMP_VALUE = 'KRPOW_DROP_AMP_VALUE'
    CFPHA_DROP_AMP_VALUE = 'CFPHA_DROP_AMP_VALUE'
    CRPHA_DROP_AMP_VALUE = 'CRPHA_DROP_AMP_VALUE'
    CPPHA_DROP_AMP_VALUE = 'CPPHA_DROP_AMP_VALUE'
    CFPOW_DROP_AMP_VALUE = 'CFPOW_DROP_AMP_VALUE'
    KFPHA_DROP_AMP_VALUE = 'KFPHA_DROP_AMP_VALUE'
    KRPHA_DROP_AMP_VALUE = 'KRPHA_DROP_AMP_VALUE'
    OUTSIDE_MASK_CHECK_TIME = 'OUTSIDE_MASK_CHECK_TIME'
    #OUTSIDE_MASK_COOLDOWN_TIME = 'OUTSIDE_MASK_COOLDOWN_TIME'

    CFPOW_MASK_START = 'CFPOW_MASK_START'
    CRPOW_MASK_START = 'CRPOW_MASK_START'
    CPPOW_MASK_START = 'CPPOW_MASK_START'
    KFPOW_MASK_START = 'KFPOW_MASK_START'
    KRPOW_MASK_START = 'KRPOW_MASK_START'
    CRPHA_MASK_START = 'CRPHA_MASK_START'
    CPPHA_MASK_START = 'CPPHA_MASK_START'
    CFPHA_MASK_START = 'CFPHA_MASK_START'
    KFPHA_MASK_START = 'KFPHA_MASK_START'
    KRPHA_MASK_START = 'KRPHA_MASK_START'
    CFPOW_MASK_END = 'CFPOW_MASK_END'
    CRPOW_MASK_END = 'CRPOW_MASK_END'
    CPPOW_MASK_END = 'CPPOW_MASK_END'
    KFPOW_MASK_END = 'KFPOW_MASK_END'
    KRPOW_MASK_END = 'KRPOW_MASK_END'
    CFPHA_MASK_END = 'CFPHA_MASK_END'
    CRPHA_MASK_END = 'CRPHA_MASK_END'
    CPPHA_MASK_END = 'CPPHA_MASK_END'
    KFPHA_MASK_END = 'KFPHA_MASK_END'
    KRPHA_MASK_END = 'KRPHA_MASK_END'
    CFPOW_MASK_WINDOW_START = 'CFPOW_MASK_WINDOW_START'
    CRPOW_MASK_WINDOW_START = 'CRPOW_MASK_WINDOW_START'
    CPPOW_MASK_WINDOW_START = 'CPPOW_MASK_WINDOW_START'
    KFPOW_MASK_WINDOW_START = 'KFPOW_MASK_WINDOW_START'
    KRPOW_MASK_WINDOW_START = 'KRPOW_MASK_WINDOW_START'
    CFPHA_MASK_WINDOW_START = 'CFPHA_MASK_WINDOW_START'
    CRPHA_MASK_WINDOW_START = 'CRPHA_MASK_WINDOW_START'
    CPPHA_MASK_WINDOW_START = 'CPPHA_MASK_WINDOW_START'
    KFPHA_MASK_WINDOW_START = 'KFPHA_MASK_WINDOW_START'
    KRPHA_MASK_WINDOW_START = 'KRPHA_MASK_WINDOW_START'
    CFPOW_MASK_WINDOW_END = 'CFPOW_MASK_WINDOW_END'
    CRPOW_MASK_WINDOW_END = 'CRPOW_MASK_WINDOW_END'
    CPPOW_MASK_WINDOW_END = 'CPPOW_MASK_WINDOW_END'
    KFPOW_MASK_WINDOW_END = 'KFPOW_MASK_WINDOW_END'
    KRPOW_MASK_WINDOW_END = 'KRPOW_MASK_WINDOW_END'
    CFPHA_MASK_WINDOW_END = 'CFPHA_MASK_WINDOW_END'
    CRPHA_MASK_WINDOW_END = 'CRPHA_MASK_WINDOW_END'
    CPPHA_MASK_WINDOW_END = 'CPPHA_MASK_WINDOW_END'
    KFPHA_MASK_WINDOW_END = 'KFPHA_MASK_WINDOW_END'
    KRPHA_MASK_WINDOW_END = 'KRPHA_MASK_WINDOW_END'
    CFPOW_MASK_TYPE = 'CFPOW_MASK_TYPE'
    CRPOW_MASK_TYPE = 'CRPOW_MASK_TYPE'
    CPPOW_MASK_TYPE = 'CPPOW_MASK_TYPE'
    KFPOW_MASK_TYPE = 'KFPOW_MASK_TYPE'
    KRPOW_MASK_TYPE = 'KRPOW_MASK_TYPE'
    CFPHA_MASK_TYPE = 'CFPHA_MASK_TYPE'
    CRPHA_MASK_TYPE = 'CRPHA_MASK_TYPE'
    CPPHA_MASK_TYPE = 'CPPHA_MASK_TYPE'
    KFPHA_MASK_TYPE = 'KFPHA_MASK_TYPE'
    KRPHA_MASK_TYPE = 'KRPHA_MASK_TYPE'
    CFPOW_MASK_SET_TYPE = 'CFPOW_MASK_SET_TYPE'
    CRPOW_MASK_SET_TYPE = 'CRPOW_MASK_SET_TYPE'
    CPPOW_MASK_SET_TYPE = 'CPPOW_MASK_SET_TYPE'
    KFPOW_MASK_SET_TYPE = 'KFPOW_MASK_SET_TYPE'
    KRPOW_MASK_SET_TYPE = 'KRPOW_MASK_SET_TYPE'
    CRPHA_MASK_SET_TYPE = 'CRPHA_MASK_SET_TYPE'
    CFPHA_MASK_SET_TYPE = 'CFPHA_MASK_SET_TYPE'
    CPPHA_MASK_SET_TYPE = 'CPPHA_MASK_SET_TYPE'
    KFPHA_MASK_SET_TYPE = 'KFPHA_MASK_SET_TYPE'
    KRPHA_MASK_SET_TYPE = 'KRPHA_MASK_SET_TYPE'

    KFPHA_PHASE_MASK_BY_POWER_TRACE = 'KFPHA_PHASE_MASK_BY_POWER_TRACE'
    KRPHA_PHASE_MASK_BY_POWER_TRACE = 'KRPHA_PHASE_MASK_BY_POWER_TRACE'
    CRPHA_PHASE_MASK_BY_POWER_TRACE = 'CRPHA_PHASE_MASK_BY_POWER_TRACE'
    CFPHA_PHASE_MASK_BY_POWER_TRACE = 'CFPHA_PHASE_MASK_BY_POWER_TRACE'
    CPPHA_PHASE_MASK_BY_POWER_TRACE = 'CPPHA_PHASE_MASK_BY_POWER_TRACE'

    KFPHA_PHASE_MASK_BY_POWER_LEVEL = 'KFPHA_PHASE_MASK_BY_POWER_LEVEL'
    KRPHA_PHASE_MASK_BY_POWER_LEVEL = 'KRPHA_PHASE_MASK_BY_POWER_LEVEL'
    CRPHA_PHASE_MASK_BY_POWER_LEVEL = 'CRPHA_PHASE_MASK_BY_POWER_LEVEL'
    CFPHA_PHASE_MASK_BY_POWER_LEVEL = 'CFPHA_PHASE_MASK_BY_POWER_LEVEL'
    CPPHA_PHASE_MASK_BY_POWER_LEVEL = 'CPPHA_PHASE_MASK_BY_POWER_LEVEL'

    OUTSIDE_MASK_COOLDOWN_TIME= 'OUTSIDE_MASK_COOLDOWN_TIME'

    breakdown_keywords = [CFPOW_AUTO_SET, CRPOW_AUTO_SET, CPPOW_AUTO_SET, KFPOW_AUTO_SET,
                          KRPOW_AUTO_SET, CFPHA_AUTO_SET, CRPHA_AUTO_SET, CPPHA_AUTO_SET,
                          KFPHA_AUTO_SET, KRPHA_AUTO_SET, CFPOW_DROP_AMP, CRPOW_DROP_AMP,
                          CPPOW_DROP_AMP, KFPOW_DROP_AMP, KRPOW_DROP_AMP, CFPHA_DROP_AMP,
                          CRPHA_DROP_AMP, CPPHA_DROP_AMP, KFPHA_DROP_AMP, KRPHA_DROP_AMP,
                          BREAKDOWN_TRACES, VAC_SPIKE_TRACES_TO_SAVE, CFPOW_MASK_ABS_MIN,
                          CRPOW_MASK_ABS_MIN, CPPOW_MASK_ABS_MIN, KFPOW_MASK_ABS_MIN,
                          KRPOW_MASK_ABS_MIN, CFPHA_MASK_ABS_MIN, CRPHA_MASK_ABS_MIN,
                          CPPHA_MASK_ABS_MIN, KFPHA_MASK_ABS_MIN, KRPHA_MASK_ABS_MIN,
                          CFPOW_MASK_LEVEL, CRPOW_MASK_LEVEL, CPPOW_MASK_LEVEL, KFPOW_MASK_LEVEL,
                          KRPOW_MASK_LEVEL, CFPHA_MASK_LEVEL, CRPHA_MASK_LEVEL, CPPHA_MASK_LEVEL,
                          KFPHA_MASK_LEVEL, KRPHA_MASK_LEVEL, CFPOW_CHECK_STREAK,
                          CRPOW_CHECK_STREAK, CPPOW_CHECK_STREAK, KFPOW_CHECK_STREAK,
                          KRPOW_CHECK_STREAK, CFPHA_CHECK_STREAK, CRPHA_CHECK_STREAK,
                          CPPHA_CHECK_STREAK, KFPHA_CHECK_STREAK, KRPHA_CHECK_STREAK,
                          CFPOW_MASK_FLOOR, CRPOW_MASK_FLOOR, CPPOW_MASK_FLOOR, KFPOW_MASK_FLOOR,
                          KRPOW_MASK_FLOOR, CFPHA_MASK_FLOOR, CRPHA_MASK_FLOOR, CPPHA_MASK_FLOOR,
                          KFPHA_MASK_FLOOR, KRPHA_MASK_FLOOR, CFPOW_NUM_AVERAGE_TRACES,
                          CRPOW_NUM_AVERAGE_TRACES, CPPOW_NUM_AVERAGE_TRACES,
                          KFPOW_NUM_AVERAGE_TRACES, KRPOW_NUM_AVERAGE_TRACES,
                          CFPHA_NUM_AVERAGE_TRACES, CRPHA_NUM_AVERAGE_TRACES,
                          CPPHA_NUM_AVERAGE_TRACES, KFPHA_NUM_AVERAGE_TRACES,
                          KRPHA_NUM_AVERAGE_TRACES, CRPOW_DROP_AMP_VALUE, CPPOW_DROP_AMP_VALUE,
                          KFPOW_DROP_AMP_VALUE, KRPOW_DROP_AMP_VALUE, CFPHA_DROP_AMP_VALUE,
                          CRPHA_DROP_AMP_VALUE, CPPHA_DROP_AMP_VALUE, CFPOW_DROP_AMP_VALUE,
                          KFPHA_DROP_AMP_VALUE, KRPHA_DROP_AMP_VALUE, OUTSIDE_MASK_CHECK_TIME,
                          OUTSIDE_MASK_COOLDOWN_TIME, CFPOW_MASK_START, CRPOW_MASK_START,
                          CPPOW_MASK_START, KFPOW_MASK_START, KRPOW_MASK_START, CRPHA_MASK_START,
                          CPPHA_MASK_START, CFPHA_MASK_START, KFPHA_MASK_START, KRPHA_MASK_START,
                          CFPOW_MASK_END, CRPOW_MASK_END, CPPOW_MASK_END, KFPOW_MASK_END,
                          KRPOW_MASK_END, CFPHA_MASK_END, CRPHA_MASK_END, CPPHA_MASK_END,
                          KFPHA_MASK_END, KRPHA_MASK_END, CFPOW_MASK_WINDOW_START,
                          CRPOW_MASK_WINDOW_START, CPPOW_MASK_WINDOW_START, KFPOW_MASK_WINDOW_START,
                          KRPOW_MASK_WINDOW_START, CFPHA_MASK_WINDOW_START, CRPHA_MASK_WINDOW_START,
                          CPPHA_MASK_WINDOW_START, KFPHA_MASK_WINDOW_START, KRPHA_MASK_WINDOW_START,
                          CFPOW_MASK_WINDOW_END, CRPOW_MASK_WINDOW_END, CPPOW_MASK_WINDOW_END,
                          KFPOW_MASK_WINDOW_END, KRPOW_MASK_WINDOW_END, CFPHA_MASK_WINDOW_END,
                          CRPHA_MASK_WINDOW_END, CPPHA_MASK_WINDOW_END, KFPHA_MASK_WINDOW_END,
                          KRPHA_MASK_WINDOW_END, CFPOW_MASK_TYPE, CRPOW_MASK_TYPE, CPPOW_MASK_TYPE,
                          KFPOW_MASK_TYPE, KRPOW_MASK_TYPE, CFPHA_MASK_TYPE, CRPHA_MASK_TYPE,
                          CPPHA_MASK_TYPE, KFPHA_MASK_TYPE, KRPHA_MASK_TYPE, CFPOW_MASK_SET_TYPE,
                          CRPOW_MASK_SET_TYPE, CPPOW_MASK_SET_TYPE, KFPOW_MASK_SET_TYPE,
                          KRPOW_MASK_SET_TYPE, CRPHA_MASK_SET_TYPE, CFPHA_MASK_SET_TYPE,
                          CPPHA_MASK_SET_TYPE, KFPHA_MASK_SET_TYPE, KRPHA_MASK_SET_TYPE,
                          KFPHA_PHASE_MASK_BY_POWER_TRACE, KRPHA_PHASE_MASK_BY_POWER_TRACE,
                          CRPHA_PHASE_MASK_BY_POWER_TRACE, CFPHA_PHASE_MASK_BY_POWER_TRACE,
                          CPPHA_PHASE_MASK_BY_POWER_TRACE, KFPHA_PHASE_MASK_BY_POWER_LEVEL,
                          KRPHA_PHASE_MASK_BY_POWER_LEVEL, CRPHA_PHASE_MASK_BY_POWER_LEVEL,
                          CFPHA_PHASE_MASK_BY_POWER_LEVEL, CPPHA_PHASE_MASK_BY_POWER_LEVEL]

    LOG_RAMP_CURVE_NUMSTEPS = 'LOG_RAMP_CURVE_NUMSTEPS '
    LOG_RAMP_CURVE_PULSES_PER_STEP = 'LOG_RAMP_CURVE_PULSES_PER_STEP'
    LOG_RAMP_CURVE_RAMP_RATE = 'LOG_RAMP_CURVE_RAMP_RATE'

    #
    # modulator
    MODULATOR_CHECK_TIME = 'MODULATOR_CHECK_TIME'
    modulator_keywords = [MODULATOR_CHECK_TIME]
    #
    # RF protection
    RF_PROT_CHECK_TIME = 'RF_PROT_CHECK_TIME'
    rfprot_keywords = [RF_PROT_CHECK_TIME, RF_STRUCTURE]
    #
    # General Monitoring,
    GMON_SUFFIX = 'GMON_SUFFIX'
    gmonitor_keywords = [GMON_SUFFIX]
    #
    # gui
    GUI_UPDATE_TIME = 'GUI_UPDATE_TIME'
    gui_keywords = [GUI_UPDATE_TIME]

    # If successfully created, these variables will be dictionaries that contain subsets of
    # config
    # they are used by the various classes that set parameters
    vac_config = None  # 1
    dc_config = None  # 2
    log_config = None  # 3
    vac_valve_config = None  # 4
    water_temp_config = None  # 5
    cavity_temp_config = None  # 6
    llrf_config = None  # 7
    breakdown_config = None  # 8
    modulator_config = None  # 9
    rfprot_config = None  # 10
    gui_config = None  # 11
    solenoid_config = None  # 12
    monitor_config = None  # 13
    #
    # we'll also have a dictionary for all the individual configs
    VAC_CONFIG = "vac_config"  # 1
    DC_CONFIG = "DC_config"  # 2
    LOG_CONFIG = "log_config"  # 3
    VAC_VALVE_CONFIG = "vac_valve_config"  # 4
    WATER_TEMP_CONFIG = "water_temp_config"  # 5
    CAVITY_TEMP_CONFIG = "cavity_temp_config"  # 6
    LLRF_CONFIG = "llrf_config"  # 7
    BREAKDOWN_CONFIG = "breakdown_config"  # 8
    MOD_CONFIG = "modulator_config"  # 9
    RFPROT_CONFIG = 'rfprot_config'  # 10
    GUI_CONFIG = "gui_config"  # 11
    SOL_CONFIG = "sol_config"  # 12
    MONITOR_CONFIG = "monitor_config"  # 13

    all_config = {VAC_CONFIG: vac_config,  # 1
                  DC_CONFIG: dc_config,  # 2
                  LOG_CONFIG: log_config,  # 3
                  VAC_VALVE_CONFIG: vac_valve_config,  # 4
                  WATER_TEMP_CONFIG: water_temp_config,  # 5
                  CAVITY_TEMP_CONFIG: cavity_temp_config,  # 6
                  LLRF_CONFIG: llrf_config,  # 7
                  BREAKDOWN_CONFIG: breakdown_config,  # 8
                  MOD_CONFIG: modulator_config,  # 9
                  GUI_CONFIG: gui_config,  # 10
                  SOL_CONFIG: solenoid_config,  # 11
                  MONITOR_CONFIG: monitor_config,  # 12
                  RFPROT_CONFIG: rfprot_config  # 13
                  }

    # ALL THE CONFIG KEYWORDS MUST BE IN THIS LIST (OR BE  GEN_MON KEYWORD)
    # OTHERWISE TEH PROGRAMM WILL NOT START PROPERLY
    all_config_keywords = [MODE]
    for item in [llrf_keywords, vac_keywords, dc_keywords, log_keywords,
                           vac_valve_keywords, water_temp_keywords, cavity_temp_keywords,
                           solenoid_keywords, breakdown_keywords, modulator_keywords,
                 rfprot_keywords, gui_keywords]:
        for key in item:
            all_config_keywords.append(key)

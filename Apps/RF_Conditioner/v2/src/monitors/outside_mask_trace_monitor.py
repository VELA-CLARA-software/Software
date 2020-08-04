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
//  FileName:    outside_mask_trace_monitor.py
//  Description: The outside_mask_trace_monitor monitors the c++ LLRF module for outside mask
//      		 events, when they occurs it gets and pickles the data, increments the breakdown
//				 count. The main difference between this and the llrf_monitor is this updates
//               often
//
//*/
'''
from monitor import monitor
from src.data.state import state


class outside_mask_trace_monitor(monitor):
    """
    This class monitors a number of LLRF signals (some of these could go in llrf_monitor):
        pulse_count (number of RF pulses seen)
        the number of Ouside Mask Events (OME)
        There are two timers,
        timer ->  update svalues
        cooldown_timer -> when an event is detected cooldown is started, when it completes it
        sets breakdown_status back to GOOD
    """
    def __init__(self):
        # init base-ccaget lass
        monitor.__init__(self)

        # aliases for CATAP llrf control
        self.llrf_control = self.hardware.llrf_control
        self.llrf_obj = self.hardware.llrf_obj

        # set cool-down mode to TIMED, OME are ***always*** timed cool-down
        self.set_cooldown_mode('TIMED')
        # connect the cool_down timer timeout signal  to self.cooldown_finished
        self.cooldown_timer.setSingleShot(True)
        self.cooldown_timer.timeout.connect(self.cooldown_finished)

        # to count the number of pulses since th e last event we need to know the starting pulse
        # count
        self.event_pulse_count_zero = 0

        # last ome count (so we can know if we have a new one)
        self.previous_omed_count = 0

        # set breakdown state to good
        self.values[self.data.breakdown_status] = state.GOOD

        # This is a gflag that is set when there is new data to clect
        self.new_omed_data = False

        # we store a counter of the number of ome detected for each trace
        trace_names = self.llrf_control.getTraceNames()
        self.ome_counts = {}
        for name in trace_names:
            self.ome_counts[name] = 0

        # The timer runs update_values
        self.timer.timeout.connect(self.update_value)
        self.timer.start(self.config_data[self.config.OUTSIDE_MASK_CHECK_TIME])

        self.set_success = True

    def reset_event_pulse_count_OLD(self):
        """
        We keep a count of the number of pulses since the last 'event'
        This function resets those counters
        :return:
        """
        pass
        # self.event_pulse_count_zero = self.values[self.datat.pulse_count]
        # self.values[self.data.event_pulse_count] = 0
        # self.logger.message_header(__name__ + ' reset_event_pulse_count', add_to_text_log=True,
        #                            show_time_stamp=True)
        # self.logger.message('event_pulse_count_zero = {}'.format(self.event_pulse_count_zero),
        #                     add_to_text_log=True, show_time_stamp=False)

    def cooldown_finished(self):
        self.logger.message(__name__ + ', cool down ended')
        self.incool_down = False
        self.values[self.data.breakdown_status] = state.GOOD

    def update_value(self):
        """
        This is the main update function, it handles the pulse-counting and OMED-counting
        """
        #print('update_value() from outside_mask_trace_monitor')
        # The number of pulses
        self.values[self.data.pulse_count] = self.llrf_obj[0].active_pulse_count

        # the number of pulses since last 'event' (actually includes since last ramp, so re-name)
        #self.values[self.data.event_pulse_count] = self.values[self.data.pulse_count] - self.event_pulse_count_zero
        self.values[self.data.event_pulse_count] = self.values[self.data.pulse_count] - self.values[self.data.event_pulse_count_zero]

        #print 'Pulse count = {}\nEvent pulse count = {}'.format(self.values[self.data.pulse_count], self.values[self.data.event_pulse_count])
        # elapsed time since we started
        self.values[self.data.elapsed_time] = self.llrf_control.elapsedTime()
        # Number of Outside Mask Events Detected (OMED) by CATAP llrf
        self.values[self.data.num_outside_mask_traces] = self.llrf_obj[0].omed_count
        #
        # If the number of events has increased, there must have been a new event
        if self.values[self.data.num_outside_mask_traces] > self.previous_omed_count:
            self.new_breakdown()
            self.new_omed_data = True
            self.previous_omed_count = self.values[self.data.num_outside_mask_traces]
            #print('num_outside_mask_traces = {}'.format(self.values[self.data.num_outside_mask_traces]))
            #print('previous_omed_count = {}'.format(self.previous_omed_count))

        # else:
        #     print('num_outside_mask_traces <= previous_omed_count:\nnum_outside_mask_traces = {}\nprevious_omed_count = {}'.
        #           format(self.values[self.data.num_outside_mask_traces], self.previous_omed_count))
        #
        # Now we try collecting any new data, the OME data usually includes "future traces" (traces
        # that are saved after the event trace). This means we have to wait for those traces
        # before we can collect them. This is accomplished with the new_omed_data flag
        #
        # if we have new data, check if we can collect it
        if self.new_omed_data:

            # if we can collect it, collect it
            if self.llrf_control.canGetOutsideMaskEventData():
                print('New OME data & can collect OME data')
                self.collect_ome_data()
                # RESET FLAG
                self.new_omed_data = False
            else:
                print('New OME data but cannot collect OME')

            '''
        message("checkCollectingFutureTraces(): Num collected = ", llrf.omed.num_collected, "/",
                llrf.omed.extra_traces_on_outside_mask_event + UTL::THREE_SIZET,
                " (",llrf.omed.num_still_to_collect  ,")");
            '''

        else:
            pass
        # we then update the last million pulses log, this is a list of how many breakdwons in the
        # last 1 million pulses ...
        #self.data.update_last_million_pulse_log() # OLD NAME!!!
        self.data.update_active_pulse_breakdown_log()

    def new_breakdown(self):
        """
        When a new OME is detected this function sets the bad state and starts the timer
        :return:
        """
        # set the breakdown_status to bad
        self.values[self.data.breakdown_status] = state.BAD
        # start or restart the cooldown_timer
        print("cooldown_timer.start, time = {}".format(self.config_data[self.config.OUTSIDE_MASK_COOLDOWN_TIME]))
        self.cooldown_timer.start(self.config_data[self.config.OUTSIDE_MASK_COOLDOWN_TIME])

    def collect_ome_data(self):
        """
        Collects the OME data from CATAP llrf
        :return:
        """
        self.logger.message_header(__name__+ ' Collecting Outside Mask Event Data',
                                   add_to_text_log=True, show_time_stamp=True)
        self.logger.message('event_pulse_count_zero = ' + str(self.event_pulse_count_zero),  show_time_stamp=False)
        # new is a dictionary returned from CATAP llrf that conatins the data, messages etc
        # This is copied from the c++ code in liberaLLRFController.cpp
        #
        # dictionary[std::string("trace_name")] = boost::python::object(data.trace_that_caused_OME);
        # dictionary[std::string("mask_floor")] = boost::python::object(data.mask_floor);
        # dictionary[std::string("time_vector")] = getTimeVector_Py();
        # dictionary[std::string("is_collecting")] = boost::python::object(data.is_collecting);
        # dictionary[std::string("num_collected_traces")] = boost::python::object(data.num_collected);
        # dictionary[std::string("message")] = boost::python::object(data.outside_mask_trace_message);
        # dictionary[std::string("num_events")] = boost::python::object(data.num_events);
        # dictionary[std::string("outside_mask_index")] = boost::python::object(
        # data.outside_mask_index);
        #
        new = self.llrf_control.getOutsideMaskEventData()
        # add in some other data
        new.update({'vacuum': self.values[self.data.vac_level]})
        new.update({'DC': self.values[self.data.DC_level]})
        new.update({'SOL': self.values[self.data.sol_value]})
        #
        # We now FORCE an update to the breakdown count, the CATAP module can see more than one
        # event (i.e there was an event in a future trace as well as the original event)
        # (update breakdown count, will only work if all states are not bad???????)
        self.data.force_update_breakdown_count(new["num_events"])  # MAGIC_STRING

        # TODO force update pulse_breakdown log with "correct" data (i./e take into account if we are log ramping or not ...

        self.logger.message("Python OME Message:\n" + new['message'],show_time_stamp=False)
        self.logger.message(__name__+' adding {} events '.format(new["num_events"]))

        self.ome_counts[new['trace_name']] += 1
        filename = new['trace_name'] + '_' + str(self.ome_counts[new['trace_name']])
        self.logger.dump_ome_data(filename=filename, object=new)

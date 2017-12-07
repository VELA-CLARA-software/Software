# DJS Sept 2017
#
# breakdown monitor
# emits breakdown_signal giving:
#   the number of breakdowns
#   the breakdown rate
#
#
# This class runs in a separate Qthread
# so after instantiation you must call start on it (!)
# Assuming connecting the interface works
# it has a timer that checks the number of breakdowns
# if there is a new breakdown it emits breakdown_signal
# which gives the total number of breakdowns
# and the breakdown rate
#
# This class assumes that breakdown monitoring has already been
# set-up and is running in the HWC
#
#  base-class
from monitor import monitor
from PyQt4.QtCore import pyqtSignal


class break_down_monitor(monitor):
    # the number of breakdowns captured before 'now'
    # (i.e. before whenever you next check the number of breakdowns)
    _previous_number_of_breakdowns = 0
    # the breakdown data, saved in the HWC
    break_down_data = {}
    # signal to emit after new breakdown
    breakdown_signal = pyqtSignal(int,float)
    def __init__(self,
                 # the HWC
                 llrf_controller = None,
                 # time between checking breakdown counts
                 update_time = 50, # ms
                 # breakdowns are ALWAYS defined from the CAVITY_REVERSE_POWER trace
                 CRPow = 'CAVITY_REVERSE_POWER'):
        # init base-class
        # super(monitor, self).__init__()
        monitor.__init__(self)
        # which llrf trace to check for breakdowns
        self.CRPow = CRPow
        # a general_monitor HWC
        self.llrf_controller = llrf_controller
        # how often to call the timer_function
        self.update_time = update_time
        # if passed controller, start working
        if llrf_controller is not None:
            # const ref to the HWC virtual llrf object
            self.llrfObj = [self.llrf_controller.getLLRFObjConstRef()]
            # a timer to run check_breakdown_count automatically every self.update_time
            self.timer.timeout.connect(self.check_breakdown_count)
            self.timer.start(self.update_time)

    def check_breakdown_count(self):
        # latest number of breakdowns
        current_number_of_breakdowns = self.llrfObj[0].num_outside_mask_traces
        if  current_number_of_breakdowns > self._previous_number_of_breakdowns:
            print ('new breakdown detected! ', current_number_of_breakdowns)
            # get all the breakdown data from the HWC, this could be improved by having a method that
            # just gets new breakdown data to append to old data
            self.break_down_data = self.llrf_controller.getOutsideMaskData()
            # update _previous_number_of_breakdowns
            self._previous_number_of_breakdowns = current_number_of_breakdowns
            # estimate breakdown rates
            self._break_down_rate = self.rf_pulse_count / self._previous_number_of_breakdowns
            self.breakdown_signal.emit(self._previous_number_of_breakdowns,self._break_down_rate)



    # how many rf pulses have been captured by the HWC
    @property
    def rf_pulse_count(self):
        return self.llrfObj[0].trace_data[ self.CRPow ].shot

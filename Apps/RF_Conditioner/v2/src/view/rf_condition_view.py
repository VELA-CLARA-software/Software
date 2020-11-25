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
//  Last edit:   03-07-2019
//  FileName:    rf_condition_view.py
//  Description: The rf_condition_view is the main gui
//
//
//
//
//*/
'''
# from PyQt4.QtGui import QApplication
# from PyQt4.QtCore import QTimer
# from controller_base import controller_base
# from src.gui.gui_conditioning import gui_conditioning
# import src.data.rf_condition_data_base as dat
# from src.data.state import state
import sys
from src.view.rf_condition_view_base import Ui_rf_condition_mainWindow
from VELA_CLARA_RF_Modulator_Control import GUN_MOD_STATE
from VELA_CLARA_RF_Modulator_Control import L01_MOD_STATE
from VELA_CLARA_Vac_Valve_Control import VALVE_STATE
from VELA_CLARA_RF_Protection_Control import RF_PROT_STATUS
from VELA_CLARA_RF_Modulator_Control import HOLD_RF_ON_STATE
from src.data.rf_conditioning_data import rf_conditioning_data

from src.data.state import state
from PyQt4.QtGui import *

from PyQt4.QtGui import QPixmap
from PyQt4.QtGui import QTextCursor
from PyQt4.QtCore import QTimer
import pyqtgraph


class OutLog:
    initial_stdout = sys.stdout

    def __init__(self, edit, out=None, color=None):
        """(edit, out=None, color=None) -> can write stdout, stderr to a
        QTextEdit.
        edit = QTextEdit
        out = alternate stream ( can be the original sys.stdout )
        color = alternate color (i.e. color stderr a different color)
        """
        self.edit = edit
        self.out = None
        self.color = color

    def write(self, m):
        """
        here we are providing a new "write" method for the stdout
        https://docs.python.org/2/library/sys.html#module-sys
        sys.stdin
        sys.stdout
        sys.stderr
        File objects corresponding to the interpreter’s standard input, output and error streams.
        stdin is used for all interpreter input except for scripts but including calls to input()
        and raw_input(). stdout is used for the output of print and expression statements and for
        the prompts of input() and raw_input(). The interpreter’s own prompts and (almost all of)
        its error messages go to stderr. stdout and stderr needn’t be built-in file objects: any
        object is acceptable as long as it has a write() method that takes a string argument. (
        Changing these objects doesn’t affect the standard I/O streams of processes executed by
        os.popen(), os.system() or the exec*() family of functions in the os module.)
        :param m: the string to be written
        :return:
        """
        if self.color:
            tc = self.edit.textColor()
            self.edit.setTextColor(self.color)

        # self.edit.moveCursor(QTextCursor.End)
        self.edit.insertPlainText(m)

        if self.out:
            self.out.write(m)
        # also write message to the initial standard out
        OutLog.initial_stdout.write(m)  # class main_controller(controller_base):


class rf_condition_view(QMainWindow, Ui_rf_condition_mainWindow):
    # constant colors for GUI update
    good = open = rf_on = 'green'
    bad = error = closed = off = rf_off = interlock = 'red'
    unknown = 'magenta'
    major_error = 'cyan'
    timing = 'yellow'
    init = 'orange'
    standby = 'purple'
    one = 'green'
    zero = 'yellow'

    #
    # other attributes will be initialised in base-class
    def __init__(self, columnwidth=80):
        QMainWindow.__init__(self)
        Ui_rf_condition_mainWindow.__init__(self)
        self.setupUi(self)
        self.message_pad.setLineWrapColumnOrWidth(columnwidth)

        self.config = None
        self.data = None
        self.values = None

        self.pixmap = QPixmap('resources\\rf_conditioning\\fine.png')
        self.label.setScaledContents(True)
        # self.label.setPixmap(self.pixmap.scaled(self.label.size()))
        self.label.setPixmap(self.pixmap)
        # redirect PYTHON std out ...
        sys.stdout = OutLog(edit=self.message_pad)
        # sys.stderr = OutLog(edit=self.message_pad, color=QColor(255, 0, 0))

        # dict for widgets to simplfy updating values
        self.widget = {}
        self.expert_widget = {}
        self.llrf_enable_button.clicked.connect(self.handle_llrf_enable_button)
        self.llrf_enable_button.setStyleSheet('QPushButton { background-color : ' + self.good + '; '
                                                                                                'color : black; }')
        self.llrf_enable_button.setText('RF Enabled')
        # initialise gui_can_ramp_button to "RAMP DISABLED"
        self.can_ramp_button.clicked.connect(self.handle_can_ramp_button)
        self.can_ramp_button.setStyleSheet('QPushButton { background-color : ' + self.bad + '; color : black; }')
        self.can_ramp_button.setText('RAMP Disabled')
        self.plot_item = self.graphicsView.getPlotItem()
        
        # Close down the app if close button pressed on GUI:
        self.aboutToQuit.connect(self.closeEvent)


    def closeEvent(self):
        '''
            Closes down the app if close button pressed on GUI.
        '''
        print('Close button pressed on RF_Night_Watch GUI.')
        sys.exit(0)


    def closeEvent(self, unknown_arg):
        # TODO AJG:  this is getting called in backend_pyqt5.py
        '''
            Closes down the app if close button pressed on GUI.
        '''
        #print('unknown_arg in closeEvent = {}'.format(self.unknown_arg))
        print('Close button pressed on No-ARCv2 GUI.')
        sys.exit(0)


    def update_plot(self):
        '''
            plot the binned data, the current working point (as a vertical line due to no kfpow for that amp_sp), lines of best fit
        '''
        rcd = rf_conditioning_data
        pg = pyqtgraph
        data = rf_conditioning_data.amp_vs_kfpow_running_stat
        x = data.keys()
        x.sort()
        y = []
        # data =
        for item in x:
            y.append(data[item][1])

        # do we need to clear ???
        self.plot_item.clear()

        # Plot unbinned data in greyscale
        self.plot_item.plot(x, y, pen={'color': 0.9, 'width': 1.0})

        # plot upper and lower limits for bin exclusion
        #All_amp_sp = rcd.binned_amp_vs_kfpow[rcd.All_amp_sp]
        polyfit_4th_order_All_amp_sp = rcd.binned_amp_vs_kfpow[rcd.polyfit_4th_order_All_amp_sp]
        #DATA_lower_limit = rcd.binned_amp_vs_kfpow[rcd.DATA_lower_limit]
        #DATA_upper_limit = rcd.binned_amp_vs_kfpow[rcd.DATA_upper_limit]

        #self.plot_item.plot(All_amp_sp, DATA_lower_limit, pen={'color': 'y', 'width': 0.7})
        #self.plot_item.plot(All_amp_sp, polyfit_4th_order_All_amp_sp, pen={'color': 'y', 'width': 2.0})
        #self.plot_item.plot(All_amp_sp, DATA_upper_limit, pen={'color': 'y', 'width': 0.7})

        # draw vertical line at the new amp_sp
        current_amp = int(self.values[rf_conditioning_data.amp_sp])
        current_X = [current_amp, current_amp]
        current_Y = [min(y), max(y)]


        if current_amp < 0.0:
            pass
        else:
            self.plot_item.plot(current_X, current_Y, pen=pg.mkPen('b', width=2))


        # call in binned data to plot
        bin_X = rcd.binned_amp_vs_kfpow['BIN_X']
        bin_Y = rcd.binned_amp_vs_kfpow['BIN_mean']


        self.plot_item.plot(bin_X, bin_Y, symbol='+', pen={'color': 'g', 'width': 2.0})

        # Create current_Y using best fit data and current_X:

        m = rcd.values[rcd.m]
        c = rcd.values[rcd.c]
        expected_Y = (current_amp * m) + c

        old_m = rcd.values[rcd.old_m]
        old_c = rcd.values[rcd.old_c]
        expected_Y_old = (current_amp * old_m) + old_c

        #print('expected_Y = {}\nexpected_Y_old = {}'.format(expected_Y, expected_Y_old))

        #print('\nFrom update_plot\nm = {}\nc = {}\nexpected_Y = {}\nold_m = {}\nold_c = {}\nexpected_Y_old = {}\n'.format(m, c, expected_Y, old_m,
        #                                                                                                                  old_c, expected_Y_old))
        #print('type(m) = {}\ntype(c) = {}\ntype(expected_Y) = {}\ntype(old_m) = {}\ntype(old_c) = {}\ntype(expected_Y_old) = {}'.format(type(m),
        #             type(c), type(expected_Y), type(old_m), type(old_c), type(expected_Y_old)))


        x_min = self.values[rcd.x_min]
        old_x_min = self.values[rcd.old_x_min]
        y_min = self.values[rcd.y_min]
        old_y_min = self.values[rcd.old_y_min]

        #print('x_min = {}\nold_x_min = {}\ny_min = {}\nold_y_min = {}\n'.format(x_min, old_x_min, y_min, old_y_min))
        #print('type(x_min) = {}\ntype(old_x_min) = {}\ntype(y_min) = {}\ntype(old_y_min) = {}\n'.format(type(x_min), type(old_x_min), type(y_min),
        #                                                                                                type(old_y_min)))

        # raw_input()

        if y_min < 0.0 or x_min < 0.0:
            pass
        else:

            # add in straight line fits ...'new data'
            self.plot_item.plot([x_min, current_amp], [y_min, expected_Y], pen={'color': 'r', 'width': 1.5})

            # add in plot of old SLF,
            self.plot_item.plot([old_x_min, current_amp], [old_y_min, expected_Y_old], pen={'color': 'y', 'width': 1.5})


        # Add second order polyfit to plot (all data):
        #data_to_fit_x_all = rcd.values['polyfit_2order_X_all']
        #polyfit_2nd_order_y_all = rcd.values['polyfit_2order_Y_all']

        # print('\n\nFrom polyfit_2order_X_all:\ntype(data_to_fit_x) = {}\ndata_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x,
        #                                                                                                                       type(data_to_fit_x),
        #                                                                                                                       polyfit_2nd_order_y))

        #self.plot_item.plot(data_to_fit_x_all, polyfit_2nd_order_y_all, pen={'color': 'c', 'width': 2.0})


        # Add second order polyfit to plot (up to current sp & num_sp_to_fit data):
        data_x_current_sp_to_fit = rcd.values['polyfit_2order_X_current_sp_to_fit']
        polyfit_2order_Y_current_sp_to_fit = rcd.values['polyfit_2order_Y_current_sp_to_fit']

        # do not plot the origin:
        data_x_current_sp_to_fit = data_x_current_sp_to_fit[1:]
        polyfit_2order_Y_current_sp_to_fit = polyfit_2order_Y_current_sp_to_fit[1:]

        # print('data_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x, polyfit_2nd_order_y))

        self.plot_item.plot(data_x_current_sp_to_fit, polyfit_2order_Y_current_sp_to_fit, pen={'color': 'm', 'width': 2.0})

        # Add second order polyfit to plot (all viable bins up to current sp):
        #polyfit_2order_X_current_sp = rcd.values['polyfit_2order_X_current_sp']
        #polyfit_2order_Y_current_sp = rcd.values['polyfit_2order_Y_current_sp']

        # rint('data_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x, polyfit_2nd_order_y))

        #if len(polyfit_2order_X_current_sp) == 1:
            # print('type(data_to_fit_x) = {}'.format( type(data_to_fit_x)))
        #    pass
        #else:
        #    self.plot_item.plot(polyfit_2order_X_current_sp, polyfit_2order_Y_current_sp, pen={'color': 'b', 'width': 2.0})
            #print('From quick_update_plot:\ndata_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x, polyfit_2nd_order_y))

        # Rescale plots everytime function is called? can be annoying  # self.plot_item.setXRange(0.0, current_amp+200.0)  #
        # self.plot_item.setYRange(0.0, max(y)*1.4)

    def quick_update_plot(self):
        '''
              plot the binned data, the curret working point (as a vertical line due to no kfpow for that amp_sp), lines of best fit
          '''

        rcd = rf_conditioning_data
        pg = pyqtgraph
        data = rf_conditioning_data.amp_vs_kfpow_running_stat
        x = data.keys()
        x.sort()
        y = []
        # data =
        for item in x:
            y.append(data[item][1])

        # do we need to clear ???
        self.plot_item.clear()

        # Plot unbinned data in greyscale
        self.plot_item.plot(x, y, pen={'color': 0.9, 'width': 1.0})

        # plot upper and lower limits for bin exclusion

        # TODO AJG: remove all reduced data tendrils

        #All_amp_sp = rcd.binned_amp_vs_kfpow[rcd.All_amp_sp]
        polyfit_4th_order_All_amp_sp = rcd.binned_amp_vs_kfpow[rcd.polyfit_4th_order_All_amp_sp]
        #DATA_lower_limit = rcd.binned_amp_vs_kfpow[rcd.DATA_lower_limit]
        #DATA_upper_limit = rcd.binned_amp_vs_kfpow[rcd.DATA_upper_limit]

        #self.plot_item.plot(All_amp_sp, DATA_lower_limit, pen={'color': 'y', 'width': 0.7})
        #self.plot_item.plot(All_amp_sp, polyfit_4th_order_All_amp_sp, pen={'color': 'y', 'width': 2.0})
        #self.plot_item.plot(All_amp_sp, DATA_upper_limit, pen={'color': 'y', 'width': 0.7})

        # draw vertical line at the new amp_sp
        current_amp = int(self.values[rf_conditioning_data.amp_sp])
        current_X = [current_amp, current_amp]
        current_Y = [min(y), max(y)]


        if current_amp < 0.0:
            pass
        else:
            self.plot_item.plot(current_X, current_Y, pen=pg.mkPen('b', width=2))


        # call in binned data to plot
        bin_X = rcd.binned_amp_vs_kfpow['BIN_X']
        bin_Y = rcd.binned_amp_vs_kfpow['BIN_mean']


        self.plot_item.plot(bin_X, bin_Y, symbol='+', pen={'color': 'g', 'width': 2.0})

        # Create current_Y using best fit data and current_X:

        m = rcd.values[rcd.m]
        c = rcd.values[rcd.c]
        expected_Y = (current_amp * m) + c

        old_m = rcd.values[rcd.old_m]
        old_c = rcd.values[rcd.old_c]
        expected_Y_old = (current_amp * old_m) + old_c

        #print('expected_Y = {}\nexpected_Y_old = {}'.format(expected_Y, expected_Y_old))

        #print('\nFrom update_plot\nm = {}\nc = {}\nexpected_Y = {}\nold_m = {}\nold_c = {}\nexpected_Y_old = {}\n'.format(m, c, expected_Y, old_m,
        #                                                                                                                  old_c, expected_Y_old))
        #print('type(m) = {}\ntype(c) = {}\ntype(expected_Y) = {}\ntype(old_m) = {}\ntype(old_c) = {}\ntype(expected_Y_old) = {}'.format(type(m),
        #             type(c), type(expected_Y), type(old_m), type(old_c), type(expected_Y_old)))


        x_min = self.values[rcd.x_min]
        old_x_min = self.values[rcd.old_x_min]
        y_min = self.values[rcd.y_min]
        old_y_min = self.values[rcd.old_y_min]

        #print('x_min = {}\nold_x_min = {}\ny_min = {}\nold_y_min = {}\n'.format(x_min, old_x_min, y_min, old_y_min))
        #print('type(x_min) = {}\ntype(old_x_min) = {}\ntype(y_min) = {}\ntype(old_y_min) = {}\n'.format(type(x_min), type(old_x_min), type(y_min),
        #                                                                                                type(old_y_min)))

        # raw_input()

        if y_min < 0.0 or x_min < 0.0:
            pass
        else:

            # add in straight line fits ...'new data'
            self.plot_item.plot([x_min, current_amp], [y_min, expected_Y], pen={'color': 'r', 'width': 1.5})

            # add in plot of old SLF,
            self.plot_item.plot([old_x_min, current_amp], [old_y_min, expected_Y_old], pen={'color': 'y', 'width': 1.5})


        # Add second order polyfit to plot (all data):
        #data_to_fit_x_all = rcd.values['polyfit_2order_X_all']
        #polyfit_2nd_order_y_all = rcd.values['polyfit_2order_Y_all']

        # print('\n\nFrom polyfit_2order_X_all:\ntype(data_to_fit_x) = {}\ndata_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x,
        #                                                                                                                       type(data_to_fit_x),
        #                                                                                                                       polyfit_2nd_order_y))

        #self.plot_item.plot(data_to_fit_x_all, polyfit_2nd_order_y_all, pen={'color': 'c', 'width': 2.0})


        # Add second order polyfit to plot (up to current sp & num_sp_to_fit data):
        data_x_current_sp_to_fit = rcd.values['polyfit_2order_X_current_sp_to_fit']
        polyfit_2order_Y_current_sp_to_fit = rcd.values['polyfit_2order_Y_current_sp_to_fit']

        # do not plot the origin:
        data_x_current_sp_to_fit = data_x_current_sp_to_fit[1:]
        polyfit_2order_Y_current_sp_to_fit = polyfit_2order_Y_current_sp_to_fit[1:]

        # print('data_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x, polyfit_2nd_order_y))

        self.plot_item.plot(data_x_current_sp_to_fit, polyfit_2order_Y_current_sp_to_fit, pen={'color': 'm', 'width': 2.0})

        # Add second order polyfit to plot (all viable bins up to current sp):
        #polyfit_2order_X_current_sp = rcd.values['polyfit_2order_X_current_sp']
        #polyfit_2order_Y_current_sp = rcd.values['polyfit_2order_Y_current_sp']

        # rint('data_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x, polyfit_2nd_order_y))

        #if len(polyfit_2order_X_current_sp) == 1:
            # print('type(data_to_fit_x) = {}'.format( type(data_to_fit_x)))
        #    pass
        #else:
        #    self.plot_item.plot(polyfit_2order_X_current_sp, polyfit_2order_Y_current_sp, pen={'color': 'b', 'width': 2.0})
            #print('From quick_update_plot:\ndata_to_fit_x = {}\npolyfit_2nd_order_y = {}'.format(data_to_fit_x, polyfit_2nd_order_y))


    def handle_can_ramp_button(self):
        if self.values[rf_conditioning_data.gui_can_ramp]:
            self.values[rf_conditioning_data.gui_can_ramp] = False
            self.can_ramp_button.setStyleSheet('QPushButton { background-color : ' + self.bad + '; color : black; }')
            self.can_ramp_button.setText('RAMP Disabled')
        else:
            self.values[rf_conditioning_data.gui_can_ramp] = True
            self.can_ramp_button.setStyleSheet('QPushButton { background-color : ' + self.good + '; color : black; }')

<<<<<<< HEAD
    # TODO AJG: add funtion to handle individual_trace_updates button:
    def handle_update_individual_trace_button(self):
        if self.values[rf_conditioning_data.update_individual_trace]:
            self.values[rf_conditioning_data.update_individual_trace] = False
            self.update_individual_trace_button.setStyleSheet('QPushButton { background-color : ' + self.bad + '; color : black; }')
            self.update_individual_trace_button.setText('Individual Trace Updates Stopped')

        else:
            self.values[rf_conditioning_data.update_individual_trace] = True
            self.update_individual_trace_button.setStyleSheet('QPushButton { background-color : ' + self.good + '; color : black; }')
            self.update_individual_trace_button.setText('Individual Trace Updates at 10 Hz')
=======
            self.can_ramp_button.setText('RAMP Enabled')
>>>>>>> parent of 903bfae1... Added handle_update_individual_trace button to NO-ARCv2 GUI that toggles the updating of individual traces between passive and 10Hz.

    def handle_llrf_enable_button(self):
        if self.values[rf_conditioning_data.gui_can_rf_output]:
            self.values[rf_conditioning_data.gui_can_rf_output] = False
            self.llrf_enable_button.setStyleSheet('QPushButton { background-color : ' + self.bad + '; color : black; }')
            self.llrf_enable_button.setText('RF Disabled')
        else:
            self.values[rf_conditioning_data.gui_can_rf_output] = True
            self.llrf_enable_button.setStyleSheet('QPushButton { background-color : ' + self.good + '; color : black; }')
            self.llrf_enable_button.setText('RF Enabled')

    def start_gui_update(self):
        # reference to the values dictionary
        self.data = rf_conditioning_data()
        self.values = self.data.values
        self.expert_values = self.data.expert_values
        self.set_up_expert_widgets()

        # connect checkBOx for exper mode active
        self.edit_mode_checkbox.stateChanged.connect(self.handle_edit_mode)
        # self.init_widget_dict()
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.update_gui)
        self.timer.start(self.config.raw_config_data[self.config.GUI_UPDATE_TIME])

        self.timer2 = QTimer()
        self.timer2.setSingleShot(False)
        self.timer2.timeout.connect(self.quick_update_plot)
        self.timer2.start(self.config.raw_config_data[self.config.GUI_UPDATE_TIME] * 10)

    def handle_edit_mode(self):
        print("handle_edit_mode")
        for key, value in self.expert_widget.iteritems():
            print(key)
            value.setEnabled(self.edit_mode_checkbox.isChecked())

    # main update gui function, loop over all widgets, and if values is new update gui with new
    # value
    def update_gui(self):

        rcd = rf_conditioning_data
        QApplication.processEvents()
        # Call various update functions for each widget / group of widgets
        self.update_cav_pwr_ratio_and_max()
        self.update_mean_power_widgets()
        # vac level, and can we ramp due to vac
        self.update_vac_level()
        # updat evac_valve
        self.update_vac_valve()
        # update main status flags
        self.update_status_flags()
        # RF protection status
        self.update_RF_prot()
        # modulator state
        self.update_modulator_status()
        self.update_temperature_values()
        self.update_CATAP_AMPSP_limit()  # TODO only needs calling once
        self.update_DAQ_rep_rate()
        self.update_all_counters()

        self.update_amp_sp()
        # other stuff

        self.pulse_length_outputwidget.setText(str(self.values[self.data.pulse_length]))
        self.set_widget_color(self.pulse_length_outputwidget, self.values[self.data.pulse_length_status])

        self.current_ramp_index.setText('{}'.format(self.values[self.data.current_ramp_index]))

        self.log_ramp_curve_index_outputwidget.setText(
            '{} / {}'.format(self.values[self.data.log_ramp_curve_index], self.config.raw_config_data['LOG_RAMP_CURVE_NUMSTEPS']))

        self.next_power_increse_outputwidget.setText('{}'.format(self.values[rcd.next_requested_power_change]))
        self.last_power_increase_outputwidget.setText('{}'.format(self.values[rcd.last_requested_power_change]))
        self.last_increase_method_outputwidget.setText(str(self.values[rcd.last_ramp_method]))

        self.slf_predicted_next_amp_sp.setText('{}'.format(self.values[rcd.SP_SLF]))
        self.quad_all_predicted_next_amp_sp.setText('{}'.format(self.values[rcd.SP_QUAD_ALL]))
        self.quad_less_current_predicted_next_amp_sp.setText('{}'.format(self.values[rcd.SP_QUAD_CURRENT]))
        self.quad_less_current_cut_predicted_next_amp_sp.setText('{}'.format(self.values[rcd.SP_QUAD_CURRENT_SP_TO_FIT]))

        self.set_widget_color_text(self.check_mask_outputwidget, self.values[rcd.global_mask_checking])

        # higher level state widgets
        self.set_widget_color_text(self.can_rf_output_status_outputwidget, self.data.values[rcd.can_rf_output_status])
        self.set_widget_color_text(self.can_ramp_status_outputwidget, self.data.values[rcd.can_ramp_status])
        self.set_widget_color_text(self.can_llrf_output_state_outputwidget, self.data.values[rcd.can_llrf_output_state])
        self.set_widget_color_text(self.BD_state_outputwidget, self.data.values[rcd.BD_state])

        self.set_widget_color_text(self.hold_rf_on_state_outputwidget, self.values[self.data.hold_rf_on_state])

        self.set_widget_color_text(self.is_amp_ff_connected_outputwidget,  self.values[self.data.is_amp_ff_connected])



        if self.data.get_kf_running_stat_power_at_set_point(self.values[self.data.last_amp_sp]):
            if self.data.get_kf_running_stat_power_at_current_set_point():
                self.delta_power_outputwidget.setText('{}'.format(int(self.values[self.data.delta_kfpow])))
            else:
                self.delta_power_outputwidget.setText('power now is NONE')
        else:
            self.delta_power_outputwidget.setText('last power NONE')

        if self.data.log_ramp_curve:
            self.log_ramp_final_setpoint_outputwidget.setText( str(self.data.log_ramp_curve[-1][1]) )
        else:
            self.log_ramp_final_setpoint_outputwidget.setText("NONE")

        self.live_amp_set_outputwidget.setText( str(int(self.values[self.data.amp_sp])) )

        # Heartbeat flash on/off
        #print('self.data.values[self.data.llrf_heart_beat_value]= {}'.format(self.values[self.data.llrf_heart_beat_value]))
        #raw_input()

        if self.data.values[self.data.llrf_heart_beat_value] == 0.0:
            self.RF_Heartbeat_outputwidget.setText('HEARTBEAT: REST')
            self.RF_Heartbeat_outputwidget.setStyleSheet('QLabel { background-color : ' + self.zero + '; color : black; }')

        elif self.data.values[self.data.llrf_heart_beat_value] == 1.0:
            self.RF_Heartbeat_outputwidget.setText('HEARTBEAT: PULSE')
            self.RF_Heartbeat_outputwidget.setStyleSheet('QLabel { background-color : ' + self.one + '; color : black; }')
        else:
            self.RF_Heartbeat_outputwidget.setText('HEARTBEAT: UNKNOWN')
            self.RF_Heartbeat_outputwidget.setStyleSheet('QLabel { background-color : ' + self.unknown + '; color : black; }')


    def update_amp_sp(self):
        self.amp_set_outputwidget.setText('{} / {}'.format(int(self.values[self.data.latest_amp_sp_from_ramp]), int(self.values[self.data.last_amp_sp])))

    def update_DAQ_rep_rate(self):
        self.trace_rep_rate_outpuwidget.setText('{:0=4.2f}'.format(self.values[self.data.llrf_DAQ_rep_rate]))
        self.set_widget_color(self.trace_rep_rate_outpuwidget, self.values[self.data.llrf_DAQ_rep_rate_status])

    def update_amp_phase_setpoint(self):
        self.amp_set_outputwidget.setText(str(int(self.values[self.data.amp_sp])))

    def update_CATAP_AMPSP_limit(self):
        self.catap_amp_level_outputwidget.setText( "{} / {} ".format(  str(int(self.values[self.data.llrf_max_amp])), str(int(self.values[
                                                                                                                                     self.data.catap_max_amp]))))
        # TODO thsi needs to incldue the LLRF_MAX_AMP_SP
        self.set_widget_color(self.catap_amp_level_outputwidget, self.values[self.data.catap_max_amp_can_ramp_status])
    def update_temperature_values(self):
        # technically, these are defined at run time, as there cna be more than one PV to record,
        # this is a bit of a hack to get some numbers into the GUI
        self.cav_temp_outputwidget.setText('{:0=4.2f}'.format(self.values[self.data.cav_temp_gui]))
        # We  # don't have a a water anymore ... .  #
        # self.water_temp_outputwidget.setText(  #     '{  # :0=4.2f}'.format(self.values[self.data.water_temp_gui]))

    # # the outputwidget is update based on data type
    # def update_widget(self, key, val, widget):
    #     print("update_widget() called,", type(val), key, widget.objectName())
    #     # meh
    #     if key == self.data.breakdown_rate_low:
    #         self.set_widget_color(widget, not val)
    #     elif key == self.data.vac_decay_level:
    #         self.set_widget_color(widget, val)
    #     elif key == self.data.pulse_length_status:
    #         self.set_widget_color(widget, val)
    #     elif key == self.data.llrf_interlock_status:
    #         self.set_widget_color_text(widget, val)
    #     elif key == self.data.llrf_trigger_status:
    #         self.set_widget_color_text(widget, val)
    #     elif key == self.data.vac_spike_status:
    #         self.set_widget_color_text(widget, val)
    #     elif key == self.data.DC_spike_status:
    #         self.set_widget_color_text(widget, val)
    #     elif key == self.data.llrf_DAQ_rep_rate_status:
    #         self.set_widget_color(widget, val)
    #     elif key == self.data.llrf_output_status:
    #         self.set_widget_color_text(widget, val)
    #     elif widget == self.event_pulse_count_outputwidget:
    #         widget.setText(('%i' % val) + ('/%i' % self.values[
    #             self.data.required_pulses]))  #   # self.clip_vals[key] = widget.text()
    #     elif type(val) is long:
    #         widget.setText('%i' % val)  # self.clip_vals[key] = widget.text()
    #     elif type(val) is int:
    #         # print(key,' is a int')
    #         widget.setText('%i' % val)  # self.clip_vals[key] = widget.text()
    #     elif type(val) is float:
    #         widget.setText('%.2E' % val)  # self.clip_vals[key] = widget.text()
    #     elif type(val) is RF_PROT_STATUS:
    #         self.set_RF_prot(widget, val)
    #     elif type(val) is GUN_MOD_STATE:
    #         self.set_gun_mod_state(widget, val, key)
    #     elif type(val) is L01_MOD_STATE:
    #         self.set_L01_mod_state(widget, val, key)
    #     elif type(val) is VALVE_STATE:
    #         self.set_valve(widget, val)
    #     elif type(val) is bool:
    #         self.set_widget_color_text(widget, val)
    #     elif type(val) is float64:
    #         widget.setText('%.2E' % val)  # self.clip_vals[key] = widget.text()
    #     elif type(val) is str:
    #         widget.setText('%i' % -1)
    #     else:
    #         print 'update_widget error ' + str(val) + ' ' + str(type(val))

    def normal_output_writer(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.message_pad.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.message_pad.setTextCursor(cursor)
        self.message_pad.ensureCursorVisible()

    def error_output_writer(self, text):
        """Append text to the QTextEdit."""
        # Maybe QTextEdit.append() works as well, but this is how I do it:
        cursor = self.message_pad.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(text)
        self.message_pad.setTextCursor(cursor)
        self.message_pad.ensureCursorVisible()

    def update_RF_prot(self):
        widget = self.RF_protection_outputwidget
        val = self.values[self.data.rfprot_state]
        if val == RF_PROT_STATUS.GOOD:
            self.set_widget_color_text(widget, state.GOOD)
        elif val == RF_PROT_STATUS.BAD:
            self.set_widget_color_text(widget, state.BAD)
        elif val == RF_PROT_STATUS.ERROR:
            self.set_widget_color_text(widget, state.ERROR)
        elif val == RF_PROT_STATUS.UNKNOWN:
            self.set_widget_color_text(widget, state.UNKNOWN)
        else:
            self.set_widget_color_text(widget, state.ERROR)

    def update_vac_level(self):
        self.vac_level_outputwidget.setText('{}'.format(self.values[self.data.vac_level]))
        self.set_widget_color(self.vac_level_outputwidget, self.values[self.data.vac_level_can_ramp])

    def update_status_flags(self):

        self.set_widget_color_text(self.llrf_interlock_outputwidget, self.values[self.data.llrf_interlock_status])
        self.set_widget_color_text(self.llrf_trace_interlock_outputwidget, self.values[self.data.llrf_interlock_status])
        self.set_widget_color_text(self.llrf_output_outputwidget, self.values[self.data.llrf_output_status])
        self.set_widget_color_text(self.llrf_ff_amp_locked_outputwidget, self.values[self.data.llrf_ff_amp_locked_status])
        self.set_widget_color_text(self.llrf_ff_ph_locked_outputwidget, self.values[self.data.llrf_ff_ph_locked_status])
        self.set_widget_color_text(self.llrf_trigger_outputwidget, self.values[self.data.llrf_trigger_status])
        self.set_widget_color_text(self.vac_spike_status_outputwidget, self.values[self.data.vac_spike_status])
        #self.set_widget_color_text(self.DC_spike_status_outputwidget, self.values[self.data.DC_spike_status])

    def update_mean_power_widgets(self):
        self.set_power_text(self.probe_power_outputwidget, self.values[self.data.probe_pwr])
        self.set_power_text(self.probe_power_outputwidget, self.values[self.data.probe_pwr])
        self.set_power_text(self.fwd_cav_power_outputwidget, self.values[self.data.fwd_cav_pwr])
        self.set_power_text(self.rev_cav_power_outputwidget, self.values[self.data.rev_cav_pwr])
        self.set_power_text(self.fwd_kly_power_outputwidget, self.values[self.data.fwd_kly_pwr])
        self.set_power_text(self.rev_kly_power_outputwidget, self.values[self.data.rev_kly_pwr])

    def set_power_text(self, widget, value):
        # widget.setText('{:0=4f}'.format( int(value * 0.001) ))
        widget.setText('{:1.2f} kW'.format(value * 0.001))

    def update_all_counters(self):



        #TODO AJG: added countdown until BDR is low here
        if self.values[rf_conditioning_data.breakdown_rate_low]:

            self.BDR_ramp_countdown_pulses_outputwidget.setText('BDR good')
            self.BDR_ramp_countdown_pulses_outputwidget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')
            self.BDR_ramp_countdown_time_outputwidget.setText('BDR good')
            self.BDR_ramp_countdown_time_outputwidget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')

        else:
            self.BDR_ramp_countdown_pulses_outputwidget.setText('{} pulses'.format(self.values[
                                    self.data.breakdown_rate_able_to_ramp_countdown_pulses]))
            self.BDR_ramp_countdown_pulses_outputwidget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')

            self.BDR_ramp_countdown_time_outputwidget.setText('{}'.format(self.values[
                                    self.data.breakdown_rate_able_to_ramp_countdown_HrMinSec]))
            self.BDR_ramp_countdown_time_outputwidget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')



        self.pulse_count_outputwidget.setText('{}'.format(self.values[self.data.pulse_count]))



        self.event_pulse_count_outputwidget.setText(
            '{} / {}'.format(self.values[self.data.event_pulse_count], self.values[self.data.required_pulses]))

        ''' HOW MNAY PULES TO NEXT RAMP (INLCDUGIN BD RATE BEING GOOD ETC, SO COULD BE  thousands'''
        self.pulses_to_next_ramp_outputwidget.setText('{}'.format(self.values[self.data.pulses_to_next_ramp]))

        self.breakdown_count_outputwidget.setText(
            '{} / {}'.format(self.values[self.data.active_breakdown_count], self.values[self.data.total_breakdown_count]))
        self.set_widget_color( self.breakdown_count_outputwidget, self.values[rf_conditioning_data.breakdown_rate_low] )






    def update_expert_values_in_gui(self):
        """
        update the exper_values panels
        :return: none
        """
        # loop over each widghet in
        for key, widget in self.expert_widget.iteritems():
            if key in self.expert_values:
                if isinstance(widget, QComboBox):
                    pass
                else:
                    print("Updating ", key, " with values = ", self.expert_values[key])
                    self.update_expert_widget(key=key, val=self.expert_values[key], widget=widget)

    def update_expert_widget(self, key, val, widget):

        if isinstance(widget, QLineEdit):
            widget.setText(str(val))

        #  # if key is self.data.is_breakdown_monitor_kf_pow:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_kr_pow:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_cf_pow:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_cr_pow:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_cp_pow:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_kf_pha:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_kr_pha:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_cf_pha:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_cr_pha:  #     self.set_widget_color_text(widget, val)  # elif key is
        #  self.data.is_breakdown_monitor_cp_pha:  #     self.set_widget_color_text(widget, val)  # else:  #     pass

    def set_widget_color_text(self, widget, val):
        self.set_widget_color(widget, val)
        self.set_widget_text(widget, val)  # MAGIC_STRING

    # self.clip_vals[status] = str(widget.text())

    def update_vac_valve(self):
        widget = self.vac_valve_status_outputwidget
        val = self.values[self.data.vac_valve_status]
        if val == VALVE_STATE.VALVE_OPEN:
            self.set_widget_color(widget, state.GOOD)
            widget.setText('OPEN')
        elif val == VALVE_STATE.VALVE_CLOSED:
            self.set_widget_color(widget, state.BAD)
            widget.setText('CLOSED')
        elif val == VALVE_STATE.VALVE_TIMING:
            self.set_widget_color_text(widget, state.TIMING)
            widget.setText('TIMING')
        elif val == VALVE_STATE.VALVE_ERROR:
            self.set_widget_color_text(widget, state.ERROR)
        else:
            self.set_widget_color_text(widget, state.ERROR)

    def set_widget_text(self, widget, val):
        if val == state.GOOD:
            widget.setText('GOOD')
        elif val == state.BAD:
            widget.setText('BAD')
        elif val == state.INIT:
            widget.setText('INIT')
        elif val == state.UNKNOWN:
            widget.setText('UNKNOWN')
        elif val == True:
            widget.setText('GOOD')
        elif val == False:
            widget.setText('BAD')
        elif val == state.TIMING:
            widget.setText('TIMING')
        elif val == state.STANDBY:
            widget.setText('STANDBY')
        elif val == 0.0:
            widget.setText('HEARTBEAT 0')
        elif val == 1.0:
            widget.setText('HEARTBEAT 1')
        elif val == HOLD_RF_ON_STATE.MANUAL_RF:
            widget.setText('MANUAL_RF')
        elif val == HOLD_RF_ON_STATE.HOLD_RF_ON:
            widget.setText('HOLD_RF_ON')
        elif val == HOLD_RF_ON_STATE.HOLD_RF_ON_CON:
            widget.setText('HOLD_RF_ON_CON')
        elif val == HOLD_RF_ON_STATE.UNKNOWN_HOLD_RF_ON_STATE:
            widget.setText('UNKNOWN_HOLD_RF_ON_STATE')
        else:
            widget.setText('UNKNOWN')

    def set_widget_color(self, widget, val):
        if val == state.GOOD:
            widget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')
        elif val == state.BAD:
            widget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')
        elif val == state.INIT:
            widget.setStyleSheet('QLabel { background-color : ' + self.init + '; color : black; }')
        elif val == state.UNKNOWN:
            widget.setStyleSheet('QLabel { background-color : ' + self.unknown + '; color : black; }')
        elif val == state.INTERLOCK:
            widget.setStyleSheet('QLabel { background-color : ' + self.interlock + '; color : black; }')
        elif val == True:
            widget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')
        elif val == False:
            widget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')
        elif val == state.TIMING:
            widget.setStyleSheet('QLabel { background-color : ' + self.timing + '; color : black; }')
        elif val == state.STANDBY:
            widget.setStyleSheet('QLabel { background-color : ' + self.standby + '; color : black; }')
        elif val == 0.0:
            widget.setStyleSheet('QLabel { background-color : ' + self.zero + '; color : black; }')
        elif val == 1.0:
            widget.setStyleSheet('QLabel { background-color : ' + self.one + '; color : black; }')
        elif val == HOLD_RF_ON_STATE.MANUAL_RF:
            widget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')
        elif val == HOLD_RF_ON_STATE.HOLD_RF_ON:
            widget.setStyleSheet('QLabel { background-color : ' + self.bad + '; color : black; }')
        elif val == HOLD_RF_ON_STATE.HOLD_RF_ON_CON:
            widget.setStyleSheet('QLabel { background-color : ' + self.good + '; color : black; }')
        elif val == HOLD_RF_ON_STATE.UNKNOWN_HOLD_RF_ON_STATE:
            widget.setStyleSheet('QLabel { background-color : ' + self.unknown + '; color : black; }')

        else:
            widget.setStyleSheet('QLabel { background-color : ' + self.unknown + '; color : black; }')

    def set_up_expert_widgets(self):
        # The value IS THE SAME as the key for the expert_values data dictionary, by doing this
        # we can link the two together
        self.expert_widget[self.data.vac_pv_val] = self.vac_pv_val
        self.expert_widget[self.data.vac_decay_mode_val] = self.vac_decay_mode_val
        self.expert_widget[self.data.vac_decay_time_val] = self.vac_decay_time_val
        self.expert_widget[self.data.vac_decay_level] = self.vac_decay_level
        self.expert_widget[self.data.vac_drop_amp] = self.vac_drop_amp
        self.expert_widget[self.data.vac_hi_pressure] = self.vac_hi_pressure
        self.expert_widget[self.data.vac_spike_delta_val] = self.vac_spike_delta_val
        self.expert_widget[self.data.vac_num_samples_to_average_val] = self.vac_num_samples_to_average_val
        self.expert_widget[self.data.vac_drop_amp_val] = self.vac_drop_amp_val
        self.expert_widget[self.data.ramp_when_hi] = self.ramp_when_hi
        self.expert_widget[self.data.vac_decay_mode] = self.vac_decay_mode
        self.expert_widget[self.data.vac_decay_level_val] = self.vac_decay_level_val
        self.expert_widget[self.data.vac_hi_pressure_val] = self.vac_hi_pressure_val
        self.expert_widget[self.data.ramp_when_hi_val] = self.ramp_when_hi_val
        self.expert_widget[self.data.vac_spike_check_time_val] = self.vac_spike_check_time_val
        self.expert_widget[self.data.vac_spike_check_time] = self.vac_spike_check_time
        self.expert_widget[self.data.is_breakdown_monitor_kf_pow] = self.is_breakdown_monitor_kf_pow
        self.expert_widget[self.data.is_breakdown_monitor_kr_pow] = self.is_breakdown_monitor_kr_pow
        self.expert_widget[self.data.is_breakdown_monitor_cf_pow] = self.is_breakdown_monitor_cf_pow
        self.expert_widget[self.data.is_breakdown_monitor_cr_pow] = self.is_breakdown_monitor_cr_pow
        self.expert_widget[self.data.is_breakdown_monitor_cp_pow] = self.is_breakdown_monitor_cp_pow
        self.expert_widget[self.data.is_breakdown_monitor_kf_pha] = self.is_breakdown_monitor_kf_pha
        self.expert_widget[self.data.is_breakdown_monitor_kr_pha] = self.is_breakdown_monitor_kr_pha
        self.expert_widget[self.data.is_breakdown_monitor_cf_pha] = self.is_breakdown_monitor_cf_pha
        self.expert_widget[self.data.is_breakdown_monitor_cr_pha] = self.is_breakdown_monitor_cr_pha
        self.expert_widget[self.data.is_breakdown_monitor_cp_pha] = self.is_breakdown_monitor_cp_pha  #
        self.expert_widget[self.data.mean_start_kf_pow] = self.mean_start_kf_pow  #
        self.expert_widget[self.data.mean_start_kr_pow] = self.mean_start_kr_pow  #
        self.expert_widget[self.data.mean_start_cf_pow] = self.mean_start_cf_pow  #
        self.expert_widget[self.data.mean_start_cr_pow] = self.mean_start_cr_pow  #
        self.expert_widget[self.data.mean_start_cp_pow] = self.mean_start_cp_pow  #
        self.expert_widget[self.data.mean_start_kf_pha] = self.mean_start_kf_pha  #
        self.expert_widget[self.data.mean_start_kr_pha] = self.mean_start_kr_pha  #
        self.expert_widget[self.data.mean_start_cf_pha] = self.mean_start_cf_pha  #
        self.expert_widget[self.data.mean_start_cr_pha] = self.mean_start_cr_pha  #
        self.expert_widget[self.data.mean_start_cp_pha] = self.mean_start_cp_pha  #
        self.expert_widget[self.data.mean_end_kf_pow] = self.mean_end_kf_pow  #
        self.expert_widget[self.data.mean_end_kr_pow] = self.mean_end_kr_pow  #
        self.expert_widget[self.data.mean_end_cf_pow] = self.mean_end_cf_pow  #
        self.expert_widget[self.data.mean_end_cr_pow] = self.mean_end_cr_pow  #
        self.expert_widget[self.data.mean_end_cp_pow] = self.mean_end_cp_pow  #
        self.expert_widget[self.data.mean_end_kf_pha] = self.mean_end_kf_pha  #
        self.expert_widget[self.data.mean_end_kr_pha] = self.mean_end_kr_pha  #
        self.expert_widget[self.data.mean_end_cf_pha] = self.mean_end_cf_pha  #
        self.expert_widget[self.data.mean_end_cr_pha] = self.mean_end_cr_pha  #
        self.expert_widget[self.data.mean_end_cp_pha] = self.mean_end_cp_pha  #

        self.expert_widget[self.data.mask_units_kf_pow] = self.mask_units_kf_pow  #
        self.expert_widget[self.data.mask_units_kr_pow] = self.mask_units_kr_pow  #
        self.expert_widget[self.data.mask_units_cf_pow] = self.mask_units_cf_pow  #
        self.expert_widget[self.data.mask_units_cr_pow] = self.mask_units_cr_pow  #
        self.expert_widget[self.data.mask_units_cp_pow] = self.mask_units_cp_pow  #
        self.expert_widget[self.data.mask_units_kf_pha] = self.mask_units_kf_pha  #
        self.expert_widget[self.data.mask_units_kr_pha] = self.mask_units_kr_pha  #
        self.expert_widget[self.data.mask_units_cf_pha] = self.mask_units_cf_pha  #
        self.expert_widget[self.data.mask_units_cr_pha] = self.mask_units_cr_pha  #
        self.expert_widget[self.data.mask_units_cp_pha] = self.mask_units_cp_pha  #

        self.expert_widget[self.data.mask_start_kf_pow] = self.mask_start_kf_pow  #
        self.expert_widget[self.data.mask_start_kr_pow] = self.mask_start_kr_pow  #
        self.expert_widget[self.data.mask_start_cf_pow] = self.mask_start_cf_pow  #
        self.expert_widget[self.data.mask_start_cr_pow] = self.mask_start_cr_pow  #
        self.expert_widget[self.data.mask_start_cp_pow] = self.mask_start_cp_pow  #
        self.expert_widget[self.data.mask_start_kf_pha] = self.mask_start_kf_pha  #
        self.expert_widget[self.data.mask_start_kr_pha] = self.mask_start_kr_pha  #
        self.expert_widget[self.data.mask_start_cf_pha] = self.mask_start_cf_pha  #
        self.expert_widget[self.data.mask_start_cr_pha] = self.mask_start_cr_pha  #
        self.expert_widget[self.data.mask_start_cp_pha] = self.mask_start_cp_pha  #
        self.expert_widget[self.data.mask_end_kf_pow] = self.mask_end_kf_pow  #
        self.expert_widget[self.data.mask_end_kr_pow] = self.mask_end_kr_pow  #
        self.expert_widget[self.data.mask_end_cf_pow] = self.mask_end_cf_pow  #
        self.expert_widget[self.data.mask_end_cr_pow] = self.mask_end_cr_pow  #
        self.expert_widget[self.data.mask_end_cp_pow] = self.mask_end_cp_pow  #
        self.expert_widget[self.data.mask_end_kr_pha] = self.mask_end_kr_pha  #
        self.expert_widget[self.data.mask_end_kf_pha] = self.mask_end_kf_pha  #
        self.expert_widget[self.data.mask_end_cf_pha] = self.mask_end_cf_pha  #
        self.expert_widget[self.data.mask_end_cr_pha] = self.mask_end_cr_pha  #
        self.expert_widget[self.data.mask_end_cp_pha] = self.mask_end_cp_pha  #
        self.expert_widget[self.data.mask_window_start_kf_pow] = self.mask_window_start_kf_pow
        self.expert_widget[self.data.mask_window_start_kr_pow] = self.mask_window_start_kr_pow
        self.expert_widget[self.data.mask_window_start_cf_pow] = self.mask_window_start_cf_pow
        self.expert_widget[self.data.mask_window_start_cr_pow] = self.mask_window_start_cr_pow
        self.expert_widget[self.data.mask_window_start_cp_pow] = self.mask_window_start_cp_pow
        self.expert_widget[self.data.mask_window_start_kf_pha] = self.mask_window_start_kf_pha
        self.expert_widget[self.data.mask_window_start_kr_pha] = self.mask_window_start_kr_pha
        self.expert_widget[self.data.mask_window_start_cf_pha] = self.mask_window_start_cf_pha
        self.expert_widget[self.data.mask_window_start_cr_pha] = self.mask_window_start_cr_pha
        self.expert_widget[self.data.mask_window_start_cp_pha] = self.mask_window_start_cp_pha
        self.expert_widget[self.data.mask_window_end_kf_pow] = self.mask_window_end_kf_pow  #
        self.expert_widget[self.data.mask_window_end_kr_pow] = self.mask_window_end_kr_pow  #
        self.expert_widget[self.data.mask_window_end_cf_pow] = self.mask_window_end_cf_pow  #
        self.expert_widget[self.data.mask_window_end_cr_pow] = self.mask_window_end_cr_pow  #
        self.expert_widget[self.data.mask_window_end_cp_pow] = self.mask_window_end_cp_pow  #
        self.expert_widget[self.data.mask_window_end_kf_pha] = self.mask_window_end_kf_pha  #
        self.expert_widget[self.data.mask_window_end_kr_pha] = self.mask_window_end_kr_pha  #
        self.expert_widget[self.data.mask_window_end_cf_pha] = self.mask_window_end_cf_pha  #
        self.expert_widget[self.data.mask_window_end_cr_pha] = self.mask_window_end_cr_pha  #
        self.expert_widget[self.data.mask_window_end_cp_pha] = self.mask_window_end_cp_pha  #
        self.expert_widget[self.data.mask_min_kf_pow] = self.mask_min_kf_pow  #
        self.expert_widget[self.data.mask_min_kr_pow] = self.mask_min_kr_pow  #
        self.expert_widget[self.data.mask_min_cf_pow] = self.mask_min_cf_pow  #
        self.expert_widget[self.data.mask_min_cr_pow] = self.mask_min_cr_pow  #
        self.expert_widget[self.data.mask_min_cp_pow] = self.mask_min_cp_pow  #
        self.expert_widget[self.data.mask_min_kf_pha] = self.mask_min_kf_pha  #
        self.expert_widget[self.data.mask_min_kr_pha] = self.mask_min_kr_pha  #
        self.expert_widget[self.data.mask_min_cf_pha] = self.mask_min_cf_pha  #
        self.expert_widget[self.data.mask_min_cr_pha] = self.mask_min_cr_pha  #
        self.expert_widget[self.data.mask_min_cp_pha] = self.mask_min_cp_pha  #
        self.expert_widget[self.data.num_averages_kf_pow] = self.num_averages_kf_pow  #
        self.expert_widget[self.data.num_averages_kr_pow] = self.num_averages_kr_pow  #
        self.expert_widget[self.data.num_averages_cf_pow] = self.num_averages_cf_pow  #
        self.expert_widget[self.data.num_averages_cr_pow] = self.num_averages_cr_pow  #
        self.expert_widget[self.data.num_averages_cp_pow] = self.num_averages_cp_pow  #
        self.expert_widget[self.data.num_averages_kf_pha] = self.num_averages_kf_pha  #
        self.expert_widget[self.data.num_averages_kr_pha] = self.num_averages_kr_pha  #
        self.expert_widget[self.data.num_averages_cf_pha] = self.num_averages_cf_pha  #
        self.expert_widget[self.data.num_averages_cr_pha] = self.num_averages_cr_pha  #
        self.expert_widget[self.data.num_averages_cp_pha] = self.num_averages_cp_pha  #
        self.expert_widget[self.data.mask_auto_set_kf_pow] = self.mask_auto_set_kf_pow  #
        self.expert_widget[self.data.mask_auto_set_kr_pow] = self.mask_auto_set_kr_pow  #
        self.expert_widget[self.data.mask_auto_set_cf_pow] = self.mask_auto_set_cf_pow  #
        self.expert_widget[self.data.mask_auto_set_cr_pow] = self.mask_auto_set_cr_pow  #
        self.expert_widget[self.data.mask_auto_set_cp_pow] = self.mask_auto_set_cp_pow  #
        self.expert_widget[self.data.mask_auto_set_kf_pha] = self.mask_auto_set_kf_pha  #
        self.expert_widget[self.data.mask_auto_set_kr_pha] = self.mask_auto_set_kr_pha  #
        self.expert_widget[self.data.mask_auto_set_cf_pha] = self.mask_auto_set_cf_pha  #
        self.expert_widget[self.data.mask_auto_set_cr_pha] = self.mask_auto_set_cr_pha  #
        self.expert_widget[self.data.mask_auto_set_cp_pha] = self.mask_auto_set_cp_pha  #

        self.expert_widget[self.data.mask_type_kr_pow] = self.mask_type_kr_pow  #
        self.expert_widget[self.data.mask_type_kf_pow] = self.mask_type_kf_pow  #
        self.expert_widget[self.data.mask_type_cf_pow] = self.mask_type_cf_pow  #
        self.expert_widget[self.data.mask_type_cr_pow] = self.mask_type_cr_pow  #
        self.expert_widget[self.data.mask_type_cp_pow] = self.mask_type_cp_pow  #
        self.expert_widget[self.data.mask_type_kf_pha] = self.mask_type_kf_pha  #
        self.expert_widget[self.data.mask_type_kr_pha] = self.mask_type_kr_pha  #
        self.expert_widget[self.data.mask_type_cf_pha] = self.mask_type_cf_pha  #
        self.expert_widget[self.data.mask_type_cr_pha] = self.mask_type_cr_pha  #
        self.expert_widget[self.data.mask_type_cp_pha] = self.mask_type_cp_pha  #

        self.expert_widget[self.data.mask_level_kf_pow] = self.mask_level_kf_pow  #
        self.expert_widget[self.data.mask_level_kr_pow] = self.mask_level_kr_pow  #
        self.expert_widget[self.data.mask_level_cf_pow] = self.mask_level_cf_pow  #
        self.expert_widget[self.data.mask_level_cr_pow] = self.mask_level_cr_pow  #
        self.expert_widget[self.data.mask_level_cp_pow] = self.mask_level_cp_pow  #
        self.expert_widget[self.data.mask_level_kf_pha] = self.mask_level_kf_pha  #
        self.expert_widget[self.data.mask_level_kr_pha] = self.mask_level_kr_pha  #
        self.expert_widget[self.data.mask_level_cf_pha] = self.mask_level_cf_pha  #
        self.expert_widget[self.data.mask_level_cr_pha] = self.mask_level_cr_pha  #
        self.expert_widget[self.data.mask_level_cp_pha] = self.mask_level_cp_pha  #
        # self.expert_widget[self.data.mask_end_by_power_kf_pow] = self.mask_end_by_power_kf_pow
        # self.expert_widget[self.data.mask_end_by_power_kr_pow] = self.mask_end_by_power_kr_pow
        # self.expert_widget[self.data.mask_end_by_power_cf_pow] = self.mask_end_by_power_cf_pow
        # self.expert_widget[self.data.mask_end_by_power_cf_pow] = self.mask_end_by_power_cf_pow
        # self.expert_widget[self.data.mask_end_by_power_cp_pow] = self.mask_end_by_power_cp_pow
        # self.expert_widget[self.data.mask_end_by_power_kf_pha] = self.mask_end_by_power_kf_pha
        # self.expert_widget[self.data.mask_end_by_power_kr_pha] = self.mask_end_by_power_kr_pha
        # self.expert_widget[self.data.mask_end_by_power_cf_pha] = self.mask_end_by_power_cf_pha
        # self.expert_widget[self.data.mask_end_by_power_cr_pha] = self.mask_end_by_power_cr_pha
        # self.expert_widget[self.data.mask_end_by_power_cp_pha] = self.mask_end_by_power_cp_pha
        self.expert_widget[self.data.mask_end_power_kf_pow] = self.mask_end_power_kf_pow  #
        self.expert_widget[self.data.mask_end_power_kr_pow] = self.mask_end_power_kr_pow  #
        self.expert_widget[self.data.mask_end_power_cf_pow] = self.mask_end_power_cf_pow  #
        self.expert_widget[self.data.mask_end_power_cr_pow] = self.mask_end_power_cr_pow  #
        self.expert_widget[self.data.mask_end_power_cp_pow] = self.mask_end_power_cp_pow  #
        self.expert_widget[self.data.mask_end_power_kf_pha] = self.mask_end_power_kf_pha  #
        self.expert_widget[self.data.mask_end_power_kr_pha] = self.mask_end_power_kr_pha  #
        self.expert_widget[self.data.mask_end_power_cf_pha] = self.mask_end_power_cf_pha  #
        self.expert_widget[self.data.mask_end_power_cr_pha] = self.mask_end_power_cr_pha  #
        self.expert_widget[self.data.mask_end_power_cp_pha] = self.mask_end_power_cp_pha  #

        # self.expert_widget[self.data.drop_amplitude_kf_pow] = self.drop_amplitude_kf_pow  #
        # self.expert_widget[self.data.drop_amplitude_kr_pow] = self.drop_amplitude_kr_pow  #
        # self.expert_widget[self.data.drop_amplitude_cf_pow] = self.drop_amplitude_cf_pow  #
        # self.expert_widget[self.data.drop_amplitude_cf_pow] = self.drop_amplitude_cf_pow  #
        # self.expert_widget[self.data.drop_amplitude_cp_pow] = self.drop_amplitude_cp_pow  #
        # self.expert_widget[self.data.drop_amplitude_kf_pha] = self.drop_amplitude_kf_pha  #
        # self.expert_widget[self.data.drop_amplitude_kr_pha] = self.drop_amplitude_kr_pha  #
        # self.expert_widget[self.data.drop_amplitude_cf_pha] = self.drop_amplitude_cf_pha  #
        # self.expert_widget[self.data.drop_amplitude_cr_pha] = self.drop_amplitude_cr_pha  #
        # self.expert_widget[self.data.drop_amplitude_cp_pha] = self.drop_amplitude_cp_pha  #

        self.expert_widget[self.data.streak_kf_pow] = self.streak_kf_pow
        self.expert_widget[self.data.streak_kr_pow] = self.streak_kr_pow
        self.expert_widget[self.data.streak_cf_pow] = self.streak_cf_pow
        self.expert_widget[self.data.streak_cr_pow] = self.streak_cr_pow
        self.expert_widget[self.data.streak_cp_pow] = self.streak_cp_pow
        self.expert_widget[self.data.streak_kf_pha] = self.streak_kf_pha
        self.expert_widget[self.data.streak_kr_pha] = self.streak_kr_pha
        self.expert_widget[self.data.streak_cf_pha] = self.streak_cf_pha
        self.expert_widget[self.data.streak_cr_pha] = self.streak_cr_pha
        self.expert_widget[self.data.streak_cp_pha] = self.streak_cp_pha

        self.expert_widget[self.data.saved_on_breakdown_event_kf_pow] = self.saved_on_breakdown_event_kf_pow
        self.expert_widget[self.data.saved_on_breakdown_event_kr_pow] = self.saved_on_breakdown_event_kr_pow
        self.expert_widget[self.data.saved_on_breakdown_event_cf_pow] = self.saved_on_breakdown_event_cf_pow
        self.expert_widget[self.data.saved_on_breakdown_event_cr_pow] = self.saved_on_breakdown_event_cr_pow
        self.expert_widget[self.data.saved_on_breakdown_event_cp_pow] = self.saved_on_breakdown_event_cp_pow
        self.expert_widget[self.data.saved_on_breakdown_event_kf_pha] = self.saved_on_breakdown_event_kf_pha
        self.expert_widget[self.data.saved_on_breakdown_event_kr_pha] = self.saved_on_breakdown_event_kr_pha
        self.expert_widget[self.data.saved_on_breakdown_event_cf_pha] = self.saved_on_breakdown_event_cf_pha
        self.expert_widget[self.data.saved_on_breakdown_event_cr_pha] = self.saved_on_breakdown_event_cr_pha
        self.expert_widget[self.data.saved_on_breakdown_event_cp_pha] = self.saved_on_breakdown_event_cp_pha

        self.expert_widget[self.data.saved_on_vac_spike_kf_pow] = self.saved_on_vac_spike_kf_pow
        self.expert_widget[self.data.saved_on_vac_spike_kr_pow] = self.saved_on_vac_spike_kr_pow
        self.expert_widget[self.data.saved_on_vac_spike_cf_pow] = self.saved_on_vac_spike_cf_pow
        self.expert_widget[self.data.saved_on_vac_spike_cr_pow] = self.saved_on_vac_spike_cr_pow
        self.expert_widget[self.data.saved_on_vac_spike_cp_pow] = self.saved_on_vac_spike_cp_pow
        self.expert_widget[self.data.saved_on_vac_spike_kf_pha] = self.saved_on_vac_spike_kf_pha
        self.expert_widget[self.data.saved_on_vac_spike_kr_pha] = self.saved_on_vac_spike_kr_pha
        self.expert_widget[self.data.saved_on_vac_spike_cf_pha] = self.saved_on_vac_spike_cf_pha
        self.expert_widget[self.data.saved_on_vac_spike_cr_pha] = self.saved_on_vac_spike_cr_pha
        self.expert_widget[self.data.saved_on_vac_spike_cp_pha] = self.saved_on_vac_spike_cp_pha

        self.expert_widget[self.data.drop_amp_on_bd_kf_pow] = self.drop_amp_on_bd_kf_pow
        self.expert_widget[self.data.drop_amp_on_bd_kr_pow] = self.drop_amp_on_bd_kr_pow
        self.expert_widget[self.data.drop_amp_on_bd_cf_pow] = self.drop_amp_on_bd_cf_pow
        self.expert_widget[self.data.drop_amp_on_bd_cr_pow] = self.drop_amp_on_bd_cr_pow
        self.expert_widget[self.data.drop_amp_on_bd_cp_pow] = self.drop_amp_on_bd_cp_pow
        self.expert_widget[self.data.drop_amp_on_bd_kf_pha] = self.drop_amp_on_bd_kf_pha
        self.expert_widget[self.data.drop_amp_on_bd_kr_pha] = self.drop_amp_on_bd_kr_pha
        self.expert_widget[self.data.drop_amp_on_bd_cf_pha] = self.drop_amp_on_bd_cf_pha
        self.expert_widget[self.data.drop_amp_on_bd_cr_pha] = self.drop_amp_on_bd_cr_pha
        self.expert_widget[self.data.drop_amp_on_bd_cp_pha] = self.drop_amp_on_bd_cp_pha

        self.expert_widget[self.data.phase_end_by_power_kf_pow] = self.phase_end_by_power_kf_pow
        self.expert_widget[self.data.phase_end_by_power_kr_pow] = self.phase_end_by_power_kr_pow
        self.expert_widget[self.data.phase_end_by_power_cf_pow] = self.phase_end_by_power_cf_pow
        self.expert_widget[self.data.phase_end_by_power_cr_pow] = self.phase_end_by_power_cr_pow
        self.expert_widget[self.data.phase_end_by_power_cp_pow] = self.phase_end_by_power_cp_pow
        self.expert_widget[self.data.phase_end_by_power_kf_pha] = self.phase_end_by_power_kf_pha
        self.expert_widget[self.data.phase_end_by_power_kr_pha] = self.phase_end_by_power_kr_pha
        self.expert_widget[self.data.phase_end_by_power_cf_pha] = self.phase_end_by_power_cf_pha
        self.expert_widget[self.data.phase_end_by_power_cr_pha] = self.phase_end_by_power_cr_pha
        self.expert_widget[self.data.phase_end_by_power_cp_pha] = self.phase_end_by_power_cp_pha

        # self.expert_widget[self.data.phase_end_by_power_kf_pow] = self.phase_end_by_power_kf_pow
        # self.expert_widget[self.data.phase_end_by_power_kr_pow] = self.phase_end_by_power_kr_pow
        # self.expert_widget[self.data.phase_end_by_power_cf_pow] = self.phase_end_by_power_cf_pow
        # self.expert_widget[self.data.phase_end_by_power_cr_pow] = self.phase_end_by_power_cr_pow
        # self.expert_widget[self.data.phase_end_by_power_cp_pow] = self.phase_end_by_power_cp_pow
        # self.expert_widget[self.data.phase_end_by_power_kf_pha] = self.phase_end_by_power_kf_pha
        # self.expert_widget[self.data.phase_end_by_power_kr_pha] = self.phase_end_by_power_kr_pha
        # self.expert_widget[self.data.phase_end_by_power_cf_pha] = self.phase_end_by_power_cf_pha
        # self.expert_widget[self.data.phase_end_by_power_cr_pha] = self.phase_end_by_power_cr_pha
        # self.expert_widget[self.data.phase_end_by_power_cp_pha] = self.phase_end_by_power_cp_pha

        self.expert_widget[self.data.drop_amplitude_kf_pow] = self.drop_amplitude_kf_pow
        self.expert_widget[self.data.drop_amplitude_kr_pow] = self.drop_amplitude_kr_pow
        self.expert_widget[self.data.drop_amplitude_cf_pow] = self.drop_amplitude_cf_pow
        self.expert_widget[self.data.drop_amplitude_cr_pow] = self.drop_amplitude_cr_pow
        self.expert_widget[self.data.drop_amplitude_cp_pow] = self.drop_amplitude_cp_pow
        self.expert_widget[self.data.drop_amplitude_kf_pha] = self.drop_amplitude_kf_pha
        self.expert_widget[self.data.drop_amplitude_kr_pha] = self.drop_amplitude_kr_pha
        self.expert_widget[self.data.drop_amplitude_cf_pha] = self.drop_amplitude_cf_pha
        self.expert_widget[self.data.drop_amplitude_cr_pha] = self.drop_amplitude_cr_pha
        self.expert_widget[self.data.drop_amplitude_cp_pha] = self.drop_amplitude_cp_pha

        self.expert_widget[self.data.num_future_traces_val] = self.num_future_traces_val
        self.expert_widget[self.data.active_power_val] = self.active_power_val
        self.expert_widget[self.data.keep_valve_open_valves_val] = self.keep_valve_open_valves_val
        self.expert_widget[self.data.keep_valve_open_val] = self.keep_valve_open_val
        self.expert_widget[self.data.breakdown_rate_aim_val] = self.breakdown_rate_aim_val
        self.expert_widget[self.data.number_of_pulses_in_history_val] = self.number_of_pulses_in_history_val
        self.expert_widget[self.data.expected_daq_rep_rate_val] = self.expected_daq_rep_rate_val
        self.expert_widget[self.data.daq_rep_rate_error_val] = self.daq_rep_rate_error_val
        self.expert_widget[self.data.min_cool_down_time_val] = self.min_cool_down_time_val
        self.expert_widget[self.data.trace_buffer_size_val] = self.trace_buffer_size_val
        self.expert_widget[self.data.default_pulse_count_val] = self.default_pulse_count_val
        self.expert_widget[self.data.default_amp_increase_val] = self.default_amp_increase_val
        self.expert_widget[self.data.max_amp_increase_val] = self.max_amp_increase_val
        self.expert_widget[self.data.num_fit_points_val] = self.num_fit_points_val

        # self.expert_widget[  #  #  # self.expert_widget[  #     self.data.saved_on_breakdown_event_kf_pow] =  #
        # self.saved_on_breakdown_event_kf_pow  # # self.expert_widget[  #  # self.data.saved_on_breakdown_event_kr_pow] =
        # self.saved_on_breakdown_event_kr_pow  #  # self.expert_widget[  #     self.data.saved_on_breakdown_event_cf_pow] =  #
        # self.saved_on_breakdown_event_cf_pow  # self.expert_widget[  #  # self.data.saved_on_breakdown_event_cf_pow] =
        # self.saved_on_breakdown_event_cf_pow  #  # self.expert_widget[  #     self.data.saved_on_breakdown_event_cp_pow] =  #
        # self.saved_on_breakdown_event_cp_pow  # self.expert_widget[  #  # self.data.saved_on_breakdown_event_kf_pha] =
        # self.saved_on_breakdown_event_kf_pha  #  # self.expert_widget[  #     self.data.saved_on_breakdown_event_kr_pha] =  #
        # self.saved_on_breakdown_event_kr_pha  # self.expert_widget[  #  # self.data.saved_on_breakdown_event_cf_pha] =
        # self.saved_on_breakdown_event_cf_pha  #  # self.expert_widget[  #     self.data.saved_on_breakdown_event_cr_pha] =  #
        # self.saved_on_breakdown_event_cr_pha  # self.expert_widget[  #  # self.data.saved_on_breakdown_event_cp_pha] =
        # self.saved_on_breakdown_event_cp_pha  #  # self.expert_widget[self.data.saved_on_vac_spike_kf_pow] =  # self.saved_on_vac_spike_kf_pow  #
        # self.expert_widget[  # self.data.saved_on_vac_spike_kr_pow] = self.saved_on_vac_spike_kr_pow  #  # self.expert_widget[
        # self.data.saved_on_vac_spike_cf_pow] =  # self.saved_on_vac_spike_cf_pow  # self.expert_widget[  # self.data.saved_on_vac_spike_cf_pow] =
        # self.saved_on_vac_spike_cf_pow  #  # self.expert_widget[self.data.saved_on_vac_spike_cp_pow] =  # self.saved_on_vac_spike_cp_pow  #
        # self.expert_widget[  # self.data.saved_on_vac_spike_kf_pha] = self.saved_on_vac_spike_kf_pha  #  # self.expert_widget[
        # self.data.saved_on_vac_spike_kr_pha] =  # self.saved_on_vac_spike_kr_pha  # self.expert_widget[  # self.data.saved_on_vac_spike_cf_pha] =
        # self.saved_on_vac_spike_cf_pha  #  # self.expert_widget[self.data.saved_on_vac_spike_cr_pha] =  # self.saved_on_vac_spike_cr_pha  #
        # self.expert_widget[  # self.data.saved_on_vac_spike_cp_pha] = self.saved_on_vac_spike_cp_pha  #  # self.data.streak_kr_pow] =
        # self.streak_kr_pow  # self.expert_widget[  # self.data.streak_cf_pow] = self.streak_cf_pow  # self.expert_widget[  #
        # self.data.streak_cf_pow] = self.streak_cf_pow  # self.expert_widget[  # self.data.streak_cp_pow] = self.streak_cp_pow  #
        # self.expert_widget[  # self.data.streak_kf_pha] = self.streak_kf_pha  # self.expert_widget[  # self.data.streak_kr_pha] =
        # self.streak_kr_pha  # self.expert_widget[  # self.data.streak_cf_pha] = self.streak_cf_pha  # self.expert_widget[  #
        # self.data.streak_cr_pha] = self.streak_cr_pha  # self.expert_widget[  # self.data.streak_cp_pha] = self.streak_cp_pha  #
        # self.expert_widget[  # self.data.breakdown_rate_aim] = self.breakdown_rate_aim  # self.expert_widget[  #
        # self.data.breakdown_rate_aim_val] = self.breakdown_rate_aim_val  # self.expert_widget[  # self.data.expected_daq_rep_rate_val] =
        # self.expected_daq_rep_rate_val  #  # self.expert_widget[self.data.daq_rep_rate_error_val] = self.daq_rep_rate_error_val  #  #
        # self.expert_widget[  #     self.data.number_of_pulses_in_history_val] =  # self.number_of_pulses_in_history_val  # self.expert_widget[  #
        # self.data.trace_buffer_size_val] = self.trace_buffer_size_val  # self.expert_widget[  # self.data.default_pulse_count_val] =
        # self.default_pulse_count_val  #  # #self.expert_widget[self.data.default_amp_increase] = self.default_amp_increase  #  #
        # self.expert_widget[self.data.default_amp_increase_val] = self.default_amp_increase_val  # #self.expert_widget[self.data.max_amp_increase]
        # = self.max_amp_increase  #  # self.expert_widget[self.data.max_amp_increase_val] = self.max_amp_increase_val  #  # #self.expert_widget[
        # self.data.num_fit_points] = self.num_fit_points  #  # self.expert_widget[self.data.num_fit_points_val] = self.num_fit_points_val  #  #
        # #self.expert_widget[self.data.active_power] = self.active_power  # self.expert_widget[  # self.data.active_power_val] =
        # self.active_power_val  # #self.expert_widget[  # self.data.num_future_traces] = self.num_future_traces  # self.expert_widget[  #
        # self.data.num_future_traces_val] = self.num_future_traces_val  # #self.expert_widget[  # self.data.keep_valve_open] =
        # self.keep_valve_open  # self.expert_widget[  # self.data.keep_valve_open_val] = self.keep_valve_open_val

    def update_modulator_status(self):
        widget = self.mod_state_outputwidget
        val = self.values[self.data.modulator_state]
        if type(val) is GUN_MOD_STATE:
            self.set_gun_mod_state(widget, val)
        elif type(val) is L01_MOD_STATE:
            self.set_L01_mod_state(widget, val)
        else:
            self.set_widget_color_text(widget, state.ERROR)

    # these enums will need updating, especially as we introduce more RF structures ...
    def set_gun_mod_state(self, widget, val):
        '''Replace all this cancer with a dictionary '''

        if val == GUN_MOD_STATE.RF_ON:
            self.set_widget_color(widget, state.GOOD)
            widget.setText('RF_ON')
        elif val == GUN_MOD_STATE.UNKNOWN_STATE:
            self.set_widget_color(widget, state.UNKNOWN)
            widget.setText('RF_ON')
        elif val == GUN_MOD_STATE.OFF:
            self.set_widget_color(widget, state.BAD)
            widget.setText('OFF')
        elif val == GUN_MOD_STATE.OFF_REQUEST:
            self.set_widget_color(widget, state.TIMING)
            widget.setText('OFF_REQUEST')
        elif val == GUN_MOD_STATE.HV_INTERLOCK:
            self.set_widget_color(widget, state.INTERLOCK)
            widget.setText('HV_INTERLOCK')
        elif val == GUN_MOD_STATE.HV_OFF_REQUEST:
            self.set_widget_color(widget, state.TIMING)
            widget.setText('HV_OFF_REQUEST')
        elif val == GUN_MOD_STATE.HV_REQUEST:
            self.set_widget_color(widget, state.TIMING)
            widget.setText('HV_REQUEST')
        elif val == GUN_MOD_STATE.HV_ON:
            self.set_widget_color(widget, state.INIT)
            widget.setText('HV_ON')
        elif val == GUN_MOD_STATE.STANDBY_REQUEST:
            self.set_widget_color(widget, state.TIMING)
            widget.setText('STANDBY_REQUEST')
        elif val == GUN_MOD_STATE.STANDBY:
            self.set_widget_color(widget, state.STANDBY)
            widget.setText('STANDBY')
        elif val == GUN_MOD_STATE.STANDYBY_INTERLOCK:
            self.set_widget_color(widget, state.INTERLOCK)
            widget.setText('STANDYBY_INTERLOCK')
        elif val == GUN_MOD_STATE.RF_ON_REQUEST:
            self.set_widget_color(widget, state.TIMING)
            widget.setText('RF_ON_REQUEST')
        elif val == GUN_MOD_STATE.RF_OFF_REQUEST:
            self.set_widget_color(widget, state.TIMING)
            widget.setText('RF_OFF_REQUEST')
        elif val == GUN_MOD_STATE.RF_ON_INTERLOCK:
            self.set_widget_color(widget, state.INTERLOCK)
            widget.setText('RF_ON_INTERLOCK')
        else:
            self.set_widget_color_text(widget, state.ERROR)
            widget.setText('ERROR')  # self.clip_vals[status] = str(widget.text())

    def set_L01_mod_state(self, widget, val):
        if val == L01_MOD_STATE.STATE_UNKNOWN:
            self.set_widget_color_text(widget, state.UNKNOWN)
            widget.setText('STATE_UNKNOWN')
        elif val == L01_MOD_STATE.L01_OFF:
            self.set_widget_color_text(widget, state.BAD)
            widget.setText('L01_OFF')
        elif val == L01_MOD_STATE.L01_STANDBY:
            self.set_widget_color_text(widget, state.STANDBY)
            widget.setText('L01_STANDBY')
        elif val == L01_MOD_STATE.L01_HV_ON:
            self.set_widget_color_text(widget, state.INIT)
            widget.setText('L01_HV_ON')
        elif val == L01_MOD_STATE.L01_RF_ON:
            self.set_widget_color_text(widget, state.GOOD)
            widget.setText('L01_RF_ON')  # self.clip_vals[status] = str(widget.text())

    def set_RF_prot(self, widget, val):
        if val == RF_PROT_STATUS.GOOD:
            self.set_widget_color_text(widget, state.GOOD)
        elif val == RF_PROT_STATUS.BAD:
            self.set_widget_color_text(widget, state.BAD)
        elif val == RF_PROT_STATUS.ERROR:
            self.set_widget_color_text(widget, state.ERROR)
        elif val == RF_PROT_STATUS.UNKNOWN:
            self.set_widget_color_text(widget, state.UNKNOWN)
        else:
            self.set_widget_color_text(widget, state.ERROR)

    def update_cav_pwr_ratio_and_max(self):
        '''
            Updates one GUI widget with current cavity power ratio and the max ratio allowed as defined in the config.yaml.
        '''
        cav_pwr_ratio = self.values[self.data.cav_pwr_ratio]
        max_cav_pwr_ratio = self.config.raw_config_data['CAV_PWR_RATIO']
        self.cav_pwr_ratio_outputwidget.setText('{:1.2f}%/ {}%'.format(cav_pwr_ratio, max_cav_pwr_ratio))
        self.set_widget_color(self.cav_pwr_ratio_outputwidget, self.values[self.data.cav_pwr_ratio_can_ramp])

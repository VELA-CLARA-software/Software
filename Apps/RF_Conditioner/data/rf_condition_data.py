import numpy as np
import matplotlib.pyplot as plt
import rf_condition_data_base as dat
from ramp import *


class rf_condition_data(dat.rf_condition_data_base):
    # whoami
    my_name = 'rf_condition_data'
    #
    # these are just monitors that are working
    # they are used for the main_loop
    # they are VAC,DC,BREAKDOWN,BREAKDOWN_RATE,RF
    main_monitor_states = {}
    previous_main_monitor_states = {}
    # settings from config file
    power_increase_1= None
    power_increase_2= None

    # log of last million pulses including:
    # Total ACTIVE Pulses, # breakdowns, amp_set, index (point on pulse / power curve) , pulse length
    last_million_log = None
    current_power = 0


    def __init__(self):
        dat.rf_condition_data_base.__init__(self)
        self.values = dat.rf_condition_data_base.values
        self.ramp_max_index = len(ramp) -1


    # these functions move up and down the ramp curve
    # and set the next increase, decrease values,
    # if ramping down delete previous entries that are above our new working point
    def move_up_ramp_curve(self):
        self.move_ramp_index(1)

    def move_down_ramp_curve(self):
        self.clear_last_sp_history()
        self.move_ramp_index(-1)

    def clear_last_sp_history(self):
        if len(dat.rf_condition_data_base.amp_sp_history) > 1:
            # delete last entry from amp_history
            dat.rf_condition_data_base.amp_sp_history = dat.rf_condition_data_base.amp_sp_history[:-1]
        # could maybe do this more clever like
        # if we only keep mean values, just delete last entry in mean pwr vs amp_sp data dicts
        dat.rf_condition_data_base.sp_pwr_hist = [x for x in dat.rf_condition_data_base.sp_pwr_hist if x[0] < dat.rf_condition_data_base.amp_sp_history[-1] ]
        # delete entries from amp_pwr_mean_data
        dat.rf_condition_data_base.amp_pwr_mean_data = {key: value for key, value in
                                                        dat.rf_condition_data_base.amp_pwr_mean_data.iteritems()
                     if key > dat.rf_condition_data_base.amp_sp_history[-1]}

    def move_ramp_index(self,val):
        print('move_ramp_index')
        self.values[dat.current_ramp_index] += val
        if self.values[dat.current_ramp_index] < 0:
            self.values[dat.current_ramp_index] = 0
        elif self.values[dat.current_ramp_index] > self.ramp_max_index:
            self.values[dat.current_ramp_index] = self.ramp_max_index
        self.set_ramp_values()


    def set_ramp_values(self):
        dat.rf_condition_data_base.values[dat.required_pulses] = ramp[dat.rf_condition_data_base.values[dat.current_ramp_index]][0]
        dat.rf_condition_data_base.values[dat.next_power_increase] = float(ramp[dat.rf_condition_data_base.values[dat.current_ramp_index]][1])

        self.set_next_sp_decrease()

        self.logger.header( self.my_name + ' set_ramp_values ', True)
        self.logger.message(['current ramp index   = ' + str(dat.rf_condition_data_base.values[dat.current_ramp_index]),
                             'next required pulses = ' + str(dat.rf_condition_data_base.values[dat.required_pulses]),
                             'next power increase  = ' + str(dat.rf_condition_data_base.values[dat.next_power_increase]),
                             'next sp decrease     = ' + str(dat.rf_condition_data_base.values[dat.next_sp_decrease])],True)

    def set_next_sp_decrease(self):
        a = dat.rf_condition_data_base.values[dat.next_sp_decrease]
        if len(dat.rf_condition_data_base.amp_sp_history) > 1:
            dat.rf_condition_data_base.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
        else:
            self.logger.message('Warning len(dat.rf_condition_data_base.amp_sp_history) not > 1')
            dat.rf_condition_data_base.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[0]
        self.logger.message('Changed next_sp_decrease from ' + str(a) + ' to ' + str(dat.rf_condition_data_base.values[dat.next_sp_decrease]))

    def get_new_sp(self):
        return self.get_new_set_point( self.get_next_power())

    def get_new_set_point_DEV(self,pwr_w):
        if len(dat.rf_condition_data_base.amp_pwr_mean_data ) > 3:

            self.x_tofit = np.array([])
            self.y_tofit = np.array([])
            for key,value in reversed(sorted(dat.rf_condition_data_base.amp_pwr_mean_data.iterkeys())):
                self.x_tofit = np.append(self.x_tofit ,key)
                self.y_tofit = np.append(self.y_tofit ,value[0])
                if len(x_tofit) == 4:
                    break
            self.m, self.c = np.polyfit(self.x_tofit, self.y_tofit, 1)

            self.current_power = self.y_tofit[0]
            self.requested_power = self.current_power + pwr_w

            self.predicted_sp = int((self.requested_power  - self.c) / self.m)

            #p =[predicted_sp, requested_power ]
            self.logger.header(self.my_name + ' get_new_set_point for power = ' ,True)
            self.logger.message('current sp/W   = ' + "%i"%self.x_tofit[0] + ", %.3E"%self.current_power, True)
            self.logger.message('predict sp/W   = ' + "%i"%self.predicted_sp +  ", %.3E"%self.requested_power, True)
            self.logger.message('Delta SP/power = ' + str(self.predicted_sp-self.x_tofit[0]) \
                                +str(self.requested_power - self.current_power), True)
            # plotting values
            self.x_plot = []
            self.y_plot = []
            for key,value in dat.rf_condition_data_base.amp_pwr_mean_data.iterkeys():
                self.x_plot.append(key)
                self.y_plot.append(value[0])
            self.x_min = min(self.x_tofit)
            self.x_max = max(self.x_tofit)
            self.plot(self.x_plot, self.y_plot, self.m, self.c, self.x_min, self.x_max, [self.predicted_sp, self.requested_power ])

        else:
#            self.logger.message('current sp/W = ' + str(self.current_power - self.previous_power) + ' ' + str(pwr_w),True)
            return None


        # neatean up!
    # neatean up!
    # neatean up!
    # neatean up!
    def get_new_set_point(self, pwr_win):
        self.previous_power = self.current_power
        x = np.array([i[0] for i in dat.rf_condition_data_base.sp_pwr_hist])
        y = np.array([i[1] for i in dat.rf_condition_data_base.sp_pwr_hist])
        # for p in x:
        #     print p,
        myset = sorted(set(x))

        self.current_power = np.mean(np.array([f[1] for f in dat.rf_condition_data_base.sp_pwr_hist if f[0] == max(myset)]))

        # frig because start-up is using sp steps
        pwr_w = pwr_win
        if len(myset) == 4:
            pwr_w = dat.rf_condition_data_base.values[dat.next_power_increase] = float(
                ramp[dat.rf_condition_data_base.values[dat.current_ramp_index]][1])
        if len(myset) > 3:
            dat.rf_condition_data_base.values[dat.next_power_increase] = float(
                ramp[dat.rf_condition_data_base.values[dat.current_ramp_index]][1])

            min_sp =list(myset)[-4]
            # print 'myset[-3] ' + str(min_sp)
            a = [[x2,y2] for x2,y2 in dat.rf_condition_data_base.sp_pwr_hist if x2 >= min_sp]

            # fit with np.polyfit
            x_tofit = np.array([i[0] for i in a])
            y_tofit = np.array([i[1] for i in a])

            x_min = min(x_tofit)
            x_max = max(x_tofit)

            current_power_data = [[x2,y2] for x2,y2 in a if x2==max(x_tofit)]
            #
            self.current_power = np.mean(np.array([i[1] for i in current_power_data]))

            m, c = np.polyfit(x_tofit, y_tofit, 1)
            print(m,c,self.current_power,dat.rf_condition_data_base.values[dat.last_mean_power], pwr_w )

            predict = int((self.current_power + pwr_w - c) / m)
            p =[predict,self.current_power + pwr_w]
            self.logger.header(self.my_name + ' get_new_set_point New SP',True)
            self.logger.message('current sp/W   = ' + "%.3E"%max(x_tofit) + ", %.3E"%self.current_power, True)
            self.logger.message('predict sp/W   = ' + "%.3E"%p[0] +  ", %.3E"%p[1], True)
            self.logger.message('currentx/request = ' + str(self.current_power - self.previous_power) + ' ' + str(pwr_w), True)
            self.plot(x,y,m,c,x_min,x_max,p)
            if m <=0:
                return None
            elif p[0] == x_max:
                return None
            else:
                return p[0]
        else:
            self.logger.message('current sp/W = ' + str(self.current_power - self.previous_power) + ' ' + str(pwr_w), True)
            return None



    def init_after_config_read(self):
        if self.llrf_config is not None:
            self.get_pulse_count_breakdown_log()
            self.values[dat.power_aim] = self.llrf_config['POWER_AIM']
            self.values[dat.pulse_length_start] = self.llrf_config['PULSE_LENGTH_START']
            self.values[dat.pulse_length_aim] = self.llrf_config['PULSE_LENGTH_AIM']
            self.values[dat.pulse_length_step] = self.llrf_config['PULSE_LENGTH_STEP']
            self.values[dat.breakdown_rate_aim] = self.llrf_config['BREAKDOWN_RATE_AIM']
            self.logger.header(self.my_name + ' init_after_config_read')
            self.logger.message([dat.pulse_length_start + ' ' +str(self.values[dat.pulse_length_start]),
            dat.pulse_length_aim + ' ' +str(self.values[dat.pulse_length_aim]),
            dat.pulse_length_step + ' ' +str(self.values[dat.pulse_length_step]),
            dat.breakdown_rate_aim + ' ' +str(self.values[dat.breakdown_rate_aim])])

    def update_last_million_pulse_log(self):
        self.last_million_log.pop()
        self.last_million_log.append([
            self.values[dat.pulse_count],
            self.values[dat.breakdown_count],
            self.values[dat.current_ramp_index],
            self.values[dat.pulse_length]]
        )
        while self.last_million_log[-1][0] - self.last_million_log[0][0]  > self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']:
            print('deleting ',self.last_million_log[0])
            self.last_million_log.pop(0)
        #
        # for i  in self.last_million_log:
        #     print i
        self.update_breakdown_stats()



    def update_breakdown_stats(self):
        self.values[dat.breakdown_count] = self.last_million_log[-1][1]
        self.values[dat.last_106_bd_count] = self.last_million_log[-1][1] - self.last_million_log[0][1]

        if self.last_million_log[-1][0] > self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']:
            self.values[dat.breakdown_rate] = self.values[dat.last_106_bd_count]
        else:
            if self.last_million_log[-1][0] == 0:
                self.values[dat.breakdown_rate] = 0
            else:
                self.values[dat.breakdown_rate] = \
            float(self.values[dat.last_106_bd_count] * self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']) \
            / \
            float(self.last_million_log[-1][0] - self.last_million_log[0][0])
        self.values[dat.breakdown_rate_hi] = self.values[dat.breakdown_rate] > self.values[dat.breakdown_rate_aim]


    def get_pulse_count_breakdown_log(self):
        # this is waaay too complicated
        pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        # based on the log file we set active pulse count total,
        # the starting point is the one before the last entry
        # save the last entry, number of breakdowns and breakdown rate
        # keep thsi seperate as pulse_count will get overwritten!!
        self.values[dat.log_pulse_count] = int(pulse_break_down_log[-1][0])
        self.values[dat.breakdown_count] = int(pulse_break_down_log[-1][1])
        # first amp is the second to last one in log file
        last_amp_sp_in_file = int(pulse_break_down_log[-1][2])
        # remove values greater than than last_amp_sp_in_file
        to_remove = []
        temp = 0
        for i in pulse_break_down_log:
            if i[2] > last_amp_sp_in_file:
                to_remove.append(temp)
            temp += 1
        for i in reversed(to_remove):
            del pulse_break_down_log[i]
        # sort the list by sp (part 2) then pulse (part 0)
        sorted_pulse_break_down_log_1 = sorted(pulse_break_down_log, key=lambda x: (x[2], x[0]))
        # the final list is the sp point with highest pulse count
        sorted_pulse_break_down_log_2 = []
        last_i = sorted_pulse_break_down_log_1[0]
        for i in sorted_pulse_break_down_log_1:
            #print i
            if last_i[2] == i[2]:
                pass
            else:
                sorted_pulse_break_down_log_2.append(i)
            last_i=i
        # delete the last element
        del sorted_pulse_break_down_log_2[-1]
        print('rationalised pulse log ')
        for i in sorted_pulse_break_down_log_2:
            print i

        # next we must insert the values
        # set the ramp index
        self.values[dat.current_ramp_index] = sorted_pulse_break_down_log_2[-1][3]
        # sp history
        dat.rf_condition_data_base.amp_sp_history = [int(i[2]) for i in sorted_pulse_break_down_log_2 ]
        # amp_set
        self.values[dat.log_amp_set] = dat.rf_condition_data_base.amp_sp_history[-1]
        # next decrease
        self.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
        # pulse length
        self.values[dat.log_pulse_length] = float(sorted_pulse_break_down_log_2[-1][4]) / float(1000.0)# warning UNIT
        self.llrf_config['PULSE_LENGTH_START'] = self.values[dat.log_pulse_length]
        # next number of pulses
        self.values[dat.required_pulses]=self.llrf_config['DEFAULT_PULSE_COUNT']


        self.logger.header( self.my_name + ' pulse_count_breakdown_log ', True)
        self.logger.message([
            dat.log_pulse_count + ' ' + str(self.values[dat.log_pulse_count]),
            dat.required_pulses + ' ' + str(self.values[dat.required_pulses]),
            dat.breakdown_count + ' ' + str(self.values[dat.breakdown_count]),
            dat.log_amp_set + ' ' + str(self.values[dat.log_amp_set]),
            dat.current_ramp_index + ' ' + str(self.values[dat.current_ramp_index]),'pulse length = ' + str(self._llrf_config['PULSE_LENGTH_START']),
            dat.next_sp_decrease + ' ' + str(self.values[dat.next_sp_decrease])
        ],True)
        # set the last 10^6 breakdown last_106_bd_count
        # find the breakdown count self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY'] pulse before
        temp = self.values[dat.log_pulse_count] - self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']
        temp_2 = [x for x in pulse_break_down_log if x[0] >= temp ]
        sorted_pulse_break_down_log_2.insert(0,temp_2[0])
        self.last_million_log = [x for x in sorted_pulse_break_down_log_2 if x[0] >= temp ]
        self.last_million_log[-1][1] = self.values[dat.breakdown_count]
        self.last_million_log[-1][0] = self.values[dat.log_pulse_count]
        self.logger.header('Last million pulses',True)
        self.logger.message('Million pulses agao  = ' + str(temp),True)

        # for i in self.last_million_log:
        #     print 'get_last_million_pulse ',i
        self.update_breakdown_stats()


    # REPLACE WITH LOOKUP TABLE FO RPOWER - EVENT PULSES

    def ceiling(self,x, base=1000):
        if base ==0:
            print 'MAJOR ERROR'
        return int(base * np.ceil(float(x) / base))

    def power_increase(self):
        # will break if setting in config have not been passed
        if self.values[dat.pulse_count] < self.power_increase_2:
            a = self.power_increase_1 * self.values[dat.pulse_count]
        else:
            a = self._llrf_config['NORMAL_POWER_INCREASE']
        print(self.my_name + ' power_increase = ' +str(a) + ' ' + str(self.ceiling(a, self._llrf_config['LOW_POWER_INCREASE'])) )
        return self.ceiling(a, self._llrf_config['LOW_POWER_INCREASE'])

    # neaten up, do we have to redraw each time?
    def plot(self,x,y,m,c,x0,x1,predict):
        plt.clf()
        plt.plot(x, y, '.')
        plt.plot( np.unique([self.old_x_min,self.old_x_max]), self.old_m * np.unique([self.old_x_min,self.old_x_max]) + self.old_c, '-')
        plt.plot( np.unique([x0,x1]), m * np.unique([x0,x1]) + c, '-')
        plt.plot(predict[0],predict[1], '*')
        plt.draw()
        plt.pause(0.00001)
        self.old_x_min = x0
        self.old_x_max = x1
        self.old_m = m
        self.old_c = c
    #close function
    def close(self):
        plt.close()





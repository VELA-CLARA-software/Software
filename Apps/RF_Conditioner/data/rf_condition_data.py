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


    def __init__(self):
        dat.rf_condition_data_base.__init__(self)
        self.values = dat.rf_condition_data_base.values

    # def get_next_ramp_values(self):
    #     self.values[dat.next_sp_decrease]


    def ramp_up(self):
        self.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]
        self.move_ramp_index(1)

    def ramp_down(self):
        self.move_ramp_index(-1)

    def clear_last_sp_history(self):
        limit = dat.rf_condition_data_base.amp_sp_history[-2]
        print('limit = ', limit)
        # could maybe do this more clever like
        dat.rf_condition_data_base.amp_sp_history = [x for x in dat.rf_condition_data_base.amp_sp_history if x <= limit ]
        dat.rf_condition_data_base.sp_pwr_hist = [x for x in dat.rf_condition_data_base.sp_pwr_hist if x[0] <= limit ]

    def move_ramp_index(self,val):
        self.values[dat.log_index] += val
        self.set_ramp_values()


    def set_ramp_values(self):
        self.values[dat.required_pulses] = ramp[self.values[dat.log_index]][0]
        self.values[dat.next_power_increase] = ramp[self.values[dat.log_index]][1]

        self.logger.header( self.my_name + ' set_ramp_values ', True)
        self.logger.message(['next required pulses =' + str(self.values[dat.required_pulses]),
                             'next power increase  =' + str(self.values[dat.next_power_increase]),
                             'next sp decrease  =' + str(self.values[dat.next_sp_decrease])])


    def get_new_sp(self):
        return self.get_new_set_point( self.get_next_power())

    # neatean up!
    def get_new_set_point(self,pwr_kw):
        self.previous_power = self.current_power
        x = np.array([i[0] for i in self.sp_pwr_hist])
        y = np.array([i[1] for i in self.sp_pwr_hist]) / 1000
        # for p in x:
        #     print p,
        myset = sorted(set(x))
        if len(myset) > 3:
            min_sp =list(myset)[-4]
            # print 'myset[-3] ' + str(min_sp)
            a = [[x2,y2] for x2,y2 in self.sp_pwr_hist if x2>=min_sp]

            # fit with np.polyfit
            x_tofit = np.array([i[0] for i in a])
            y_tofit = np.array([i[1] for i in a]) / 1000

            x_min = min(x_tofit)
            x_max = max(x_tofit)

            current_power_data = [[x2,y2] for x2,y2 in a if x2==max(x_tofit)]

            #print(current_power_data)

            self.current_power = np.mean(  np.array([i[1] for i in current_power_data]) ) / 1000

            m, c = np.polyfit(x_tofit, y_tofit, 1)

            predict = (self.current_power + pwr_kw - c) / m
            p =[predict,self.current_power + pwr_kw]
            print('current = ', "%.3E"%max(x_tofit),"%.3E"%self.current_power)
            print('predict = ', "%.3E"%p[0],"%.3E"%p[1])
            print('Measured Power increase = ' + str(self.current_power - self.previous_power))
            self.plot(x,y,m,c,x_min,x_max,p)
            return p[0]
        else:
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
            self.values[dat.log_index],
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
            self.values[dat.breakdown_rate] = \
            float(self.values[dat.last_106_bd_count] * self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']) \
            / \
            float(self.last_million_log[-1][0] - self.last_million_log[0][0])
        self.values[dat.breakdown_rate_hi] = self.values[dat.breakdown_rate] > self.values[dat.breakdown_rate_aim]


    def get_pulse_count_breakdown_log(self):
        pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        #for x in self.pulse_break_down_log:
        # based on the log file we set active pulse count total,
        # number of breakdowns and breakdown rate
        self.values[dat.log_active_pulse_count] = int(pulse_break_down_log[-1][0])
        self.values[dat.pulse_count] = self.values[dat.log_active_pulse_count]
        self.values[dat.log_breakdown_count] = int(pulse_break_down_log[-1][1])
        self.values[dat.log_amp_set] = int(pulse_break_down_log[-1][2])

        dat.rf_condition_data_base.amp_sp_history = sorted(list(set( [ int(i[2]) for i in pulse_break_down_log] )))

        self.values[dat.next_sp_decrease] = dat.rf_condition_data_base.amp_sp_history[-2]

        self.values[dat.log_index] = int(pulse_break_down_log[-1-2][3])# WARNING we add a rpeat of th elast last_million_log !



        self.values[dat.log_pulse_length] = float(pulse_break_down_log[-1][4]) / float(1000.0)
        self.set_ramp_values()

        self.llrf_config['PULSE_LENGTH_START'] = ( pulse_break_down_log[-1][4] * 0.001)# !!!

        self.logger.header( self.my_name + ' pulse_count_breakdown_log ', True)
        self.logger.message([
            dat.log_active_pulse_count + ' ' + str(self.values[dat.log_active_pulse_count]),
            dat.log_breakdown_count + ' ' + str(self.values[dat.log_breakdown_count]),
            dat.log_amp_set + ' ' + str(self.values[dat.log_amp_set]),
            dat.log_index + ' ' + str(self.values[dat.log_index]),' PULSE_LENGTH_START = ' + str(self._llrf_config['PULSE_LENGTH_START']),
            dat.next_sp_decrease + ' ' + str(self.values[dat.next_sp_decrease])
        ],True)

        # set the last 10^6 breakdown last_106_bd_count
        temp = pulse_break_down_log[-1][0] - self.llrf_config['NUMBER_OF_PULSES_IN_BREAKDOWN_HISTORY']
        self.last_million_log = [x for x in pulse_break_down_log if x[0] >= temp ]
        #[x for x in if x[0] > temp ]
        for i in self.last_million_log:
            print 'get_last_million_pulse ',i
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

    def power_increase_set_up(self):
        #these are constants in the power_increase function
        self.power_increase_1 = self._llrf_config['RF_INCREASE_RATE'] * \
                                self._llrf_config['NORMAL_POWER_INCREASE'] / \
                                self._llrf_config['LOW_POWER_INCREASE_RATE_LIMIT']
        self.power_increase_2 = self._llrf_config['LOW_POWER_INCREASE_RATE_LIMIT'] / \
                                self._llrf_config['RF_INCREASE_RATE']

        self.logger.header( self.my_name + ' power_increase_set_up  ', True)
        self.logger.message(['power_increase_set_up: ' + str(self._llrf_config['RF_INCREASE_RATE']) + '  ' + str(
        self._llrf_config['NORMAL_POWER_INCREASE']) + ' ' + str(self._llrf_config['LOW_POWER_INCREASE_RATE_LIMIT']),
        self.my_name + ' power_increase_set_up: power_increase_1  =  ' + str(self.power_increase_1) +
         ' power_increase_2 = ' + str(self.power_increase_2)])



    def get_next_power(self):
        pwr_inc = self.power_increase()
        power = self.ceiling( self.values[dat.pulse_count] * self._llrf_config['RF_INCREASE_RATE'], pwr_inc )
        print(self.my_name + ' get_next_power: power_inc = ' + str(pwr_inc) + ', power =   ' + str(power) )
        return pwr_inc / 1000 # kW !



    # neaten up, do we have to redraw each time?
    def plot(self,x,y,m,c,x0,x1,predict):
        plt.clf()
        plt.plot(x, y, '.')
        plt.plot( np.unique([self.old_x0,self.old_x1]), self.old_m * np.unique([self.old_x0,self.old_x1]) + self.old_c, '-')
        plt.plot( np.unique([x0,x1]), m * np.unique([x0,x1]) + c, '-')
        plt.plot(predict[0],predict[1], '*')
        plt.draw()
        plt.pause(0.00001)
        self.old_x0 = x0
        self.old_x1 = x1
        self.old_m = m
        self.old_c = c
    #close function
    def close(self):
        plt.close()





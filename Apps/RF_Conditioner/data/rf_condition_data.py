import numpy as np
import matplotlib.pyplot as plt
import rf_condition_data_base as dat


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
    llrf_param = None
    power_increase_1= None
    power_increase_2= None

    pulse_break_down_log = None

    def __init__(self,logger=None):
        dat.rf_condition_data_base.__init__(self,logger=logger)
        self.llrf = None



    def power_increase_set_up(self):
        #these are constants in the power_increase function
        self.power_increase_1 = self.llrf_param['RF_INCREASE_RATE'] * self.llrf_param['NORMAL_POWER_INCREASE'] / self.llrf_param['LOW_POWER_INCREASE_RATE_LIMIT']
        self.power_increase_2 = self.llrf_param['LOW_POWER_INCREASE_RATE_LIMIT'] / self.llrf_param['RF_INCREASE_RATE']
        print(self.my_name + ' power_increase_set_up: ' + str(self.llrf_param['RF_INCREASE_RATE']) + '  ' + str(self.llrf_param['NORMAL_POWER_INCREASE']) + ' ' + str(self.llrf_param['LOW_POWER_INCREASE_RATE_LIMIT']))
        print(self.my_name + ' power_increase_set_up: power_increase_1  =  ' + str(
            self.power_increase_1) + ' power_increase_2 = ' + str(self.power_increase_2))

    def get_pulse_count_breakdown_log(self):
        self.pulse_break_down_log = self.logger.get_pulse_count_breakdown_log()
        for x,y in self.pulse_break_down_log:
            print ('get_pulse_count_breakdown_log', x,y)


    def close(self):
        plt.close()

    def ceiling(self,x, base=1000):
        if base ==0:
            print 'MAJOR ERROR'
        return int(base * np.ceil(float(x) / base))

    def power_increase(self):
        # will break if setting in config have not been passed
        if self.values[dat.pulse_count] < self.power_increase_2:
            a = self.power_increase_1 * self.values[dat.pulse_count]
        else:
            a = self.llrf_param['NORMAL_POWER_INCREASE']
        print(self.my_name + ' power_increase = ' +str(a) + ' ' + str(self.ceiling(a, self.llrf_param['LOW_POWER_INCREASE'])) )
        return self.ceiling(a, self.llrf_param['LOW_POWER_INCREASE'])

    def get_next_power(self):
        pwr_inc = self.power_increase()
        power = self.ceiling( self.values[dat.pulse_count] * self.llrf_param['RF_INCREASE_RATE'], pwr_inc )
        print(self.my_name + ' get_next_power: power_inc = ' + str(pwr_inc) + ', power =   ' + str(power) )
        return pwr_inc / 1000 # kW !

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






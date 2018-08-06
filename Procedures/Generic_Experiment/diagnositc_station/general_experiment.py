from screen import screen
from magnet import magnet
from shutter import shutter
from camera import camera
from data_logger import Data_Logger
import gen_ex_config
import time

class general_experiment(object):
    screen_obj  = None
    camera_obj  = None
    shutter_obj = None
    magnet_obj  = None

    screen_working = False
    magnet_working = False
    camera_working = False
    shutter_working = False

    should_check_screen_working = True
    should_check_magnet_working = True
    should_check_camera_working = True
    should_check_shutter_working = True

    def __init__(self,config_file='',log_dir=''):
        '''
        set the log_file in the data logger
        :param config_file:
        :param log_file:
        '''
        self.logger = Data_Logger()
        self.logger.start_log(log_dir,log_file='log.txt')
        '''
            Read the config file
            :param filename:
        '''
        self.config = gen_ex_config.gen_ex_config(config_file)
        if  self.config.screen_data:
            self.logger.message('Creating screen controller object',True)
            general_experiment.screen_obj = \
                screen(mode = self.config.screen_data[gen_ex_config.machine_mode],
                       area = self.config.screen_data[gen_ex_config.machine_area])
            self.logger.message('SUCCESS Creating screen controller object',True)

        else:
            general_experiment.should_check_screen_working = False

        if  self.config.magnet_data:
            self.logger.message('Creating magnet controller object',True)
            general_experiment.magnet_obj = \
                magnet(mode = self.config.magnet_data[gen_ex_config.machine_mode],
                       area = self.config.magnet_data[gen_ex_config.machine_area])
            self.logger.message('SUCCESS Creating magnet controller object',True)
        else:
            general_experiment.should_check_magnet_working = False

        if  self.config.shutter_data is not None:
            general_experiment.shutter_obj = \
                shutter(mode = self.config.shutter_data[gen_ex_config.machine_mode],
                        area = self.config.shutter_data[gen_ex_config.machine_area])
        else:
            general_experiment.should_check_shutter_working = False

        if  self.config.camera_data is not None:
            general_experiment.camera_obj = \
                camera(mode = self.config.camera_data[gen_ex_config.machine_mode],
                       area = self.config.camera_data[gen_ex_config.machine_area])
        else:
            general_experiment.should_check_camera_working = False


        #self.run_exp()

    def run_exp(self):
        print('applying settings')
        for i in range(1,2):
            print('Applying Settings part, ' + str(i))
            self.apply_settings(i)
            while self.settings_not_applied():
                time.sleep(1)
                print('Settings Not Applied part, ' + str(i))
        raw_input()

    def settings_not_applied(self):
        print 'settings_not_applied'

        if general_experiment.should_check_screen_working:
            if self.config.screen_data:
                general_experiment.screen_working = general_experiment.screen_obj.is_busy()
                if general_experiment.screen_working:
                    print('Waiting for screen')
                else:
                    general_experiment.should_check_screen_working = False

        if general_experiment.should_check_magnet_working:
            if self.config.magnet_data:
                general_experiment.magnet_working =  general_experiment.magnet_obj.is_busy()
                if general_experiment.magnet_working:
                    print('Waiting for magnet')
                else:
                    general_experiment.should_check_magnet_working = False

        if general_experiment.should_check_camera_working:
            if self.config.camera_data:
                general_experiment.camera_working = general_experiment.camera_obj.is_busy()
                if general_experiment.camera_working:
                    print('Waiting for camera')
                else:
                    general_experiment.should_check_camera_working = False

        if general_experiment.should_check_shutter_working:
            if self.config.shutter_data:
                general_experiment.shutter_working =  general_experiment.shutter_obj.is_busy()
                if general_experiment.shutter_working:
                    print('Waiting for shutter')
            else:
                general_experiment.should_check_shutter_working = False

        if general_experiment.screen_working:
            return True
        if general_experiment.camera_working:
            return True
        if general_experiment.magnet_working:
            return True
        if general_experiment.shutter_working:
            return True
        return False

    def apply_settings(self,num):
        if self.config.screen_data:
            general_experiment.screen_obj.next_step(num)
        if self.config.magnet_data:
            general_experiment.magnet_obj.next_step(num)
        if self.config.camera_data:
            general_experiment.camera_obj.next_step(num)
        if self.config.shutter_data:
            general_experiment.shutter_obj.next_step(num)









    # magnet_data = None
    # camera_data = None
    # shutter_data = None
#
#
# screentest = screen.screen()
#
# if screentest.has_controller:
#     print('Have screen controller')
#
# print 'set procedure'
# raw_input()
#
#
#
# raw_input()
# raw_input()
#
# it1 = [['S02-SCR-01',SCREEN_STATE.SCREEN_IN],
#        ['S02-SCR-02',SCREEN_STATE.SCREEN_OUT],
#       ]
#
# it2 = [['S02-SCR-01',SCREEN_STATE.SCREEN_OUT],
#        ['S02-SCR-02',SCREEN_STATE.SCREEN_IN],
#       ]
#
# procedure_good = screentest.test_procedure([it1,it2])
#
# if procedure_good:
#     print('procedure good')
# else:
#     print('procedure bad')
#
# screentest.next_step(it1)
#
# while screentest.is_busy:
#     print 'waiting for screen'
#     time.sleep(2)
# print 'screen it finished'
# print 'fin'
# raw_input()
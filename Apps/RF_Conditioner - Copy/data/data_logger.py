


class data_logger(object):

    def __init__(self,
                 log_param,

                 )





        def start_data_logging(self, log_param):
            print(self.my_name + ' starting monitoring, update time = ' + \
                  str(log_param['DATA_LOG_TIME']))  # MAGIC_STRING
            self.data_log_directory = log_param['DATA_LOG_DIRECTORY']  # MAGIC_STRING
            self.data_log_filename = log_param['DATA_LOG_FILENAME']  # MAGIC_STRING

            self.log_start = datetime.datetime.now()
            time = str(self.log_start.year) + '-' + \
                   '{:02d}'.format(self.log_start.month) + '-' + \
                   '{:02d}'.format(self.log_start.day) + '-' + \
                   '{:02d}'.format(self.log_start.hour) + '-' + \
                   '{:02d}'.format(self.log_start.minute) + '-' + \
                   '{:02d}'.format(self.log_start.second)
            self.path = self.data_log_directory + self.data_log_filename + '_' + time


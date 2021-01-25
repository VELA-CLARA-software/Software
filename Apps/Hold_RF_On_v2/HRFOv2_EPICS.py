'''
Author: Anthony Gilfellon
Date:   25/01/2021
'''

from HRFOv2_EPICS_main_controller import main_controller
from HRFOv2_EPICS_reader import reader

class CASCADE_2():
    '''
        Mainly a wrapper class that just gets things started.
    '''

    def __init__(self):
        # read config
        read = reader()
        read.read_yaml()
        #Start main sequence
        main_controller()


if __name__ == '__main__':
    print('\nStarting HRFOv2_EPICS.\n')
    CASCADE_2()
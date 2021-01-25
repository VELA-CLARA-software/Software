from dataclasses import dataclass
import numpy as np, cmath, math
from decimal import Decimal, getcontext
import re
from HRFOv2_EPICS_figures import figures


# set number of decimal places for Decimal to use....
getcontext().prec = 20

# @dataclass
# class C2_data:
#     # #def __init__(self, title, author, pages, price):
#     # title : str
#     # author : str
#     # pages : int
#     # price : float
#     Interpolated_datapath: str
#     Master_Dict_path: str
#     savepath: str
#     NBIN: int
#     Results_Power: list

class bcolors:
    '''
    Provides colours for print outs for ease of reading if required
    '''
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

class data_functions():
    '''
    handles all operations on data
    '''
    def __init__(self):
        print('Initiated data_functions()')

    def remove_char_from_str(self, string_1):
        '''
        Removes characters in '[!@#$:]' form string and returns ammended string
        :param string_1:
        :return:
        '''
        self.string_1 = string_1

        self.string_2 = re.sub('[!@#$:]', '', self.string_1)

        return self.string_2

# Values dictionary:

values = {}  # Initiated empty dictionary
all_value_keys = []  # A list of the keys for values
Dummy_int = int(-999999)
Dummy_float = float(-999.999)
Dummy_decimal = Decimal(-999.999)

#TODO: make a dictionary of
# PV names,
# savenames (PV name minus the ":" character,
# and PV index.

all_mod_PVs = 'all_mod_PVs'
all_value_keys.append(all_mod_PVs)
values[all_mod_PVs] = []

interlock_PVs = 'interlock_PVs'
all_value_keys.append(interlock_PVs)
values[interlock_PVs] = []

savepath = 'savepath'
all_value_keys.append(savepath)
values[savepath] = 'Dummy str'

PV_idx_dict = 'PV_idx_dict'
all_value_keys.append(PV_idx_dict)
values[PV_idx_dict] = {}

PV_TIME_DATA = 'PV_TIME_DATA'
all_value_keys.append(PV_TIME_DATA)
values[PV_TIME_DATA] = []

PV_YAXIS_DATA = 'PV_YAXIS_DATA'
all_value_keys.append(PV_YAXIS_DATA)
values[PV_YAXIS_DATA] = []

READ_PVs = 'READ_PVs'
all_value_keys.append(READ_PVs)
values[READ_PVs] = True

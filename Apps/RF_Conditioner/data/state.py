from enum import Enum


# flags states for different monitors
class state(Enum):
    BAD = 0
    GOOD = 1
    UNKNOWN = 2
    INIT = 3
    NEW_BAD = 4
    NEW_GOOD = 5

    statename = { 0: 'BAD', 1: 'GOOD', 2:'UNKNOWN',3:'INIT',4:'NEW_BAD',5:'NEW_GOOD'}
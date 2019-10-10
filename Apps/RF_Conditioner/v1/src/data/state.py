from enum import Enum


# flags states for different monitors
class state(Enum):
    BAD = 0
    GOOD = 1
    UNKNOWN = 2
    INIT = 3
    NEW_BAD = 4
    NEW_GOOD = 5
    TIMING = 6
    ERROR = 7
    INTERLOCK = 8
    STANDBY = 9

    statename = { BAD: 'BAD', GOOD: 'GOOD', UNKNOWN:'UNKNOWN', INIT:'INIT', NEW_BAD:'NEW_BAD',NEW_GOOD:'NEW_GOOD',
                  TIMING:'TIMING', ERROR: 'ERROR', INTERLOCK:'INTERLOCK', STANDBY:'STANDBY' }
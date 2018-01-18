from enum import Enum


# flags states for different monitors
class state(Enum):
    BAD = 0
    GOOD = 1
    UNKNOWN = 2
    INIT = 3
    NEW_BAD = 4
    NEW_GOOD = 5
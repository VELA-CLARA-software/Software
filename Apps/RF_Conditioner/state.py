from enum import Enum


# flags states for different monitors
class state(Enum):
    BAD = 0
    GOOD = 1
    UNKNOWN = 2
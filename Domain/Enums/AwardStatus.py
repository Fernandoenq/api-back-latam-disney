from enum import Enum


class AwardStatus(Enum):
    on_hold = 1
    rescued = 2
    lost = 3
    in_test = 99

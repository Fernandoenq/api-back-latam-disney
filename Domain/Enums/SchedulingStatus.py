from enum import Enum


class SchedulingStatus(Enum):
    available = 1
    busy = 2
    confirmed = 3

from enum import auto, Enum
from ca.color import Color


class GrainType(Enum):
    INCLUSION = 'inclusion'
    GRAIN = 'grain'
    OUT_OF_RANGE = 'out of range'
    EMPTY = None


class Grain:
    def __init__(self, state=None, type=GrainType.GRAIN):
        self.prev_state = state
        self.state = state
        self.type = type

    def check_neighbours(self):
        pass

    @property
    def color(self):
        return Color.state_color(self.state)

    def __str__(self):
        return str(self.state)

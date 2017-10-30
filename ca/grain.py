from enum import Enum
from ca.color import Color


class GrainType(Enum):
    INCLUSION = 'inclusion'
    GRAIN = 'grain'
    OUT_OF_RANGE = 'out of range'
    EMPTY = None


class Grain:
    EMPTY = 0
    INCLUSION = -1
    OUT_OF_RANGE = -2

    def __init__(self, state=None):
        if state is None:
            state = Grain.EMPTY
        self.prev_state = state
        self.state = state

    @property
    def color(self):
        if self.state is Grain.INCLUSION:
            return Color.BLACK
        return Color.state_color(self.state)

    @property
    def can_be_modified(self) -> bool:
        """
        :return: boolean that tells whether grain can be modified (is neither inclusion, filled nor out of range)
        """
        return self.state == Grain.EMPTY

    @property
    def has_unq_state(self):
        return self.prev_state > Grain.EMPTY

    def __str__(self):
        return str(self.state)

    def __bool__(self):
        return self.state > Grain.EMPTY

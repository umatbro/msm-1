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
    LOCKED = -2

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value
        if self.state is Grain.INCLUSION:
            self.color = Color.BLACK
            self.locked = True
        else:
            self.color = Color.state_color(self.state)

    @property
    def locked(self):
        return self.__locked

    @locked.setter
    def locked(self, locked):
        self.__locked = locked
        self.color = Color.state_color(self.state) if not self.locked else Color.LIGHTPINK

    def __init__(self, state=None):
        self.color = None
        self.__locked = False
        self.__state = None
        if state is None:
            state = Grain.EMPTY
        self.prev_state = state
        self.state = state

    # @property
    # def color(self):
    #     if self.state is Grain.INCLUSION:
    #         return Color.BLACK
    #     return Color.state_color(self.state)

    @property
    def can_be_modified(self) -> bool:
        """
        :return: boolean that tells whether grain can be modified (is neither inclusion, filled nor out of range)
        """
        return self.state == Grain.EMPTY

    @property
    def can_influence_neighbours(self) -> bool:
        """
        :return: boolean indicating whether grain can influence other grains
        (meaning it is neither inclusion, nor locked)
        """
        return self.state > Grain.EMPTY and not self.locked

    @property
    def has_unq_state(self):
        return self.prev_state > Grain.EMPTY

    def __str__(self):
        return str(self.state)

    def __bool__(self):
        return self.prev_state > Grain.EMPTY

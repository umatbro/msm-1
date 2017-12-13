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
    ALIVE = -3
    LOCKED = -4
    DUAL_PHASE = -5
    SELECTED = -6

    @property
    def state(self):
        return self.__state

    @state.setter
    def state(self, value):
        self.__state = value
        self.color = Color.state_color(self.state)

        if self.state is Grain.INCLUSION:
            self.lock_status = Grain.LOCKED
            self.color = Color.BLACK

        elif self.state is Grain.DUAL_PHASE:
            self.lock_status = Grain.LOCKED
            self.color = Color.GREY

    @property
    def lock_status(self):
        return self.__lock_status

    @lock_status.setter
    def lock_status(self, value):
        self.__lock_status = value
        if self.lock_status is Grain.SELECTED:
            self.color = Color.LIGHTPINK
        elif self.lock_status is Grain.DUAL_PHASE:
            self.state = Grain.DUAL_PHASE
        else:
            self.color = Color.state_color(self.state)
            if self.state is Grain.DUAL_PHASE:
                self.color = Color.GREY

    def __init__(self, state=None):
        self.color = None
        self.__lock_status = None
        self.__state = None

        if state is None:
            state = Grain.EMPTY
        self.lock_status = Grain.ALIVE
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
        return self.state == Grain.EMPTY and self.lock_status == Grain.ALIVE

    @property
    def can_influence_neighbours(self) -> bool:
        """
        :return: boolean indicating whether grain can influence other grains
        (meaning it is neither inclusion, nor locked)
        """
        return self.state > Grain.EMPTY and self.lock_status > Grain.LOCKED

    @property
    def has_unq_state(self):
        return self.prev_state > Grain.EMPTY

    @property
    def is_locked(self):
        return self.lock_status < Grain.ALIVE

    def toggle_selected(self):
        self.lock_status = Grain.SELECTED if self.lock_status is Grain.ALIVE else Grain.ALIVE

    def __str__(self):
        return str(self.state)

    def __bool__(self):
        return self.prev_state > Grain.EMPTY or self.lock_status < Grain.ALIVE

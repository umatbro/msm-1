from enum import Enum
from ca.color import Color
from um.visuals import color


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

        if self.state is Grain.INCLUSION:
            self.lock_status = Grain.LOCKED

        elif self.state is Grain.DUAL_PHASE:
            self.lock_status = Grain.LOCKED

    @property
    def lock_status(self):
        return self.__lock_status

    @lock_status.setter
    def lock_status(self, value):
        self.__lock_status = value

    def __init__(self, state=None):
        self.__lock_status = None
        self.__state = None

        if state is None:
            state = Grain.EMPTY
        self.lock_status = Grain.ALIVE
        self.prev_state = state
        self.state = state
        self.energy_value = 0

    @property
    def color(self):
        if self.state is Grain.INCLUSION:
            return Color.BLACK
        if self.lock_status is Grain.SELECTED:
            return Color.LIGHTPINK
        if self.lock_status is Grain.DUAL_PHASE or self.state is Grain.DUAL_PHASE:
            return Color.GREY
        return Color.state_color(self.state)

    @property
    def energy_color(self):
        if self.energy_value == 5:
            return color.BLUE500
        if self.energy_value == 2:
            return color.LIGHT_GREEN300
        if self.energy_value == 0:
            return color.WHITE
        raise Exception('Cell energy value ({}) not expected'.format(self.energy_value))

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

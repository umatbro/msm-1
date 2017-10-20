import random

import pygame
from ca.color import Color

from ca.grain import Grain, GrainType
from statistics import mode, StatisticsError


class GrainField:
    """
    :ivar resolution: number of pixels in square side
    """

    def __init__(self, x_size, y_size, resolution=10):
        if type(x_size) or type(y_size) is float:
            x_size = int(x_size)
            y_size = int(y_size)
        self.width = x_size
        self.height = y_size
        self.resolution = resolution

        # init list
        self.field = [[Grain() for y in range(self.height)] for x in range(self.width)]

    def von_neumann(self, x, y):
        """
        Check grain neighbours in x, y coordinates

        :return: tuple (left, top, right, bottom)
        """
        return (
            self.field[x - 1][y] if x > 0 else Grain(type=GrainType.OUT_OF_RANGE),  # left
            self.field[x][y - 1] if y > 0 else Grain(type=GrainType.OUT_OF_RANGE),  # top
            self.field[x + 1][y] if x < self.width - 1 else Grain(type=GrainType.OUT_OF_RANGE),  # right
            self.field[x][y + 1] if y < self.height - 1 else Grain(type=GrainType.OUT_OF_RANGE),  # bottom
        )

    def upd(self):
        # go through all grains
        # check state - if prev state is not none go next
        # if prev state is none check neighbours and set state
        # update prev state
        for x in range(self.width):
            for y in range(self.height):
                grain = self.field[x][y]
                # if there is inclusion in grain - do nothing with this grain
                if grain.type is GrainType.INCLUSION:
                    continue
                if grain.state is not None and grain.state is not 0:
                    grain.prev_state = grain.state
                    continue
                # grain.prev_state = grain.state
                neighbours = self.von_neumann(x, y)
                grain.state = decide_state(neighbours)

        # after all current states are set - update prev state
        for y in range(self.height):
            for x in range(self.width):
                grain = self.field[x][y]
                grain.prev_state = grain.state

    def display(self, screen):
        rect = pygame.Rect(0, 0, self.resolution, self.resolution)
        for x, col in enumerate(self.field):  # type: list
            rect.x = x * self.resolution
            for y, grain in enumerate(col):
                color = grain.color
                rect.y = y * self.resolution
                pygame.draw.rect(screen, color, rect)
                # if resolution is less than 5 don't draw borders
                if self.resolution > 5:
                    pygame.draw.rect(screen, Color.BLACK.value, rect, 1)

    def set_grain_state(self, x, y, state):
        grain = self.field[x][y]  # type: Grain
        grain.state = state
        grain.prev_state = grain.state

    def __str__(self):
        result = '\n'
        for x in range(self.width):
            for y in range(self.height):
                grain = self.field[x][y]
                result += '{} '.format(grain.state if grain.state is not None else 0)
            result += '\n'
        return result

    def str(self):
        grains = []
        for x in range(self.width):
            for y in range(self.height):
                grains.append(self.field[x][y])

        if not any([grain.state for grain in grains]):
            return 'Empty field {} x {}'.format(self.width, self.height)
        else:
            return 'Field {} x {}'.format(self.width, self.height)


def random_field(size_x, size_y, num_of_grains, resolution=6):
    field = GrainField(size_x, size_y, resolution)
    for x in range(num_of_grains):
        field.set_grain_state(
            random.randint(0, size_x - 1),
            random.randint(0, size_y - 1),
            # random.randint(1, grain_states)
            x + 1
        )

    return field


def decide_state(neighbours):
    """
    Decide which state should be chosen based on amount of surrounding neighbours

    :param neighbours: neighbour grains from which to pick state
    :return: state to be set
    """
    # list of surrounding states
    unq_states = [neighbour.prev_state for neighbour in neighbours if
                  neighbour.type is GrainType.GRAIN and neighbour.prev_state is not None]
    while unq_states:
        try:
            # mode function returns the item that occurred most times in a list
            return mode(unq_states)
        except StatisticsError:
            # if the amount is the same - pop item from the list
            unq_states.pop()

import random

import pygame
from ca.color import Color

from ca.grain import Grain


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
            self.field[x-1][y] if x > 0 else None,                  # left
            self.field[x][y - 1] if y > 0 else None,                # top
            self.field[x+1][y] if x < self.width - 1 else None,     # right
            self.field[x][y+1] if y < self.height - 1 else None,    # bottom
        )

    def upd(self):
        # go through all grains
        # check state - if prev state is not none go next
        # if prev state is none check neighbours and set state
        # update prev state
        for x in range(self.width):
            for y in range(self.height):
                grain = self.field[x][y]
                if grain.state is not None:
                    grain.prev_state = grain.state
                    continue
                # grain.prev_state = grain.state
                neighbours = self.von_neumann(x, y)
                for neighbour in neighbours:  # type: Grain
                    if neighbour and neighbour.prev_state:
                        grain.state = neighbour.prev_state
                        break

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
        grain = self.field[y][x]  # type: Grain
        grain.prev_state = grain.state
        grain.state = state

    def __str__(self):
        result = '\n'
        for x in range(self.width):
            for y in range(self.height):
                grain = self.field[y][x]
                result += '{} '.format(grain.state if grain.state is not None else 0)
            result += '\n'
        return result


def random_field(size_x, size_y, num_of_grains, resolution=6):
    field = GrainField(size_x, size_y,  resolution)
    for x in range(num_of_grains):
        field.set_grain_state(
            random.randint(0, size_x - 1),
            random.randint(0, size_y - 1),
            # random.randint(1, grain_states)
            x + 1
        )

    return field

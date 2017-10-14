import pygame
from pygame.math import Vector2

from color import Color
from grain import Grain


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
        self.field = [[Grain() for x in range(self.width)] for y in range(self.height)]
        # self.field = [Grain() for x in range(self.height * self.width)]

    def von_neumann(self, x, y):
        """
        Check neighbours of given x,y grain

        :param x:
        :param y:
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
        for y in range(self.height):
            for x in range(self.width):
                grain = self.field[x][y]
                if grain.state is not None:
                    grain.prev_state = grain.state
                    continue
                # grain.prev_state = grain.state
                neighbours = self.von_neumann(x, y)
                for neighbour in neighbours:  # type: Grain
                    if neighbour and neighbour.prev_state:
                        grain.state = neighbour.prev_state
                        # self.set_grain_state(x, y, neighbour.prev_state)
                        break
                # grain.prev_state = grain.state

        for y in range(self.height):
            for x in range(self.width):
                grain = self.field[x][y]
                grain.prev_state = grain.state

    def display(self, screen):
        rect = pygame.Rect(0, 0, self.resolution, self.resolution)
        for y, row in enumerate(self.field):  # type: list
            rect.y = y * self.resolution
            for x, grain in enumerate(row):
                color = grain.color
                rect.x = x * self.resolution
                pygame.draw.rect(screen, color, rect)
                # if resolution is less than 5 dont draw borders
                if self.resolution > 5:
                    pygame.draw.rect(screen, Color.BLACK.value, rect, 1)

    def set_grain_state(self, x, y, state):
        grain = self.field[x][y]  # type: Grain
        grain.state = state
        grain.prev_state = grain.state

import pygame

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
        self.field = [[] for x in range(self.width)]

        for x in range(self.width):
            self.field[x] = [Grain() for y in range(self.height)]

    def von_neumann(self, x, y):
        """
        Check neighbours of given x,y grain

        :param x:
        :param y:
        :return: tuple (left, top, right, bottom)
        """
        return (
            self.field[x-1][y] if x > 0 else None,
            self.field[x][y+1] if y < self.height-1 else None,
            self.field[x+1][y] if x < self.width - 1 else None,
            self.field[x][y-1] if y > 0 else None
        )

    def update(self):
        for x, row in enumerate(self.field):
            for y, grain in enumerate(row):
                neighbours = self.von_neumann(x, y)
                if grain.prev_state is None and any([neighbour.prev_state for neighbour in neighbours]):
                    # set state to neighbours state
                    for neighbour in neighbours:
                        if bool(neighbour):
                            grain.state = neighbour.state
                            break

                    grain.prev_state = grain.state

    def display(self, screen):
        for x, row in enumerate(self.field):  # type: list
            for y, grain in enumerate(row):
                color = grain.color
                pygame.draw.rect(screen, color, pygame.Rect(x * self.resolution, y * self.resolution, self.resolution,
                                                            self.resolution))
                # if resolution is less than 5 dont draw borders
                if self.resolution > 5:
                    pygame.draw.rect(screen, Color.BLACK.value, pygame.Rect(x * self.resolution, y * self.resolution, self.resolution, self.resolution), 1)

    def set_grain_state(self, x, y, state):
        grain = self.field[x][y]  # type: Grain
        grain.prev_state = grain.state
        grain.state = state

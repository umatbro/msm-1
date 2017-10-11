import pygame
from grain import Grain


class GrainField:
    def __init__(self, screen, x_size, y_size):
        self.screen = screen
        self.width = x_size
        self.height = y_size

        # init list
        self.field = [[] for x in range(self.width)]

        for x in range(self.width):
            self.field[x] = [Grain() for y in range(self.height)]

    # def __init__(self, screen, x_size, y_size):
    #     self.grains = []
    #
    #     for x in range(x_size):
    #         for y in range(y_size):
    #             self.grains.append(Grain(x, y))

    def check_neighbours(self, x, y):
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
                neighbours = self.check_neighbours(x, y)
                if grain.prev_state is None and any(neighbours):
                    # set state to neighbours state
                    for neighbour in neighbours:
                        if bool(neighbour):
                            grain.state = neighbour.state
                            break

                    grain.prev_state = grain.state

    def display(self):
        for x, row in enumerate(self.field):  # type: list
            for y, grain in enumerate(row):  # type: Grain
                color = (0, 200, 0) if grain.state is None else (0, 0, 0)
                pygame.draw.circle(self.screen, color, (x, y), 1)

    def set_grain_state(self, x, y, state):
        grain = self.field[x][y]  # type: Grain
        grain.prev_state = grain.state
        grain.state = state

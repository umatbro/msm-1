import sys

import pygame

from ca.grain_field import random_field
from files import export_image, export_text, import_text

MAX_FRAMES = 60


def run(
        x_size=100,
        y_size=100,
        num_of_grains=70,
        resolution=6,
        num_of_inclusions=0,
        inclusions_size=1,
        type_of_inclusions='square'
):
    """
    Run pygame window with visualisation

    :param x_size: number of columns
    :param y_size: number of rows
    :param num_of_grains: initial number of grains
    :param resolution: length of square sides (in pixels)
    """
    pygame.init()

    window_width = x_size * resolution
    window_height = y_size * resolution

    # create screen
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Grain field')

    # create clock
    clock = pygame.time.Clock()
    total_time = 0

    # field
    grain_field = random_field(x_size, y_size, num_of_grains, resolution)
    grain_field.random_inclusions(num_of_inclusions, inclusions_size, type_of_inclusions)
    # screen.fill((0, 0, 0))

    # main loop
    while 1337:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                return grain_field
                sys.exit(0)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
                pygame.quit()
                return grain_field
                sys.exit(0)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_SPACE:
                grain_field.upd()
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_r:
                grain_field = random_field(x_size, y_size, num_of_grains, resolution)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_i:
                export_image(grain_field)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_t:
                export_text(grain_field)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_l:
                grain_field = import_text('field.txt')

        total_time += clock.tick(MAX_FRAMES)

        # m_pos = pygame.mouse.get_pos()
        grain_field.upd()
        # if not grain_field.upd():
        #     break
        grain_field.display(screen)
        pygame.display.update()


if __name__ == '__main__':
    run(300, 300, 70, 1, 10, 10)
import sys

import pygame

from ca.grain import Grain
from ca.grain_field import random_field, GrainField
from files import export_image, export_text, import_text

MAX_FRAMES = 60


def run_field(grain_field: GrainField, resolution, probability=100,  paused=False):
    pygame.init()

    window_width = grain_field.width * resolution
    window_height = grain_field.height * resolution

    # create screen
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption('Grain field')

    # create clock
    clock = pygame.time.Clock()
    total_time = 0

    # selected cells
    selected_cells = {}
    # main loop
    while 1337:
        for event in pygame.event.get():
            if event.type is pygame.QUIT:
                pygame.quit()
                return grain_field, selected_cells
                sys.exit(0)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
                pygame.quit()
                return grain_field, selected_cells
                sys.exit(0)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_SPACE:
                grain_field.update(probability)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_r:
                grain_field = random_field(grain_field.width, grain_field.height, 70)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_i:
                export_image(grain_field)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_t:
                export_text(grain_field)
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_l:
                grain_field = import_text('field.txt')
            elif event.type is pygame.KEYDOWN and event.key is pygame.K_p:
                paused = not paused

        lmb, rmb, mmb = pygame.mouse.get_pressed()
        if lmb:
            print('pressed')
            gx, gy = mouse2grain_coords(pygame.mouse.get_pos(), resolution)
            grain = grain_field[gx, gy]
            state = grain.prev_state

            if grain.locked:
                # unlock it then
                for cell in selected_cells[state]:
                    cell.locked = False
                del selected_cells[state]
            elif state is not Grain.INCLUSION:
                selected_cells[state] = grain_field.cells_of_state(state)
                for cell in selected_cells[state]:  # type: Grain
                    cell.locked = True

        total_time += clock.tick(MAX_FRAMES)

        # m_pos = pygame.mouse.get_pos()
        if not paused:
            grain_field.update(probability)

        grain_field.display(screen, resolution)
        pygame.display.update()


def run(
        x_size=100,
        y_size=100,
        num_of_grains=70,
        resolution=6,
        probability=100,
        num_of_inclusions=0,
        inclusions_size=1,
        type_of_inclusions='square',
        paused=False
):
    """
    Run pygame window with visualisation

    :param x_size: number of columns
    :param y_size: number of rows
    :param num_of_grains: initial number of grains
    :param probability: probability of inclusion (in percents)
    :param resolution: length of square sides (in pixels)
    :param num_of_inclusions: number of inclusions
    :param inclusions_size: radius for circles, side length for squares
    :param type_of_inclusions: either square or circle
    :param paused: boolean indicating whether simulation will be paused on start
    """

    # field
    grain_field = GrainField(x_size, y_size)
    grain_field\
        .random_inclusions(num_of_inclusions, inclusions_size, type_of_inclusions)\
        .random_grains(num_of_grains)

    return run_field(grain_field, resolution, probability, paused)


def mouse2grain_coords(mpos, resolution):
    """Get mouse coords and convert to field coords based on given resolution"""
    mx, my = mpos
    return mx//resolution, my//resolution


if __name__ == '__main__':
    # run(300, 300, 3, 1, 100, 5, 'square')
    mouse2grain_coords((10, 10),1)
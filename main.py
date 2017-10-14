import sys
import pygame
import random
from time import sleep
from grain_field import GrainField

pygame.init()

X_SIZE = 70
Y_SIZE = 70
resolution = 6

WIDTH = X_SIZE * resolution
HEIGHT = Y_SIZE * resolution
MAX_FRAMES = 60

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Grain field')

# create clock
clock = pygame.time.Clock()
total_time = 0

# field
grain_field = GrainField(WIDTH/resolution, HEIGHT/resolution, resolution)
for x in range(50):
    grain_field.set_grain_state(
        random.randint(0, X_SIZE - 1),
        random.randint(0, Y_SIZE - 1),
        random.randint(1, 4)
    )
screen.fill((0, 0, 0))

# main loop
while 1337:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
            sys.exit(0)
        elif event.type is pygame.KEYDOWN and event.key is pygame.K_SPACE:
            grain_field.upd()
        elif event.type is pygame.KEYDOWN and event.key is pygame.K_r:
            grain_field = GrainField(WIDTH / resolution, HEIGHT / resolution, resolution)
            for x in range(3):
                grain_field.set_grain_state(
                    random.randint(0, X_SIZE - 1),
                    random.randint(0, Y_SIZE - 1),
                    x + 1
                )

    total_time += clock.tick(MAX_FRAMES)

    m_pos = pygame.mouse.get_pos()
    grain_field.upd()
    # if not grain_field.upd():
    #     break
    # sleep(1)
    grain_field.display(screen)
    pygame.display.update()
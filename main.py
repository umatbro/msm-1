import sys
import pygame
from grain_field import GrainField


pygame.init()

WIDTH = 640
HEIGHT = 480
MAX_FRAMES = 60

# create screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# create clock
clock = pygame.time.Clock()
total_time = 0

# field
grain_field = GrainField(screen, WIDTH, HEIGHT)
grain_field.set_grain_state(100, 100, 20)
screen.fill((255, 255, 255))

# main loop
while 1337:
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            pygame.quit()
            sys.exit(0)
        elif event.type is pygame.KEYDOWN and event.key is pygame.K_ESCAPE:
            sys.exit(0)

    total_time += clock.tick(MAX_FRAMES)
#    screen.fill((255, 255, 255))

    m_pos = pygame.mouse.get_pos()
    grain_field.display()
    pygame.display.update()
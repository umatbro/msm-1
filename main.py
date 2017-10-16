import sys
import pygame
from grain_field import GrainField, random_field

pygame.init()

X_SIZE = 500
Y_SIZE = 500
resolution = 1

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
# grain_field = GrainField(X_SIZE, Y_SIZE, resolution)
# for x in range(70):
#     grain_field.set_grain_state(
#         random.randint(0, X_SIZE - 1),
#         random.randint(0, Y_SIZE - 1),
#         # random.randint(1, 30)
#         x + 1
#     )
grain_field = random_field(X_SIZE, Y_SIZE, 700,  resolution)
# screen.fill((0, 0, 0))

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
            grain_field = random_field(X_SIZE, Y_SIZE, 70, resolution)

    total_time += clock.tick(MAX_FRAMES)

    m_pos = pygame.mouse.get_pos()
    grain_field.upd()
    # if not grain_field.upd():
    #     break
    # sleep(1)
    grain_field.display(screen)
    pygame.display.update()
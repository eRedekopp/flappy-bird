"""
Flappy Bird clone game
"""

import pygame
import random as rand

################################## Constants ###################################

# screen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600

# physics
GRAVITY = 3.5
JUMP_VELOCITY = -35
MAX_Y_VELOCITY = 12
FRAME_RATE = 60

# colours
WHITE  = 255, 255, 255
BLACK  = 0, 0, 0
BLUE   = 115, 233, 251
YELLOW = 233, 244, 14
GREY   = 100, 100, 100
GREEN  = 40, 190, 40

# graphics
BIRD_RADIUS = 15    # the radius of the circle representing the bird
BIRD_COLOUR = YELLOW
BAR_WIDTH   = 60
MAX_BAR_LENGTH = 400
MIN_BAR_LENGTH = 150
GROUND_HEIGHT = 40
GROUND_LEVEL  = SCREEN_HEIGHT - GROUND_HEIGHT # the position of the top of the
                                              # ground
BIRD_INITIAL_POSITION = bird_x, bird_y= 200, GROUND_LEVEL - BIRD_RADIUS


################################## Functions ###################################

"""
Returns a green surface of width BAR_WIDTH and random height within length 
restrictions
"""
def generate_bar():
    height = rand.randint(MIN_BAR_LENGTH, MAX_BAR_LENGTH)
    surface = pygame.Surface((BAR_WIDTH, height))
    surface.fill(GREEN)
    return surface


#################################### Setup #####################################

# startup
pygame.init()
pygame.display.set_caption("Flappy Bird")

# set up screen
screen = pygame.display.set_mode(SCREEN_SIZE)

background = pygame.Surface(SCREEN_SIZE).convert()   # background
background.fill(BLUE)
floor = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT)).convert()
floor.fill(GREY)
background.blit(floor, (0, GROUND_LEVEL))

foreground = pygame.Surface(SCREEN_SIZE).convert()   # foreground
foreground.set_colorkey(BLACK)

################################## Main Loop ###################################

mainloop = True
bird_y_velocity = GRAVITY
clock = pygame.time.Clock()
bar = generate_bar()
while mainloop:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            mainloop = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_y_velocity = JUMP_VELOCITY

    # handle physics
    if bird_y >= GROUND_LEVEL - BIRD_RADIUS and bird_y_velocity > 0:
        bird_y_velocity = 0
        bird_y = GROUND_LEVEL - BIRD_RADIUS
    elif bird_y_velocity < MAX_Y_VELOCITY \
            and bird_y < GROUND_LEVEL - BIRD_RADIUS:
        bird_y_velocity += GRAVITY
    bird_y += int(bird_y_velocity)

    # redraw and update screen
    foreground.fill(BLACK)
    pygame.draw.circle(foreground,
                       BIRD_COLOUR,
                       (bird_x, bird_y),
                       BIRD_RADIUS)

    foreground.blit(bar, (300, GROUND_LEVEL - bar.get_height()))

    screen.blit(background, (0, 0))
    screen.blit(foreground, (0, 0))
    pygame.display.flip()

    # force frame rate
    clock.tick(FRAME_RATE)



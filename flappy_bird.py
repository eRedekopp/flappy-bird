"""
Flappy Bird clone game
"""

import pygame

################################## Constants ###################################

# screen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600

# physics
METER   = 20 # number of pixels in one "meter"
GRAVITY = 9.8
JUMP_VELOCITY = -10
MAX_Y_VELOCITY = 100
FRAME_RATE = 60
DT = 1/FRAME_RATE # time in seconds for one frame
DV = GRAVITY * DT # dv = g * dt


# colours
WHITE  = 255, 255, 255
BLACK  = 0, 0, 0
BLUE   = 115, 233, 251
YELLOW = 233, 244, 14
GREY   = 100, 100, 100

# graphics
BIRD_INITIAL_POSITION = bird_x, bird_y= 200, 200
BIRD_RADIUS = 10    # the radius of the circle representing the bird
BIRD_COLOUR = YELLOW
GROUND_HEIGHT = 30
GROUND_LEVEL = SCREEN_HEIGHT - GROUND_HEIGHT # the position of the top of the
                                             # ground

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
bird_y_velocity = 0
clock = pygame.time.Clock()
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
    elif bird_y_velocity < MAX_Y_VELOCITY:
        bird_y_velocity += DV

    bird_y += bird_y_velocity
    bird_y  = int(bird_y)   # force integer

    # redraw and update screen
    foreground.fill(BLACK)
    pygame.draw.circle(foreground,
                       BIRD_COLOUR,
                       (bird_x, bird_y),
                       BIRD_RADIUS)
    screen.blit(background, (0, 0))
    screen.blit(foreground, (0, 0))
    pygame.display.flip()

    # force frame rate
    clock.tick(FRAME_RATE)



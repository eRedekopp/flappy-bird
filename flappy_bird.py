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
SCROLL_RATE = 30

# colours
WHITE  = 255, 255, 255
BLACK  = 0, 0, 0
BLUE   = 115, 233, 251
YELLOW = 233, 244, 14
GREY   = 100, 100, 100
GREEN  = 40, 190, 40

# graphics
BIRD_RADIUS    = 15     # the radius of the circle representing the bird
BIRD_COLOUR    = YELLOW
BAR_WIDTH      = 60
BAR_GAP        = 120
BAR_FREQUENCY  = 30
BAR_COLOUR     = GREEN
BG_COLOUR      = BLUE
MAX_BAR_LENGTH = 400
MIN_BAR_LENGTH = 150
GROUND_HEIGHT  = 40
GROUND_LEVEL   = SCREEN_HEIGHT - GROUND_HEIGHT # the position of the top of the
                                               # ground
BIRD_INITIAL_POSITION = bird_x, bird_y= 200, GROUND_LEVEL - BIRD_RADIUS

################################### Classes ####################################

class BarPair:
    @staticmethod
    def generate_bar_pair():
        height = rand.randint(MIN_BAR_LENGTH, MAX_BAR_LENGTH)
        surface = pygame.Surface((BAR_WIDTH, GROUND_LEVEL))
        bottom_bar = pygame.Surface((BAR_WIDTH, GROUND_LEVEL - height))
        top_bar = pygame.Surface((BAR_WIDTH, GROUND_LEVEL - height - BAR_GAP))
        bottom_bar.fill(BAR_COLOUR)
        top_bar.fill(BAR_COLOUR)
        surface.fill(BG_COLOUR)
        surface.blit(top_bar, (0, 0))
        surface.blit(bottom_bar, (0, GROUND_LEVEL - height))
        return surface

    def __init__(self):
        self.__surface = self.generate_bar_pair()
        self.__x_pos = SCREEN_WIDTH

    """
    Returns the x position of the bar pair
    """
    def get_x(self):
        return self.__x_pos

    """
    Returns the surface representation of the bar pair
    """
    def get_surface(self):
        return self.__surface

    """
    Moves the bar pair to the left by SCROLL_RATE pixels
    """
    def scroll(self):
        self.__x_pos -= SCROLL_RATE

class BarList():
    def __init__(self):
        self.__list = []
        self.__n_scrolls = 0

    def to_tuple(self):
        return tuple(self.__list)

    def addNewBar(self):
        self.__list.append(BarPair())

    def scroll(self):
        if len(self.__list) == 0:
            self.addNewBar()
        for pair in self.__list:
            pair.scroll()
        if self.__list[0].get_x() <= 0:
            self.__list.pop()
        if self.__n_scrolls % BAR_FREQUENCY == 0:
            self.addNewBar()
        self.__n_scrolls += 1

#################################### Setup #####################################

# startup
pygame.init()
pygame.display.set_caption("Flappy Bird")

# set up screen
screen = pygame.display.set_mode(SCREEN_SIZE)

background = pygame.Surface(SCREEN_SIZE).convert()   # background
background.fill(BG_COLOUR)
floor = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT)).convert()
floor.fill(GREY)
background.blit(floor, (0, GROUND_LEVEL))

foreground = pygame.Surface(SCREEN_SIZE).convert()   # foreground
foreground.set_colorkey(BLACK)

################################## Main Loop ###################################

mainloop = True
bird_y_velocity = GRAVITY
clock = pygame.time.Clock()
bars = BarList()
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

    # redraw foreground
    foreground.fill(BLACK)
    bars.scroll()
    pygame.draw.circle(foreground,
                       BIRD_COLOUR,
                       (bird_x, bird_y),
                       BIRD_RADIUS)
    for pair in bars.to_tuple():
        foreground.blit(pair.get_surface(), (pair.get_x(), 0))

    screen.blit(background, (0, 0))
    screen.blit(foreground, (0, 0))
    pygame.display.flip()

    # force frame rate
    clock.tick(FRAME_RATE)



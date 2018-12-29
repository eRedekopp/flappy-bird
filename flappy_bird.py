"""
Flappy Bird clone game
"""

import pygame
import random as rand

################################## Constants ###################################

# screen
SCREEN_SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600

# physics
GRAVITY = 3.15
JUMP_VELOCITY = -31
MAX_Y_VELOCITY = 12
FRAME_RATE = 55
SCROLL_RATE = 7

# colours
WHITE  = 255, 255, 255
BLACK  = 0, 0, 0
BLUE   = 115, 233, 251
YELLOW = 233, 244, 14
GREY   = 100, 100, 100
GREEN  = 40, 190, 40

# graphics
BAR_WIDTH      = 50
BAR_GAP        = 140
BAR_FREQUENCY  = 45    # lower = more frequent
BAR_COLOUR     = GREEN
BG_COLOUR      = BLUE
MAX_BAR_LENGTH = 400
MIN_BAR_LENGTH = 150
GROUND_HEIGHT  = 40
GROUND_LEVEL   = SCREEN_HEIGHT - GROUND_HEIGHT # the position of the top of the
                                               # ground

################################### Classes ####################################

class BarPair:
    """
    Returns a surface containing a representation of a randomly generated bar
    pair, and the height of the bottom bar.
    """
    @staticmethod
    def __generate_bar_pair():
        height = rand.randint(MIN_BAR_LENGTH, MAX_BAR_LENGTH)
        surface = pygame.Surface((BAR_WIDTH, GROUND_LEVEL))
        top_bar = pygame.Surface((BAR_WIDTH, GROUND_LEVEL - BAR_GAP - height))
        bottom_bar = pygame.Surface((BAR_WIDTH, height))

        bottom_bar.fill(BAR_COLOUR)
        top_bar.fill(BAR_COLOUR)
        surface.fill(BG_COLOUR)

        surface.blit(top_bar, (0, 0))
        surface.blit(bottom_bar, (0, GROUND_LEVEL - height))
        return surface.convert(), height

    def __init__(self):
        self.__surface, self.__height = self.__generate_bar_pair()
        self.__x_pos = SCREEN_WIDTH - BAR_WIDTH

    """
    Returns the x position of the bar pair
    """
    def get_x(self):
        return self.__x_pos

    """
    Returns True if any part of the bird is within the bounds of the top or 
    bottom bar (ie. if the bird is in collision with a bar), else False
    
    Treats the bird as a square 
    """
    def detect_collision(self, bird):
        # checks whether any part of the bird "square" contacts either of the
        # bars
        # This is as neat as I could make it look without going over 80 chars
        if ((GROUND_LEVEL - self.__height - bird.radius) < bird.get_pos()[1]
            or (GROUND_LEVEL - self.__height - BAR_GAP + bird.radius) >
                        bird.get_pos()[1])\
            and self.get_x()-bird.radius <= bird.get_pos()[0] \
                                <= self.get_x()+ BAR_WIDTH +  bird.radius:
            return True
        else:
            return False

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

class BarList:
    def __init__(self):
        self.__list = []
        self.__list.append(BarPair())
        self.__frames_since_last_pipe = 0
        self.__bars_passed = 0

    def n_bars(self):
        return len(self.__list)

    def n_bars_passed(self):
        return self.__bars_passed

    def to_tuple(self):
        return tuple(self.__list)

    def __addNewBar(self):
        new_bar_pair = BarPair()
        self.__list.append(new_bar_pair)

    """
    Returns True if new bar is required, else False.
    Should only be called once per frame
    """
    def __req_new_bar(self):
        if self.__frames_since_last_pipe == BAR_FREQUENCY:
            self.__frames_since_last_pipe = 0
            return True
        else:
            self.__frames_since_last_pipe += 1
            return False

    """
    Scrolls all bars on the screen over by one frame, adds a new bar if 
    necessary
    """
    def scroll(self):
        if self.__req_new_bar():
            self.__addNewBar()
        for pair in self.__list:
            pair.scroll()
        if self.n_bars() > 0 and self.__list[0].get_x() <= 0:
            self.__list.pop(0)
            self.__bars_passed += 1

    """
    Checks all bar pairs for collision, returns True if collision else False
    """
    def detect_collision(self, bird):
        for bar_pair in self.__list:
            if bar_pair.detect_collision(bird):
                return True
        return False

class Bird:
    def __init__(self):
        self.__x = 50
        self.__y = 200
        self.__y_velocity = GRAVITY
        self.colour = YELLOW
        self.radius = 15

    """
    Set y velocity to JUMP_VELOCITY
    """
    def jump(self):
        self.__y_velocity = JUMP_VELOCITY

    """
    Adjust position and velocity for one frame
    """
    def next_frame(self):
        if self.__y >= GROUND_LEVEL - self.radius and self.__y_velocity > 0:
            self.__y_velocity = 0
            self.__y = GROUND_LEVEL - self.radius
        elif self.__y_velocity < MAX_Y_VELOCITY \
                and self.__y < GROUND_LEVEL - self.radius:
            self.__y_velocity += GRAVITY
        self.__y += int(self.__y_velocity)

    def get_pos(self):
        return self.__x, self.__y

"""
A frame containing the graphics of the game
"""
class Frame:
    def __init__(self):
        # startup
        pygame.init()
        pygame.display.set_caption("Flappy Bird")

        # set up screen
        self.__screen = pygame.display.set_mode(SCREEN_SIZE)

        self.__background = pygame.Surface(SCREEN_SIZE).convert()  # background
        self.__background.fill(BG_COLOUR)
        self.__floor = pygame.Surface((SCREEN_WIDTH, GROUND_HEIGHT)).convert()
        self.__floor.fill(GREY)
        self.__background.blit(self.__floor, (0, GROUND_LEVEL))

        self.__foreground = pygame.Surface(SCREEN_SIZE).convert()  # foreground
        self.__foreground.set_colorkey(BLACK)

    """
    Updates the foreground to represent the given barlist and bird 
    """
    def redraw_foreground(self, barlist, bird):
        # redraw foreground
        self.__foreground.fill(BLACK)
        for pair in barlist.to_tuple():
            self.__foreground.blit(pair.get_surface(), (pair.get_x(), 0))
        pygame.draw.circle(self.__foreground,
                           bird.colour,
                           bird.get_pos(),
                           bird.radius)

    def update(self):
        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__foreground, (0, 0))
        pygame.display.flip()

################################## Main Loop ###################################

mainloop = True
frame = Frame()
clock = pygame.time.Clock()
bars = BarList()
bird = Bird()
while mainloop:
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            mainloop = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird.jump()

    # handle physics/graphics
    bird.next_frame()
    bars.scroll()
    if bars.detect_collision(bird): # exit if collision
        pygame.quit()
        mainloop = False
        print("You suck")
        continue

    frame.redraw_foreground(bars, bird)
    frame.update()

    # force frame rate
    clock.tick(FRAME_RATE)



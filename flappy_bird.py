"""
Flappy Bird clone game
"""

import pygame
import random as rand

################################### Classes ####################################

"""
A frame containing the graphics of the game
"""
class Frame:
    SIZE = WIDTH, HEIGHT = 400, 600

    WHITE = 255, 255, 255
    BLACK = 0, 0, 0
    BLANK = 1, 1, 1   # use this for Surface color key
    BLUE = 115, 233, 251
    YELLOW = 233, 244, 14
    GREY = 100, 100, 100
    GREEN = 40, 190, 40
    BG_COLOUR = BLUE

    GROUND_HEIGHT = 40
    GROUND_LEVEL = HEIGHT - GROUND_HEIGHT  # the y position of the top of the
                                           # ground

    def __init__(self):
        # startup
        pygame.init()
        pygame.display.set_caption("Flappy Bird")

        # set up screen
        self.__screen = pygame.display.set_mode(Frame.SIZE)

        self.__background = pygame.image.load("background.png").convert()
        self.__floor = pygame.Surface((Frame.WIDTH,
                                       Frame.GROUND_HEIGHT)).convert()
        self.__floor.fill(Frame.GREY)
        self.__background.blit(self.__floor, (0, Frame.GROUND_LEVEL))

        self.__foreground = pygame.Surface(Frame.SIZE).convert()  # foreground
        self.__foreground.set_colorkey(Frame.BLANK)

        self.font = pygame.font.SysFont('Arial', 50)

    """
    Updates the foreground to represent the given BarList and bird, 
    and displays the score
    """
    def redraw_foreground(self, barlist, bird):
        self.__foreground.fill(Frame.BLANK)            # erase foreground
        for pair in barlist.to_tuple():                # draw bars
            self.__foreground.blit(pair.get_surface(),
                                   (pair.get_x(), 0))
        bird_x, bird_y = bird.get_pos()                # draw bird
        bird_surface_x = bird_x - bird.RADIUS
        bird_surface_y = bird_y - bird.RADIUS
        self.__foreground.blit(bird.get_surface(),
                              (bird_surface_x, bird_surface_y))

        text_box = self.font.render(str(barlist.n_bars_passed()), # draw score
                                    True,
                                    Frame.WHITE)
        text_x_location = Frame.WIDTH // 2 - text_box.get_width() // 2
        self.__foreground.blit(text_box,
                               (text_x_location, 5))


    """
    Redraws the background and foreground onto the display
    """
    def update(self):
        self.__screen.blit(self.__background, (0, 0))
        self.__screen.blit(self.__foreground, (0, 0))
        pygame.display.flip()

    """
    Erases the current foreground and replaces it with the game over screen
    """
    def draw_gameover_to_fg(self, score):
        game_over_text = "GAME OVER"
        score_text     = "Score: " + str(score)
        self.__foreground.fill(Frame.BLANK)
        gameover_box = self.font.render(game_over_text,
                                    True,
                                    Frame.WHITE)
        score_box = self.font.render(score_text,
                                     True,
                                     Frame.WHITE)
        text_box_width = max([gameover_box.get_width(), score_box.get_width()])
        text_box_height = gameover_box.get_height() + score_box.get_height()
        text_box = pygame.Surface((text_box_width,
                                  text_box_height))
        text_box.blit(gameover_box, (0, 0))
        text_box.blit(score_box, (0, gameover_box.get_height()))
        text_box_position = Frame.WIDTH // 2 - text_box.get_width() // 2, \
                            Frame.HEIGHT // 2 - text_box.get_height() // 2
        self.__foreground.blit(text_box, text_box_position)


"""
Represents an individual pair of bars: contains a graphical representation as a 
pygame.Surface, the height of the bottom of its gap, and its horizontal 
position
"""
class BarPair:
    WIDTH = 70
    GAP_SIZE   = 140  # size of gap between top and bottom bars
    MAX_BAR_LENGTH = 400
    MIN_BAR_LENGTH = 150
    COLOUR = Frame.GREEN

    """
    Returns a surface containing a representation of a randomly generated bar
    pair, and the height of the bottom bar.
    """
    @staticmethod
    def __generate_bar_pair():
        height = rand.randint(BarPair.MIN_BAR_LENGTH, BarPair.MAX_BAR_LENGTH)
        surface = pygame.Surface((BarPair.WIDTH,
                                  Frame.GROUND_LEVEL))
        surface.fill(Frame.BLANK)
        surface.set_colorkey(Frame.BLANK)
        top_bar = pygame.Surface((BarPair.WIDTH,
                                  Frame.GROUND_LEVEL -
                                    BarPair.GAP_SIZE -
                                    height))
        top_bar_inside = pygame.Surface((BarPair.WIDTH - 4,
                                  Frame.GROUND_LEVEL -
                                    BarPair.GAP_SIZE -
                                    height - 2))
        bottom_bar = pygame.Surface((BarPair.WIDTH,
                                     height))
        bottom_bar_inside = pygame.Surface((BarPair.WIDTH - 4,
                                            height - 2))

        bottom_bar.fill(Frame.BLACK) # create outlines
        bottom_bar_inside.fill(BarPair.COLOUR)
        bottom_bar.blit(bottom_bar_inside, (2, 2))
        top_bar.fill(Frame.BLACK)
        top_bar_inside.fill(BarPair.COLOUR)
        top_bar.blit(top_bar_inside, (2, 0))

        surface.blit(top_bar, (0, 0))
        surface.blit(bottom_bar, (0, Frame.GROUND_LEVEL - height))
        return surface.convert(), height

    def __init__(self):
        self.__surface, self.__height = self.__generate_bar_pair()
        self.__x_pos = Frame.WIDTH - BarPair.WIDTH

    """
    Returns the x position of the bar pair
    """
    def get_x(self):
        return self.__x_pos

    """
    Returns True if any part of the bird is within the bounds of the top or 
    bottom bar (ie. if the bird is in collision with a bar), else False
    
    Treats the bird as a square with sides as long as the bird's radius
    """
    def detect_collision(self, bird):
        bottom_limit = Frame.GROUND_LEVEL - self.__height - bird.RADIUS
        top_limit = Frame.GROUND_LEVEL - self.__height \
                    - BarPair.GAP_SIZE + bird.RADIUS
        bird_x, bird_y = bird.get_pos()
        if (bird_y > bottom_limit or bird_y < top_limit)     \
            and                                              \
                 self.get_x() - bird.RADIUS                  \
              <= bird_x                                      \
              <= self.get_x() + BarPair.WIDTH +  bird.RADIUS:
            return True
        else:
            return False

    """
    Returns the graphical representation of the bar pair as a pygame.Surface
    """
    def get_surface(self):
        return self.__surface

    """
    Moves the bar pair to the left by SCROLL_RATE pixels
    """
    def scroll(self):
        self.__x_pos -= Game.SCROLL_RATE

"""
A list of bars that appear on the screen at a given time; acts like a queue. 
Also keeps track of the number of bars successfully passed since it was created
"""
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
        if self.__frames_since_last_pipe == Game.BAR_FREQUENCY:
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

"""
Represents the player-controlled bird's position, velocity, and graphical 
information
"""
class Bird:
    RADIUS = 15

    """
    Returns a new pygame.Surface containing the graphical representation of the 
    Bird
    """
    @staticmethod
    def generate_graphic():
        surface = pygame.Surface((2*Bird.RADIUS, 2*Bird.RADIUS))
        surface.set_colorkey(Frame.BLACK)
        bird = pygame.image.load("bird.png").convert()
        surface.blit(bird, (0, 0))
        return surface

    def __init__(self):
        self.__x = 50
        self.__y = 200
        self.__y_velocity = Game.GRAVITY
        self.__surface = Bird.generate_graphic()

    """
    Returns a surface containing a graphical representation of the bird
    """
    def get_surface(self):
        return self.__surface

    """
    Set y velocity to Game.JUMP_VELOCITY
    """
    def jump(self):
        self.__y_velocity = Game.JUMP_VELOCITY

    """
    Adjust position and velocity for one frame
    """
    def next_frame(self):
        if self.__y >= Frame.GROUND_LEVEL - self.RADIUS \
                and self.__y_velocity > 0:
            self.__y_velocity = 0
            self.__y = Frame.GROUND_LEVEL - self.RADIUS
        elif self.__y_velocity < Game.MAX_Y_VELOCITY \
                and self.__y < Frame.GROUND_LEVEL - self.RADIUS:
            self.__y_velocity += Game.GRAVITY
        self.__y += int(self.__y_velocity)

    """
    Returns the x and y position of the bird's centre as a tuple
    """
    def get_pos(self):
        return self.__x, self.__y


"""
Controller class that runs all operations of a game
"""
class Game:
    GRAVITY = 3.15
    JUMP_VELOCITY = -31
    MAX_Y_VELOCITY = 12
    FRAME_RATE = 55
    SCROLL_RATE = 7
    BAR_FREQUENCY = 45  # n of frames between new bars

    def __init__(self):
        self.__frame = Frame()
        self.__clock = pygame.time.Clock()
        self.__bars  = BarList()
        self.__bird  = Bird()
        self.__running = False

    """
    Checks whether game has received any input since the last frame. Also 
    runs quit() if the user asked to quit since last frame 
    """
    def __check_for_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                self.__bird.jump()

    """
    Scrolls bars and handles gravity on bird for one frame
    """
    def __handle_physics(self):
        self.__bird.next_frame()
        self.__bars.scroll()
        if self.__bars.detect_collision(self.__bird):  # exit if collision
            self.__running = False

    """
    Show game over screen; return when user presses enter or exit game if 
    user presses x button on window
    """
    def __game_over(self):
        self.__frame.draw_gameover_to_fg(self.__bars.n_bars_passed())
        self.__frame.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    return

    """
    Begins a game. Loops until the game is over or the user presses the x 
    button on the frame, then displays the game over screen until the user 
    exits, or presses Enter to start a new game.
    """
    def run(self):
        self.__running = True
        while self.__running:
            self.__check_for_input()
            self.__handle_physics()
            self.__frame.redraw_foreground(self.__bars, self.__bird)
            self.__frame.update()
            self.__clock.tick(Game.FRAME_RATE)

        return self.__game_over()

    """
    Shuts down the game and exits the program entirely
    """
    @staticmethod
    def quit():
        pygame.quit()
        quit(0)


################################ Main Program ##################################

# Infinite loop: game can only be exited by hitting x button of window
while True:
    game = Game()
    game.run()


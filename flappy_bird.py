"""
Flappy Bird clone game
"""

import pygame
import random as rand

# constants
screen_size = screen_width, screen_height = 400, 600
bird_initial_position = 200, 550
bird_radius = 10    # the radius of the circle representing the bird
ground_height = screen_height - (bird_initial_position[1] + bird_radius)
ground_level = screen_height - ground_height # the position of the top of the
                                             # ground
white  = 255, 255, 255
blue   = 115, 233, 251
yellow = 233, 244, 14
grey   = 100, 100, 100
bird_colour = yellow

# startup
pygame.init()
pygame.display.set_caption("Flappy Bird")

# set up screen
screen = pygame.display.set_mode(screen_size)

background = pygame.Surface(screen_size).convert()   # background
background.fill(blue)
floor = pygame.Surface((screen_width, ground_height)).convert()
floor.fill(grey)
background.blit(floor, (0, screen_height-ground_height))
screen.blit(background, (0, 0))

foreground = pygame.Surface(screen_size).convert()   # foreground
foreground.set_colorkey((0, 0, 0))

while True:  # keep drawing the same picture over and over
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # change bird to random colour when user presses space
            bird_colour = rand.randint(0, 255), \
                          rand.randint(0, 255), \
                          rand.randint(0, 255)
    pygame.draw.circle(foreground,
                       bird_colour,
                       bird_initial_position,
                       bird_radius)
    screen.blit(background, (0, 0))
    background.blit(foreground, (0, 0))
    pygame.display.flip()


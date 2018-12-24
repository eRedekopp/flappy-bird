"""
Flappy Bird clone game
"""

import pygame

# constants
screen_size = width, height = 400, 600
bird_initial_position = 200, 550
white  = 255, 255, 255
blue   = 115, 233, 251
yellow = 233, 244, 14

# startup
pygame.init()
pygame.display.set_caption("Flappy Bird")

# set up screen
screen = pygame.display.set_mode(screen_size)
background = pygame.Surface(screen_size)
background.fill(blue)
screen.blit(background, (0, 0))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break
    screen.fill(blue)
    pygame.draw.circle(background, yellow, bird_initial_position, 10)
    screen.blit(background, (0, 0))
    pygame.display.flip()

pygame.quit()


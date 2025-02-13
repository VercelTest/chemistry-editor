import pygame
from sys import exit

pygame.init()
Screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Chemistry Editor")
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    pygame.display.update()
    # frame rate
    clock.tick(30)
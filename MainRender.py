import pygame
from BallPhysics import *
from sys import exit

pygame.init()
screen = pygame.display.set_mode((800, 400))
clock = pygame.time.Clock()
# Title
pygame.display.set_caption("Chemistry Editor")

# Fonts
TitleFont = pygame.font.Font('Fonts/Interphases Regular.ttf', 40)

# Render
Information = TitleFont.render("Interphases", True, 'white')
text_rect = Information.get_rect(center=(800/2, 30))

ball = pygame.image.load('AtomImages/test 2.webp')
ball = pygame.transform.scale(ball, (50,50))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
            
        if event.type == pygame.MOUSEMOTION:
                print(event)
                
    screen.blit(ball, (0,0))
    screen.blit(Information, text_rect)

    pygame.display.update()
    # frame rate
    clock.tick(30)
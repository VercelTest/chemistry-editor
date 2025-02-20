import pygame
from AtomPhysics import *
from sys import exit
from AtomPresets import AtomImages

# init variables
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 800
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
Vector2 = pygame.math.Vector2

# Window Title
pygame.display.set_caption("Chemistry Editor")

# Fonts
TitleFont = pygame.font.Font('Fonts/Interphases Regular.ttf', 40)

# Assets
Information = TitleFont.render("Hi this is text", True, 'white')
text_rect = Information.get_rect(center=(SCREEN_WIDTH/2, 30)) # center text

AddButtonImage = pygame.image.load('Assets/Buttons/Add Button.png').convert_alpha()

# Classes
class Button():
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (scale, scale))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
        self.clicked = False 

    def draw(self):
        action = False

        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                action = True
        
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        screen.blit(self.image, (self.rect.x, self.rect.y))

        return action

class Atom():
    def __init__(self):
        return 'not yet!!!!'

# Buttons
AddButton = Button(SCREEN_WIDTH - 75, SCREEN_HEIGHT - 75, AddButtonImage, 75)

# Renderer
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    screen.fill((0, 15, 38))

    screen.blit(Information, text_rect)
    if AddButton.draw():
        print('START')

    pygame.display.update()
    # frame rate
    clock.tick(30)
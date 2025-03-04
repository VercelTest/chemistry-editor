import pygame
from AtomHandler import Atom
from sys import exit
from AtomPresets import AtomImages

# init variables
SCREEN_HEIGHT = 400
SCREEN_WIDTH = 800
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

AtomList = []
Mode = "Drag"
OverrideInformation = False
user_text = ''

# Window Title
pygame.display.set_caption("Chemistry Editor")

# Fonts
TitleFont = pygame.font.Font('Fonts/Interphases Regular.ttf', 40)
InputFont = pygame.font.Font('Fonts/Interphases Regular.ttf', 35)

# Assets
Information = TitleFont.render("Hi this is text", True, 'white')
text_rect = Information.get_rect(center=(SCREEN_WIDTH/2, 30)) # center text
pause_screen = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
pause_screen.set_alpha(128)
pause_screen.fill('black')

AddButtonImage = pygame.image.load('Assets/Buttons/Add Button.png').convert_alpha()
ViewButtonImage = pygame.image.load('Assets/Buttons/Magnifying.png').convert_alpha()

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

# Buttons
AddButton = Button(SCREEN_WIDTH - 75, SCREEN_HEIGHT - 75, AddButtonImage, 75)
ViewButton = Button(SCREEN_WIDTH - 150, SCREEN_HEIGHT - 75, ViewButtonImage, 75)

# Functions
def newAtom(Type):
    AtomList.append(Atom(Type, AtomImages[Type]))

# Renderer
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        
        # prevent multi dragging bug
        for atom in reversed(AtomList):
            atom.check_dragging_priority(event, Mode)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if Mode == "Add":
                    Mode = "Drag"
                    if user_text.capitalize() in AtomImages:
                        newAtom(user_text.capitalize())
            
            elif event.key == pygame.K_BACKSPACE:
                user_text = user_text[0:-1]
            else:
                user_text += event.unicode


    screen.fill((0, 15, 38))

    # screen.blit(Information, text_rect)

    for atom in AtomList:
        data = atom.physics(Mode)
        atom.draw(screen)
        atom.detectbond(AtomList)

        if data:
            OverrideInformation = True
            Information = TitleFont.render(data, True, 'white')
    
    if AddButton.draw():
        Mode = "Add"
        user_text = ''
    
    if ViewButton.draw():
        if Mode == "Drag":
            Mode = "View"
        elif Mode == "View":
            Mode = "Drag"
    
    if Mode == "Add":
        screen.blit(pause_screen, (0,0))
        OverrideInformation = True
        Information = TitleFont.render("Type an element below then press enter:" , True, 'white')

        Input = InputFont.render(user_text, True, 'white')
        screen.blit(Input, Input.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2)))

    if OverrideInformation == False:
         Information = TitleFont.render("Mode: " + Mode, True, 'white')
    info_text_rect = Information.get_rect(center=(SCREEN_WIDTH/2, 30)) # center text

    OverrideInformation = False

    screen.blit(Information, info_text_rect)

    pygame.display.update()
    clock.tick(60)
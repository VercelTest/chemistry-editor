import pygame
from MathFuncs import *
from AtomPresets import AtomValenceValues
import math

selected_atom = None
Vector2 = pygame.math.Vector2

class Atom():
    def __init__(self, type, image):
        self.name = type
        self.type = image
        self.ValenceElectronType = AtomValenceValues[type]
        self.x = 400
        self.y = 200  
        self.xvel = 0
        self.yvel = 0

        self.rect = self.type.get_rect()
        self.scale = image.get_width()
        self.rect.topleft = (self.x, self.y)

        self.ElectronsLeft = self.ValenceElectronType
        self.bonded = False
        self.dragging = False  
        self.offset = Vector2(0, 0)
        self.prev_pos = Vector2(self.x, self.y)

    def check_dragging_priority(self, event, Mode):
        global selected_atom

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and selected_atom is None:

                if Mode == "Drag":
                    self.dragging = True
                    mousepos = pygame.mouse.get_pos()
                    self.offset = Vector2(mousepos[0] - self.x, mousepos[1] - self.y)
                    selected_atom = self

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                selected_atom = None

    # basically only free physics so change this later
    def freephysics(self):
        mousepos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # EVENTS
        if self.dragging:
            self.x = mousepos[0] - self.offset.x
            self.y = mousepos[1] - self.offset.y

            # edges
            if self.x > 800 - self.scale:
                self.x = 800 - self.scale

            if self.x < 0:
                self.x = 0

            if self.y > 400 - self.scale:
                self.y = 400 - self.scale

            if self.y < 0:
                self.y = 0
            
            self.xvel = self.x - self.prev_pos.x
            self.yvel = self.y - self.prev_pos.y


        if not mouse_pressed:
            self.dragging = False  

        if not self.dragging:
            self.x += self.xvel
            self.y += self.yvel

            # friction
            self.xvel *= 0.95
            self.yvel *= 0.95

            # edges
            if self.x > 800 - self.scale:
                self.x = 800 - self.scale
                self.xvel *= -1

            if self.x < 0:
                self.x = 0
                self.xvel *= -1

            if self.y > 400 - self.scale:
                self.y = 400 - self.scale
                self.yvel *= -1

            if self.y < 0:
                self.y = 0
                self.yvel *= -1

        self.prev_pos = Vector2(self.x, self.y)
        self.rect.topleft = (self.x, self.y)

    def physics(self, Mode):
        mousepos = pygame.mouse.get_pos()
        
        if not self.bonded:
            self.freephysics()

        if self.rect.collidepoint(mousepos):
            if Mode == "View":
                    if not self.bonded:
                        return str(self.name) + ", " + str(self.ElectronsLeft) + " Valence Electron(s)"
                    else:
                        return "this is not available yet"


    # broken
    def bond_with(self, other_atom):
        if other_atom not in self.bonded_atoms and len(self.bonded_atoms) < self.ElectronsLeft:
            self.bonded_atoms.append(other_atom)
            other_atom.bonded_atoms.append(self)
            self.bonded = True
            other_atom.bonded = True
            self.realign_bonded_atoms()

    def realign_bonded_atoms(self):
        if len(self.bonded_atoms) == 0:
            return
        
        angle_step = 360 / len(self.bonded_atoms)
        radius = self.scale // 2 + 10
        
        for index, atom in enumerate(self.bonded_atoms):
            angle = math.radians(index * angle_step)
            atom.x = self.x + radius * math.cos(angle)
            atom.y = self.y + radius * math.sin(angle)
            atom.rect.topleft = (atom.x, atom.y)
            
    def update_bonded_atoms(self):
        for atom in self.bonded_atoms:
            atom.xvel = self.xvel
            atom.yvel = self.yvel
            atom.x += self.xvel
            atom.y += self.yvel
            atom.rect.topleft = (atom.x, atom.y)
    
    def draw(self, screen):
        screen.blit(self.type, (self.x, self.y))

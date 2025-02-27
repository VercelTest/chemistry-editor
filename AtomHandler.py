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
        self.bonded_atoms = []  # Initialize the bonded_atoms list
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

    # Check if a move would push any atom in the bonded group off-screen
    def is_valid_move(self, delta_x, delta_y, screen_width, screen_height):
        # Check this atom first
        new_x = self.x + delta_x
        new_y = self.y + delta_y
        
        if new_x < 0 or new_x + self.scale > screen_width or new_y < 0 or new_y + self.scale > screen_height:
            return False
            
        # Then check all bonded atoms
        for atom in self.bonded_atoms:
            new_x = atom.x + delta_x
            new_y = atom.y + delta_y
            
            if new_x < 0 or new_x + atom.scale > screen_width or new_y < 0 or new_y + atom.scale > screen_height:
                return False
                
        return True

    # basically only free physics so change this later
    def freephysics(self, screen_width=800, screen_height=400):
        mousepos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # EVENTS
        if self.dragging:
            # Calculate potential new position
            new_x = mousepos[0] - self.offset.x
            new_y = mousepos[1] - self.offset.y
            
            # Calculate potential movement
            delta_x = new_x - self.x
            delta_y = new_y - self.y
            
            # Check if this move is valid (doesn't push any atom off-screen)
            if self.bonded and not self.is_valid_move(delta_x, delta_y, screen_width, screen_height):
                # If not valid, find the maximum valid movement
                # This is a simplified approach - we just don't move in that direction
                if not self.is_valid_move(delta_x, 0, screen_width, screen_height):
                    delta_x = 0
                if not self.is_valid_move(0, delta_y, screen_width, screen_height):
                    delta_y = 0
                    
                # Apply the adjusted movement
                self.x += delta_x
                self.y += delta_y
            else:
                # Apply normal movement with boundary checks
                self.x = new_x
                self.y = new_y
                
                # Apply boundary checks for this atom
                if self.x > screen_width - self.scale:
                    self.x = screen_width - self.scale
                if self.x < 0:
                    self.x = 0
                if self.y > screen_height - self.scale:
                    self.y = screen_height - self.scale
                if self.y < 0:
                    self.y = 0
            
            # Calculate velocity based on movement
            self.xvel = self.x - self.prev_pos.x
            self.yvel = self.y - self.prev_pos.y

        if not mouse_pressed:
            self.dragging = False  

        if not self.dragging:
            # Calculate potential new position with physics
            new_x = self.x + self.xvel
            new_y = self.y + self.yvel
            
            # Check boundaries for this atom
            if new_x > screen_width - self.scale:
                new_x = screen_width - self.scale
                self.xvel *= -1
            if new_x < 0:
                new_x = 0
                self.xvel *= -1
            if new_y > screen_height - self.scale:
                new_y = screen_height - self.scale
                self.yvel *= -1
            if new_y < 0:
                new_y = 0
                self.yvel *= -1
                
            # Apply movement
            self.x = new_x
            self.y = new_y
            
            # Apply friction
            self.xvel *= 0.95
            self.yvel *= 0.95

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

    def draw(self, screen):
        # Draw bonds
        if self.bonded:
            center_x = self.x + self.scale / 2
            center_y = self.y + self.scale / 2
            
            for atom in self.bonded_atoms:
                atom_center_x = atom.x + atom.scale / 2
                atom_center_y = atom.y + atom.scale / 2
                
                # Draw a line representing the bond
                pygame.draw.line(screen, (255, 255, 255), 
                                 (center_x, center_y), 
                                 (atom_center_x, atom_center_y), 2)
        
        screen.blit(self.type, (self.x, self.y))
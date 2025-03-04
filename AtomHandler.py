import pygame
from MathFuncs import *
from AtomPresets import AtomValenceValues
from AtomPresets import BondingRules
import math

selected_atom = None
Vector2 = pygame.math.Vector2

def check_lists(a, b):
    # Sort both lists
    a.sort()
    b.sort()
    
    # Compare if sorted lists are the same
    return a == b

class Atom():
    def __init__(self, type, image):
        self.name = type
        self.type = image

        self.x = 400
        self.y = 200  
        self.xvel = 0
        self.yvel = 0

        self.rect = self.type.get_rect()
        self.scale = image.get_width()
        self.rect.topleft = (self.x, self.y)

        self.ElectronsLeft = AtomValenceValues[self.name]
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
                    selected_atom = self
                    mousepos = pygame.mouse.get_pos()

                    self.offset = Vector2(mousepos[0] - self.x, mousepos[1] - self.y)
                    
                    if self.bonded:
                        for atom in self.bonded_atoms:
                            atom.offset = Vector2(event.pos[0] - atom.x, event.pos[1] - atom.y)
                    

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging:
                self.dragging = False
                selected_atom = None

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

    def equalize_valence(self, otheratom):
        bond_key = (self.name, otheratom.name)
        if bond_key not in BondingRules:
            bond_key = (otheratom.name, self.name)

        bond_values = BondingRules.get(bond_key, (0, 0))
        self.ElectronsLeft += bond_values[0]
        otheratom.ElectronsLeft += bond_values[1]

        return bond_values[0]         
        
    def detectbond(self, AtomList):
        for atom in AtomList:
            if atom != self:
                # better edge detect
                self_center = Vector2(self.x + self.scale // 2, self.y + self.scale // 2)
                atom_center = Vector2(atom.x + atom.scale // 2, atom.y + atom.scale // 2)

                dx = atom_center.x - self_center.x
                dy = atom_center.y - self_center.y
                distance = (dx**2 + dy**2) ** 0.5
                
                ideal_distance = (self.scale + atom.scale) // 2 

                if distance <= ideal_distance:
                    estimatedlist = []

                    if not atom in self.bonded_atoms:
                        estimatedlist.append(atom.name)
                    

                    for bonded in self.bonded_atoms:
                        estimatedlist.append(bonded.name)

                    estimatedlist.append(self.name)
                    
                    if check_lists(estimatedlist, ):
                        print("OMGG")

                    self.equalize_valence(atom)

                    if atom not in self.bonded_atoms:
                        self.bonded = True
                        atom.bonded = True

                        print("NEW BOND DETECTED")
                        self.bonded_atoms.append(atom)
                        atom.bonded_atoms.append(self)

                        if distance != 0:
                            dx /= distance
                            dy /= distance
                            
                            if len(atom.bonded_atoms) == 0:  
                                atom.x = self_center.x + dx * ideal_distance - atom.scale // 2
                                atom.y = self_center.y + dy * ideal_distance - atom.scale // 2
                                atom.rect.topleft = (atom.x, atom.y)
                            else:
                                self.x = atom_center.x - dx * ideal_distance - self.scale // 2
                                self.y = atom_center.y - dy * ideal_distance - self.scale // 2
                                self.rect.topleft = (self.x, self.y)
      
    def bondedphysics(self):
        mousepos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        if self.dragging:
            # Calculate velocity based on previous position
            self.xvel = (mousepos[0] - self.prev_pos.x) * 0.3
            self.yvel = (mousepos[1] - self.prev_pos.y) * 0.3

            # Move primary atom
            self.x = mousepos[0] - self.offset.x
            self.y = mousepos[1] - self.offset.y
            self.rect.topleft = (self.x, self.y)

            # Move bonded atoms while keeping their relative positions
            for atom in self.bonded_atoms:
                atom.xvel = (mousepos[0] - atom.prev_pos.x) * 0.3
                atom.yvel = (mousepos[1] - atom.prev_pos.y) * 0.3

                atom.x = mousepos[0] - atom.offset.x
                atom.y = mousepos[1] - atom.offset.y
                atom.rect.topleft = (atom.x, atom.y)

        if not mouse_pressed:
            self.dragging = False 

            self.rect.topleft = (self.x, self.y)

            for atom in self.bonded_atoms:
                atom.rect.topleft = (self.x, self.y)


        # fix distance bug
        for atom in self.bonded_atoms:
            dx = atom.x - self.x
            dy = atom.y - self.y
            distance = (dx**2 + dy**2) ** 0.5
            ideal_distance = (self.scale + atom.scale) // 2  

            if distance != ideal_distance and distance != 0:
                correction_factor = (ideal_distance - distance) / distance
                move_x = dx * correction_factor * 0.5
                move_y = dy * correction_factor * 0.5

                self.x -= move_x
                self.y -= move_y
                atom.x += move_x
                atom.y += move_y

                self.rect.topleft = (self.x, self.y)
                atom.rect.topleft = (atom.x, atom.y)

        self.prev_pos = Vector2(self.x, self.y)
        
        for atom in self.bonded_atoms:
            atom.prev_pos = Vector2(atom.x, atom.y)

    def format_atoms(self):
        print(self.bonded_atoms)
    
    def physics(self, Mode):
        mousepos = pygame.mouse.get_pos()
        
        if not self.bonded:
            self.freephysics()
        else:
            self.bondedphysics()
        

        if self.rect.collidepoint(mousepos):
            if Mode == "View":
                    if not self.bonded:
                        return str(self.name) + ", " + str(self.ElectronsLeft) + " Valence Electron(s)"
                    else:
                        return str(self.ElectronsLeft)

    def draw(self, screen):
        screen.blit(self.type, (self.x, self.y))
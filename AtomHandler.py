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

    def physics(self, Mode, atom_list, screen_width=800, screen_height=400):
        mousepos = pygame.mouse.get_pos()
        
        if self.bonded and self.dragging:
            # If this atom is bonded and being dragged, update positions of bonded atoms
            self.update_bonded_atoms(screen_width, screen_height)
        elif not self.bonded:
            self.freephysics(screen_width, screen_height)
            
            # Check for collisions with other atoms
            if Mode == "Bond":
                self.check_for_bonding(atom_list)

        if self.rect.collidepoint(mousepos):
            if Mode == "View":
                if not self.bonded:
                    return f"{self.name}, {self.ElectronsLeft} Valence Electron(s)"
                else:
                    bonded_names = [atom.name for atom in self.bonded_atoms]
                    return f"{self.name} bonded with {', '.join(bonded_names)}"

    def check_for_bonding(self, atom_list):
        # Only check for bonding if we have electrons available
        if self.ElectronsLeft <= 0 or self.bonded and len(self.bonded_atoms) >= self.ElectronsLeft:
            return
            
        for atom in atom_list:
            if atom != self and not atom in self.bonded_atoms and atom.ElectronsLeft > 0:
                # Calculate center points
                self_center = Vector2(self.x + self.scale/2, self.y + self.scale/2)
                atom_center = Vector2(atom.x + atom.scale/2, atom.y + atom.scale/2)
                
                # Calculate distance between centers
                distance = self_center.distance_to(atom_center)
                
                # If atoms are close enough, bond them
                if distance < (self.scale + atom.scale) / 2.5:  # Adjust this value for sensitivity
                    self.bond_with(atom)
                    return  # Only bond with one atom at a time

    def bond_with(self, other_atom):
        if other_atom not in self.bonded_atoms and self.ElectronsLeft > 0 and other_atom.ElectronsLeft > 0:
            # Create the bond
            self.bonded_atoms.append(other_atom)
            other_atom.bonded_atoms.append(self)
            
            # Decrement available electrons
            self.ElectronsLeft -= 1
            other_atom.ElectronsLeft -= 1
            
            # Set bonded flag
            self.bonded = True
            other_atom.bonded = True
            
            # Arrange atoms
            self.realign_bonded_atoms()

    def realign_bonded_atoms(self, screen_width=800, screen_height=400):
        if len(self.bonded_atoms) == 0:
            return
        
        # Get center of this atom
        center_x = self.x + self.scale / 2
        center_y = self.y + self.scale / 2
        
        # Calculate angle step
        angle_step = 2 * math.pi / len(self.bonded_atoms)
        
        # Calculate positioning radius (sum of radii plus a small gap)
        for i, atom in enumerate(self.bonded_atoms):
            # Calculate angle for this atom
            angle = i * angle_step
            
            # Calculate distance for bonding (half of both scales plus a small gap)
            distance = (self.scale + atom.scale) / 2
            
            # Calculate new position
            new_x = center_x + math.cos(angle) * distance - (atom.scale / 2)
            new_y = center_y + math.sin(angle) * distance - (atom.scale / 2)
            
            # Ensure the position is within screen boundaries
            new_x = max(0, min(screen_width - atom.scale, new_x))
            new_y = max(0, min(screen_height - atom.scale, new_y))
            
            # Update atom position
            atom.x = new_x
            atom.y = new_y
            atom.rect.topleft = (atom.x, atom.y)
            
            # Update velocity to match this atom
            atom.xvel = self.xvel
            atom.yvel = self.yvel
            
            # Update atom's previous position
            atom.prev_pos = Vector2(atom.x, atom.y)
            
    def update_bonded_atoms(self, screen_width=800, screen_height=400):
        # Get movement delta
        delta_x = self.x - self.prev_pos.x
        delta_y = self.y - self.prev_pos.y
        
        # Move each bonded atom by the same delta
        for atom in self.bonded_atoms:
            # Calculate new position
            new_x = atom.x + delta_x
            new_y = atom.y + delta_y
            
            # Apply boundary checks
            new_x = max(0, min(screen_width - atom.scale, new_x))
            new_y = max(0, min(screen_height - atom.scale, new_y))
            
            # Update position
            atom.x = new_x
            atom.y = new_y
            atom.rect.topleft = (atom.x, atom.y)
            atom.prev_pos = Vector2(atom.x, atom.y)
            
            # Update velocity
            atom.xvel = self.xvel
            atom.yvel = self.yvel
    
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
import pygame

# Adjusted atom sizes (scaled down to fit 400x800 screen)
AtomImages = {
    "Hydrogen": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Hydrogen.png'), (50, 50)),
    "Oxygen": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Oxygen.png'), (55, 55)),
    "Aluminum": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Aluminum.png'), (90, 90)),
    "Boron": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Boron.png'), (72, 72)),
    "Carbon": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Carbon.png'), (65, 65)),
    "Chlorine": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Chlorine.png'), (85, 85)),
    "Fluorine": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Fluorine.png'), (48, 48)),
    "Nitrogen": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Nitrogen.png'), (60, 60)),
    "Phosphorus": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Phosphorus.png'), (95, 95)),
    "Silicon": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Silicon.png'), (98, 98)),
    "Sodium": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Sodium.png'), (95, 95)),
    "Sulfur": pygame.transform.scale(pygame.image.load('Assets/AtomImages/Sulfur.png'), (90, 90)),
}

AtomValenceValues = {
    "Hydrogen": 1,
    "Oxygen": 6,
    "Aluminum": 3,
    "Boron": 3,
    "Carbon": 4,
    "Chlorine": 7,
    "Fluorine": 7,
    "Nitrogen": 5,
    "Phosphorus": 5,
    "Silicon": 4,
    "Sodium": 1,
    "Sulfur": 6,
}



import pygame
from itertools import permutations

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

BondingRules = {}

def determine_bond(val1, val2):
    if val1 <= 3 and val2 > 3:
        return (-val1, min(val1, 8 - val2)) 
    elif val1 > 3 and val2 <= 3:
        return (min(val2, 8 - val1), -val2)
    
    needed1 = 2 - val1 if val1 == 1 else 8 - val1
    needed2 = 2 - val2 if val2 == 1 else 8 - val2 
    bond_strength = min(needed1, needed2)
    return (-bond_strength, -bond_strength) 


for atom1, atom2 in permutations(AtomValenceValues.keys(), 2):
    val1, val2 = AtomValenceValues[atom1], AtomValenceValues[atom2]
    BondingRules[(atom1, atom2)] = determine_bond(val1, val2)
    BondingRules[(atom2, atom1)] = determine_bond(val2, val1) 

# self bonds
for atom in AtomValenceValues.keys():
    val = AtomValenceValues[atom]
    BondingRules[(atom, atom)] = determine_bond(val, val)

AlternateMolStructures = {
    ("Carbon", "Oxygen", "Oxygen"): [0, 8, 8],
    ("Carbon", "Oxygen", "Oxygen", "Oxygen"): [0, 8, 8, 6],
    ("Sulfur", "Oxygen", "Oxygen"): [8, 8, 8],
    ("Sulfur", "Oxygen", "Oxygen", "Oxygen"): [8, 8, 8, 8],
    ("Sulfur", "Oxygen", "Oxygen", "Oxygen", "Oxygen"): [8, 8, 7, 7],
}

AlternateMolStructures = {
    tuple(sorted(key)): value for key, value in AlternateMolStructures.items()
}

CommonMolecules = {
    "H2O": "Water",
    "CO2": "Carbon Dioxide",
    "CO": "Carbon Monoxide",
    "CO3": "Carbonate Ion",
    "HCO3": "Bicarbonate Ion",
    "NaHCO3": "Baking Soda",
    "O2": "Oxygen Gas",
    "N2": "Nitrogen Gas",
    "N2": "Chlorine Gas",
    "F2": "Fluorine Gas",
    "NH3": "Ammonia",
    "CH4": "Methane",
    "SO4": "Sulfate Ion",
    "NO3": "Nitrate Ion",
    "H2SO4": "Sulfuric Acid",
    "NaCl": "Salt",
}

def get_molecule_name(list):
    formula = list.generate_molecular_formula()
    return CommonMolecules.get(formula, formula)  # Return name if found, else return formula


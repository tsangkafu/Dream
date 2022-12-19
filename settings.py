from map.medieval import *

# general setting
WIDTH = 576
HEIGHT = 1024
FPS = 60
TILESIZE = 64
FONT = os.path.join("./font", "BreatheFireIii-PKLOB.ttf")

# map ui
HP_BAR_SIZE = (115, 11)
HP_BAR_COLOR = (140, 30, 30)
EXP_BAR_SIZE = (115, 6)
EXP_BAR_COLOR = (200, 200, 50)
LEVEL_COLOR = (200, 200, 200)
NODE_LINE_COLOR = (113, 10, 10)

# fader
FADER = pygame.Surface((WIDTH, HEIGHT))
FADER.set_alpha(200)
FADER.fill((0, 0, 0))

# battle ui
BATTLE_HP_BAR_SIZE = (170, 30)
BATTLE_HP_BAR_COLOR = (140, 30, 30)
BATTLE_HP_BAR_BG_COLOR = (150, 150, 150)
BATTLE_NAME_TEXT_COLOR = (170, 170, 170)

# dialog ui
DIALOG_TEXT_COLOR = (30, 30, 30)

# game over ui
GAME_OVER_TEXT_COLOR = (230, 30, 30)
GAME_OVER_TEXT_COLOR_SHADOW = (100, 25, 25)

# title ui
TITLE_TEXT_COLOR = (240, 70, 240)
TITLE_TEXT_SHADOW_COLOR = (45, 15, 70)

# item image size
ITEM_SIZE = (55, 55)
ITEM_LARGE_SIZE = (120, 120)

# list of enemies
# the key of the dictionary is corresponding to the scene number
ENEMIES = {
    0: {
        "theme": "md",
        "name": "Stone Mumbler",
        "max_hp": 80,
        "hp": 80,
        "attack": 13,
        "defense": 3,
        "exp": 50,
        "items": [],
        "money": 30,
        "h_offset": 0,
        "sound": 3},
    1: {
        "theme": "md",
        "name": "Taintpaw",
        "max_hp": 120,
        "hp": 120,
        "attack": 20,
        "defense": 5,
        "exp": 70,
        "items": ["Taintpaw"],
        "money": 80,
        "h_offset": 20,
        "sound": 2},
    2: {
        "theme": "md",
        "name": "Corpsesword",
        "max_hp": 300,
        "hp": 300,
        "attack": 200,
        "defense": 10,
        "exp": 500,
        "items": ["Corpsesword", "Myrkul's Mirror"],
        "money": 30,
        "h_offset": 0,
        "sound": 6},
    3: {
        "theme": "md",
        "name": "Bowel Skinner",
        "max_hp": 40,
        "hp": 40,
        "attack": 15,
        "defense": 3,
        "exp": 50,
        "items": ["Honor's Call"],
        "money": 30,
        "h_offset": 30,
        "sound": 5},
    4: {
        "theme": "md",
        "name": "Phantomfreak",
        "max_hp": 300,
        "hp": 300,
        "attack": 45,
        "defense": 15,
        "exp": 500,
        "items": ["Extinction", "Iron Oath"],
        "money": 30,
        "h_offset": 0,
        "sound": 0},
    5: {
        "theme": "md",
        "name": "Bonehand",
        "max_hp": 120,
        "hp": 120,
        "attack": 35,
        "defense": 10,
        "exp": 250,
        "items": ["Toothpick"],
        "money": 30,
        "h_offset": -40,
        "sound": 9},
    6: {
        "theme": "md",
        "name": "Dreadsnare",
        "max_hp": 140,
        "hp": 140,
        "attack": 30,
        "defense": 5,
        "exp": 150,
        "items": ["Gladius", "Conquest's Cuisses"],
        "money": 30,
        "h_offset": 0,
        "sound": 8},
    7: {
        "theme": "md",
        "name": "Defiant Hunter",
        "max_hp": 150,
        "hp": 150,
        "attack": 35,
        "defense": 15,
        "exp": 140,
        "items": ["Suspension"],
        "money": 30,
        "h_offset": 0,
        "sound": 12},
    8: {
        "theme": "md",
        "name": "Flamepod",
        "max_hp": 200,
        "hp": 200,
        "attack": 40,
        "defense": 30,
        "exp": 450,
        "items": ["Raddle", "Flint"],
        "money": 30,
        "h_offset": 0,
        "sound": 0},
    9: {
        "theme": "md",
        "name": "Grimescream",
        "max_hp": 250,
        "hp": 250,
        "attack": 70,
        "defense": 20,
        "exp": 700,
        "items": ["Ataraxia", "Glory of Gond"],
        "money": 30,
        "h_offset": 0,
        "sound": 7},
    10: {
        "theme": "md",
        "name": "Cindersword",
        "max_hp": 150,
        "hp": 150,
        "attack": 80,
        "defense": 5,
        "exp": 600,
        "items": ["Infinitum", "Feral Plackart"],
        "money": 30,
        "h_offset": 0,
        "sound": 12},
    11: {
        "theme": "md",
        "name": "Bladetalon",
        "max_hp": 350,
        "hp": 350,
        "attack": 80,
        "defense": 20,
        "exp": 850,
        "items": ["Kinslayer"],
        "money": 30,
        "h_offset": 0,
        "sound": 5},
    12: {
        "theme": "md",
        "name": "Behemoth",
        "max_hp": 500,
        "hp": 500,
        "attack": 80,
        "defense": 40,
        "exp": 1500,
        "items": ["Heartseeker"],
        "money": 30,
        "h_offset": 0,
        "sound": 13},
    13: {
        "theme": "md",
        "name": "Mournfoot",
        "max_hp": 300,
        "hp": 300,
        "attack": 70,
        "defense": 30,
        "exp": 700,
        "items": [],
        "money": 30,
        "h_offset": -40,
        "sound": 10},
    14: {
        "theme": "md",
        "name": "Dismal Abortion",
        "max_hp": 250,
        "hp": 250,
        "attack": 45,
        "defense": 35,
        "exp": 500,
        "items": ["Dismal Head"],
        "money": 30,
        "h_offset": 0,
        "sound": 9},
    15: {
        "theme": "md",
        "name": "MAIRE",
        "max_hp": 400,
        "hp": 400,
        "attack": 110,
        "defense": 10,
        "exp": 1500,
        "items": ["Artificer's Opus"],
        "money": 30,
        "h_offset": 150,
        "sound": 9},
    16: {
        "theme": "md",
        "name": "URSINUS",
        "max_hp": 350,
        "hp": 350,
        "attack": 60,
        "defense": 10,
        "exp": 650,
        "items": ["Tyrant's Crown"],
        "money": 30,
        "h_offset": 0,
        "sound": 1},
    17: {
        "theme": "md",
        "name": "PRUDDENTIUS",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": ["Arcane Pauldron"],
        "money": 30,
        "h_offset": 0,
        "sound": 3},
    18: {
        "theme": "md",
        "name": "EGNATIUS",
        "max_hp": 500,
        "hp": 500,
        "attack": 90,
        "defense": 50,
        "exp": 2000,
        "items": ["Nerves of Steel"],
        "money": 30,
        "h_offset": 0,
        "sound": 12},
    19: {
        "theme": "md",
        "name": "IDUMA",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": ["Mercy"],
        "money": 30,
        "h_offset": 100,
        "sound": 11},
    # chapter 2 enemies
    20: {
        "theme": "gs",
        "name": "Mario Maddog",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11},
    21: {
        "theme": "gs",
        "name": "Pietro Ferocious",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11},
    22: {
        "theme": "gs",
        "name": "Frankie Blades",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    23: {
        "theme": "gs",
        "name": "Davide Coldblooded",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    24: {
        "theme": "gs",
        "name": "Angelo The Animal",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    25: {
        "theme": "gs",
        "name": "Carlo Hammer",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    26: {
        "theme": "gs",
        "name": "Johnny Hands",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": ["Head"],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    27: {
        "theme": "gs",
        "name": "Vito Savage",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    28: {
        "theme": "gs",
        "name": "Antonio Viper",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    29: {
        "theme": "gs",
        "name": "Incendiary Giovanni",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    30: {
        "theme": "gs",
        "name": "Salvatore Scarface",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
    31: {
        "theme": "gs",
        "name": "Francesco Pistolero",
        "max_hp": 100,
        "hp": 100,
        "attack": 14,
        "defense": 5,
        "exp": 80,
        "items": [],
        "money": 30,
        "h_offset": 100,
        "sound": 11
    },
}


"""
Type 0 = Item, Type 1 = Weapon, Type 2 = Shield
"""
ITEMS = {
    # weapons
    "toothpick": {
        "type": 1,
        "attack": 30,
        "defense": 5,
        "value": 5
    },
    "gladius": {
        "type": 1,
        "attack": 18,
        "defense": 0,
        "value": 15
    },
    "taintpaw": {
        "type": 1,
        "attack": 15,
        "defense": 2,
        "value": 14
    },
    "heartseeker": {
        "type": 1,
        "attack": 80,
        "defense": 0,
        "value": 15
    },
    "kinslayer": {
        "type": 1,
        "attack": 35,
        "defense": 0,
        "value": 18
    },
    "honor's_call":{
        "type": 1,
        "attack": 10,
        "defense": 5,
        "value": 15
    },
    "extinction": {
        "type": 1,
        "attack": 40,
        "defense": 10,
        "value": 20
    },
    "corpsesword": {
        "type": 1,
        "attack": 40,
        "defense": 10,
        "value": 50
    },
    "raddle": {
        "type": 1,
        "attack": 60,
        "defense": -15,
        "value": 50
    },
    "verdict": {
        "type": 1,
        "attack": 20,
        "defense": 10,
        "value": 50
    },
    "suspension": {
        "type": 1,
        "attack": 15,
        "defense": 5,
        "value": 50
    },
    "ataraxia": {
        "type": 1,
        "attack": 35,
        "defense": 0,
        "value": 50
    },
    # shields
    "artificer's_opus": {
        "type": 2,
        "attack": 15,
        "defense": 40,
        "value": 50
    },
    "myrkul's_mirror": {
        "type": 2,
        "attack": 20,
        "defense": 10,
        "value": 50
    },
    "iron_oath": {
        "type": 2,
        "attack": 0,
        "defense": 40,
        "value": 50
    },
    "conquest's_cuisses": {
        "type": 2,
        "attack": 0,
        "defense": 15,
        "value": 50
    },
    "feral_plackart": {
        "type": 2,
        "attack": 0,
        "defense": 30,
        "value": 50
    },
    "infinitum": {
        "type": 2,
        "attack": 15,
        "defense": 15,
        "value": 50
    },
    "arcane_pauldron": {
        "type": 2,
        "attack": 20,
        "defense": 10,
        "value": 50
    },
    "glory_of_gond": {
        "type": 2,
        "attack": 20,
        "defense": 20,
        "value": 50
    },
    "nerves_of_steel": {
        "type": 2,
        "attack": 20,
        "defense": 10,
        "value": 50
    },
    "tyrant's_crown": {
        "type": 2,
        "attack": 10,
        "defense": 60,
        "value": 50
    },
    # items
    "dismal_head": {
        "type": 0,
        "attack": 0,
        "defense": 0,
        "value": 50
    },
    "flint": {
        "type": 0,
        "attack": 0,
        "defense": 0,
        "value": 50
    },
    "mercy": {
        "type": 0,
        "attack": 999,
        "defense": 0,
        "value": 18
    },

    # chapter 2 items
    "head": {
        "type": 0,
        "attack": 999,
        "defense": 0,
        "value": 18
    },
}

NPCS = {
    0: {
        "theme": "md",
        "name": "Egnatius Barbatus",
        "max_hp": 80,
        "hp": 80,
        "attack": 18,
        "defense": 3,
        "exp": 50,
        "items": [],
        "money": 30,
        "h_offset": 0,
        "pos": (440, 230)
    },
    1: {
        "theme": "md",
        "name": "Iduma Macer",
        "max_hp": 80,
        "hp": 80,
        "attack": 18,
        "defense": 3,
        "exp": 50,
        "items": [],
        "money": 30,
        "h_offset": 0,
        "pos": (190, 90)
    },
    2: {
        "theme": "md",
        "name": "Maire Whelani",
        "max_hp": 80,
        "hp": 80,
        "attack": 18,
        "defense": 3,
        "exp": 50,
        "items": [],
        "money": 30,
        "h_offset": 0,
        "pos": (380, 500)
    },
    3: {
        "theme": "md",
        "name": "Prudentius Stolo",
        "max_hp": 80,
        "hp": 80,
        "attack": 18,
        "defense": 3,
        "exp": 50,
        "items": [],
        "money": 30,
        "h_offset": 0,
        "pos": (140, 650)
    },
    4: {
        "theme": "md",
        "name": "Ursinus Clodianus",
        "max_hp": 80,
        "hp": 80,
        "attack": 18,
        "defense": 3,
        "exp": 50,
        "items": [],
        "money": 30,
        "h_offset": 0,
        "pos": (90, 400)
    }
}
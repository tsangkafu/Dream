from map.medieval import *

# general setting
WIDTH = 576
HEIGHT = 1024
FPS = 60
TILESIZE = 64

# map ui
HP_BAR_SIZE = (115, 11)
HP_BAR_COLOR = (140, 30, 30)
EXP_BAR_SIZE = (115, 6)
EXP_BAR_COLOR = (200, 200, 50)
LEVEL_COLOR = (200, 200, 200)

# battle ui
BATTLE_HP_BAR_SIZE = (170, 30)
BATTLE_HP_BAR_COLOR = (140, 30, 30)
BATTLE_HP_BAR_BG_COLOR = (150, 150, 150)
BATTLE_NAME_TEXT_COLOR = (170, 170, 170)

# dialog ui
DIALOG_TEXT_COLOR = (30, 30, 30)

# list of enemies
ENEMIES = {
    1: {
        "theme": "md",
        "name": "Stone Mumbler",
        "max_hp": 80,
        "hp": 70,
        "attack": 5,
        "defense": 3,
        "exp": 30,
        "items": [],
        "h_offset": 0
    }
}
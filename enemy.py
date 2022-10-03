import pygame
import os

from settings import *

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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, theme, name, max_hp, hp, attack, defense, exp, items, h_offset):
        super().__init__(groups)
        self.theme = theme
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.items = items
        # offset of the position of the enemy to match different scene
        self.h_offset = h_offset
        self.image = pygame.image.load(os.path.join("./graphics/enemy/md", self.name.replace(" ", "_").lower() + ".png")).convert_alpha()
        self.rect = self.image.get_rect()
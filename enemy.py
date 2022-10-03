import pygame
import os

from settings import *

ENEMIES = {
    1: {
        "theme": "md",
        "name": "Stone Mumbler",
        "hp": 80,
        "attack": 5,
        "defense": 3,
        "exp": 30,
        "items": [],
        "h_offset": 0
    }
}

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, theme, name, hp, attack, defense, exp, items, h_offset):
        super().__init__(groups)
        self.theme = theme
        self.name = name
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.items = items
        self.h_offset = h_offset
        self.image = pygame.image.load(os.path.join("./graphics/enemy/md", self.name.replace(" ", "_").lower() + ".png")).convert_alpha()
        self.rect = self.image.get_rect()
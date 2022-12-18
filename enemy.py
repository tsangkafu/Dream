import pygame
import os

from settings import *

class Enemy(pygame.sprite.Sprite):
    def __init__(self, groups, key, theme, name, max_hp, hp, attack, defense, exp, items, money, h_offset, sound):
        super().__init__(groups)
        self.theme = theme
        self.key = key
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.items = items
        self.money = money
        # offset of the position of the enemy to match different scene
        self.h_offset = h_offset
        self.sound = sound
        try:
            self.image = pygame.image.load(os.path.join("./graphics/enemy/" + theme, self.name.replace(" ", "_").lower() + ".png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/enemy/md", self.name.replace(" ", "_").lower() + ".png")).convert_alpha()
        self.large_image = pygame.transform.smoothscale(self.image, (160, 280)).convert_alpha()
        self.large_image.convert_alpha()
        self.rect = self.image.get_rect()
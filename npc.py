import pygame
import os
from scene import scenes

from settings import *

class NPC(pygame.sprite.Sprite):
    def __init__(self, groups, theme, name, max_hp, hp, attack, defense, exp, items, money, h_offset, pos):
        super().__init__(groups)
        self.theme = theme
        self.name = name
        self.max_hp = max_hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp = exp
        self.items = items
        self.money = money
        # indicate if talking with the NPC help player to recover HP
        self.help_recover = False
        # offset of the position of the enemy to match different scene
        self.h_offset = h_offset
        try:
            self.image = pygame.image.load(os.path.join("./graphics/npc/" + theme, self.name.replace(" ", "_").lower() + ".png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/npc/md", self.name.replace(" ", "_").lower() + ".png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.large_image = self.image.copy().convert_alpha()
        # image that used in the village
        self.v_image = pygame.transform.smoothscale(self.image, (70, 123)).convert_alpha()
        self.v_rect = self.v_image.get_rect(center = self.rect.center)
        self.dialogs = []
        self.dialog_count = 0
        self.get_dialog()


    def update(self, screen):
        screen.blit(self.v_image, self.v_rect)

    """
    A method to traverse the dialog to get those dialog containing npc name
    Put it into the list "dialogs" to keep track of the dialog
    """
    def get_dialog(self):
        for scene in scenes:
            for sentence in scenes[scene]:
                if self.name in sentence and scene not in self.dialogs:
                    self.dialogs.append(scene)

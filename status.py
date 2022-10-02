import pygame
import os

from settings import *

HP_BAR_SIZE = (115, 11)
HP_BAR_COLOR = (140, 30, 30)
EXP_BAR_SIZE = (115, 6)
EXP_BAR_COLOR = (200, 200, 50)

class Status(pygame.sprite.Sprite):
    def __init__(self, screen, groups, player):
        super().__init__(groups)
        self.screen = screen
        self.player = player
        self.image = pygame.image.load(os.path.join("./graphics/ui", "status_bar.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = (WIDTH - self.image.get_width(), 5))
        self.level = player.level
        self.max_hp = player.max_hp
        self.hp = player.hp
        self.exp = player.exp
        
        self.hp_bar = pygame.Surface(HP_BAR_SIZE)
        self.hp_bar.fill(HP_BAR_COLOR)
        # hp bar position should be relational to status bar's rect
        self.hp_bar_rect = self.hp_bar.get_rect(topleft = (self.rect.topleft[0] + 74, self.rect.topleft[1] + 25))

        self.exp_bar = pygame.Surface(EXP_BAR_SIZE)
        self.exp_bar.fill(EXP_BAR_COLOR)
        self.exp_bar_rect = self.hp_bar.get_rect(topleft = (self.rect.topleft[0] + 74, self.rect.topleft[1] + 42))
    
    def draw(self):
        self.screen.blit(self.hp_bar, self.hp_bar_rect)
        self.screen.blit(self.exp_bar, self.exp_bar_rect)
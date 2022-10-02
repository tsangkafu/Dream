import pygame
import os

from settings import *

class Status(pygame.sprite.Sprite):
    def __init__(self, screen, groups, player):
        super().__init__(groups)
        self.screen = screen
        self.player = player
        self.image = pygame.image.load(os.path.join("./graphics/ui", "status_bar.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = (WIDTH - self.image.get_width() - 5, 10))
        self.level = player.level
        self.hp = player.hp
        self.exp = player.exp
        
        self.hp_bar = pygame.Surface((115, 11))
        self.hp_bar.fill((140, 30, 30))
        self.hp_bar_rect = self.hp_bar.get_rect(topleft = (WIDTH - 127, 35))
        self.exp_bar = pygame.Surface((115, 7))
        self.exp_bar.fill((200, 200, 50))
        self.exp_bar_rect = self.hp_bar.get_rect(topleft = (WIDTH - 127, 51))
    
    def draw(self):
        self.screen.blit(self.hp_bar, self.hp_bar_rect)
        self.screen.blit(self.exp_bar, self.exp_bar_rect)
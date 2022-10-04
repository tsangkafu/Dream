import pygame
import os

from settings import *

class Status(pygame.sprite.Sprite):
    def __init__(self, screen, groups, player):
        super().__init__(groups)
        self.screen = screen
        self.player = player
        self.image = pygame.image.load(os.path.join("./graphics/ui/md", "status_bar.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = (WIDTH - self.image.get_width(), 5))
            
    def draw(self, theme):
        self.image = pygame.image.load(os.path.join("./graphics/ui/" + theme, "status_bar.png")).convert_alpha()
        
        self.hp_bar = pygame.Surface(HP_BAR_SIZE)
        self.hp_bar.fill(HP_BAR_COLOR)
        # hp bar position should be relational to status bar
        self.hp_bar_rect = self.hp_bar.get_rect(topleft = (self.rect.topleft[0] + 74, self.rect.topleft[1] + 25))

        self.exp_bar = pygame.Surface(EXP_BAR_SIZE)
        self.exp_bar.fill(EXP_BAR_COLOR)
        self.exp_bar_rect = self.exp_bar.get_rect(topleft = (self.rect.topleft[0] + 74, self.rect.topleft[1] + 42))

        # scaling health bar
        hp_ratio = self.player.hp / self.player.max_hp
        # time ratio with the hp bar to get the new hp bar
        new_hp_bar = pygame.Surface((HP_BAR_SIZE[0] * hp_ratio, HP_BAR_SIZE[1]))
        new_hp_bar.fill(HP_BAR_COLOR)

        exp_ratio = self.player.exp / self.player.exp_to_upgrade
        new_exp_bar = pygame.Surface((EXP_BAR_SIZE[0] * exp_ratio, EXP_BAR_SIZE[1]))
        new_exp_bar.fill(EXP_BAR_COLOR)

        # print the level to the status bar
        self.font = pygame.font.Font(os.path.join("./font", "BreatheFireIii-PKLOB.ttf"), 40)
        level_surface = self.font.render(str(self.player.level), True, LEVEL_COLOR)
        # level number should be relationship to the status bar
        level_surface_rect = level_surface.get_rect(center = (self.rect.topleft[0] + 37, self.rect.topleft[1] + 37))

        self.screen.blit(new_hp_bar, self.hp_bar_rect)
        self.screen.blit(new_exp_bar, self.exp_bar_rect)
        self.screen.blit(level_surface, level_surface_rect)
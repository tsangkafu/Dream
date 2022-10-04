import pygame
import os

from settings import *


HP_BAR_SIZE = (170, 30)
HP_BAR_COLOR = (140, 30, 30)
HP_BAR_BG_COLOR = (150, 150, 150)
TEXT_COLOR = (200, 200, 200)

class Battle():
    def __init__(self, screen, player):
        # a number serving as the index of the ENEMIES dict
        self.screen = screen
        self.player = player
        # copy the image to the battle object
        self.player_image = self.player.large_image
        self.finished_battle = []
        self.battle_end = True
        self.background_alpha = 0
        self.object_alpha = 0
        self.font = pygame.font.Font(os.path.join("./font", "BreatheFireIii-PKLOB.ttf"), 25)


    def start(self, theme, enemy, scene):
        if scene not in self.finished_battle:
            self.battle_end = False
            # create the scene
            self.scene = scene
            self.enemy = enemy
            # copy the image to the battle object
            self.enemy_image = self.enemy.image
            # draw the background
            self.draw_background()
            # populate enemy and player
            self.draw_character()
            # draw ui
            self.draw_ui(theme)
    
    def draw_background(self):
        image = pygame.image.load(os.path.join("./graphics/scene/", str(self.scene) + ".png"))
        # fade in transition
        if self.background_alpha < 255: 
            self.background_alpha += 20
        image.set_alpha(self.background_alpha)
        self.screen.blit(image, (0, 0))


    def draw_character(self):
        # fade in transition
        if self.object_alpha < 255:
            self.object_alpha += 10
            self.player_image.set_alpha(self.object_alpha)
            self.enemy_image.set_alpha(self.object_alpha)

        self.player_image_rect = self.player_image.get_rect(topleft = (30, 695))
        # add the h_offset in case the enemy will show up in different height of the background
        self.enemy_image_rect = self.enemy_image.get_rect(topleft = (365, 410 + self.enemy.h_offset))

        self.screen.blit(self.player_image, self.player_image_rect)
        self.screen.blit(self.enemy_image, self.enemy_image_rect)

    def draw_ui(self, theme):
        # the background of the ui
        player_info = pygame.image.load(os.path.join("./graphics/ui/" + theme, "player_info.png"))
        player_info.set_alpha(self.object_alpha)
        player_info_rect = player_info.get_rect(topleft = (
            self.player_image_rect.topleft[0] + 205,
            self.player_image_rect.topleft[1] + 130))
        self.screen.blit(player_info, player_info_rect)

        enemy_info = pygame.image.load(os.path.join("./graphics/ui/" + theme, "enemy_info.png"))
        enemy_info.set_alpha(self.object_alpha)
        enemy_info_rect = enemy_info.get_rect(topleft = (
            self.enemy_image_rect.topleft[0] - 345,
            self.enemy_image_rect.topleft[1]))
        self.screen.blit(enemy_info, enemy_info_rect)

        # name of player
        player_name_surface = self.font.render(self.player.name, True, TEXT_COLOR)
        player_name_rect = player_name_surface.get_rect(center = (
            player_info_rect.topleft[0] + 200,
            player_info_rect.topleft[1] + 55))
        # the player name should be relational to the info box
        player_name_surface.set_alpha(self.object_alpha)
        self.screen.blit(player_name_surface, player_name_rect)

        # name of the enemy
        enemy_name_surface = self.font.render(self.enemy.name, True, TEXT_COLOR)
        # the enemy name should be relational to the info box
        enemy_name_rect = enemy_name_surface.get_rect(center = (
            enemy_info_rect.topleft[0] + 190,
            enemy_info_rect.topleft[1] + 50))
        enemy_name_surface.set_alpha(self.object_alpha)
        self.screen.blit(enemy_name_surface, enemy_name_rect)

        print(player_info_rect.topleft, enemy_info_rect.topleft)
        # hp bar of the player
        player_hp_ratio = self.player.hp / self.player.max_hp
        player_hp_bar = pygame.Surface((HP_BAR_SIZE[0] * player_hp_ratio, HP_BAR_SIZE[1]))
        player_hp_bar.fill(HP_BAR_COLOR)
        player_hp_bar_bg = pygame.Surface(HP_BAR_SIZE)
        player_hp_bar_bg.fill(HP_BAR_BG_COLOR)
        player_hp_bar_bg.set_alpha(100)
        # the hp bar should be relational to the info box
        player_hp_bar_pos = (
            player_info_rect.topleft[0] + 115,
            player_info_rect.topleft[1] + 90)
        # the position of the hp bar should be on the hp bar background
        player_hp_bar_rect = player_hp_bar.get_rect(topleft = player_hp_bar_pos)
        player_hp_bar_bg_rect = player_hp_bar_bg.get_rect(topleft = player_hp_bar_pos)
        self.screen.blit(player_hp_bar_bg, player_hp_bar_bg_rect)
        self.screen.blit(player_hp_bar, player_hp_bar_rect)

        # hp bar of the enemy
        enemy_hp_ratio = self.enemy.hp / self.enemy.max_hp
        enemy_hp_bar = pygame.Surface((HP_BAR_SIZE[0] * enemy_hp_ratio, HP_BAR_SIZE[1]))
        enemy_hp_bar.fill(HP_BAR_COLOR)
        enemy_hp_bar_bg = pygame.Surface(HP_BAR_SIZE)
        enemy_hp_bar_bg.fill(HP_BAR_BG_COLOR)
        enemy_hp_bar_bg.set_alpha(100)
        # the position of the hp bar should be on the hp bar background
        enemy_hp_bar_pos = (
            enemy_info_rect.topleft[0] + 105,
            enemy_info_rect.topleft[1] + 85)
            # enemy_info.get_width() - 195,
            # HEIGHT - enemy_info.get_height() - 345 + self.enemy.h_offset)
        enemy_hp_bar_rect = enemy_hp_bar.get_rect(topleft = enemy_hp_bar_pos)
        enemy_hp_bar_bg_rect = enemy_hp_bar_bg.get_rect(topleft = enemy_hp_bar_pos)
        self.screen.blit(enemy_hp_bar_bg, enemy_hp_bar_bg_rect)
        self.screen.blit(enemy_hp_bar, enemy_hp_bar_rect)
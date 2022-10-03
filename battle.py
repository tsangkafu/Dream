import pygame
import os

from settings import *

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
        self.character_alpha = 0

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
        if self.character_alpha < 255:
            self.character_alpha += 10
            self.player_image.set_alpha(self.character_alpha)
            self.enemy_image.set_alpha(self.character_alpha)
        self.screen.blit(self.player_image, (30, HEIGHT - self.player_image.get_height() - 50))
        self.screen.blit(self.enemy_image, (
                WIDTH - self.enemy_image.get_width() - 50,
                HEIGHT - self.enemy_image.get_height() + self.enemy.h_offset - 320
            )
        )

    def draw_ui(self, theme):
        # player ui
        player_info = pygame.image.load(os.path.join("./graphics/ui/" + theme, "player_info.png"))
        enemy_info = pygame.image.load(os.path.join("./graphics/ui/" + theme, "enemy_info.png"))
        self.screen.blit(player_info, (self.player_image.get_rect().topleft))
        self.screen.blit(enemy_info, (0, 0))

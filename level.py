from tkinter import Y
import pygame

from settings import *
from node import Node
from player import Player
from debug import debug

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        self.visible_sprites = pygame.sprite.Group()
        self.obstacles_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        for i, row in enumerate(MEDIEVAL_MAP):
            for j, col in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE
                # empty node
                if col == "N":
                    Node((x, y), [self.visible_sprites])
                # player
                if col == "P":
                    self.player = Player((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.draw(self.display_surface)
        self.visible_sprites.update()
        debug(self.player.direction)
import pygame

from settings import *
from node import Node
from player import Player
from cursor import Cursor
from debug import debug

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # including player, enemy
        self.visible_sprites = pygame.sprite.Group()
        self.empty_node_sprites = pygame.sprite.Group()
        self.create_map()
        self.cursor = Cursor(pygame.mouse.get_pos())

    # will only be called once    
    def create_map(self):
        for i, row in enumerate(MEDIEVAL_MAP):
            for j, col in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE
                # empty nodes
                if col == "N":
                    Node((x, y), "empty", [self.empty_node_sprites])
                # player
                if col == "P":
                    self.player = Player((x, y), [self.visible_sprites])
                # emenies
                if col == "E":
                    Node((x, y), "enemy" ,[self.empty_node_sprites])

    def run(self):
        self.empty_node_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)

        # initalize the cursor if not collided
        self.cursor.swap_cursor("normal")

        for empty_node in self.empty_node_sprites:
            # if the empty node is collided with cursor position, switch the cursor
            if empty_node.rect.collidepoint(pygame.mouse.get_pos()):
                self.cursor.swap_cursor("hand")
                break

        debug(self.player.pos)

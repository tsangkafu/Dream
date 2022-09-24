import pygame
import math

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
        self.node_sprites = pygame.sprite.Group()
        self.nodes = []
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
                    node = Node((x, y), (j, i), "empty", [self.node_sprites])
                    self.nodes.append(node)
                    print((j, i))
                # player
                if col == "P":
                    # create a empty node where the player is
                    node = Node((x, y), (j, i), "empty", [self.node_sprites])
                    self.nodes.append(node)
                    # create player
                    self.player = Player((x, y), [self.visible_sprites])
                # emenies
                if col == "E":
                    node = Node((x, y), (j, i), "enemy", [self.node_sprites])
                    self.nodes.append(node)
                    print((j, i))
                # village
                if col == "V":
                    node = Node((x, y), (j, i), "village", [self.node_sprites])
                    self.nodes.append(node)
                    print((j, i))
                if col == "B":
                    node = Node((x, y), (j, i), "boss", [self.node_sprites])
                    self.nodes.append(node)
                    print((j, i))

    def run(self):
        # draw lines between current node and every neighbor node
        for node in self.nodes:
            # get the node where the player is
            if node.rect.collidepoint(self.player.rect.center):
                # loop to get the the target node
                for target_node in self.nodes:
                    if target_node.ab_pos in MEDIEVAL_GRAPH[node.ab_pos]:
                        node.set_neighbor(target_node)
                        pygame.draw.line(self.display_surface, (113, 10, 10), node.rect.center, target_node.rect.center, 7)

        self.node_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)

        # initalize the cursor if not collided
        self.cursor.swap_cursor("normal")
        for empty_node in self.node_sprites:
            # if the empty node is collided with cursor position, switch the cursor
            if empty_node.rect.collidepoint(pygame.mouse.get_pos()):
                self.cursor.swap_cursor("hand")
                break
        
        # import debug window to get the abstract coordinate faster
        debug(self.player.pos)
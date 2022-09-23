import pygame
import os

from settings import *


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, ab_pos, node_type, groups):
        super().__init__(groups)
        # represent the node with proper image according to node type
        if (node_type == "enemy"):
            self.image = pygame.image.load(os.path.join("./graphics/node", "enemy_node.png")).convert_alpha()
        elif (node_type == "empty"):
            self.image = pygame.image.load(os.path.join("./graphics/node", "empty_node.png")).convert_alpha()
        # a tuple representing abstract coordinates that scaled to 9 * 16 map
        self.ab_pos = ab_pos
        self.rect = self.image.get_rect(topleft = pos)
        # a list that will store all the neighbors
        self.neighbors = set()

    def set_neighbor(self):
        pass

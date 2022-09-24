import pygame
import os

from settings import *


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, ab_pos, node_type, groups):
        super().__init__(groups)
        self.image = self.get_image(node_type)
        # a tuple representing abstract coordinates that scaled to 9 * 16 map
        self.ab_pos = ab_pos
        self.rect = self.image.get_rect(topleft = pos)
        # a list that will store all the neighbors
        self.neighbors = []

    def set_neighbor(self, node):
        self.neighbors.append(node)

    def is_neighor(self, node):
        return node in self.neighbors

    # represent the node with proper image according to node type
    def get_image(self, node_type):
        if (node_type == "enemy"):
            return pygame.image.load(os.path.join("./graphics/node", "enemy_node.png")).convert_alpha()
        elif (node_type == "empty"):
            return pygame.image.load(os.path.join("./graphics/node", "empty_node.png")).convert_alpha()
        elif (node_type == "village"):
            return pygame.image.load(os.path.join("./graphics/node", "village_node.png")).convert_alpha()
        elif (node_type == "boss"):
            return pygame.image.load(os.path.join("./graphics/node", "boss_node.png")).convert_alpha()
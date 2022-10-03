import pygame
import os

from settings import *


class Node(pygame.sprite.Sprite):
    def __init__(self, pos, ab_pos, node_type, groups):
        super().__init__(groups)
        self.node_type = node_type
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
        return pygame.image.load(os.path.join("./graphics/node", node_type + "_node.png")).convert_alpha()
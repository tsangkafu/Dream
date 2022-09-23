import pygame
import os

from settings import *

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, node_type, groups):
        super().__init__(groups)
        if (node_type == "enemy"):
            self.image = pygame.image.load(os.path.join("./graphics/node", "enemy_node.png")).convert_alpha()
        elif (node_type == "empty"):
            self.image = pygame.image.load(os.path.join("./graphics/node", "empty_node.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

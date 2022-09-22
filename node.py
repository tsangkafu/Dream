import pygame
import os

from settings import *

class Node(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.image.load(os.path.join("./graphics/node", "unchecked_node.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

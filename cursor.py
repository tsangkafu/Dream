from sqlite3 import Cursor
import pygame
import os

class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        # replace the cursor
        pygame.mouse.set_visible(False)
        # default cursor is a normal cursor
        self.image = pygame.image.load(os.path.join("./graphics/cursor", "normal_cursor.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def swap_cursor(self, cursor):
        if cursor == "normal":
            self.image = pygame.image.load(os.path.join("./graphics/cursor", "normal_cursor.png")).convert_alpha()
        if cursor == "hand":
            self.image = pygame.image.load(os.path.join("./graphics/cursor", "hand_cursor.png")).convert_alpha()
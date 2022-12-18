import pygame
import os

class Cursor(pygame.sprite.Sprite):
    def __init__(self, pos, theme):
        # replace the cursor
        pygame.mouse.set_visible(False)
        # default cursor is a normal cursor
        try:
            self.image = pygame.image.load(os.path.join("./graphics/cursor" + theme, "normal.png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/cursor/md", "normal.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)

    def swap_cursor(self, theme, cursor):
        try:
            self.image = pygame.image.load(os.path.join("./graphics/cursor/" + theme, cursor + ".png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/cursor/md", cursor + ".png")).convert_alpha()
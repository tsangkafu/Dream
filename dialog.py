from tkinter import FALSE
import pygame
import os
import settings

class Dialog(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = self.get_image()
        self.rect = self.image.get_rect()

    def get_image(self):
        return pygame.image.load(os.path.join("./graphics/menu/md", "md_dialog.png")).convert_alpha()

    def update(self):
        pass

    def draw(self, screen):
        pass

class DialogManager():
    pass
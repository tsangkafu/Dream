from tkinter import FALSE
import pygame
import os
import settings

class Dialog():
    def __init__(self):
        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.is_shown = True

    def get_image(self):
        return pygame.image.load(os.path.join("./graphics/menu/md", "md_dialog.png")).convert_alpha()

    def show_bubble(self, screen):
        screen.blit(self.image, (0, settings.HEIGHT - self.rect.h))

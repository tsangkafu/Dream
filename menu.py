import pygame
import os

# menu_type: game_menu, equipment_menu...
class Menu():
    def __init__(self, menu_type):
        self.image = self.get_image(menu_type)

    def get_image(self, menu_type):
        return pygame.image.load(os.path.join("./graphics/menu", menu_type + ".png")).convert_alpha()
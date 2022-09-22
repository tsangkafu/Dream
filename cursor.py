from sqlite3 import Cursor
import pygame
import os

class Cursor():
    def __init__(self):
        pass

    def normal_cursor(self):
        return pygame.image.load(os.path.join("./graphics/cursor", "normal_cursor.png"))
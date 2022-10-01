import pygame
import sys

from settings import *
from level import Level
from map.medieval import *
from cursor import Cursor
from node import *
from menu import Menu

class Game:
    def __init__(self):
        pygame.init()
        self.md_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dream")
        self.clock = pygame.time.Clock()
        self.md_level = Level("md", self.md_screen)

    def run(self):
        while True:
            self.md_level.run()

            # update the whole screen
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
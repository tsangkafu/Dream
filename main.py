import pygame
import sys

from settings import *
from level import Level
from map.medieval import *

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dream")
        self.clock = pygame.time.Clock()
        self.level = Level("md", self.screen)

    def run(self):
        while True:
            self.level.run()

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
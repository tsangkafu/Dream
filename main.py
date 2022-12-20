import pygame
import sys

from settings import *
from level import Level
from map.medieval import *

class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 2048)
        pygame.init()
        pygame.display.set_caption("Dream")
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            self.level.run()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
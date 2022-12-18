import pygame
import sys

from settings import *
from level import Level
from map.medieval import *

class Game:
    def __init__(self):
        pygame.mixer.pre_init(22050, -16, 2, 2048)
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Dream")
        self.clock = pygame.time.Clock()
        self.level = Level("gs", self.screen)
        self.changed_level = True

    def run(self):
        while True:
            self.level.run()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            self.clock.tick(FPS)

    def change_level(self, theme):
        if not self.changed_level:
            self.level = Level(theme, self.screen)
            self.changed_level = True

    def reset(self):
        self.level = Level("md", self.screen)

if __name__ == '__main__':
    game = Game()
    game.run()
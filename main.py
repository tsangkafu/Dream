import pygame
import sys

from settings import *
from level import Level
from map.medieval import *
from cursor import Cursor

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # title of the game
        pygame.display.set_caption("Dream")
        self.clock = pygame.time.Clock()

        self.level = Level()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # track the cursor
            self.level.cursor.rect.center = pygame.mouse.get_pos()

            # fill screen with background
            # put in the loop because 
            self.screen.blit(MEDIEVAL_BACKGROUND, (0,0))

            self.level.run()

            # refresh the cursor after the map and node have been generated
            self.screen.blit(self.level.cursor.image, pygame.mouse.get_pos())

            pygame.display.update()

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
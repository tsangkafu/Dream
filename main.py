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
        self.cursor = pygame.image.load(os.path.join("./graphics/cursor", "normal_cursor.png"))

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # fill screen with background
            self.screen.blit(MEDIEVAL_BACKGROUND, (0,0))

            self.level.run()

            # track the position of cursor
            mx, my = pygame.mouse.get_pos()
            # replace the cursor
            pygame.mouse.set_visible(False)
            self.screen.blit(self.cursor, (mx, my))

            pygame.display.update()

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
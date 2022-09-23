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
        # self.health
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        while True:
            # track the cursor
            self.level.cursor.rect.center = pygame.mouse.get_pos()

            # fill screen with background
            self.screen.blit(MEDIEVAL_BACKGROUND, (0,0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for node in self.level.node_sprites:
                        if node.rect.collidepoint(pygame.mouse.get_pos()):
                            self.level.player.set_target(node.rect.topleft)

            # for sprites in self.level.node_sprites:
            #     pygame.draw.line(self.screen, (255,0,0), sprites.rect.center, self.level.player.rect.center, 5)


            self.level.run()

            self.level.player.update()

            # refresh the cursor after the map and node have been generated
            self.screen.blit(self.level.cursor.image, pygame.mouse.get_pos())

            pygame.display.flip()

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
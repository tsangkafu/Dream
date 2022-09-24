import pygame
import sys

from settings import *
from level import Level
from map.medieval import *
from cursor import Cursor
from node import *

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
                # set the target for the player upon mouse click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for target_node in self.level.nodes:
                        # find the node where the mouse is clicked
                        if target_node.rect.collidepoint(pygame.mouse.get_pos()):
                            # find the node where the player is
                            for current_node in self.level.nodes:
                                # only allow player to move to the neighor node
                                if current_node.is_neighor(target_node) and current_node.rect.center == self.level.player.rect.center:
                                    self.level.player.set_target(target_node.rect.topleft)

            self.level.run()

            self.level.player.update()

            # refresh the cursor after the map and node have been generated
            self.screen.blit(self.level.cursor.image, pygame.mouse.get_pos())

            pygame.display.flip()

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
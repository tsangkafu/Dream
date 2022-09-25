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
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        # title of the game
        pygame.display.set_caption("Dream")
        # self.health
        self.clock = pygame.time.Clock()
        self.level = Level()
        self.font = pygame.font.Font(os.path.join("./font", "BreatheFireIii-PKLOB.ttf"), 30)
        self.game_menu = Menu("game_menu")
        self.in_game_menu = True

    def run(self):
        while True:
            # fill screen with background
            if self.in_game_menu:
                self.screen.blit(self.game_menu.image, (0, 0))
            else:
                self.screen.blit(MEDIEVAL_BACKGROUND, (0, 0))
                self.level.run()
                self.level.player.update()

            # track the cursor
            self.level.cursor.rect.center = pygame.mouse.get_pos()

            # refresh the cursor after the map and node have been generated
            self.screen.blit(self.level.cursor.image, pygame.mouse.get_pos())

            pygame.display.flip()

            while(self.in_game_menu):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        self.in_game_menu = False

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

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
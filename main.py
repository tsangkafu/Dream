import pygame
import sys

from settings import *
from level import Level
from map.medieval import *
from cursor import Cursor
from node import *
from menu import Menu
from dialog import Dialog

class Game:
    def __init__(self):
        pygame.init()
        self.md_screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.md_font = pygame.font.Font(os.path.join("./font", "BreatheFireIii-PKLOB.ttf"), 30)
        pygame.display.set_caption("Dream")
        self.clock = pygame.time.Clock()
        self.md_level = Level()
        self.game_menu = Menu("game_menu")
        self.in_game_menu = True
        self.dialog = Dialog()

    def run(self):
        while True:
            # fill screen with background
            if self.in_game_menu:
                self.md_screen.blit(self.game_menu.image, (0, 0))
            else:
                self.md_screen.blit(MEDIEVAL_BACKGROUND, (0, 0))
                self.md_level.run()
                # track the cursor
                self.md_level.cursor.rect.center = pygame.mouse.get_pos()
                # refresh the cursor after the map and node have been generated
                self.md_screen.blit(self.md_level.cursor.image, pygame.mouse.get_pos())
                # show bubble
                self.dialog.show_bubble(self.md_screen)

            # update the whole screen
            pygame.display.update()

            while(self.in_game_menu):
                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        self.in_game_menu = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()
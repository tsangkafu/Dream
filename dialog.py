import pygame
import os

from scene import scenes
from settings import *

class DialogManager(pygame.sprite.Sprite):
    def __init__(self, screen, groups):
        super().__init__(groups)
        self.font = pygame.font.Font(os.path.join("./font", "BreatheFireIii-PKLOB.ttf"), 25)
        self.screen = screen
        # frame of the dialog
        self.image = self.get_image("md")
        self.rect = self.image.get_rect()
        # the position of the dialog box
        self.dialog_pos = (0, HEIGHT - self.image.get_height())
        self.text_pos = (30, HEIGHT - self.image.get_height() + 60)
        # count for sentence within each scene
        self.sentence_no = 0
        self.dialog_end = False

    def get_image(self, theme):
        return pygame.image.load(os.path.join("./graphics/menu/md", theme + "_dialog.png")).convert_alpha()

    def start_dialog(self, scene_no):
        if not self.dialog_end:
            self.screen.blit(self.image, self.dialog_pos)
            # get how many sentence are in one scene
            scene_length = len(scenes[scene_no])

            text = scenes[scene_no][self.sentence_no][1]

            text_surface = self.font.render(text , True, (0, 0, 0))
            text_rect = text_surface.get_rect(topleft = self.text_pos)

            # TODO: print dialog into the dialog box
            self.screen.blit(text_surface, text_rect)

            # if mouse click is detect, kill the dialog rect
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sentence_no < scene_length - 1:
                        self.sentence_no += 1
                    else:
                        self.kill()
                        self.dialog_end = True

    def update(self):
        pass
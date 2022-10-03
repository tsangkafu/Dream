import pygame
import os

from scene import scenes
from settings import *

TEXT_COLOR = (30, 30, 30)

class DialogManager():
    def __init__(self, screen, scene_sprites):
        # the sprite group where every sprite has dialogs
        self.scene_sprites = scene_sprites

        self.font = pygame.font.Font(os.path.join("./font", "BreatheFireIii-PKLOB.ttf"), 25)
        self.screen = screen
        # frame of the dialog
        self.image = self.get_image("md")
        self.rect = self.image.get_rect()

        # the position of the dialog box
        self.dialog_pos = (0, HEIGHT - self.image.get_height())
        # the position of the text
        self.text_pos = (30, HEIGHT - self.image.get_height() + 60)
        # the position of the character's name
        self.character_name_pos = (85, HEIGHT - self.image.get_height() + 6)
        # the position of the character avatar
        self.character_pos = (WIDTH - 170, HEIGHT - 290)
        # a transparent rect to fade out the background
        self.fader = pygame.Surface((WIDTH, HEIGHT))
        self.fader.set_alpha(170)
        self.fader.fill((0, 0, 0))
        
        self.finished_scenes = []
        # count for sentence within each scene
        self.sentence_no = 0
        self.dialog_end = True

    def get_image(self, theme):
        return pygame.image.load(os.path.join("./graphics/menu/md", theme + "_dialog.png")).convert_alpha()

    def start_dialog(self, scene_no):
        if scene_no not in self.finished_scenes:
            self.dialog_end = False

            self.screen.blit(self.fader, (0, 0))
            # draw the dialog box
            self.screen.blit(self.image, self.dialog_pos)
            # get how many sentence are in one scene
            scene_length = len(scenes[scene_no])

            character_name = scenes[scene_no][self.sentence_no][0]
            character_name_surface = self.font.render(character_name, True, TEXT_COLOR)
            character_rect = character_name_surface.get_rect(topleft = self.character_name_pos)

            text = scenes[scene_no][self.sentence_no][1]
            text_surface = self.font.render(text , True, TEXT_COLOR)
            text_rect = text_surface.get_rect(topleft = self.text_pos)

            # print character picture to the dialog box
            for sprite in self.scene_sprites:
                if sprite.name == scenes[scene_no][self.sentence_no][0]:
                    self.screen.blit(sprite.large_image, self.character_pos)

            # print the name to the dialog box
            self.screen.blit(character_name_surface, character_rect)

            # print dialog to the dialog box
            self.screen.blit(text_surface, text_rect)

            # if mouse click is detect, kill the dialog rect
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sentence_no < scene_length - 1:
                        self.sentence_no += 1
                    else:
                        self.finished_scenes.append(scene_no)
                        self.sentence_no = 0
                        self.dialog_end = True

    def update(self):
        pass
import pygame
import os
import textwrap

from scene import *
from settings import *
from npc import NPC

class DialogManager():
    def __init__(self, screen, scene_sprites, sfx, theme):
        # the sprite group where every sprite has dialogs
        self.scene_sprites = scene_sprites
        
        self.font = pygame.font.Font(FONT, 25)
        self.screen = screen
        self.sfx = sfx
        # frame of the dialog
        self.image = self.get_image(theme)
        self.rect = self.image.get_rect()

        # the position of the dialog box
        self.dialog_pos = (0, HEIGHT - self.image.get_height())
        # the position of the text
        self.text_pos = (30, HEIGHT - self.image.get_height() + 60)
        self.text_pos_2 = (30, HEIGHT - self.image.get_height() + 100)
        # the position of the character's name
        self.character_name_pos = (85, HEIGHT - self.image.get_height() + 6)
        # the position of the character avatar
        self.character_pos = (WIDTH - 170, HEIGHT - 290)
        
        self.finished_scenes = []
        # count for sentence within each scene
        self.sentence_no = 0
        self.dialog_end = True
        self.end_battle_dialog_end = True
        self.upgrade_dialog_end = True

    def get_image(self, theme):
        try:
            return pygame.image.load(os.path.join("./graphics/menu/" + theme, "dialog.png")).convert_alpha()
        except:
            return pygame.image.load(os.path.join("./graphics/menu/md", "dialog.png")).convert_alpha()
    
    def show_dialog_box(self):
        # draw the fader
        self.screen.blit(FADER, (0, 0))
        # draw the dialog box
        self.screen.blit(self.image, self.dialog_pos)
    
    def start_dialog(self, scene_no):
        if scene_no not in self.finished_scenes:
            is_voiceover = True if len(scenes[scene_no][self.sentence_no][0]) == " " else False
            self.dialog_end = False

            self.show_dialog_box()

            # get how many sentence are in one scene
            scene_length = len(scenes[scene_no])

            character_name = scenes[scene_no][self.sentence_no][0]
            character_name_surface = self.font.render(character_name, True, DIALOG_TEXT_COLOR)

            text = scenes[scene_no][self.sentence_no][1]
            # print dialog
            self.wrap_text_and_blit(text)

            # print character picture to the dialog box
            if not is_voiceover:
                for sprite in self.scene_sprites:
                    if sprite.name == scenes[scene_no][self.sentence_no][0]:
                        self.screen.blit(sprite.large_image, self.character_pos)

            # print the name to the dialog box
            self.screen.blit(character_name_surface, self.character_name_pos)

            # if mouse click is detect, kill the dialog rect
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sentence_no < scene_length - 1:
                        self.sentence_no += 1
                        self.sfx.dialog_channel.play(self.sfx.page_turn)
                    else:
                        self.finished_scenes.append(scene_no)
                        self.sentence_no = 0
                        self.dialog_end = True
                        self.sfx.dialog_channel.play(self.sfx.page_turn)


    def start_end_battle_dialog(self, raw_enemy):
        if self.sentence_no < len(end_battle):
            self.show_dialog_box()
            list = []
            # format the sentence
            list.append(end_battle[0].format(name = raw_enemy["name"]))
            list.append(end_battle[1].format(exp = str(raw_enemy["exp"]), money = str(raw_enemy["money"])))
            item_str = ""

            # appending items
            for i, item in enumerate(raw_enemy["items"]):
                item_str += item + ", " if i < len(raw_enemy["items"]) - 1 else item

            if len(raw_enemy["items"]) == 0:
                list.append(end_battle[2].format(items = "nothing"))
            else:
                list.append(end_battle[2].format(items = item_str))

            # text_surface = self.font.render(list[self.sentence_no], True, DIALOG_TEXT_COLOR)
            # self.screen.blit(text_surface, self.text_pos)

            self.wrap_text_and_blit(list[self.sentence_no])
            
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.sentence_no < len(end_battle) - 1:
                        self.sentence_no += 1
                        self.sfx.dialog_channel.play(self.sfx.page_turn)
                    else:
                        self.end_battle_dialog_end = True
                        self.sentence_no = 0
                        self.sfx.dialog_channel.play(self.sfx.page_turn)
    

    def start_upgrade_dialog(self, player):
        self.show_dialog_box()

        text_surface = self.font.render(upgrade.format(last_level = player.level - 1, next_level = player.level), True, DIALOG_TEXT_COLOR)
        self.screen.blit(text_surface, self.text_pos)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.upgrade_dialog_end = True

    
    # breaking text that is too long into 2 lines and display
    def wrap_text_and_blit(self, text):
        if len(text) > 40:
            text_list = textwrap.wrap(text, 40)
            text_surface_1 = self.font.render(text_list[0] , True, DIALOG_TEXT_COLOR)
            text_surface_2 = self.font.render(text_list[1] , True, DIALOG_TEXT_COLOR)
            self.screen.blit(text_surface_1, self.text_pos)
            self.screen.blit(text_surface_2, self.text_pos_2)
        else:
            text_surface = self.font.render(text , True, DIALOG_TEXT_COLOR)
            self.screen.blit(text_surface, self.text_pos)

    # pass in a list of hidden scene to append to the dict
    def unlock_scene(self, scene_nums, scene_nums_to_remove = None):
        offset_count = 0
        selected_NPC = None
        if scene_nums_to_remove != None:
            # iterate through the scenes to be removed
            for scene in scene_nums_to_remove:
                # if the scene is not finished, append and increment the count
                if scene not in self.finished_scenes:
                    offset_count += 1
                    self.finished_scenes.append(scene)

                # look for that npc and increment the count because one scene has been appended to finished (skipped)
                for sentence in scenes[scene]:
                    for sprite in self.scene_sprites:
                        if sprite.name == sentence[0] and sprite.name != "Lucas Vopiscus":
                            selected_NPC = sprite

            if selected_NPC != None:
                selected_NPC.dialog_count += offset_count
                
        for scene in scene_nums:
            scenes[scene] = hidden_scenes[scene]
        # update the npc dialog option
        for npc in self.scene_sprites:
            if type(npc) == NPC:
                npc.get_dialog()

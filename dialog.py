from tkinter import FALSE
import pygame
import os

# cutscene_no : [(character_1, dialog_1), (character_2, dialog_2)]
dialogs = {
    0: [
        ("Lucas Vopiscus", "Where am I?"),
        ("Lucas Vopiscus", "It feels like I just woke up from a dream...")
    ],
    1: [
        
    ]
}

class Dialog(pygame.sprite.Sprite):
    def __init__(self, screen, groups):
        super().__init__(groups)
        self.screen = screen
        self.image = self.get_image()
        self.rect = self.image.get_rect()
        self.scene_no = 0

    def get_image(self):
        return pygame.image.load(os.path.join("./graphics/menu/md", "md_dialog.png")).convert_alpha()

    def start_dialog(self, scene_no):
        if scene_no < len(dialogs):
            for dialog in dialogs.get(scene_no):
                for event in pygame.event.get():
                    # set the target for the player upon mouse click
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        
                # print(dialog[0] + ": " + dialog[1])

        # TODO: end the scene and increment the scene count
        print("END!")
        self.scene_no += 1
        print(self.scene_no)

    def update(self):
        pass
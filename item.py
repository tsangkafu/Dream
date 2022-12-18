import pygame
import os
from settings import *



class Item(pygame.sprite.Sprite):
    def __init__(self, screen, groups, theme, name, pos):
        super().__init__(groups)
        self.name = name
        self.screen = screen
        raw_name = self.name.lower().replace(" ", "_")
        self.attack = ITEMS[raw_name]["attack"]
        self.defense = ITEMS[raw_name]["defense"]
        self.value = ITEMS[raw_name]["value"]
        self.type = ITEMS[raw_name]["type"]
        self.attack = ITEMS[raw_name]["attack"]
        self.defense = ITEMS[raw_name]["defense"]
        try:
            self.og_image = pygame.image.load(os.path.join("./graphics/item/" + theme, raw_name + ".png")).convert_alpha()
        except:
            self.og_image = pygame.image.load(os.path.join("./graphics/item/md", raw_name + ".png")).convert_alpha()
        self.image = pygame.transform.smoothscale(self.og_image, ITEM_SIZE).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.og_rect = self.rect.copy()

    def update(self):
        self.screen.blit(self.image, self.rect)
        
    def enlarge(self):
        self.image = pygame.transform.smoothscale(self.og_image, ITEM_LARGE_SIZE).convert_alpha()
        # create a new rect, then align the center of new and old rect
        self.rect = self.image.get_rect(center = self.og_rect.center)

    def shrink(self):
        self.image = pygame.transform.smoothscale(self.og_image, ITEM_SIZE).convert_alpha()
        self.rect = self.image.get_rect(center = self.og_rect.center)
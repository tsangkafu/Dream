import pygame
import os

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, theme, screen, pos, groups):
        super().__init__(groups)

        self.theme = theme
        self.name = self.get_name()

        # basic status
        self.level = 1
        self.max_hp = 100
        self.hp = 100
        self.exp = 25
        self.exp_to_upgrade = 9999
        self.attack = 999
        self.defense = 4
        self.money = 0
        self.items = []
        self.weapon = ""
        self.shield = ""
        self.screen = screen
        # indicating if the player just left the village
        # preventing the village from appearing after the player just left
        self.exiting = False
        self.walking = False
        # avatar of the character
        self.image = pygame.image.load(os.path.join("./graphics/character", self.name.replace(" ", "_") + "_avatar.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.large_image = pygame.image.load(os.path.join("./graphics/character", self.name.replace(" ", "_") + ".png")).convert_alpha()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 1.2
        self.target = pygame.math.Vector2(pos)

    def get_name(self):
        if self.theme == "md":
            return "Lucas Vopiscus"
        elif self.theme == "gs":
            return "Lucio Santarossa"
        elif self.theme == "cp":
            return "Cyberpunk"

    def set_target(self, target_pos):
        self.target = pygame.math.Vector2(target_pos)
        self.walking = True
    
    def update(self):
        # substracting 2 vectors, getting the difference of x and y of them
        pos_diff = self.target - self.pos
        # get the length to the vector (the distance of the player and the target)
        pos_diff_length = pos_diff.length()

        if pos_diff_length == 0:
            self.walking = False

        # if the length of the vector is less than the speed, move the player there
        if pos_diff_length < self.speed:
            self.pos = self.target
        elif pos_diff_length != 0:
            # normalize the vector
            pos_diff.normalize_ip()
            # time the speed to decide how fast the character walks
            pos_diff *= self.speed
            # add the normalized and scaled vector to the player position
            self.pos += pos_diff
            
        self.rect.topleft = self.pos

        # detect level up
        if self.exp >= self.exp_to_upgrade:
            self.upgrade()
        
        self.update_status()

    # update the user status depending on equipment
    def update_status(self):
        # 2 variable to store incremented attack and defense
        # needed because both weapon and shield will provide attack and defense
        attack, defense = 0, 0
        for item in ITEMS:
            if self.weapon.lower().replace(" ", "_") == item:
                attack += ITEMS[item]["attack"]
                defense += ITEMS[item]["defense"]
            if self.shield.lower().replace(" ", "_") == item:
                attack += ITEMS[item]["attack"]
                defense += ITEMS[item]["defense"]

            self.actual_attack = attack + self.attack
            self.actual_defense = defense + self.defense
    
    def upgrade(self):
            self.level += 1
            self.exp = self.exp - self.exp_to_upgrade
            self.exp_to_upgrade *= 2
            self.max_hp = self.level * 25 + 80
            self.attack = self.level * 5 + 15
            self.defense = self.level * 4

    def draw(self):
        self.screen.blit(self.image, self.pos)
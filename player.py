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
        self.hp = 80
        self.exp = 25
        self.exp_to_upgrade = 100
        self.attack = 10
        self.defense = 2
        self.money = 0
        
        self.screen = screen

        # avatar of the character
        self.image = pygame.image.load(os.path.join("./graphics/character", self.name.replace(" ", "_") + "_avatar.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.large_image = pygame.image.load(os.path.join("./graphics/character", self.name.replace(" ", "_") + ".png")).convert_alpha()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 5

        self.set_target(pos)

    def get_name(self):
        if self.theme == "md":
            return "Lucas Vopiscus"
        elif self.theme == "gs":
            return "Gangster"
        elif self.theme == "cp":
            return "Cyberpunk"

    def set_target(self, target_pos):
        self.target = pygame.math.Vector2(target_pos)

    def upgrade(self):
        if self.exp == self.exp_to_upgrade:
            self.level += 1
            self.exp = 0
            self.exp_to_upgrade *= 2
            self.max_hp = self.level * 20 + 80
            self.attact = self.level * 2 + 8
            self.defense = self.level * 2 + 0
    
    def update(self):
        # substracting 2 vectors, getting the difference of x and y of them
        pos_diff = self.target - self.pos
        # get the length to the vector (the distance of the player and the target)
        pos_diff_length = pos_diff.length()

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

    def draw(self):
        self.screen.blit(self.image, self.pos)
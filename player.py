import pygame
import os

from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.name = "Lucas Vopiscus"
        # avatar of the character
        self.image = pygame.image.load(os.path.join("./graphics/character", self.name.replace(" ", "_") + "_avatar.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.large_image = pygame.image.load(os.path.join("./graphics/character", self.name.replace(" ", "_") + ".png")).convert_alpha()
        self.pos = pygame.math.Vector2(pos)
        self.speed = 5
        self.set_target(pos)

    def set_target(self, target_pos):
        self.target = pygame.math.Vector2(target_pos)
    
    def update(self):
        # substracting 2 vectors, getting the difference of x and y of them
        pos_diff = self.target - self.pos
        # return the length to the vector (the distance of the player and the target)
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
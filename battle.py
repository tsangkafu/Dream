from http.client import SEE_OTHER
from http.cookiejar import DefaultCookiePolicy
import pygame
import os
import random

from settings import *

class Battle():
    def __init__(self, screen, theme, player, sfx):
        # animation variables
        self.background_alpha = 0
        self.object_alpha = 0
        self.player_alpha = 255
        self.enemy_alpha = 255
        self.theme = theme

        # a number serving as the index of the ENEMIES dict
        self.screen = screen
        self.sfx = sfx
        self.player = player

        # copy the image to the battle object
        self.player_image = self.player.large_image.copy().convert_alpha()

        self.finished_battle = []
        self.battle_end = True
        self.font = pygame.font.Font(FONT, 25)
        self.damage = 0
        self.damage_font = pygame.font.Font(FONT, 50)
        
        # indicate the frame of the attack animation
        self.player_attack_animation = -0.3
        self.enemy_attack_animation = -0.3

        self.attack_animation_end = False
        self.damage_animation_end = False
        self.value_animation_end = False
        
        self.player_round = True
        self.round_end = False
        self.attacking = False

        self.roared = False

        # if True, handle the dialog related to upgrade
        self.upgrading = False

        # the speed of the damage value
        self.damage_speed = 0

        try:
            # attack animation
            self.player_attack = [
                pygame.image.load(os.path.join("./graphics/animation/" + self.theme, "player_attack_1" + ".png")).convert_alpha(),
                pygame.image.load(os.path.join("./graphics/animation/" + self.theme, "player_attack_2" + ".png")).convert_alpha()]
        except:
            self.player_attack = [
                pygame.image.load(os.path.join("./graphics/animation/md", "player_attack_1" + ".png")).convert_alpha(),
                pygame.image.load(os.path.join("./graphics/animation/md", "player_attack_2" + ".png")).convert_alpha()]
        try:
            
            self.enemy_attack = [
                pygame.image.load(os.path.join("./graphics/animation/" + self.theme, "enemy_attack_1" + ".png")).convert_alpha(),
                pygame.image.load(os.path.join("./graphics/animation/" + self.theme, "enemy_attack_2" + ".png")).convert_alpha()]
        except: 
            self.enemy_attack = [ 
                pygame.image.load(os.path.join("./graphics/animation/md", "enemy_attack_1" + ".png")).convert_alpha(),
                pygame.image.load(os.path.join("./graphics/animation/md", "enemy_attack_2" + ".png")).convert_alpha()]
        
        try:
            self.player_info = pygame.image.load(os.path.join("./graphics/ui/" + theme, "player_info.png")).convert_alpha()
            self.enemy_info = pygame.image.load(os.path.join("./graphics/ui/" + theme, "enemy_info.png")).convert_alpha()
        except:
            self.player_info = pygame.image.load(os.path.join("./graphics/ui/md", "player_info.png")).convert_alpha()
            self.enemy_info = pygame.image.load(os.path.join("./graphics/ui/md", "enemy_info.png")).convert_alpha()

        self.background_imported = False

    def start(self, enemy, scene):
        if scene not in self.finished_battle:
            self.battle_end = False
            # create the scene
            self.scene = scene
            self.enemy = enemy
            if not self.roared:
                # play the monster sound according to their sound
                self.sfx.fight_channel_three.play(self.sfx.monster_roars[enemy.sound])
                self.roared = True
            # copy the image to the battle object
            self.enemy_image = self.enemy.image.convert_alpha()
            self.is_boss = True if self.enemy_image.get_size()[1] > 699 else False

            self.draw_background()
            # populate enemy and player
            self.draw_character()
            self.draw_ui(self.theme)
            self.attack()

    def attack(self):
        if self.attacking:
            self.attack_animation()
        for event in pygame.event.get():
            # attack the enemy upon mouse click
            if event.type == pygame.MOUSEBUTTONDOWN and self.enemy_image_rect.collidepoint(pygame.mouse.get_pos()):
                self.attacking = True
                # change the position of the slash animation based on cursor position
                self.attack_pos = (pygame.mouse.get_pos()[0] - 50, pygame.mouse.get_pos()[1] - 10)

    def draw_background(self):
        if not self.background_imported:
            self.background_imported = True
            self.background =  pygame.image.load(os.path.join("./graphics/scene/", str(self.scene) + ".png")).convert_alpha()

        # fade in transition
        if self.background_alpha < 255: 
            self.background_alpha += 20
        self.background.set_alpha(self.background_alpha)
        self.screen.blit(self.background, (0, 0))


    def draw_character(self):
        def outline_mask(img, pos, size):
            mask = pygame.mask.from_surface(img)
            mask_outline = mask.outline()
            mask_surface = pygame.Surface(img.get_size())
            for pixel in mask_outline:
                mask_surface.set_at(pixel, HP_BAR_COLOR)

            mask_surface.set_colorkey((0, 0, 0))
            for i in range(size):
                self.screen.blit(mask_surface, (pos[0] - i, pos[1]))
                self.screen.blit(mask_surface, (pos[0] + i, pos[1]))
                self.screen.blit(mask_surface, (pos[0], pos[1] - i))
                self.screen.blit(mask_surface, (pos[0], pos[1] + i))
            
        # fade in transition
        if self.object_alpha < 255:
            self.object_alpha += 10
            self.player_image.set_alpha(self.object_alpha)
            self.enemy_image.set_alpha(self.object_alpha)
        
        self.player_image_rect = self.player_image.get_rect(topleft = (30, 695))
        # add the h_offset in case the enemy will show up in different height of the background
        if self.is_boss:
            self.enemy_image_rect = self.enemy_image.get_rect(topleft = (200, 50 + self.enemy.h_offset))
        else:
            self.enemy_image_rect = self.enemy_image.get_rect(topleft = (365, 410 + self.enemy.h_offset))

        if self.enemy_image_rect.collidepoint(pygame.mouse.get_pos()) and not self.attacking:
            outline_mask(self.enemy_image, self.enemy_image_rect, 6)

        self.screen.blit(self.player_image, self.player_image_rect)
        self.screen.blit(self.enemy_image, self.enemy_image_rect)

    def draw_ui(self, theme):
        # draw the info of both the player and enemy
        def draw_info(character):
            character_info = self.player_info if character == "player" else self.enemy_info
            character_info.set_alpha(self.object_alpha)
            character_rect = self.player_image_rect if character == "player" else self.enemy_image_rect
            character_info_rect_pos = (
                character_rect.topleft[0] + 205,
                character_rect.topleft[1] + 130) if character == "player" else (
                character_rect.topleft[0] - 180 if self.is_boss else character_rect.topleft[0] - 345,
                character_rect.topleft[1] + 300 if self.is_boss else character_rect.topleft[1])
            character_info_rect = character_info.get_rect(topleft = character_info_rect_pos)
            self.screen.blit(character_info, character_info_rect)

            character_name = self.player.name if character == "player" else self.enemy.name
            character_name_surface = self.font.render(character_name, True, BATTLE_NAME_TEXT_COLOR)
            # the character name should be relational to the info box
            character_name_rect_pos = (
                character_info_rect.topleft[0] + 200,
                character_info_rect.topleft[1] + 55) if character == "player" else (
                character_info_rect.topleft[0] + 190,
                character_info_rect.topleft[1] + 50)
            character_name_surface.set_alpha(self.object_alpha)
            character_name_rect = character_name_surface.get_rect(center = character_name_rect_pos)
            self.screen.blit(character_name_surface, character_name_rect)

            character = self.player if character == "player" else self.enemy
            character_hp_ratio = 0 if character.hp <= 0 else character.hp / character.max_hp
            character_hp_bar = pygame.Surface((BATTLE_HP_BAR_SIZE[0] * character_hp_ratio, BATTLE_HP_BAR_SIZE[1]))
            character_hp_bar.fill(BATTLE_HP_BAR_COLOR)
            character_hp_bar_bg = pygame.Surface(BATTLE_HP_BAR_SIZE)
            character_hp_bar_bg.fill(BATTLE_HP_BAR_BG_COLOR)
            character_hp_bar_bg.set_alpha(100)
            character_hp_bar_pos = (
                character_info_rect.topleft[0] + 115,
                character_info_rect.topleft[1] + 90) if character == "player" else (
                character_info_rect.topleft[0] + 105,
                character_info_rect.topleft[1] + 85)
            character_hp_bar_rect = character_hp_bar.get_rect(topleft = character_hp_bar_pos)
            character_hp_bar_bg_rect = character_hp_bar_bg.get_rect(topleft = character_hp_bar_pos)
            self.screen.blit(character_hp_bar_bg, character_hp_bar_bg_rect)
            self.screen.blit(character_hp_bar, character_hp_bar_rect)

        # ------------------ nested methods end here ------------------ # 

        draw_info("player")
        draw_info("enemy")

    # populate the attack animation
    def attack_animation(self):
        # creating attack animation
        def show_slash():
            # make sure it is player's round before attacking
            if self.player_round:
                self.player_attack_animation += 0.15
                # when the attack animation finishes, deduct health point
                if self.player_attack_animation >= len(self.player_attack):
                    self.player_attack_animation = 0
                    self.attack_animation_end = True
                    # randomness to attack value
                    self.damage = random.randint(
                        int(self.player.actual_attack * 0.7),
                        int(self.player.actual_attack * 1.2)) - self.enemy.defense
                    # 15% chance of missing
                    self.damage = 0 if random.randint(1, 100) > 85 else self.damage
                    if self.damage > 0:
                        self.enemy.hp -= self.damage
                        self.sfx.fight_channel.play(self.sfx.player_slashs[random.randint(0, len(self.sfx.player_slashs) - 1)])
                    else:
                        self.sfx.fight_channel.play(self.sfx.player_miss)
                else:
                    self.screen.blit(
                        self.player_attack[int(self.player_attack_animation)],
                        self.attack_pos)
            
            elif not self.player_round:
                self.enemy_attack_animation += 0.15
                if self.enemy_attack_animation >= len(self.enemy_attack):
                    self.enemy_attack_animation = 0
                    self.attack_animation_end = True
                    self.damage = random.randint(
                        int(self.enemy.attack * 0.7),
                        int(self.enemy.attack * 1.2)) - self.player.defense
                    # 15% chance of missing
                    self.damage = 0 if random.randint(1, 100) > 85 else self.damage
                    if self.damage > 0:
                        self.player.hp -= self.damage
                        self.sfx.fight_channel.play(self.sfx.enemy_slash)
                        # not every attack will make the player moan
                        if random.randint(1, 100) > 70:
                            self.sfx.fight_channel_two.play(self.sfx.umph)
                    else:
                        self.sfx.fight_channel.play(self.sfx.enemy_miss)
                else:
                    self.screen.blit(
                        self.enemy_attack[int(self.enemy_attack_animation)],
                        self.player_image_rect.topleft)

        # creating flickering animation by changing the alpha of characters
        def show_flickering():
            if self.player_round:
                # decrease the alpha to 50 and quickly reset
                if self.enemy_alpha >= 50 and not self.damage_animation_end:
                    self.enemy_alpha -= 50
                else:
                    # when the animation finishes, reset variables
                    self.enemy_alpha = 255
                    self.damage_animation_end = True
                # animating the character when being attacked
                self.enemy_image.set_alpha(self.enemy_alpha)

            elif not self.player_round:
                if self.player_alpha >= 50 and not self.damage_animation_end:
                    self.player_alpha -= 50
                else:
                    self.player_alpha = 255
                    self.damage_animation_end = True
                self.player_image.set_alpha(self.player_alpha)

        # show the value of the damage
        def show_value():
            if self.player_round:
                # damage that less than zero will be considered MISS
                damage = self.damage if self.damage > 0 else "MISS"
                # if it is a miss then show MISS
                damage_value = self.damage_font.render("MISS" if damage == "MISS" \
                    else "-" + str(damage), True, HP_BAR_COLOR)
                # if it is a miss, offset the damage value position
                damage_pos = (self.enemy_image_rect.center[0] - 20,
                    self.enemy_image_rect.center[1]) \
                        if damage == "MISS" else (
                            self.enemy_image_rect.center[0] - 20,
                            self.enemy_image_rect.center[1])
                damage_pos_y = damage_pos[1] - self.damage_speed
                if damage_pos_y <= (self.enemy_image_rect.center[1] - 100):
                    self.damage_speed = 0
                    self.value_animation_end = True
                    self.attack_animation_end = False
                    self.damage_animation_end = False
                    self.player_round = False
                else:
                    self.damage_speed += 3
                    damage_pos_y -= self.damage_speed
                    self.screen.blit(damage_value, (damage_pos[0] - 20, damage_pos_y))

            elif not self.player_round:
                damage = self.damage if self.damage > 0 else "MISS"
                damage_value = self.damage_font.render("MISS" if damage == "MISS" \
                    else "-" + str(damage), True, HP_BAR_COLOR)
                damage_pos = (self.player_image_rect.center[0] - 20,
                    self.player_image_rect.center[1]) if damage == "MISS" \
                        else self.player_image_rect.center
                damage_pos_y = damage_pos[1] - self.damage_speed
                if damage_pos_y <= self.player_image_rect.center[1] - 100:
                    self.damage_speed = 0
                    self.value_animation_end = True
                    self.round_end = True
                else:
                    self.damage_speed += 3
                    damage_pos_y -= self.damage_speed
                    self.screen.blit(damage_value, (damage_pos[0] - 20, damage_pos_y))

        # ------------------ nested methods end here ------------------ #

        # animation starts when the background and characters finishes transition
        if self.object_alpha >= 255:
            if not self.attack_animation_end:
                show_slash()
            # when the attack animation ends
            elif self.attack_animation_end:
                show_flickering()

                if self.damage_animation_end:
                    show_value()

                    if self.value_animation_end:
                        # defeat enemy
                        if self.enemy.hp <= 0 and self.value_animation_end:
                            self.sfx.fight_channel_three.play(self.sfx.blood)
                            self.reset()
                            
                            if self.enemy.exp + self.player.exp >= self.player.exp_to_upgrade:
                                self.upgrading = True

                            # add exp to player
                            self.player.exp += self.enemy.exp
                            # add money to player
                            self.player.money += self.enemy.money
                            self.player.items.extend(self.enemy.items)
                            # destroy the weapon and shield
                            self.player.weapon = ""
                            self.player.shield = ""

                        # game over
                        if self.player.hp <= 0 and self.round_end:
                            self.sfx.fight_channel_three.play(self.sfx.scream)
                            self.reset()
                        
                        # reset after each round
                        if self.round_end:
                            self.player_round = True
                            self.attacking = False
                            self.attack_animation_end = False
                            self.damage_animation_end = False
                            self.value_animation_end = False
                            self.round_end = False
                            self.background_imported = False

    def reset(self):
        self.battle_end = True
        self.finished_battle.append(self.scene)
        self.player_round = True
        self.attacking = False
        self.object_alpha = 0
        self.background_alpha = 0
        self.player_alpha = 255
        self.enemy_alpha = 255
        self.attack_animation_end = False
        self.damage_animation_end = False
        self.value_animation_end = False
        self.background_imported = False
        self.roared = False
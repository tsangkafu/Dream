import pygame
from settings import *
from item import Item
import os

class Equipment(pygame.sprite.Sprite):
    def __init__(self, screen, theme ,groups, player, sfx):
        super().__init__(groups)
        self.sfx = sfx
        self.screen = screen
        self.player = player
        self.group = groups
        self.theme = theme
        try:
            self.image = pygame.image.load(os.path.join("./graphics/ui/" + theme, "equipment.png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/ui/md", "equipment.png")).convert_alpha()
        self.rect = self.image.get_rect(center = (WIDTH / 2, HEIGHT / 2 + 40))
        self.alpha = 0
        self.show = False
        # flag indicate whether the item needs to be updated
        # usually happens when the player change weapon or acquire new items
        self.update_item = True
        # this flag indicate whether the item changing is completed
        # mainly used to bypass update() of the selected item
        # making it not constantly show its own image after item has been repositioned
        self.changing_item = False
        
        self.grids = []

        self.item_sprites = pygame.sprite.Group()

        self.create_avatar()
        # create equipment grid
        # the starting position of the first grid (0, 0)
        # reference to the interface's rect
        self.create_grid()
        self.create_value()
        self.create_items()
        # create the layout of the info box
        self.info_box = Box(self.screen, self.theme, self.rect.center)
        # indicate which item is being hovered over
        self.selected_item = None

        # creating button
        starting_pos = (WIDTH / 2, HEIGHT / 2 + 380)
        self.button = Button(self.screen, theme, groups, starting_pos)

    def show_ui(self):
        # all behavior when the equipment window is opened
        if self.show:
            self.alpha = 255
            # draw the fader
            self.screen.blit(FADER, (0, 0))
            # draw the ui
            self.group.draw(self.screen)
            # create_item
            if self.update_item:
                self.update_items()
            
            # print the item first
            self.item_sprites.draw(self.screen)

            # show the extra item info when mouse hovers
            for item in self.item_sprites:
                if item.rect.collidepoint(pygame.mouse.get_pos()):
                    self.info_box.rect.center = item.rect.center
                    self.selected_item = item
                    item.enlarge()
                    # print the info box
                    self.info_box.update(item)
                else:
                    item.shrink()

            # show the select item on top of the info box
            if self.selected_item != None and not self.changing_item:
                self.selected_item.update()
            else:
                # reset the flag to back to false so that it won't affect next item selected
                self.changing_item = False

        # else if when the item is not shown
        else:
            self.alpha = 0
        
        # set the alpha for all equipment ui elements
        for element in self.group:
            element.image.set_alpha(self.alpha)

        # update the value of the ui, e.g., attack, defense
        self.update_value()

    def create_avatar(self):
        self.avatar = Avatar(self.screen,
            self.group,
            self.player.large_image.copy().convert_alpha(),
            (self.rect.center[0], self.rect.center[1] - 150))


    def create_grid(self):
        starting_pos = (self.rect.center[0] - 2 * 70, self.rect.center[1] + 50)
        x = 0
        # row
        for i in range(4):
            # column
            for j in range(5):
                self.grids.append(
                    Grid(self.screen,
                        self.theme,
                        self.group,
                        (starting_pos[0]  + (j * 70), starting_pos[1] + (i * 70)),
                        # assign id to the grid
                        x))
                x += 1

        # create player equipment grid
        starting_pos = (self.rect.center[0] - 160, self.rect.center[1] - 130)
        for i in range(2):
            self.grids.append(
                Grid(self.screen,
                    self.theme,
                    self.group,
                    (starting_pos[0] + i * 320, starting_pos[1]),
                    x)
            )
            x += 1

    def create_value(self):
        # draw the player hp
        self.hp = Text(self.screen,
            self.group,
            str(self.player.hp) + "/" + str(self.player.max_hp),
            LEVEL_COLOR,
            40,
            (self.rect.topleft[0] + 135, self.rect.topleft[1] + 105))

        # draw the player attack
        self.attack = Text(self.screen,
            self.group,
            "Atk: " + str(self.player.attack),
            LEVEL_COLOR,
            25,
            (self.grids[20].rect.center[0], self.grids[20].rect.center[1] + 60))
        # draw the player defense
        self.defense = Text(self.screen,
            self.group,
            "Def: " + str(self.player.defense),
            LEVEL_COLOR,
            25,
            (self.grids[21].rect.center[0], self.grids[21].rect.center[1] + 60))

    def update_value(self):
        # update attack value
        self.hp.update(str(self.player.hp) + "/" + str(self.player.max_hp))
        self.attack.update("Atk: " + str(self.player.actual_attack))
        self.defense.update("Def:" + str(self.player.actual_defense))
        
    def create_items(self):
        # unequipped items
        for i, item in enumerate(self.player.items):
            Item(self.screen, self.item_sprites, self.theme, item, self.grids[i].rect.center)

        # equipped weapon and shield
        if self.player.weapon != "":
            Item(self.screen, self.item_sprites, self.theme, self.player.weapon, self.grids[-2].rect.center)
        if self.player.shield != "":
            Item(self.screen, self.item_sprites, self.theme, self.player.shield, self.grids[-1].rect.center)

    def update_items(self):
        if self.show:
            self.sfx.equipment_channel.play(self.sfx.equip)
        self.item_sprites.empty()
        self.create_items()
        # turn off the flag so that it does not get updated every loop
        self.update_item = False
    
"""
Grid that "store" the item.
"""
class Grid(pygame.sprite.Sprite):
    def __init__(self, screen, theme, groups, pos, number):
        super().__init__(groups)
        self.screen = screen
        self.number = number
        try:
            self.image = pygame.image.load(os.path.join("./graphics/ui/" + theme, "grid.png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/ui/md", "grid.png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
"""
Exit button.
"""
class Button(pygame.sprite.Sprite):
    def __init__(self, screen, theme, groups, pos):
        super().__init__(groups)
        self.font = pygame.font.Font(FONT, 25)
        self.screen = screen
        try:
            self.image = pygame.image.load(os.path.join("./graphics/ui/" + theme, "button.png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/ui/md", "button.png")).convert_alpha()
        self.rect = self.image.get_rect(center = pos)
        self.text = Text(self.screen, groups, "EXIT", LEVEL_COLOR, 25, self.rect.center)
"""
Avatar that shown in the equipment UI.
"""
class Avatar(pygame.sprite.Sprite):
    def __init__(self, screen, groups, image, pos):
        super().__init__(groups)
        self.font = pygame.font.Font(FONT, 25)
        self.screen = screen
        self.image = image
        self.rect = self.image.get_rect(center = pos)

"""
Info box that show the extra item information.
"""
class Box():
    def __init__(self, screen, theme, pos):
        self.screen = screen
        try:
            self.image = pygame.image.load(os.path.join("./graphics/ui/" + theme, "item_box.png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/ui/md", "item_box.png")).convert_alpha()
        self.image.set_alpha(240)
        self.rect = self.image.get_rect(center = pos)

    # pass in the item to reference the info
    def update(self, item):
        # blit the image of the item
        self.screen.blit(self.image, self.rect)
        name = item.name
        attack = "Attack: " + str(item.attack)
        defense = "Defense: " + str(item.defense)
        font = pygame.font.Font(FONT, 20)

        surface = font.render(name, True, LEVEL_COLOR)
        self.screen.blit(surface, (self.rect.center[0] - surface.get_width() / 2, self.rect.top + 40))
        surface = font.render(attack, True, LEVEL_COLOR)
        self.screen.blit(surface, (self.rect.center[0] - surface.get_width() / 2, self.rect.bottom - 90))
        surface = font.render(defense, True, LEVEL_COLOR)
        self.screen.blit(surface, (self.rect.center[0] - surface.get_width() / 2, self.rect.bottom - 60))

"""
Text class that is mainly used for displaying text on the UI.
"""
class Text(pygame.sprite.Sprite):
    def __init__(self, screen, groups, text, color, size, pos):
        super().__init__(groups)
        self.font = pygame.font.Font(FONT, size)
        self.screen = screen
        self.color = color
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center = pos)
        self.image.set_alpha(0)

    def update(self, text):
        self.image = self.font.render(text, True, self.color)
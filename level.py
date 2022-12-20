import pygame

from settings import *
from nodes import Node
from player import Player
from enemy import *
from cursor import Cursor
from debug import debug
from menu import Menu
from event import EventManager
from dialog import DialogManager
from battle import Battle
from status import Status
from equipment import Equipment
from npc import NPC
from sfx import *
from map.gangster import *
from scene import *
import random


"""
Common behaviors in different levels.
""" 
class Level:
    def __init__(self):
        # md = medieval, gs = gangster, cp = cyberpunk
        self.theme = "md"
        self.md_graph = MEDIEVAL_GRAPH
        self.gs_graph = GANGSTER_GRAPH
        self.reset_level()

    def run(self):
        self.draw_background()
        self.sfx_handling()
        
        # everything happened when not in menu screen
        if not self.status == -1 and not self.status == 0:
            if not self.in_village:
                self.draw_line()
                self.node_sprites.draw(self.screen)
                # draw the player only when not in village
                self.player.draw()
                # update player
                self.player.update()
            else:
                self.village_button.update()
                self.npc_sprites.update(self.screen)
            # draw ui
            self.equipment.show_ui()
            # the status bar should be blit after the equipment ui
            # so that the fader wouldn't affect the status bar
            # also do not draw the status ui when in fight
            if self.battle.battle_end:
                self.draw_status_bar()

            # move the player
            self.player.update()
            self.event.handling()

        self.change_cursor()
        self.click_handling()
        self.track_cursor()

        # import debug window to get the abstract coordinate faster
        # debug(self.player.pos)

        pygame.display.update()

        return self.status

    def in_world_map(self):
        return self.dialog.dialog_end \
            and self.battle.battle_end \
            and self.dialog.end_battle_dialog_end \
            and self.dialog.upgrade_dialog_end \
            and self.battle.battle_end

    def render_font(self, text, size, pos, color):
        font = pygame.font.Font(FONT, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center = pos)
        self.screen.blit(text_surface, text_rect)

    def sfx_handling(self):
        # walking sound
        if self.player.walking and not self.sfx.step_channel.get_busy():
            self.sfx.step_channel.play(self.sfx.walk)
        elif self.player.walking:
            self.sfx.bonfire_channel.stop()
        elif not self.player.walking:
            self.sfx.step_channel.stop()

        # bonfire sound
        for node in self.node_sprites:
            if self.sfx.bonfire_channel.get_busy(): return
            if node.node_type == "bonfire_faded" \
            and node.rect.collidepoint(self.player.rect.center):
                self.sfx.bonfire_channel.play(self.sfx.bonfire)

            # in village sound
            if node.node_type == "village" \
            and node.rect.collidepoint(self.player.rect.center) \
            and not self.village_sfx_start \
            and not self.player.exiting:
                self.sfx.village_channel.play(self.sfx.door_open)
                self.village_sfx_start = True

        # draw sword sound
        if not self.battle.battle_end and not self.battle_sfx_start:
            self.battle_sfx_start = True
            self.sfx.fight_channel_two.play(self.sfx.draw_sword)
        

    # draw the background on the screen based on theme
    def draw_background(self):
        if self.status == -1:
            self.screen.blit(self.game_menu.image, (0, 0))
            # shawdow
            self.render_font("DREAM", 150, (WIDTH / 2 + 4, 120 + 4), TITLE_TEXT_SHADOW_COLOR)
            # title
            self.render_font("DREAM", 150, (WIDTH / 2, 120), TITLE_TEXT_COLOR)
            self.render_font("PRESS TO WAKE UP", 40, (WIDTH / 2 + 4, HEIGHT - 70 + 4), TITLE_TEXT_SHADOW_COLOR)
            self.render_font("PRESS TO WAKE UP", 40, (WIDTH / 2, HEIGHT - 70), TITLE_TEXT_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.status = 1

        elif self.status == 0:
            self.screen.blit(self.game_over_menu.image, (0, 0))
            self.render_font("GAME OVER", 70, (WIDTH / 2 + 4, HEIGHT - 70 + 4), GAME_OVER_TEXT_COLOR_SHADOW)
            self.render_font("GAME OVER", 70, (WIDTH / 2, HEIGHT - 70), GAME_OVER_TEXT_COLOR)
            # game over dialog
            self.dialog.start_dialog(200)

            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                    self.reset_level()

        else:
            if not self.in_village:
                self.screen.blit(self.background, (0, 0))
            else:
                self.screen.blit(self.village, (0, 0))


    def draw_status_bar(self):
        if not self.in_world_map(): return
        
        # draw the status bar
        self.ui_sprites.draw(self.screen)
        # draw the hp bar and exp bar
        self.status_bar.draw(self.theme)

    # draw lines between current node and every neighbor node
    def draw_line(self):
        if not self.in_world_map(): return

        for node in self.node_sprites:
            if self.theme == "md":
                graph = MEDIEVAL_GRAPH[node.ab_pos]
            elif self.theme == "gs":
                graph = GANGSTER_GRAPH[node.ab_pos]
            # get the node where the player is
            if node.rect.collidepoint(self.player.rect.center):
                # loop to get the the target node
                for target_node in self.node_sprites:
                    if target_node.ab_pos in graph:
                        node.set_neighbor(target_node)
                        pygame.draw.line(self.screen, NODE_LINE_COLOR, node.rect.center, target_node.rect.center, 7)

    # change the cursor when hover over node
    def change_cursor(self):
        # initalize the cursor if not collided
        self.cursor.swap_cursor(self.theme, "normal")
        
        if self.status == 0 or self.status == -1:
            return

        # change cursor in other logic when in equipment menu
        if self.equipment.show:
            if self.equipment.button.rect.collidepoint(pygame.mouse.get_pos()):
                self.cursor.swap_cursor(self.theme, "hand")
            # change the cursor if the status bar is hovered
            if self.status_bar.rect.collidepoint(pygame.mouse.get_pos()) and self.battle.battle_end:
                self.cursor.swap_cursor(self.theme, "hand")
            for item in self.equipment.item_sprites:
                if item.rect.collidepoint(pygame.mouse.get_pos()):
                    self.cursor.swap_cursor(self.theme, "hand")

        # change cursor to dialog bubble if in village and not in equipment ui
        elif self.in_village :
            # show the bubble only when all dialog ends
            if self.dialog.dialog_end and self.dialog.end_battle_dialog_end:
                for npc in self.npc_sprites:
                    if npc.v_rect.collidepoint(pygame.mouse.get_pos()):
                        if npc.dialog_count < len(npc.dialogs):
                            self.cursor.swap_cursor(self.theme, "bubble")
                        else:
                            self.cursor.swap_cursor(self.theme, "bubble_faded")
                # change the cursor if the status bar is hovered
                if self.status_bar.rect.collidepoint(pygame.mouse.get_pos()):
                    self.cursor.swap_cursor(self.theme, "hand")

                if self.village_button.rect.collidepoint(pygame.mouse.get_pos()):
                    self.cursor.swap_cursor(self.theme, "hand")

        # if in world map then handle the nodes
        elif self.in_world_map():
            for node in self.node_sprites:
                # get the node where the player is
                if node.rect.collidepoint(self.player.rect.center):
                    # loop to get the the target node
                    for target_node in self.node_sprites:
                        # if the can-be-moved-to node is collided with cursor position, switch the cursor
                        if node.is_neighbor(target_node) and target_node.rect.collidepoint(pygame.mouse.get_pos()):
                            self.cursor.swap_cursor(self.theme, "hand")
                            break
            # change the cursor if the status bar is hovered
            if self.status_bar.rect.collidepoint(pygame.mouse.get_pos()) and self.battle.battle_end:
                self.cursor.swap_cursor(self.theme, "hand")

        # in battle, turn into weapon
        elif not self.battle.battle_end:
            if self.battle.enemy_image_rect.collidepoint(pygame.mouse.get_pos()):
                self.cursor.swap_cursor(self.theme, "weapon")

    # track the cursor and update cursor position accordingly
    def track_cursor(self):
        # track the cursor
        self.cursor.rect.center = pygame.mouse.get_pos()
        # refresh the cursor after the map and node have been generated
        self.screen.blit(self.cursor.image, pygame.mouse.get_pos())

    # handling click event in world map, including equipment ui
    # set target for player to move upon mouse click
    # also used for click detection action e.g., click the status bar, click the items    
    def click_handling(self):
        if not self.in_world_map(): return

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                # handling menu actions
                if self.status_bar.rect.collidepoint(pygame.mouse.get_pos()):
                    if self.player.walking: return
                    self.sfx.equipment_channel.play(self.sfx.equip)
                    self.equipment.show = not self.equipment.show
                if self.equipment.button.rect.collidepoint(pygame.mouse.get_pos()) and self.equipment.show:
                    if self.player.walking: return
                    self.sfx.equipment_channel.play(self.sfx.equip)
                    self.equipment.show = not self.equipment.show
                if self.village_button.rect.collidepoint(pygame.mouse.get_pos()) and self.in_village:
                    self.in_village = False
                    self.village_sfx_start = False
                    self.sfx.village_channel.play(self.sfx.door_open)
                    # indicate the player is exiting the village
                    self.player.exiting = True
                
                # only execute when the equipment ui is opened
                if self.equipment.show:
                    # handling switch item
                    for item in self.equipment.item_sprites:
                        if item.rect.collidepoint(pygame.mouse.get_pos()):
                            # if the weapon is equipped, unequip it, same with shield
                            if item.name == self.player.weapon or item.name == self.player.shield:
                                if item.name == self.player.weapon:
                                    self.player.weapon = ""
                                elif item.name == self.player.shield:
                                    self.player.shield = ""
                                self.player.items.append(item.name)
                            # if the weapon is unequipped, equip it, same with shield
                            else:
                                # if that is a weapon
                                if item.type == 1 or item.type == 2:
                                    # in case there is weapon already, append the item to the list
                                    # so that it acts like unequipping
                                    if item.type == 1 and self.player.weapon != "":
                                        self.player.items.append(self.player.weapon)
                                    if item.type == 2 and self.player.shield != "":
                                        self.player.items.append(self.player.shield)
                                    if item.type == 1:
                                        self.player.weapon = item.name
                                    else:
                                        self.player.shield = item.name
                                    # remove the item from the list because it's equipped
                                    self.player.items.remove(item.name)

                            """
                            Handle special items here.
                            """
                            if item.type == 0:
                                # flint will light up all the bonfires again
                                if item.name == "Flint":
                                    self.player.items.remove(item.name)
                                    for node in self.node_sprites:
                                        if (node.node_type == "bonfire_faded"):
                                            node.node_type = "bonfire"
                                            node.image = node.get_image(node.node_type)
                                            self.sfx.fight_channel.play(self.sfx.reignite)

                                # using mercy will enable the next level
                                if item.name == "Mercy":
                                    # play some slash sound
                                    self.sfx.fight_channel.play(self.sfx.player_slashs[random.randint(0, len(self.sfx.player_slashs) - 1)])
                                    self.sfx.fight_channel_two.play(self.sfx.blood)
                                    self.sfx.fight_channel_three.play(self.sfx.scream)
                                    # go to next level
                                    if self.theme == "md":
                                        self.reset_level("gs")
                                    else:
                                        self.theme = "md"
                                        self.reset_level()

                                    self.player.items.remove("Mercy")
                                    
                                if item.name == "Monster's Blood":
                                    self.player.hp = self.player.max_hp
                                    self.sfx.fight_channel.play(self.sfx.swallow)
                                    self.player.items.remove(item.name)
                            
                            # setting this flag will result in fixing selected item constantly showing
                            self.equipment.changing_item = True
                            # change the selected item to None so that it won't show after item being unequipped
                            self.equipment.selected_item = None
                            # prompt equipment ui to update the item list in next loop
                            self.equipment.update_item = True
                
                # do not set the target for player if in village
                if not self.in_village:
                # set the target for the player upon mouse click
                    for target_node in self.node_sprites:
                        # find the node where the mouse is clicked
                        if target_node.rect.collidepoint(pygame.mouse.get_pos()):
                            # do not set target when equipment ui is opened
                            if self.equipment.show: return
                            # find the node where the player is
                            for current_node in self.node_sprites:
                                # only allow player to move to the neighor node
                                if current_node.is_neighbor(target_node) and \
                                current_node.rect.center == self.player.rect.center:
                                    self.player.set_target(target_node.rect.topleft)


    # create different nodes on the map according to the abstract map and coordinate
    def create_map(self):
        if self.theme == "md":
            map = MEDIEVAL_MAP
        elif self.theme == "gs":
            map = GANGSTER_MAP
        for i, row in enumerate(map):
            for j, col in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE
                # empty nodes
                if col == "F":
                    Node(self.theme, (x, y), (j, i), "bonfire", [self.node_sprites])
                # player
                if col == "P":
                    # create a empty node where the player is
                    Node(self.theme, (x, y), (j, i), "empty", [self.node_sprites])
                    # create player
                    self.player = Player(self.theme, self.screen ,(x, y), [self.player_sprites, self.scene_sprites])
                # emenies
                if col == "E":
                    Node(self.theme, (x, y), (j, i), "enemy", [self.node_sprites])
                # village
                if col == "V":
                    Node(self.theme, (x, y), (j, i), "village", [self.node_sprites])
                # boss
                if col == "B":
                    Node(self.theme, (x, y), (j, i), "boss", [self.node_sprites])

    def reset_level(self, theme = None):
        # reset the theme
        if theme != None: self.theme = theme
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.sfx = SFX(self.theme)

        # the scene has been modified, reset to its origin form
        for key in hidden_scenes:
            if key in scenes:
                scenes.pop(key)

        # reset the graph that has been modified
        for key in self.gs_graph:
            GANGSTER_GRAPH[key] = self.gs_graph[key]

        # get the display surface
        try:
            self.background = pygame.image.load(os.path.join("./graphics/map/" + self.theme, "world_map.png")).convert_alpha()
        except:
            self.background = pygame.image.load(os.path.join("./graphics/map/md", "world_map.png")).convert_alpha()
        try:
            self.village = pygame.image.load(os.path.join("./graphics/map/" + self.theme, "village.png")).convert_alpha()
        except:
            self.village = pygame.image.load(os.path.join("./graphics/map/md", "village.png")).convert_alpha()

        self.game_menu = Menu("game_menu")
        self.game_over_menu = Menu("game_over")

        # spites group
        self.player_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()
        self.node_sprites = pygame.sprite.Group()
        self.dialog_sprites = pygame.sprite.Group()
        self.scene_sprites = pygame.sprite.Group()
        self.npc_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()
        self.equipment_sprites = pygame.sprite.Group()

        self.battle_sfx_start = False
        self.village_sfx_start = False

        self.create_map()

        self.cursor = Cursor(pygame.mouse.get_pos(), self.theme)
        self.dialog = DialogManager(self.screen, self.scene_sprites, self.sfx, self.theme)
        self.battle = Battle(self.screen, self.theme, self.player, self.sfx)

        # the status used to pass back to the Game class
        # -1 = in game menu
        # 0 = gameover
        # 1 = in world
        self.status = -1 if theme == None else 1
        self.status_bar = Status(self.screen, self.ui_sprites, self.theme, self.player)
        self.event = EventManager(self, self.dialog)
        # indicating whether the player is in village
        self.in_village = False
        # equipment ui
        self.equipment = Equipment(self.screen, self.theme, self.equipment_sprites, self.player, self.sfx) 
        # create enemies and put them into the sprite group
        for i in ENEMIES:
            if ENEMIES[i]["theme"] == self.theme:
                Enemy([self.enemy_sprites, self.scene_sprites], i, **ENEMIES[i])
        for i in NPCS:
            if NPCS[i]["theme"] == self.theme:
                NPC([self.scene_sprites, self.npc_sprites], **NPCS[i])
        # exit button for village
        self.village_button = VButton(self.screen, self.theme)

class VButton(pygame.sprite.Sprite):
    def __init__(self, screen, theme):
        self.font = pygame.font.Font(FONT, 25)
        self.screen = screen
        try:
            self.image = pygame.image.load(os.path.join("./graphics/node/" + theme, "village_node.png")).convert_alpha()
        except:
            self.image = pygame.image.load(os.path.join("./graphics/node/md", "village_node.png")).convert_alpha()
        self.rect = self.image.get_rect(topleft = (WIDTH - self.image.get_size()[0] - 5, HEIGHT - self.image.get_size()[1] - 5))

    def update(self):
        self.screen.blit(self.image, self.rect)
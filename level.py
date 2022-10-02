import pygame
import math

from settings import *
from node import Node
from player import Player
from cursor import Cursor
from debug import debug
from menu import Menu
from dialog import DialogManager
from status import Status

# Common behaviors in different levels #

class Level:
    def __init__(self, theme, screen):
        # get the display surface
        self.screen = screen
        # md, gs, cp
        self.theme = theme

        # spites group
        self.player_sriptes = pygame.sprite.Group()
        self.node_sprites = pygame.sprite.Group()
        self.dialog_sprites = pygame.sprite.Group()
        self.scene_sprites = pygame.sprite.Group()
        self.ui_sprites = pygame.sprite.Group()

        self.create_map()
        self.cursor = Cursor(pygame.mouse.get_pos())
        self.dialog = DialogManager(self.screen, self.dialog_sprites, self.scene_sprites)
        
        self.game_menu = Menu("game_menu")
        self.in_game_menu = True

        self.in_battle = False

        # status bar
        self.status_bar = Status(self.screen, self.ui_sprites, self.player)

    def run(self):
        self.draw_background()
        
        # everything happened when not in menu screen
        if not self.in_game_menu:
            self.draw_line()
            self.node_sprites.draw(self.screen)
            self.player_sriptes.draw(self.screen)
            self.change_cursor()
            # update player
            self.player_sriptes.update()
            self.draw_status_bar()
            self.event_handling()
            self.set_target()
            self.track_cursor()

            # import debug window to get the abstract coordinate faster
            debug(self.player.pos)

    # draw the background on the screen based on theme
    def draw_background(self):
        if self.in_game_menu:
            self.screen.blit(self.game_menu.image, (0, 0))
            for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        self.in_game_menu = False
        else:
            if self.theme == "md":
                self.screen.blit(MEDIEVAL_BACKGROUND, (0 , 0))

    def draw_status_bar(self):
        # don't draw the line if it is in a dialog
        if not self.dialog.dialog_end:
            return
        
        # draw the status bar
        self.ui_sprites.draw(self.screen)
        # draw the hp bar and exp bar
        self.status_bar.draw()

    # draw lines between current node and every neighbor node
    def draw_line(self):
        # don't draw the line if it is in a dialog
        if not self.dialog.dialog_end:
            return

        for node in self.node_sprites:
            # get the node where the player is
            if node.rect.collidepoint(self.player.rect.center):
                # loop to get the the target node
                for target_node in self.node_sprites:
                    if target_node.ab_pos in MEDIEVAL_GRAPH[node.ab_pos]:
                        node.set_neighbor(target_node)
                        pygame.draw.line(self.screen, (113, 10, 10), node.rect.center, target_node.rect.center, 7)

    # change the cursor when hover over node
    def change_cursor(self):
        # don't swap the cursor if it is in a dialog
        if not self.dialog.dialog_end:
            return

        # initalize the cursor if not collided
        self.cursor.swap_cursor("normal")
        for node in self.node_sprites:
            # if the empty node is collided with cursor position, switch the cursor
            if node.rect.collidepoint(pygame.mouse.get_pos()):
                self.cursor.swap_cursor("hand")
                break

    # track the cursor and update cursor position accordingly
    def track_cursor(self):
        # track the cursor
        self.cursor.rect.center = pygame.mouse.get_pos()
        # refresh the cursor after the map and node have been generated
        self.screen.blit(self.cursor.image, pygame.mouse.get_pos())

    # set target for player to move upon mouse click
    def set_target(self):
        for event in pygame.event.get():
            # set the target for the player upon mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                for target_node in self.node_sprites:
                    # find the node where the mouse is clicked
                    if target_node.rect.collidepoint(pygame.mouse.get_pos()):
                        # find the node where the player is
                        for current_node in self.node_sprites:
                            # only allow player to move to the neighor node
                            if current_node.is_neighor(target_node) and current_node.rect.center == self.player.rect.center:
                                self.player.set_target(target_node.rect.topleft)
    
    # create different nodes on the map according to the abstract map and coordinate
    def create_map(self):
        for i, row in enumerate(MEDIEVAL_MAP):
            for j, col in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE
                # empty nodes
                if col == "N":
                    Node((x, y), (j, i), "empty", [self.node_sprites])
                # player
                if col == "P":
                    # create a empty node where the player is
                    Node((x, y), (j, i), "empty", [self.node_sprites])
                    # create player
                    self.player = Player((x, y), [self.player_sriptes, self.scene_sprites])
                # emenies
                if col == "E":
                    Node((x, y), (j, i), "enemy", [self.node_sprites])
                # village
                if col == "V":
                    Node((x, y), (j, i), "village", [self.node_sprites])
                # boss
                if col == "B":
                    Node((x, y), (j, i), "boss", [self.node_sprites])

    def event_handling(self):
        # all scene in medieval
        if self.theme == "md":
            # scenes related to node collision
            for node in self.node_sprites:
                # opening scene
                if node.ab_pos == (7, 15):
                    if self.player.rect.colliderect(node.rect):
                        self.dialog.start_dialog(0)
                # first encounter scene
                if node.ab_pos == (7, 13):
                    if self.player.rect.colliderect(node.rect):
                        self.dialog.start_dialog(1)

        elif self.theme == "gs":
            pass
        elif self.theme == "cp":
            pass

    def battle(self):
        pass
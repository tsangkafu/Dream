import pygame

from settings import *
from node import Node
from player import Player
from cursor import Cursor
from debug import debug

# a graph reference that indicate whether nodes are neighbor
GRAPH = {
    (7, 13): [(6, 11)]
}

class Level:
    def __init__(self):
        # get the display surface
        self.display_surface = pygame.display.get_surface()
        # including player, enemy
        self.visible_sprites = pygame.sprite.Group()
        self.node_sprites = pygame.sprite.Group()
        self.nodes = []
        self.create_map()
        self.cursor = Cursor(pygame.mouse.get_pos())

    # will only be called once    
    def create_map(self):
        for i, row in enumerate(MEDIEVAL_MAP):
            for j, col in enumerate(row):
                x = j * TILESIZE
                y = i * TILESIZE
                # empty nodes
                if col == "N":
                    node = Node((x, y), (j, i), "empty", [self.node_sprites])
                    self.nodes.append(node)
                    print((j, i))
                # player
                if col == "P":
                    self.player = Player((x, y), [self.visible_sprites])
                # emenies
                if col == "E":
                    node = Node((x, y), (j, i), "enemy" ,[self.node_sprites])
                    self.nodes.append(node)
                    print((j, i))

    def run(self):
        for node in self.nodes:
            if node.ab_pos in GRAPH:
                for node_2 in self.nodes:
                    if node_2.ab_pos in GRAPH[node.ab_pos]:
                        pygame.draw.line(self.display_surface, (0, 255, 0), node.rect.center, node_2.rect.center, 5)

        self.node_sprites.draw(self.display_surface)
        self.visible_sprites.draw(self.display_surface)

        # initalize the cursor if not collided
        self.cursor.swap_cursor("normal")
        for empty_node in self.node_sprites:
            # if the empty node is collided with cursor position, switch the cursor
            if empty_node.rect.collidepoint(pygame.mouse.get_pos()):
                self.cursor.swap_cursor("hand")
                break

        debug(self.player.pos)

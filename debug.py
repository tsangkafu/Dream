# debug window reference from https://youtu.be/QU1pPzEGrqw

import pygame

pygame.init()
font = pygame.font.Font(None, 30)

def debug(info, y = 10, x = 10):
    display_surface = pygame.display.get_surface()
    # divide by 80 to get the abstract coordinate
    debug_surf = font.render(str(info / 64), True, "White")
    debug_rect = debug_surf.get_rect(topleft = (x, y))
    pygame.draw.rect(display_surface, "Black", debug_rect)
    display_surface.blit(debug_surf, debug_rect)
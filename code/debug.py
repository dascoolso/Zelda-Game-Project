import pygame


pygame.init()
font = pygame.font.SysFont('poppins', 15, bold=True, italic=True)

def debug (info, screen, color_1, color_2, x = 10, y = 10):
    # color_1 = black, color_2 = white
    debug_surf = font.render(str(info), True, color_1)
    debug_rect = debug_surf.get_rect(topleft=(x, y))
    pygame.draw.rect(screen, color_2, debug_rect)
    screen.blit(debug_surf, debug_rect)
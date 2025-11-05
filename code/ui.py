import pygame

from settings import Settings
from support import absolute_path

def draw_enemy_health_bar(enemy, screen, offset):
    width=enemy.rect.width*(enemy.health/Settings().monster_data[enemy.monster_name]['health'])
    hb_surface = pygame.Surface((width, 10))
    hb_surface.fill(enemy.ui_details['hb_color'])


    hb_world_pos = (enemy.rect.x, enemy.rect.topleft[1] - 17)
    
    hb_screen_pos = pygame.math.Vector2(hb_world_pos) - offset

    hb_rect = hb_surface.get_rect(topleft=hb_screen_pos)
    
    screen.blit(hb_surface, hb_rect)

def draw_health_bar(screen, p_hb_d, hb_c, player):
    surf=pygame.Surface(p_hb_d[0])
    surf.set_alpha(50)
    rect = surf.get_rect(topleft=p_hb_d[1])
    screen.blit(surf, rect)
    # pygame.draw.rect(screen, p_hb_d[2], rect, border_radius=p_hb_d[4])

    hb_width = p_hb_d[0][0]
    health = player.health
    if health > 0:
        ratio = round(health/Settings().player_max_health, 2)
    else:
        ratio = 0
    rect.width = round(hb_width * ratio, 0)
    if ratio>=0.7:
        if ratio == 1.0:
            pygame.draw.rect(screen, hb_c[0], rect, border_radius=p_hb_d[4])
        else:
            pygame.draw.rect(screen, hb_c[0], rect, border_top_left_radius=p_hb_d[4], border_bottom_left_radius=p_hb_d[4])
    elif 0.3<=ratio<0.7:
        pygame.draw.rect(screen, hb_c[1], rect, border_top_left_radius=p_hb_d[4], border_bottom_left_radius=p_hb_d[4])
    else:
        pygame.draw.rect(screen, hb_c[2], rect, border_top_left_radius=p_hb_d[4], border_bottom_left_radius=p_hb_d[4])

    rect.width=hb_width
    rect.topleft = p_hb_d[1]
    pygame.draw.rect(screen, p_hb_d[3], rect, 3, p_hb_d[4])

def draw_energy_bar(screen, p_eb_d, eb_c, player):
    surf=pygame.Surface(p_eb_d[0])
    surf.set_alpha(50)
    rect = surf.get_rect(topleft=p_eb_d[1])
    screen.blit(surf, rect)

    eb_width = p_eb_d[0][0]
    energy=player.energy
    ratio = round(energy/Settings().player_max_energy, 2)
    rect.width = round(eb_width*ratio, 0)
    if ratio>=0.7:
        if ratio == 1.0:
            pygame.draw.rect(screen, eb_c[0], rect, border_radius=p_eb_d[4])
        else:
            pygame.draw.rect(screen, eb_c[0], rect, border_top_left_radius=p_eb_d[4], border_bottom_left_radius=p_eb_d[4])
    elif 0.3<=ratio<0.7:
        pygame.draw.rect(screen, eb_c[1], rect, border_top_left_radius=p_eb_d[4], border_bottom_left_radius=p_eb_d[4])
    else:
        pygame.draw.rect(screen, eb_c[2], rect, border_top_left_radius=p_eb_d[4], border_bottom_left_radius=p_eb_d[4])

    rect.width=eb_width
    rect.topleft = p_eb_d[1]
    pygame.draw.rect(screen, p_eb_d[3], rect, 3, p_eb_d[4])

def draw_experience(screen, p_e_ui, player):
    font=pygame.font.SysFont('poppins', 30, True, True)

    exp_surf=font.render(str(player.exp), True, p_e_ui[2])
    exp_rect = exp_surf.get_rect(bottomright=p_e_ui[0])

    screen.blit(exp_surf, exp_rect)

def draw_weapon_magic_icon(screen, w_m, player):
    hold_rect_weapon=pygame.draw.rect(screen, w_m[3], pygame.Rect(w_m[1], w_m[2], w_m[0], w_m[0]), border_radius=10)
    hold_rect_magic=pygame.draw.rect(screen, w_m[3], pygame.Rect(w_m[1]+w_m[0]+10, w_m[2], w_m[0], w_m[0]), border_radius=10)
    
    if player.flag=='w':
        current_time = pygame.time.get_ticks()
        if current_time-player.weapon_switching['switched_time']<=Settings().glow_activated:
            pygame.draw.rect(screen, w_m[5], hold_rect_weapon, 2, 10)
        else:
            pygame.draw.rect(screen, w_m[4], hold_rect_weapon, 2, 10)

    if player.flag=='m':
        current_time = pygame.time.get_ticks()
        if current_time-player.magic_switching['switched_time']<=Settings().glow_activated:
            pygame.draw.rect(screen, w_m[5], hold_rect_magic, 2, 10)
        else:
            pygame.draw.rect(screen, w_m[4], hold_rect_magic, 2, 10)

    weapon_image = pygame.image.load(absolute_path(Settings().weapon_data[player.current_weapon].get('image'))).convert_alpha()
    weapon_image_rect = weapon_image.get_rect(center=hold_rect_weapon.center)
    screen.blit(weapon_image, weapon_image_rect)

    magic_image = pygame.transform.scale(pygame.image.load(absolute_path(Settings().magic_data[player.current_magic].get('image'))).convert_alpha(), Settings().transformed_image_dimensions)
    magic_image_rect = magic_image.get_rect(center=hold_rect_magic.center)
    screen.blit(magic_image, magic_image_rect)

def draw_health_storage(screen, player):
    pygame.draw.rect(screen, player.hsb['color'], pygame.rect.Rect(player.hsb['position'][0], player.hsb['position'][1], player.hsb_width, player.hsb_height))
    pygame.draw.rect(screen, player.hsb['border_color'], pygame.rect.Rect(player.hsb['position'][0], player.hsb['position'][1], player.max_health_storage, player.hsb_height), 2)

def end_screen_data(screen, rect, player):
    font = pygame.font.Font(absolute_path('font/joystix.ttf'), 30)
    lines = [f"Enemies Killed: {str(player.killed_enemy)}", f"Total Experience: {str(player.total_exp)}"]

    line_spacing = 30
    start_x = rect.x + 20
    start_y = rect.y + line_spacing

    for dialog in lines:
        surface = font.render(str(dialog), True, "#FF2664")
        local_rect = surface.get_rect(topleft = (start_x, start_y))
        screen.blit(surface, local_rect)
        start_y += font.get_height() + line_spacing
    
class UI(pygame.sprite.Sprite):

    def __init__(self, screen):
        super().__init__()
        self.screen = screen

        self.player_hb_details=Settings().player_UI['health_bar']
        self.player_hb_color=Settings().player_UI['hb_color']

        self.player_eb_details=Settings().player_UI['energy_bar']
        self.player_eb_color=Settings().player_UI['eb_color']

        self.player_exp_ui=Settings().player_UI['experience_square']

        self.weapon_magic_details = Settings().player_UI['weapon_and_magic']

    def display(self, player):

        draw_health_bar(self.screen, self.player_hb_details, self.player_hb_color, player)

        draw_energy_bar(self.screen, self.player_eb_details, self.player_eb_color, player)

        draw_experience(self.screen, self.player_exp_ui, player)

        draw_weapon_magic_icon(self.screen, self.weapon_magic_details, player)

        draw_health_storage(self.screen, player)
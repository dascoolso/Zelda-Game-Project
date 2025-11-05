import pygame

from settings import Settings
from support import absolute_path


class Weapon(pygame.sprite.Sprite):

    def __init__(self, player, groups):
        super().__init__(groups)
        self.sprite_type = 'w'
        self.direction = player.status.split('_')[0]
        self.weapon = Settings().weapon_data[player.current_weapon].get('image').replace('full', self.direction)
        self.image = pygame.image.load(absolute_path(self.weapon)).convert_alpha()

        # Placement
        if self.direction == 'right':
            self.rect = self.image.get_rect(midleft=player.rect.midright+pygame.math.Vector2(0, 16))
        elif self.direction == 'left':
            self.rect = self.image.get_rect(midright=player.rect.midleft+pygame.math.Vector2(0, 16))
        if self.direction == 'up':
            self.rect = self.image.get_rect(midbottom=player.rect.midtop+pygame.math.Vector2(16, 0))
        if self.direction == 'down':
            self.rect = self.image.get_rect(midtop=player.rect.midbottom+pygame.math.Vector2(-16, 0))

        # print(self.rect.size)
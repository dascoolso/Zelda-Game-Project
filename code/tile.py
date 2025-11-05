import pygame
from settings import Settings

class Tile(pygame.sprite.Sprite):
    """A class for Game Screen Tiles"""

    def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((Settings().area, Settings().area))):
        super().__init__(groups)
        self.sprite_type = sprite_type
        self.image = surface
        # if sprite_type == 'grass':
        #     self.damage = 0
        if sprite_type == 'object':
            self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-Settings().area))
        else:
            self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -10)

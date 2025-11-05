import pygame

from random import choice


from tile import Tile
from player import Player
from debug import debug
from support import import_csv_layout, import_folder, absolute_path
from weapon import Weapon
from ui import UI, draw_enemy_health_bar, end_screen_data
from enemy import Enemy
from collision import Collision
from particles import AnimationEntities

class Level:
    """Dealing with player, obstacles and enemies. Holds all the Groups."""
    def __init__(self, main_file):
        """Initialization of everything thing."""
        # Setting up the Screen
        self.screen = main_file.screen
        self.settings = main_file.settings
        
        # Sprite Group Setup
        self.visible_sprites_group = YSortCameraGroup(self.screen)
        self.obstacle_sprites_group = pygame.sprite.Group()
        self.attackable_sprites = pygame.sprite.Group()
        self.enemy_sprites = pygame.sprite.Group()

        # Attack
        self.created_attack = None
        self.collision = Collision()

        # Map Creation for the Game
        self.create_map()
        self.animation_entities = AnimationEntities()
        self.ui_overall=UI(self.screen)

        # Ending the Game
        self.player_dead = False
        self.game_sound = main_file.main_sound
        
        self.end_image = self.get_end_image()
        self.end_image_rect = self.end_image.get_rect().inflate(40, 20)

    def create_map(self):
        """The 2D Digital Map"""
        layout_data = {
            'boundary': import_csv_layout('map_data/map_FloorBlocks.csv'),
            'grass': import_csv_layout('map_data/map_Grass.csv'),
            'object': import_csv_layout('map_data/map_Objects.csv'),
            'entities': import_csv_layout('map_data/map_Entities.csv')
        }
        layout_images = {
            'grass': import_folder('layout_images/grass'),
            'objects': import_folder('layout_images/objects')
        }
        for style, layout in layout_data.items():
            for row_idx, row in enumerate(layout):
                for col_idx, col in enumerate(row):
                    if col!='-1':
                        x = col_idx*self.settings.area
                        y = row_idx*self.settings.area
                        if style == 'boundary':
                            Tile((x, y), [self.obstacle_sprites_group], 'invisible')
                        if style == 'grass':
                            random_grass_img = choice(layout_images['grass'])
                            Tile((x, y), [self.obstacle_sprites_group, self.visible_sprites_group, self.attackable_sprites], 'grass', random_grass_img.convert_alpha())
                        if style == 'object':
                            surf = layout_images['objects'][int(col)]
                            Tile((x, y), [self.visible_sprites_group, self.obstacle_sprites_group], 'object', surf.convert_alpha())

                        if style=='entities':
                            if col=='394':
                                self.player = Player((x, y), [self.visible_sprites_group], self.obstacle_sprites_group, self.create_attack, self.destroy_attack, self.create_magic)
                            else:
                                if col == '390': monster_name = 'bamboo'
                                elif col == '391': monster_name = 'spirit'
                                elif col == '392': monster_name ='raccoon'
                                else: monster_name = 'squid'
                                Enemy(self.screen, monster_name, [self.visible_sprites_group, self.attackable_sprites, self.enemy_sprites], (x, y), self.obstacle_sprites_group, self.enemy_attack, self.trigger_action)
        
    def get_end_image(self)-> pygame.surface.Surface:
        end_image = pygame.image.load(absolute_path('layout_images/player/player.png')).convert_alpha()
        original_size = end_image.get_size()

        new_image_width = original_size[0] * self.settings.scale_factor
        new_image_height = original_size[1] * self.settings.scale_factor

        enlarged_image = pygame.transform.smoothscale(end_image, (new_image_width, new_image_height))

        return enlarged_image

    def create_attack(self):
        self.created_attack=Weapon(self.player, [self.visible_sprites_group])
        self.player.attacked = True

    def destroy_attack(self):
        if type(self.created_attack) is not str:
            self.visible_sprites_group.remove(self.created_attack)
        self.created_attack=None

    def create_magic(self, magic_name):
        self.created_attack = magic_name
        self.player.attacked = True

    def enemy_attack(self, pos, damage, attack_type, sound):
        if self.player.vulnerable:
            sound.play()
            self.trigger_action(pos, attack_type)
            self.player.health -= damage
            self.player.hurt_time = pygame.time.get_ticks()
            self.player.vulnerable = False

        if self.player.health <= 0:
            self.player_dead = True
            # self.visible_sprites_group.remove(self.player)
            # self.player.kill()
            # self.ending_screen()
            
    def trigger_action(self, pos, frame_type):
        self.animation_entities.create_particles(frame_type, pos, self.visible_sprites_group)

    def ending_screen(self):
        blur_surface = pygame.Surface((self.screen.get_width(), self.screen.get_height()))
        blur_surface.set_alpha(150)
        blur_surface.fill("#000000")
        self.screen.blit(blur_surface, (0, 0))

        surf = pygame.Surface((self.screen.get_height()*0.9, self.screen.get_height()*0.7))
        rect = surf.get_rect(center=self.screen.get_rect().center)
        pygame.draw.rect(self.screen, "#FEE2B1", rect, border_radius=2)
        pygame.draw.rect(self.screen, "#FF6A6A", rect, 3, 2)

        self.end_image_rect.bottomleft = rect.bottomleft
        self.end_image_rect.x = rect.x + self.settings.left_gap
        self.end_image_rect.bottom = rect.bottom - 30
        
        self.screen.blit(self.end_image, self.end_image_rect) 

        end_screen_data(self.screen, rect, self.player)

    def run(self):
        """The only method running the whole Game"""
        self.visible_sprites_group.custom_draw(self.player)
        
        if self.player_dead or not self.enemy_sprites:
            self.game_sound.stop()
            self.ending_screen()
        
        else:
            self.visible_sprites_group.update()

            # debug(self.player.status, self.screen, self.settings.bg_color_1, self.settings.bg_color_2)

            self.visible_sprites_group.enemy_update(self.player)
            
            self.collision.player_attack_logic(self.created_attack, self.attackable_sprites, self.player, self.visible_sprites_group)

        self.ui_overall.display(self.player)

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self, display_screen):
        super().__init__()
        self.screen = display_screen

        self.half_width = self.screen.get_width() // 2
        self.half_height = self.screen.get_height() // 2

        self.offset = pygame.math.Vector2()

        self.floor_map = pygame.image.load(absolute_path('layout_images/map/ground.png')).convert()
        self.floor_rect = self.floor_map.get_rect(topleft=(0, 0))

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        floor_offset_pos = self.floor_rect.topleft - self.offset
        self.screen.blit(self.floor_map, floor_offset_pos)

        for sprite in sorted(self.sprites(), key=lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft-self.offset
            self.screen.blit(sprite.image, offset_pos)

            if hasattr(sprite, 'sprite_type') and sprite.sprite_type == 'enemy':
                draw_enemy_health_bar(sprite, self.screen, self.offset)

    def enemy_update(self,player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)
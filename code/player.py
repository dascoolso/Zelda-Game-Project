import pygame

from typing import Tuple


from settings import Settings
from collision import Collision
from support import import_folder, absolute_path


class Player(pygame.sprite.Sprite):
    """A class for Game PLayer"""

    def __init__(self, pos: Tuple, groups, obstacle_sprites: pygame.sprite.Group, create_attack, destroy_attack, create_magic):
        super().__init__(groups)

        self.settings = Settings()

        # Getting own Attribute
        self.image = pygame.transform.scale(pygame.image.load(absolute_path('layout_images/player/down_idle/idle_down.png')).convert_alpha(), self.settings.player_dimesions)
        self.rect = self.image.get_rect(topleft=pos)
        self.hitbox = self.rect.inflate(0, -26)

        # Graphics Setup
        self.import_player_assets()
        self.status = 'down_idle'
        self.frame_index=0
        self.animation_speed = 0.15

        # Player Movements
        self.player_collision = Collision()
        self.obstacle_sprites = obstacle_sprites
        self.direction = pygame.math.Vector2()
        self.one_at_a_time = False
        self.one_at_a_time_cooldown = self.settings.action_cooldown
        self.that_time = 0

        # Player Attack and Magic
        self.killed_enemy = 0
        self.flag = 'w'
        self.create_attack = create_attack
        self.destroy_attack = destroy_attack
        self.create_magic = create_magic
        self.current_magic = 'flame'
        self.current_weapon = 'rapier'
        self.weapon_switching={
            'has_switched': False, 
            'switching_cooldown': self.settings.weapon_switch_cooldown,
            'switched_time': 0
        }
        self.magic_switching={
            'has_switched': False, 
            'switching_cooldown': self.settings.magic_switch_cooldown,
            'switched_time': 0
        }
        self.attack_type = self.settings.default_player_stats['attack_type']
        self.attacked = False
        self.volume = self.settings.other
        self.heal_sound = pygame.mixer.Sound(absolute_path(self.settings.magic_data['heal']['sound']))
        self.heal_sound.set_volume(self.volume)
        self.flame_sound = pygame.mixer.Sound(absolute_path(self.settings.magic_data['flame']['sound']))
        self.flame_sound.set_volume(self.volume)
        
        # Health Increase after Attack
        self.hsb = self.settings.health_storage_bar
        self.max_health_storage = self.hsb['max_storage']
        self.hsb_width = 0
        self.hsb_height = self.hsb['height']

        # Player Stats
        self.stats = self.settings.default_player_stats
        self.health = self.stats['health']
        self.energy = self.stats['energy']
        self.speed = self.stats['speed']
        self.magic_effect_radius = self.stats['magic_effect_radius']
        self.attack_sound = pygame.mixer.Sound(absolute_path(self.stats['attack_sound']))
        self.attack_sound.set_volume(self.volume)
        self.total_exp = 0
        self.exp = 0
        self.energy_increment_cooldown = self.settings.default_player_stats['energy_increment_cooldown']
        self.last_increment=0
        self.increase=True
        self.energy_increment_amount = self.settings.player_energy_increment_amount

        # Damage
        self.vulnerable = True
        self.hurt_time = 0
        self.invulnerability_duration = 500

    def import_player_assets(self):
        character_path = 'layout_images/player/'
        self.animations = {
            'up': [], 'down':[], 'left': [], 'right': [], 'right_idle': [], 'left_idle': [], 'up_idle': [], 'down_idle': [], 'right_attack': [], 'left_attack': [], 'up_attack': [], 'down_attack': []
        }
        for animation in self.animations.keys():
            full_path = character_path+animation
            self.animations[animation] = import_folder(full_path)

    def input(self):
        if not self.one_at_a_time:
            keys = pygame.key.get_pressed()

            # Movement
            if keys[pygame.K_UP]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:
                self.direction.x = 0
        
        # Attack Input
            if keys[self.settings.attack]:
                self.one_at_a_time = True
                self.that_time = pygame.time.get_ticks()
                self.attack_sound.play()
                self.create_attack()

        # Magic Input
            elif keys[self.settings.magic]:
                self.one_at_a_time = True
                self.that_time = pygame.time.get_ticks()
                self.create_magic(self.current_magic)

        # Assign Mode
            if keys[self.settings.magic_switch]:
                self.flag='m'
            
            if keys[self.settings.weapon_switch]:
                self.flag='w'

            if not self.vulnerable:
            # Switch Magic
                if not self.magic_switching['has_switched'] and self.flag=='m':

                    if keys[self.settings.flame]:
                        self.current_magic='flame'

                        self.magic_switching['switched_time']=pygame.time.get_ticks()
                        self.magic_switching['has_switched'] = True

                    elif keys[self.settings.heal]:
                        self.current_magic='heal'

                        self.magic_switching['switched_time']=pygame.time.get_ticks()
                        self.magic_switching['has_switched'] = True
            
            # Switch Weapon
                if not self.weapon_switching['has_switched'] and self.flag=='w':

                    if keys[self.settings.axe]:
                        self.current_weapon ='axe'

                        self.weapon_switching['switched_time']=pygame.time.get_ticks()
                        self.weapon_switching['has_switched'] = True

                    elif keys[self.settings.sword]:
                        self.current_weapon='sword'

                        self.weapon_switching['switched_time']=pygame.time.get_ticks()
                        self.weapon_switching['has_switched'] = True

                    elif keys[self.settings.lance]:
                        self.current_weapon='lance'

                        self.weapon_switching['switched_time']=pygame.time.get_ticks()
                        self.weapon_switching['has_switched'] = True

                    elif keys[self.settings.rapier]:
                        self.current_weapon='rapier'

                        self.weapon_switching['switched_time']=pygame.time.get_ticks()
                        self.weapon_switching['has_switched'] = True

                    elif keys[self.settings.sai]:
                        self.current_weapon='sai'

                        self.weapon_switching['switched_time']=pygame.time.get_ticks()
                        self.weapon_switching['has_switched'] = True

    def get_status(self):

        # idle status
        if self.direction.x == 0 and self.direction.y == 0:
            if not '_idle' in self.status and not '_attack' in self.status:
                self.status += '_idle'

        if self.one_at_a_time:
            self.direction.x = 0
            self.direction.y = 0
            if not '_attack' in self.status:
                if  '_idle' in self.status:
                    self.status = self.status.replace('_idle', '_attack')
                else:    
                    self.status += '_attack'
        else:
            if '_attack' in self.status:
                self.status=self.status.replace('_attack', '')

    def move(self):
        """
        Moves the player. Checks for collisions and revert.
        This is the "in the Place" method.
        """
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x+=self.direction.x*self.speed
        self.player_collision.collision_of_interactors_with_obstacles(self, 'horizontal', self.obstacle_sprites)

        self.hitbox.y+=self.direction.y*self.speed
        self.player_collision.collision_of_interactors_with_obstacles(self, 'vertical', self.obstacle_sprites)    

        self.rect.center = self.hitbox.center

    def increase_energy(self):
        if self.energy + self.energy_increment_amount <= self.settings.player_max_energy and self.increase:
            self.energy += self.energy_increment_amount
            self.last_increment=pygame.time.get_ticks()
            self.increase=False

    def timeout(self):
        current_time = pygame.time.get_ticks()

        if not self.increase:
            if current_time-self.last_increment>=self.energy_increment_cooldown:
                self.increase=True

        if self.one_at_a_time:
            if current_time - self.that_time >= self.one_at_a_time_cooldown:
                self.one_at_a_time = False
                self.destroy_attack()

        if self.weapon_switching['has_switched']:
            if current_time - self.weapon_switching['switched_time'] >= self.weapon_switching['switching_cooldown']:
                self.weapon_switching['has_switched'] = False

        if self.magic_switching['has_switched']:
            if current_time - self.magic_switching['switched_time'] >= self.magic_switching['switching_cooldown']:
                self.magic_switching['has_switched'] = False

        if not self.vulnerable:
            if current_time - self.hurt_time >= self.invulnerability_duration:
                self.vulnerable = True

    def player_animation(self):
        animation = self.animations[self.status]

        # Loop overthe frame index
        self.frame_index += self.animation_speed
        if self.frame_index>=len(animation):
            self.frame_index=0

        self.image = pygame.transform.scale(animation[int(self.frame_index)], self.settings.player_dimesions).convert_alpha()
        self.rect = self.image.get_rect(center=self.hitbox.center) 

        # Flicker
        if not self.vulnerable:
            alpha = Settings().wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def update(self):
        self.input()
        self.move()
        self.get_status()
        self.player_animation()
        self.increase_energy()
        self.timeout()
import pygame
# pygame.sprite.Group.add

from settings import Settings
from support import import_folder, absolute_path
from collision import Collision
from random import choice


class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, monster, groups, pos, obstacle_sprites, enemy_attack, trigger_action):
        super().__init__(groups)
        self.screen = screen
        self.frame_index = 0
        self.animation_speed = 0.15
        self.direction = pygame.math.Vector2()
        self.sprite_type = 'enemy'

        # general setup
        self.import_graphics(monster)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index].convert_alpha()
        self.rect = self.image.get_rect(topleft=pos)
        if monster=='raccoon':
            self.hitbox = self.rect.inflate(-48, -39)
        else: self.hitbox = self.rect.inflate(0, -10)
        
        self.obstacle_sprites=obstacle_sprites
        self.enemy_collision = Collision()
        self.volume = Settings().other

        # stats
        self.monster_name = monster
        self.monster_info = Settings().monster_data[monster]
        self.ui_details=Settings().monsters_ui[monster]
        self.health = self.monster_info['health']
        self.retreat = self.monster_info['retreat']
        self.damage = self.monster_info['damage']
        self.attack_type = self.monster_info['attack_type']
        self.attack_sound = pygame.mixer.Sound(absolute_path(self.monster_info['attack_sound']))
        self.attack_sound.set_volume(self.volume)
        self.push_back = Settings().monster_data['push_back']

        # player interaction
        self.can_attack = True
        self.attack_time = 0
        self.enemy_attack = enemy_attack
        self.trigger_action = trigger_action
        self.death_sound = pygame.mixer.Sound(absolute_path('audio/death.wav'))
        self.death_sound.set_volume(self.volume)
        
        # invincibility timer
        self.vulnerable = True
        self.hit_time = 0
        self.invincibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'idle':[],'move':[],'attack':[]}
        main_path = f'layout_images/monsters/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self,player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]

        if distance <= self.monster_info['attack_radius'] and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
            self.status = 'attack'
        elif distance <= self.monster_info['notice_radius']:
            self.status = 'move'
        else:
            self.status = 'idle'

    def actions(self,player):
        if self.status == 'attack' and self.can_attack and self.vulnerable:
            self.attack_time = pygame.time.get_ticks()
            self.enemy_attack(self.rect.center, self.damage, self.attack_type, self.attack_sound)

        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]
            
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        animation = self.animations[self.status]
		
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':    
                self.revert_after_attack()
                self.can_attack = False
            
            self.frame_index = 0
                
        self.image = animation[int(self.frame_index)].convert_alpha()
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = Settings().wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldown(self):
        current_time = pygame.time.get_ticks()
        if not self.can_attack:
            if current_time - self.attack_time >= self.monster_info['cooldown']:
                self.can_attack = True

        if not self.vulnerable:
            if current_time - self.hit_time >= self.invincibility_duration:
                self.vulnerable = True

    def get_damage(self, damage, player):
        if self.vulnerable:
            player.flame_sound.play()
            self.health -= damage
            self.hit_time = pygame.time.get_ticks()
            if self.check_death(player):
                inc = self.monster_info['health'] // 10
                if player.hsb_width + inc <= player.max_health_storage:
                    player.hsb_width += inc

                exp = self.monster_info['exp']
                player.exp += exp
                player.total_exp += exp

            self.vulnerable = False
                
    def check_death(self, player):
        if self.health <= 0:
            player.killed_enemy += 1
            self.death_sound.play()
            self.trigger_action(self.rect.center, self.monster_name)
            self.trigger_action(player.rect.center, 'heal')

            self.kill()

            return True
        return False
    
    def get_hit_reaction(self):
        if not self.vulnerable:
            self.direction *= -self.push_back

    def revert_after_attack(self):
        if self.direction.magnitude() != 0:
            self.direction *= -self.retreat
        else:
            take_direction = choice(Settings().enemy_revert_directions)
            self.direction = take_direction * -self.retreat
    
    def move(self):
        """Moves the enemy. Checks for collisions and revert. This is the "in the Place" method."""
        
        if self.direction != pygame.math.Vector2():
            self.direction = self.direction.normalize()

        self.hitbox.x+=self.direction.x*self.monster_info['speed']
        self.enemy_collision.collision_of_interactors_with_obstacles(self, 'horizontal', self.obstacle_sprites)

        self.hitbox.y+=self.direction.y*self.monster_info['speed']
        self.enemy_collision.collision_of_interactors_with_obstacles(self, 'vertical', self.obstacle_sprites)    

        self.rect.center = self.hitbox.center

    def update(self):
        self.get_hit_reaction()
        self.cooldown()
        self.move()
        self.animate()
        
    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)


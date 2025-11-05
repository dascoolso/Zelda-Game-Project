import pygame

from settings import Settings
from particles import AnimationEntities
from support import absolute_path
 

class Collision:
    '''Checks collision for game interactors with each other as well as obstacles'''
    def __init__(self):
        '''Just to Remove Grass set the Limit'''
        self.remove_grass_counter = 0

    def collision_of_interactors_with_obstacles(self, interactors: pygame.sprite.Sprite, direction: str, obs_spr: pygame.sprite.Group):
        '''collision with obstacles'''

        for sprite in obs_spr:
                if sprite.hitbox.colliderect(interactors.hitbox):

                    if direction=='horizontal':
                        if interactors.direction.x>0:
                            interactors.hitbox.right = sprite.hitbox.left
                        elif interactors.direction.x<0:
                            interactors.hitbox.left = sprite.hitbox.right

                    elif direction=='vertical':
                        if interactors.direction.y>0:
                            interactors.hitbox.bottom = sprite.hitbox.top
                        elif interactors.direction.y<0:
                            interactors.hitbox.top = sprite.hitbox.bottom

    def player_attack_logic(self, weapon, attackable_sprites: pygame.sprite.Group, player: pygame.sprite.Sprite, visible_sprites: pygame.sprite.Group):
        '''Player Attacking Enemy Logic'''

        if weapon:
            enemy_hit_this_swing = False
            loss = 0

            if type(weapon) is str:
                if weapon == 'flame':
                    damage = Settings().magic_data[weapon]['strength']

                    if player.attacked and player.vulnerable:
                        for sprite in attackable_sprites:
                            if sprite.sprite_type == 'enemy':
                                distance =  sprite.get_player_distance_direction(player)[0]

                                if distance <= player.magic_effect_radius:

                                    enemy_hit_this_swing = True

                                    AnimationEntities().create_particles('flame', sprite.rect.center, visible_sprites)
                                    sprite.get_damage(damage, player)
                                    player.attacked = False

                else:
                    max_health = Settings().player_max_health
                    if player.attacked and player.hsb_width and player.health != max_health:
                        inc = max_health - player.health - player.hsb_width
                        if inc <= 0:
                            player.hsb_width = -inc
                            player.health = max_health

                        else: 
                            player.health += player.hsb_width
                            player.hsb_width = 0

                        enemy_hit_this_swing = True
                        player.heal_sound.play()
                        AnimationEntities().create_particles('aura', player.rect.center, visible_sprites)
                        player.attacked = False

                loss = Settings().magic_data[weapon]['cost']

            else:
                damage = Settings().weapon_data[player.current_weapon]['damage']
                collided_sprites = pygame.sprite.spritecollide(weapon, attackable_sprites, False)

                if collided_sprites:
                    sound = pygame.mixer.Sound(absolute_path(Settings().default_player_stats['hit_sound']))
                    sound.set_volume(Settings().other)
                    sound.play()

                for sprite in collided_sprites:

                    if sprite.sprite_type == 'grass' and self.remove_grass_counter < Settings().can_remove_grass:
                        pos = sprite.rect.center
                        offset = pygame.math.Vector2(0,75)
                        AnimationEntities().create_grass_particles(pos - offset, visible_sprites)
                        sprite.kill()
                        self.remove_grass_counter += 1

                    if sprite.sprite_type == 'enemy':
                        if player.attacked and player.vulnerable:

                            enemy_hit_this_swing = True
                            AnimationEntities().create_particles(player.attack_type, weapon.rect.midtop, visible_sprites)
                            sprite.get_damage(damage, player)
                            loss = Settings().energy_loss_per_swing
                            player.attacked = False
                        
            if enemy_hit_this_swing:
                if player.energy - loss >= 0:
                    player.energy -= loss
                enemy_hit_this_swing = False
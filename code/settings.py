import pygame

from math import sin

class Settings:
    def __init__(self):
        """Static settings to control the whole Game"""

        # Screen settings
        self.width = 1444
        self.height = 720

        # Area of Tiles
        self.area = 64
        self.dimensions=(55, 55)

        # FPS
        self.fps = 60

        # BackGround Color
        self.bg_color_1 = (0, 0, 0)
        self.bg_color_2 = (255, 255, 255)

        # Player Settings
        self.player_dimesions = (48, 48)
        self.default_player_stats = {
            'health': 200, # max: 200
            'energy': 350, # max: 350
            'speed': 5,
            'energy_increment_cooldown': 500,
            'attack_type': 'sparkle', 
            'magic_effect_radius': 100,
            'attack_sound': 'audio/sword.wav',
            'hit_sound': 'audio/hit.wav'
        }
        self.player_max_health = 200
        self.player_max_energy = 350
        self.action_cooldown = 500
        self.weapon_switch_cooldown = 1500
        self.attack=pygame.K_SPACE
        self.magic=pygame.K_LALT
        self.player_energy_increment_amount = 2
        self.energy_loss_per_swing = 10

        # Weapon Details
        self.weapon_data = {
            'sword': {'cooldown': 100, 'damage': 35, 'image': 'layout_images/weapons/sword/full.png'}, 
            'lance': {'cooldown': 400, 'damage': 50, 'image': 'layout_images/weapons/lance/full.png'}, 
            'axe': {'cooldown': 300, 'damage': 40, 'image': 'layout_images/weapons/axe/full.png'}, 
            'rapier': {'cooldown': 50, 'damage': 20, 'image': 'layout_images/weapons/rapier/full.png'}, 
            'sai': {'cooldown': 80, 'damage': 25, 'image': 'layout_images/weapons/sai/full.png'}
        }
        self.axe = pygame.K_a
        self.sword = pygame.K_s
        self.lance = pygame.K_w
        self.rapier = pygame.K_z
        self.sai = pygame.K_d
        self.weapon_switch = pygame.K_LSHIFT

        # UI Settings
        self.player_UI = {
            'health_bar': [(200, 20), (10, 10), "#7C7C7C", "#303030", -1],
            'hb_color': ("#4dca44", "#FF8000", "#d10404", "#FEE01C", "#790000E1"),
            'energy_bar': [(350, 20), (10, 35), "#DDECF1", "#303030", -1],
            'eb_color': ("#7aa9ec", "#006AFF", '#00008B', "#DBF3FF", "#010153DF"),
            'experience_square': [(self.width-20, self.height-20), "#353535", "#FF9B29"],
            'weapon_and_magic': [72, 20, self.height-20-72, "#353535", "#FFFFFF", "#FFD900"]
        }
        self.glow_activated=350

        # Magic Data
        self.magic_data = {
            'flame': {'strength': 5, 'cost': 10, 'image': 'layout_images/particles/flame/fire.png', 'sound': 'audio/flame.wav'},
            'heal': {'strength': 20, 'cost': 30, 'image': 'layout_images/particles/heal/heal.png', 'sound': 'audio/heal.wav'}
        }
        self.flame = pygame.K_f
        self.heal = pygame.K_x
        self.magic_switch = pygame.K_LCTRL
        self.magic_switch_cooldown=500
        self.health_storage_bar = {
            'position': (20, 60),
            'color': "#F722AC", 
            'border_color': "#000000",
            'max_storage': 75,
            'height': 10
        }
        self.transformed_image_dimensions = (56, 56)

        # Enemy Details
        self.monster_data = {
	        'squid': {'health': 100,'cooldown':600,'damage':20,'attack_type': 'slash', 'attack_sound': 'audio/attack/slash.wav', 'speed': 3, 'retreat': 3, 'attack_radius': 80, 'notice_radius': 360, 'exp': 30},
	        'raccoon': {'health': 300,'cooldown':1250,'damage':40,'attack_type': 'claw',  'attack_sound': 'audio/attack/claw.wav','speed': 2, 'retreat': 3, 'attack_radius': 120, 'notice_radius': 400, 'exp': 80},
	        'spirit': {'health': 100,'cooldown':445,'damage':8,'attack_type': 'thunder', 'attack_sound': 'audio/attack/fireball.wav', 'speed': 4, 'retreat': 3, 'attack_radius': 60, 'notice_radius': 350, 'exp': 15},
	        'bamboo': {'health': 70,'cooldown':750,'damage':6,'attack_type': 'leaf_attack', 'attack_sound': 'audio/attack/slash.wav', 'speed': 3, 'retreat': 3, 'attack_radius': 50, 'notice_radius': 300, 'exp': 10},
            'push_back': 5
        }
        self.monsters_ui = {
            'squid': {'health': 75, 'energy': 80, 'hb_color': "#B00202"},
            'raccoon': {'health': 250, 'energy': 300, 'hb_color': "#1F0032"},
            'spirit': {'health': 75, 'energy': 80, 'hb_color': "#8202B0"},
            'bamboo': {'health': 75, 'energy': 80, 'hb_color': "#257901"}
        }

        self.can_remove_grass = 10
        self.enemy_revert_directions = [
                pygame.math.Vector2(1, 0), 
                pygame.math.Vector2(0, 1), 
                pygame.math.Vector2(-1, 0), 
                pygame.math.Vector2(0, -1)
            ]
        
        # Sound Volume
        self.main_sound = 0.3
        self.other = 0.5

        # End Screen
        self.scale_factor = 3
        self.left_gap = 60
        
    
    def wave_value(self):
        value = sin(pygame.time.get_ticks())
        if value >= 0:
            return 255
        
        return 0
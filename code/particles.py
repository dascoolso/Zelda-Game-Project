import pygame

from support import import_folder
from random import choice

class AnimationEntities:
    def __init__(self):
        self.frames = {
			# magic
			'flame': import_folder('layout_images/particles/flame/frames'),
			'aura': import_folder('layout_images/particles/aura'),
			'heal': import_folder('layout_images/particles/heal/frames'),
			
			# attacks 
			'claw': import_folder('layout_images/particles/claw'),
			'slash': import_folder('layout_images/particles/slash'),
			'sparkle': import_folder('layout_images/particles/sparkle'),
			'leaf_attack': import_folder('layout_images/particles/leaf_attack'),
			'thunder': import_folder('layout_images/particles/thunder'),

			# monster deaths
			'squid': import_folder('layout_images/particles/smoke_orange'),
			'raccoon': import_folder('layout_images/particles/raccoon'),
			'spirit': import_folder('layout_images/particles/nova'),
			'bamboo': import_folder('layout_images/particles/bamboo'),
			
			# leafs 
			'leaf': (
				import_folder('layout_images/particles/leaf1'),
				import_folder('layout_images/particles/leaf2'),
				import_folder('layout_images/particles/leaf3'),
				import_folder('layout_images/particles/leaf4'),
				import_folder('layout_images/particles/leaf5'),
				import_folder('layout_images/particles/leaf6'),
				self.reflect_images(import_folder('layout_images/particles/leaf1')),
				self.reflect_images(import_folder('layout_images/particles/leaf2')),
				self.reflect_images(import_folder('layout_images/particles/leaf3')),
				self.reflect_images(import_folder('layout_images/particles/leaf4')),
				self.reflect_images(import_folder('layout_images/particles/leaf5')),
				self.reflect_images(import_folder('layout_images/particles/leaf6'))
				)
			}
        
    def reflect_images(self,frames):
        new_frames = []

        for frame in frames:
            flipped_frame = pygame.transform.flip(frame,True,False)
            new_frames.append(flipped_frame)
        return new_frames
    
    def create_grass_particles(self, pos, group): 
        '''Spawn After a Grass is killed'''
        animation_frames = self.frames['leaf'][choice(range(11))]
        pos[1] -= 75
        ParticlesEffect(pos, animation_frames, group)
    
    def create_particles(self, type, pos, group): 
        '''Deployed under certain Actions'''
        animation_frames = self.frames[type]
        ParticlesEffect(pos, animation_frames, group)

class ParticlesEffect(pygame.sprite.Sprite):
    def __init__(self, pos, animation_frames, group):
        super().__init__(group)
        self.frame_index = 0
        self.animation_speed = 0.15
        self.frames = animation_frames
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)

    def animate(self):
        self.frame_index += self.animation_speed
        if self.frame_index >= len(self.frames):
            self.kill()
        else:
            self.image = self.frames[int(self.frame_index)]

    def update(self):
        self.animate()
        
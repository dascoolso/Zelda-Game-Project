import pygame, sys

from settings import Settings
from level import Level
from support import absolute_path

class Game:
    def __init__(self):
        """Getting all the Features, Assembling Everyone"""
        pygame.init()

        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.width, self.settings.height))
        pygame.display.set_caption("Zelda") 
        pygame.display.set_icon(pygame.image.load('Zelda Logo.ico'))
        self.clock = pygame.time.Clock()
        
        self.main_sound = pygame.mixer.Sound(absolute_path('audio/main.ogg'))
        self.main_sound.set_volume(self.settings.main_sound)
        self.main_sound.play(-1)
        
        self.level = Level(self)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    sys.exit("\nExited from the Game\n")

            self.screen.fill(self.settings.bg_color_1)
            self.level.run()
            pygame.display.flip()
            self.clock.tick(self.settings.fps)        

if __name__ == '__main__':
    game = Game()
    game.run()
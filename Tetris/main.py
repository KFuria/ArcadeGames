import pygame
import sys, random

from settings import Settings
from tetris import *

class Main:
    '''Overall class to manage game assets and behavior'''
    
    def __init__(self):
        '''Initialize the game, and create game resources'''
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(Settings.screen_size)
        pygame.display.set_caption("Tetris")
        
        self.game = Tetris()       
   
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
    
    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            self.game.move_right()
        elif event.key == pygame.K_LEFT:
            self.game.move_left()
        elif event.key == pygame.K_DOWN:
            self.game.move_down()

    def run(self):
        '''Start game loop'''
        while True:
            self._check_events()
            self.game.draw_screen(self.screen)
            pygame.display.flip()
            self.clock.tick(25)
            
            
if __name__ == '__main__':
    game = Main()
    game.run()
    

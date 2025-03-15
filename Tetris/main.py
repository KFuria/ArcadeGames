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
        
        # initialize game
        self.game = Tetris()
        
        # setup screen
        self.screen = pygame.display.set_mode(Settings.screen_size)
        pygame.display.set_caption("Tetris")
        
        self.title_font = pygame.font.Font(Settings.font_path, Settings.title_font_size)
        self.title_surface = self.title_font.render("Tetris", True, Settings.title_font_color)
        
        self.text_font = pygame.font.Font(Settings.font_path, Settings.text_font_size)
        self.score_surface = self.text_font.render("Score", True, Settings.text_font_color)
        self.next_surface = self.text_font.render("Next Shape", True, Settings.text_font_color)
        
        self.game_over_font = pygame.font.Font(Settings.font_path, Settings.game_over_font_size)
        self.game_over_surface = self.game_over_font.render("Game Over!", True, Settings.text_font_color)
        
        self.reset_font = pygame.font.Font(Settings.font_path, Settings.reset_font_size)
        self.reset_surface = self.reset_font.render("Press r to reset the game", True, Settings.text_font_color)
        
        self.score_rect = pygame.Rect(Settings.score_rect_pos_size)
        self.next_rect = pygame.Rect(Settings.next_rect_pos_size)
        
        # event to move block in game
        self.game_update = pygame.USEREVENT
        pygame.time.set_timer(self.game_update, Settings.game_speed)
        
               
                       
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == self.game_update and self.game.game_over == False and self.game.game_pause == False:
                self.game.move_down()
    
    def _check_keydown_events(self, event):
        """Respond to keypresses"""
        if event.key == pygame.K_RIGHT and self.game.game_over == False and self.game.game_pause == False:
            self.game.move_right()
        elif event.key == pygame.K_LEFT and self.game.game_over == False and self.game.game_pause == False:
            self.game.move_left()
        elif event.key == pygame.K_DOWN and self.game.game_over == False and self.game.game_pause == False:
            self.game.move_down()
            self.game.update_score(0, 1)
        elif event.key == pygame.K_UP and self.game.game_over == False and self.game.game_pause == False:
            self.game.rotate()
        elif event.key == pygame.K_r and self.game.game_over == True:
            self.game.game_over = False
            self.game.reset()
        elif event.key == pygame.K_p and self.game.game_over == False:
            self.game.game_pause = True
        elif event.key == pygame.K_c and self.game.game_over == False:
            self.game.game_pause = False
    
    def display_title_score_next(self):
        # title
        self.screen.blit(self.title_surface, Settings.title_surface_dest)
        # score
        self.screen.blit(self.score_surface, Settings.score_surface_dest)
        pygame.draw.rect(self.screen, Settings.score_rect_color, self.score_rect, 0, 12)
        
        self.score_value_surface = self.text_font.render(str(self.game.score), True, Settings.text_font_color)
        self.screen.blit(self.score_value_surface, self.score_value_surface.get_rect(centerx = self.score_rect.centerx, 
                                                                                     centery = self.score_rect.centery))
        #next
        self.screen.blit(self.next_surface, Settings.next_surface_dest)
        pygame.draw.rect(self.screen, Settings.next_rect_color, self.next_rect, 0, 20)

        if self.game.game_over == True:
            self.screen.blit(self.game_over_surface, Settings.game_over_dest)
            self.screen.blit(self.reset_surface, Settings.reset_surface_dest)
            
    def run(self):
        '''Start game loop'''
        while True:
            self._check_events()
            self.screen.fill(Settings.black)
            self.display_title_score_next()
            self.game.draw_screen(self.screen)
            pygame.display.flip()
            self.clock.tick(25)
            
            
if __name__ == '__main__':
    game = Main()
    game.run()
    

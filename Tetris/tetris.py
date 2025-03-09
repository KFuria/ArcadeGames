import pygame, random
import numpy as np
from collections import namedtuple
from settings import Settings

class Tetris: 
    def __init__(self):
        self.board = Board()
        self.shapes = [LShape(), JShape(), IShape(), OShape(), SShape(), TShape(), ZShape()]
        self.current_shape = self.get_random_shape()
        self.next_shape = self.get_random_shape()
        
    def get_random_shape(self):
        if len(self.shapes) == 0:
            self.shapes = [LShape(), JShape(), IShape(), OShape(), SShape(), TShape(), ZShape()]
        shape = random.choice(self.shapes)
        self.shapes.remove(shape)
        return shape
    
    def is_inside(self, row, col):
        if row >=1 and row < (Settings.board_height + 1) and col >=1 and col < (Settings.board_width + 1):
            return True
        return False
    
    def shape_inside(self):
        tiles = self.current_shape.get_shape_pos()
        for tile in tiles:
            if self.is_inside(tile.row + 1, tile.col + 1) == False:
                return False
        return True
                  
    def move_left(self):
        self.current_shape.move(0, -1)
        if self.shape_inside() == False:
            self.current_shape.move(0, 1)
        
    def move_right(self):
        self.current_shape.move(0, 1)
        if self.shape_inside() == False:
            self.current_shape.move(0, -1)
        
    def move_down(self):
        self.current_shape.move(1, 0)
        if self.shape_inside() == False:
            self.current_shape.move(-1, 0)
        
    def draw_screen(self, screen):
        self.board.draw(screen)
        self.current_shape.draw(screen)

class Board:
    '''Class for the game board'''
    def __init__(self):
        self.colors = Settings._get_color()
        self.matrix = [[0 if x in range(1, Settings.board_width + 1) else -1 \
            for x in range(Settings.board_width + 2)] \
            if y in range(1, Settings.board_height + 1) else [-1 for x in range(Settings.board_height + 2)] 
            for y in range(Settings.board_height + 2)]
        
    def draw(self, screen):
        '''Draw game board'''
        blocksize = Settings.board_blocksize
        x_offset = Settings.board_x_offset
        y_offset = Settings.board_y_offset
        for y in range(0, Settings.board_height+2):
            for x in range(0, Settings.board_width+2):
                rect = pygame.Rect(x_offset + x * blocksize, y_offset + y * blocksize, blocksize-1, blocksize-1)
                pygame.draw.rect(screen, self.colors[self.matrix[y][x]], rect)
        
                          
class Shape:
    '''Class to represent a general shape'''
    def __init__(self, id):
        self.id = id
        self.blocks = {}
        self.rotation = 0
        self.colors = Settings._get_color()
        self.blocksize = Settings.board_blocksize
        self.x_offset = Settings.board_x_offset
        self.y_offset = Settings.board_y_offset
        self.pos = namedtuple('pos', ['row', 'col'])
        self.row_offset = 0
        self.col_offset = 0
        
    def move(self, rows, cols):
        self.row_offset += rows
        self.col_offset += cols
        
    def get_shape_pos(self):
        tiles = self.blocks[self.rotation]
        moved_tiles = []
        for tile in tiles:
            pos = self.pos(tile.row + self.row_offset, tile.col + self.col_offset)
            moved_tiles.append(pos)
        return moved_tiles
            
    def draw(self, screen):
        '''Draw shape on screen'''
        tiles = self.get_shape_pos()
        for tile in tiles:
            rect = pygame.Rect((tile.col + 1) * self.blocksize + self.x_offset, \
                               (tile.row + 1) * self.blocksize + self.y_offset, self.blocksize - 1, self.blocksize - 1)
            pygame.draw.rect(screen, self.colors[self.id], rect)
    
class LShape(Shape):
    '''Class for L shape Tetromino '''
    def __init__(self):
        super().__init__(id = 1)
        self.blocks = {
            0: [self.pos(0,2), self.pos(1,0), self.pos(1,1), self.pos(1,2)],
            1: [self.pos(0,1), self.pos(1,1), self.pos(2,1), self.pos(2,2)],
            2: [self.pos(1,0), self.pos(1,1), self.pos(1,2), self.pos(2,0)],
            3: [self.pos(0,0), self.pos(0,1), self.pos(1,1), self.pos(2,1)]
        }
        self.move(0,3)

class JShape(Shape):
    '''Class for J shape Tetromino'''
    def __init__(self):
        super().__init__(id = 2)
        self.blocks = {
            0: [self.pos(0,0), self.pos(1,0), self.pos(1,1), self.pos(1,2)],
            1: [self.pos(0,1), self.pos(0,2), self.pos(1,1), self.pos(2,1)],
            2: [self.pos(1,0), self.pos(1,1), self.pos(1,2), self.pos(2,2)],
            3: [self.pos(0,1), self.pos(1,1), self.pos(2,0), self.pos(2,1)]
        }
        self.move(0,3)
        
class IShape(Shape):
    '''Class for I shape Tetromino'''
    def __init__(self):
        super().__init__(id = 3)
        self.blocks = {
            0: [self.pos(1,0), self.pos(1,1), self.pos(1,2), self.pos(1,3)],
            1: [self.pos(0,2), self.pos(1,2), self.pos(2,2), self.pos(3,2)],
            2: [self.pos(2,0), self.pos(2,1), self.pos(2,2), self.pos(2,3)],
            3: [self.pos(0,1), self.pos(1,1), self.pos(2,1), self.pos(3,1)]
        }
        self.move(-1,3)

class OShape(Shape):
    '''Class for O shape Tetromino'''
    def __init__(self):
        super().__init__(id = 4)
        self.blocks = {
            0: [self.pos(0,0), self.pos(0,1), self.pos(1,0), self.pos(1,1)]
        }
        self.move(0,4)
        
class SShape(Shape):
    '''Class for S shape Tetromino'''
    def __init__(self):
        super().__init__(id = 5)
        self.blocks = {
            0: [self.pos(0,1), self.pos(0,2), self.pos(1,0), self.pos(1,1)],
            1: [self.pos(0,1), self.pos(1,1), self.pos(1,2), self.pos(2,2)],
            2: [self.pos(1,1), self.pos(1,2), self.pos(2,0), self.pos(2,1)],
            3: [self.pos(0,0), self.pos(1,0), self.pos(1,1), self.pos(2,1)]
        }
        self.move(0,3)
        
class TShape(Shape):
    '''Class for T shape Tetromino'''
    def __init__(self):
        super().__init__(id = 6)
        self.blocks = {
            0: [self.pos(0,1), self.pos(1,0), self.pos(1,1), self.pos(1,2)],
            1: [self.pos(0,1), self.pos(1,1), self.pos(1,2), self.pos(2,1)],
            2: [self.pos(1,0), self.pos(1,1), self.pos(1,2), self.pos(2,1)],
            3: [self.pos(0,1), self.pos(1,0), self.pos(1,1), self.pos(2,1)]
        }
        self.move(0,3)

class ZShape(Shape):
    '''Class for Z shape Tetromino'''
    def __init__(self):
        super().__init__(id = 7)
        self.blocks = {
            0: [self.pos(0,0), self.pos(0,1), self.pos(1,1), self.pos(1,2)],
            1: [self.pos(0,2), self.pos(1,1), self.pos(1,2), self.pos(2,1)],
            2: [self.pos(1,0), self.pos(1,1), self.pos(2,1), self.pos(2,2)],
            3: [self.pos(0,1), self.pos(1,0), self.pos(1,1), self.pos(2,0)]
        }
        self.move(0,3)
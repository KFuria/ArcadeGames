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
        self.game_over = False
        self.game_pause = False
        self.lines_cleared = 0
        self.score = 0
    
    def update_score(self, lines_cleared, move_down_points):
        if lines_cleared == 1:
            self.score += 100
        elif lines_cleared == 2:
            self.score += 300
        elif lines_cleared == 3:
            self.score += 500
        self.score += move_down_points
        
    def get_random_shape(self):
        if len(self.shapes) == 0:
            self.shapes = [LShape(), JShape(), IShape(), OShape(), SShape(), TShape(), ZShape()]
        shape = random.choice(self.shapes)
        self.shapes.remove(shape)
        return shape
    
    def is_inside(self, row, col):
        if row >=0 and row < Settings.board_height and col >=0 and col < Settings.board_width:
            return True
        return False
    
    def shape_inside(self):
        tiles = self.current_shape.get_shape_pos()
        for tile in tiles:
            if self.is_inside(tile.row, tile.col) == False:
                return False
        return True
                  
    def move_left(self):
        self.current_shape.move(0, -1)
        if self.shape_inside() == False or self.block_fits() == False:
            self.current_shape.move(0, 1)
        
    def move_right(self):
        self.current_shape.move(0, 1)
        if self.shape_inside() == False or self.block_fits() == False:
            self.current_shape.move(0, -1)
        
    def move_down(self):
        self.current_shape.move(1, 0)
        if self.shape_inside() == False or self.block_fits() == False:
            self.current_shape.move(-1, 0)
            self.freeze()
            
    def rotate(self):
        self.current_shape.rotate()
        if self.shape_inside() == False or self.block_fits() == False:
            self.current_shape.undo_rotate()
    
    def freeze(self):
        tiles = self.current_shape.get_shape_pos()
        for tile in tiles:
            self.board.matrix[tile.row][tile.col] = self.current_shape.id
        self.current_shape = self.next_shape
        self.next_shape = self.get_random_shape()
        lines_cleared = self.board.clear_completed_rows()
        self.update_score(lines_cleared, 0)
        if self.block_fits() == False:
            self.game_over = True
        
    def block_fits(self):
        tiles = self.current_shape.get_shape_pos()
        for tile in tiles:
            if self.board.is_block_empty(tile.row, tile.col) == False:
                return False
        return True
        
    def draw_screen(self, screen):
        self.board.draw_board(screen)
        self.current_shape.draw(screen)
        self.board.draw_border(screen)
        if self.next_shape.id == 3:
            self.next_shape.draw_next_shape(screen, *Settings.next_shape_pos_3_4)
        elif self.next_shape.id == 4:
            self.next_shape.draw_next_shape(screen, *Settings.next_shape_pos_3_4)
        else:
            self.next_shape.draw_next_shape(screen, *Settings.next_shape_pos)

    def reset(self):
        self.game_pause = False
        self.board.reset()
        self.shapes = [LShape(), JShape(), IShape(), OShape(), SShape(), TShape(), ZShape()]
        self.current_shape = self.get_random_shape()
        self.next_shape = self.get_random_shape()
        self.score = 0
                

class Board:
    '''Class for the game board'''
    def __init__(self):
        self.colors = Settings._get_color()
        self.matrix = [[0 for x in range(Settings.board_width)] for y in range(Settings.board_height)]
        self.border = [[0 for x in range(Settings.board_width)] for y in range(Settings.board_height-1)]
        self.border = np.pad(self.border, pad_width=1, constant_values=1)
    
    def display_matrix(self):
        for y in range(Settings.board_height):
            for x in range(Settings.board_width):
                print(self.matrix[y][x], end = " ")
            print()
            
    def is_block_empty(self, row, col):
        if self.matrix[row][col] == 0:
            return True
        return False
    
    def is_row_completed(self, row):
        if 0 in self.matrix[row][:]:
            return False
        return True
    
    def clear_row(self, row):
        self.matrix[row][:] = [0]*Settings.board_width
            
    def move_row_down(self, row, num_rows):
        self.matrix[row+num_rows][:] = self.matrix[row][:]
        self.matrix[row][:] = [0]*Settings.board_width
    
    def clear_completed_rows(self):
        completed_rows = 0
        for row in range(Settings.board_height - 1, 0, -1):
            if self.is_row_completed(row):
                self.clear_row(row)
                completed_rows += 1
            elif completed_rows > 0:
                self.move_row_down(row, completed_rows)
        return completed_rows
              
    def draw_board(self, screen):
        '''Draw game board'''
        blocksize = Settings.board_blocksize
        x_offset = Settings.board_x_offset
        y_offset = Settings.board_y_offset
        # draw board
        for y in range(Settings.board_height):
            for x in range(Settings.board_width):
                rect = pygame.Rect(x_offset + x * blocksize, y_offset + y * blocksize, blocksize-1, blocksize-1)
                pygame.draw.rect(screen, self.colors[self.matrix[y][x]], rect)
    
    def draw_border(self, screen):
        '''Draw game board border'''
        blocksize = Settings.board_blocksize
        border_x_offset = Settings.board_x_offset - blocksize
        border_y_offset = Settings.board_y_offset
        # draw border
        for y in range(Settings.board_height+1):
            for x in range(Settings.board_width+2):
                if self.border[y][x] == 1:
                    rect = pygame.Rect(border_x_offset + x * blocksize, border_y_offset + y * blocksize, blocksize-1, blocksize-1)
                    pygame.draw.rect(screen, Settings.border_color, rect) 
    
    def reset(self):
        self.matrix = [[0 for x in range(Settings.board_width)] for y in range(Settings.board_height)]
        self.completed_rows = 0
        
                        
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
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.blocks)
        
    def undo_rotate(self):
        self.rotation = (self.rotation - 1) % len(self.blocks)
        
    def get_shape_pos(self):
        tiles = self.blocks[self.rotation]
        moved_tiles = []
        for tile in tiles:
            pos = self.pos(tile.row + self.row_offset, tile.col + self.col_offset)
            moved_tiles.append(pos)
        return moved_tiles
            
    def draw(self, screen):
        '''Draw current shape on screen'''
        tiles = self.get_shape_pos()
        for tile in tiles:
            rect = pygame.Rect((tile.col) * self.blocksize + self.x_offset, \
                               (tile.row) * self.blocksize + self.y_offset, self.blocksize - 1, self.blocksize - 1)
            pygame.draw.rect(screen, self.colors[self.id], rect)
    
    def draw_next_shape(self, screen, x_offset, y_offset):
        '''Draw next shape on screen'''
        tiles = self.get_shape_pos()
        for tile in tiles:
            rect = pygame.Rect((tile.col) * self.blocksize + x_offset - 1, \
                               (tile.row) * self.blocksize + y_offset - 1, self.blocksize+1, self.blocksize+1)
            pygame.draw.rect(screen, Settings.black, rect)
            rect = pygame.Rect((tile.col) * self.blocksize + x_offset, \
                               (tile.row) * self.blocksize + y_offset, self.blocksize - 1, self.blocksize - 1)
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
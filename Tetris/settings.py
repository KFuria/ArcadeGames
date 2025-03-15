class Settings:
    '''A class to store all game settings'''
    screen_size = (770, 770)
    board_x_offset = 35
    board_y_offset = 0
    board_blocksize = 35
    board_height = 21
    board_width = 10

    font_path = 'Fonts/BrokenConsole.ttf'
    
    title_font_size = 50
    title_font_color = (242,240,239)
    title_surface_dest = (510, 50)
    
    text_font_size = 25
    text_font_color = (242,240,239)
    
    score_surface_dest = (560, 150)
    score_rect_pos_size = (550, 185, 100, 60)
    score_rect_color = (102, 97, 94)
    
    next_surface_dest = (520, 300)
    next_rect_pos_size = (500, 335, 210, 140)
    next_rect_color = (102, 97, 94)
    next_shape_pos = (445, 370)
    next_shape_pos_3_4 = (430, 370)
    
    game_over_font_size = 40
    game_over_dest = (480, 520)
    reset_font_size = 15
    reset_surface_dest = (490, 580)    
        
    game_speed = 250
    
    # Tetromino Colors
    black = (0, 0, 0)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    
    border_color = (201,200,199)
    
    @classmethod
    def _get_color(cls):
        return [cls.black, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue]
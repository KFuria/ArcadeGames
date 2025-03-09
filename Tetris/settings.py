class Settings:
    '''A class to store all game settings'''
    screen_size = (900, 900)
    board_x_offset = 100
    board_y_offset = 65
    board_blocksize = 35
    board_height = 20
    board_width = 10
    
    # Colors
    black = (0, 0, 0)
    green = (47, 230, 23)
    red = (232, 18, 18)
    orange = (226, 116, 17)
    yellow = (237, 234, 4)
    purple = (166, 0, 247)
    cyan = (21, 204, 209)
    blue = (13, 64, 216)
    dark_grey = (127,127,127)
        
    @classmethod
    def _get_color(cls):
        return [cls.black, cls.green, cls.red, cls.orange, cls.yellow, cls.purple, cls.cyan, cls.blue, cls.dark_grey]
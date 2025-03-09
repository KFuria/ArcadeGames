

class Shape:
    '''Class to represent a general shape'''
    def __init__(self, id):
        self.id = id
        self.blocks = {}
        self.blocksize = 35
        self.rotation = 0

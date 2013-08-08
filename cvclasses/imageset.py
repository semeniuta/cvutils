# -*- coding: utf-8 -*-

class CalibrationImageSet:
    def __init__(self, name, imagemask, pattern_size, square_size):
        self.name = name        
        self.imagemask = imagemask
        self.pattern_size = pattern_size
        self.square_size = square_size
        
    def get_tuple(self):
        return (self.imagemask, self.pattern_size, self.square_size, self.name)
        
    def __str__(self):
        return 'CalibrationImageSet %s (%s)' % (self.name, self.imagemask)
         
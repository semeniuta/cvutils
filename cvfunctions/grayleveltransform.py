# -*- coding: utf-8 -*-

def invert(image):
    return 255 - image
    
def clamp(image, a, b):
    interval_len = b - a    
    return (interval_len/255) * image + a
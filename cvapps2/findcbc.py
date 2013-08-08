# -*- coding: utf-8 -*-

import cv2
from cvfunctions import chessboard

flags_sets = {
    'default': cv2.CALIB_CB_ADAPTIVE_THRESH + cv2.CALIB_CB_NORMALIZE_IMAGE, 
    'adtresh_or_filquads': cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS    
}

def open_images_and_find_corners(imset1, imset2, findcbc_flags):
    mask_left = imset1.imagemask
    mask_right = imset2.imagemask
    pattern_size = imset1.pattern_size
    return chessboard.open_images_and_find_corners_universal(mask_left, pattern_size, mask_right, findcbc_flags)
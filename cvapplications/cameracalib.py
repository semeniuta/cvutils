# -*- coding: utf-8 -*-

'''
This module contain functions for simple camera calibration tasks
such as calibration a camera using a predefined set of images

@author: Oleksandr Semeniuta
'''

from cvfunctions import chessboard
from cvfunctions import calibration

def calibrate_camera(imageset, findcbc_flags):
    
    corners, images, filenames = chessboard.open_images_and_find_corners_universal(imageset.imagemask, imageset.pattern_size, findcbc_flags=findcbc_flags)
    calib_res = calibration.calibrate_camera(images, imageset.pattern_size, imageset.square_size, corners)
    rms, camera_matrix, dist_coefs = calib_res[:3]
    return rms, camera_matrix, dist_coefs
    
    
    
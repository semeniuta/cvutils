# -*- coding: utf-8 -*-

'''
Script that merges two rectified images of chessboard and draws lines 
that verify row-alignment of the images
'''

import cv2
import os
from cvfunctions import output, images, chessboard
import numpy as np
from cvapplications.confmanager import ConfigManager

cm = ConfigManager()

stereo_dir = cm.get_pyramid_parameters()['stereo_dir']
img_dir = os.path.join(stereo_dir, 'rectified_images')
pattern_size = (10, 8)

n = 1   
im1 = images.open_image(os.path.join(img_dir, '%d_0.jpg' % n))
im2 = images.open_image(os.path.join(img_dir, '%d_1.jpg' % n))

im_c = np.concatenate((im1, im2), axis=1)

output.plot_image(im_c)

f = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS
res = chessboard.chessboard_corners_maxtrix_to_lists(chessboard.find_chessboard_corners([im1], pattern_size, findcbc_flags=f)[0][1])

output.plot_points(res[0], res[1])

y_list = res[1]
rows = pattern_size[0]
for i in range(0, len(y_list), rows):
    y = res[1][i]
    output.draw_horizontal_line(y)
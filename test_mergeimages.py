# -*- coding: utf-8 -*-

import cv2
import os
from cvfunctions import output, images, chessboard
import numpy as np

left_dir = r'D:\Dropbox\SINTEF\rectified\2013-08-01_143421_LEFT'
right_dir = r'D:\Dropbox\SINTEF\rectified\2013-08-01_143421_RIGHT'
pattern_size = (10, 8)

n = 11   
im1 = images.open_image(os.path.join(left_dir, '%d.jpg' % n))
im2 = images.open_image(os.path.join(right_dir, '%d.jpg' % n))

im_c = np.concatenate((im1, im2), axis=1)

output.plot_image(im_c)

f = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS
res = chessboard.chessboard_corners_maxtrix_to_lists(chessboard.find_chessboard_corners([im1], pattern_size, f)[0][1])

output.plot_points(res[0], res[1])

y_list = res[1]
rows = pattern_size[0]
for i in range(0, len(y_list), rows):
    y = res[1][i]
    output.draw_horizontal_line(y)
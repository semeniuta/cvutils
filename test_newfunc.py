# -*- coding: utf-8 -*-

from params import ImageSets
from cvfunctions import chessboard
import cv2

imageset = ImageSets.raufoss_set2_left

mask = imageset[0]
pattern_size = imageset[1]

f = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS 
res1 = chessboard.open_images_and_find_corners(mask, pattern_size, findcbc_flags=f)

res2 = chessboard.open_images_and_find_corners_universal(mask, pattern_size, findcbc_flags=f)

size1 = len(res1[0])
size2 = len(res2[0])

print size1, size2

im1 = res1[1]
im2 = res2[1]
for i in range(size1):
    a = (res1[0][i][1] == res2[0][i][1]).all()     
    b = (res1[1][i] == res2[1][i]).all()     
    print a, b
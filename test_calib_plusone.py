# -*- coding: utf-8 -*-

import cv2
from cvfunctions import calibration, chessboard
from cvapplications.confmanager import ConfigManager

cm = ConfigManager()

imageset = cm.get_chessboard_imageset('raufoss_set2_left')
images_mask, pattern_size, square_size, experiment_name = imageset.get_tuple()

'''
Using the following flags
(see: http://answers.opencv.org/question/15438/findchessboardcorners-is-not-working-for/)
'''
f = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS
corners, images = chessboard.open_images_and_find_corners(images_mask, pattern_size, f)

print len(images)

im1 = images[:20]
im2 = images[:21]
cor1 = corners[:20]
cor2 = corners[:21]

res1 = calibration.calibrate_camera(im1, pattern_size, square_size, cor1)
res2 = calibration.calibrate_camera(im2, pattern_size, square_size, cor2)

print res1[1:3]
print res2[1:3]

#images = open_images_from_mask(images_mask)
#corners = chessboard.find_chessboard_corners(images, pattern_size)


# -*- coding: utf-8 -*-

from cvfunctions import images, chessboard
import cv2

img_filename = r'D:\Dropbox\SINTEF\img\new\Camera1-2\20130731130339.bmp'

img = images.open_image(img_filename)
pattern_size = (10, 8)

f = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS
res = cv2.findChessboardCorners(img, pattern_size, flags=f)

chessboard.plot_corners(img, res)

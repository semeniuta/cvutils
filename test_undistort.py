# -*- coding: utf-8 -*-

from params import ImageSets, Directories
from cvfunctions import images as im
from cvfunctions import chessboard
from cvfunctions import calibration
from cvfunctions import transform
from cvfunctions import output
import os
import time
import cv2
import numpy as np

def test_undistort_images(images, intrinsics, save=True):
    images_undist = transform.undistort_images(images, intrinsics)
    
    if save == True:
        timelabel = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        savedir = os.path.join(Directories.undistortion_test, timelabel)
        im.save_images_to_dir(images, savedir, '%d_0.jpg')
        im.save_images_to_dir(images_undist, savedir, '%d_1.jpg')
    
    return images_undist
    
if __name__ == '__main__':
    imageset = ImageSets.opencv_sample_left

    pattern_size = imageset[1]
    square_size = imageset[2]
    
    images = im.open_images_from_mask(imageset[0])
    corners = chessboard.find_chessboard_corners(images, pattern_size)
    corners, images = chessboard.filter_chessboard_corners_results(corners, images)
    intrinsics = calibration.calibrate_camera(images, pattern_size, square_size, corners)[1:3]
    cm, dc = intrinsics

    images_undist = test_undistort_images(images, intrinsics, save=False)
    
    corners_undist = transform.undistort_chessboard_corners(corners, intrinsics)
    
    output.plot_image(images_undist[0])
    x, y = chessboard.chessboard_corners_maxtrix_to_lists(corners_undist[0][1])
    output.plot_points(x, y)
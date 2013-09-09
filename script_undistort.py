# -*- coding: utf-8 -*-

'''
Script that computes camera intrinsics parameters
and undistorts the input images
'''

from cvfunctions import images as im
from cvfunctions import chessboard
from cvfunctions import calibration
from cvfunctions import transform
from cvfunctions import output
from cvapplications.confmanager import ConfigManager
import os
import time

cm = ConfigManager()

def test_undistort_images(images, intrinsics, save=True):
    images_undist = transform.undistort_images(images, intrinsics)
    
    if save == True:
        timelabel = time.strftime('undistort_%Y-%m-%d_%H%M%S', time.localtime(time.time()))
        savedir = os.path.join(cm.get_root_directory(), timelabel)
        im.save_images_to_dir(images, savedir, '%d_0.jpg')
        im.save_images_to_dir(images_undist, savedir, '%d_1.jpg')
    
    return images_undist
    
if __name__ == '__main__':
    imageset = cm.get_chessboard_imageset('opencv_sample_left')

    images = im.open_images_from_mask(imageset.imagemask)
    corners = chessboard.find_chessboard_corners(images, imageset.pattern_size)
    corners, images = chessboard.filter_chessboard_corners_results(corners, images)
    intrinsics = calibration.calibrate_camera(images, imageset.pattern_size, imageset.square_size, corners)[1:3]
    camera_matrix, dc = intrinsics

    images_undist = test_undistort_images(images, intrinsics, save=True)
    
    corners_undist = transform.undistort_chessboard_corners(corners, intrinsics)
    
    output.plot_image(images_undist[0])
    x, y = chessboard.chessboard_corners_maxtrix_to_lists(corners_undist[0][1])
    output.plot_points(x, y)
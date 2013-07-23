# -*- coding: utf-8 -*-

import cPickle as pickle
from params import DataDirs, ImageSets
from cvhelpers import stereovision as sv
from cvhelpers import images
from cvhelpers import chessboard
import os
import cv2

def unpickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data
    
if __name__ == '__main__':
    
    imageset_left = ImageSets.new_set_1
    imageset_right = ImageSets.new_set_2
    
    print 'Opening images'    
    images_left = images.open_images_from_mask(imageset_left[0])[:20]
    images_right = images.open_images_from_mask(imageset_right[0])[:20]
    
    pattern_size = imageset_left[1]
    square_size = imageset_left[2]
    
    intrinsics_left = unpickle_data(os.path.join(DataDirs.left, 'intrinsics.pickle'))
    intrinsics_right = unpickle_data(os.path.join(DataDirs.right, 'intrinsics.pickle'))
    
    print 'Finding chessboard corners'
    corners_left = [cv2.findChessboardCorners(img, pattern_size) for img in images_left]    
    corners_right = [cv2.findChessboardCorners(img, pattern_size) for img in images_right]
    corners_left_f, corners_right_f, images_left_f, images_right_f = chessboard.filter_chessboard_corners_results_stereo(corners_left, corners_right, images_left, images_right)
    
    ''' STEREO CALIBRATION '''    
    print 'Performing stereo calibration'    
    res = sv.calibrate_stereo_vision_system(images_left_f, images_right_f, pattern_size, square_size, intrinsics_left, intrinsics_right, corners_left_f, corners_right_f)
    R, T, E, F = res[5:]

    fm1 = cv2.findFundamentalMat(corners_left_f[0][1], corners_right_f[0][1])
    fm2 = cv2.findFundamentalMat(corners_left_f[0][1], corners_right_f[0][1])
    
    ''' STEREO RECTIFICATION '''
    print 'Performing stereo rectification'
    image_size = images.get_image_size(images_left_f[0])
    rect_res = sv.stereo_rectify(intrinsics_left, intrinsics_right, image_size, R, T)
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = rect_res
    
    new_images = sv.undistort_and_rectify(images_left_f, images_right_f, intrinsics_left, intrinsics_right, (R1, R2), (P1, P2))
    
    im1 = new_images[0][0]
    im2 = new_images[1][0]
    
    
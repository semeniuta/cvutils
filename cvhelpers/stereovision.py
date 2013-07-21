# -*- coding: utf-8 -*-
from cvhelpers import calibration
import cv2

def calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right, chessboard_corners_results_left, chessboard_corners_results_right):    
        
    '''
    Gather arguments for cv2.stereoCalibrate function call:
     - object points
     - image points for both cameras
     - camera matrices for both cameras
     - distortion coeffitients for both cameras
     - image size
    '''
    
    print 'Preparing data'
    
    lr_images = [images_left, images_right]        

    object_points = calibration.get_object_points(len(lr_images[0]), pattern_size, square_size)    
    
    lr_chessboard_corners_results = [chessboard_corners_results_left, chessboard_corners_results_right]        
    image_points_left = calibration.get_image_points(lr_images[0], lr_chessboard_corners_results[0])
    image_points_right = calibration.get_image_points(lr_images[1], lr_chessboard_corners_results[1])
    
    lr_image_points = [image_points_left, image_points_right]
    
    lr_camera_matrices = [intrinsics_left[0], intrinsics_right[0]]
    lr_dist_coefs = [intrinsics_left[1], intrinsics_right[1]]
    
    h, w = images_left[0].shape
    
    ''' 
    Performing stereo calibration    
    '''
    print 'Performing stereo calibration'    
    res = cv2.stereoCalibrate(object_points, lr_image_points[0], lr_image_points[1], (w, h), lr_camera_matrices[0], lr_dist_coefs[0], lr_camera_matrices[1], lr_dist_coefs[1])
    return res
    
    
    
    
    
    
    
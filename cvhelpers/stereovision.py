# -*- coding: utf-8 -*-
from cvhelpers import calibration
import cv2

def calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right):    
        
    ''' 
    Find chessboard corners for each image pair (left+right) 
    If chessboard corners are found on both images, add them to the
    filtered lists
    '''
    print 'Finding chessboard corners'
    chessboard_corners_left = []    
    chessboard_corners_right = []
    images_left_filtered = []
    images_right_filtered = []
    for i in range(len(images_left)):
        res_left = cv2.findChessboardCorners(images_left[i], pattern_size)
        res_right = cv2.findChessboardCorners(images_right[i], pattern_size)
        found_left, found_right = res_left[0], res_right[0]        
        if found_left and found_right:
            images_left_filtered.append(images_left[i])
            images_right_filtered.append(images_right[i])
            chessboard_corners_left.append(res_left)
            chessboard_corners_right.append(res_right)
        
    '''
    Gather arguments for cv2.stereoCalibrate function call:
     - object points
     - image points for both cameras
     - camera matrices for both cameras
     - distortion coeffitients for both cameras
     - image size
    '''
    
    print 'Preparing data'
    
    lr_images = [images_left_filtered, images_right_filtered]        

    object_points = calibration.get_object_points(len(lr_images[0]), pattern_size, square_size)    
    
    lr_chessboard_corners_results = [chessboard_corners_left, chessboard_corners_right]        
    image_points_left = calibration.get_image_points(lr_images[0], lr_chessboard_corners_results[0])
    image_points_right = calibration.get_image_points(lr_images[1], lr_chessboard_corners_results[1])
    
    lr_image_points = [image_points_left, image_points_right]
    
    lr_camera_matrices = [intrinsics_left[0], intrinsics_right[0]]
    lr_dist_coefs = [intrinsics_left[1], intrinsics_right[1]]
    
    h, w = images_left_filtered[0].shape
    
    ''' 
    Performing stereo calibration    
    '''
    print 'Performing stereo calibration'    
    res = cv2.stereoCalibrate(object_points, lr_image_points[0], lr_image_points[1], (w, h), lr_camera_matrices[0], lr_dist_coefs[0], lr_camera_matrices[1], lr_dist_coefs[1])
    return res
    
    
    
    
    
    
    
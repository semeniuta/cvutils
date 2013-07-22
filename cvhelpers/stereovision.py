# -*- coding: utf-8 -*-
from cvhelpers import calibration
from cvhelpers import images
import cv2

def calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right, chessboard_corners_results_left, chessboard_corners_results_right):    
    ''' 
    Conducts calibration of a stereo vision system using the photos 
    of chessboard pattern taken by left and right cameras

    Arguments:
    images_left -- a list of images from left camera
    images_right -- a list of images from left camera
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    intrinsics_left -- a tuple (camera_matrix_left, dist_coefs_left)
                       containing left camera intrinsic parameters: 
                       camera matrix and distortion coeffitient     
    intrinsics_right -- a tuple (camera_matrix_right, dist_coefs_right)
                        containing right camera intrinsic parameters: 
                        camera matrix and distortion coeffitient     
    chessboard_corners_results_left -- a list of tuples got from the
                                       cv2.findChessboardCorners function call
                                       for each image taken by left camera
                                       
    chessboard_corners_results_right -- a list of tuples got from the
                                        cv2.findChessboardCorners function call
                                        for each image taken by right camera
    
    IMPORTANT: all the images passed to the function must already be 
    filtered out, so that there is no images that didn't succeed in being
    passed to cv2.findChessboardCorners function; use 
    cvhelpers.chessboard.filter_chessboard_corners_results_stereo function
    to achieve this
    
    Returns a tuple as a result of the cv2.stereoCalibrate function call,
    containing the following calibration results:
    rms, camera_matrix_left, dist_coefs_left,
    camera_matrix_right, dist_coefs_right, R, T, E, F    
    '''    

    
    '''
    Gathering arguments for cv2.stereoCalibrate function call:
     - object points
     - image points for both cameras
     - camera matrices for both cameras
     - distortion coeffitients for both cameras
     - image size
    '''
    
    lr_images = [images_left, images_right]        

    object_points = calibration.get_object_points(len(lr_images[0]), pattern_size, square_size)    
    
    lr_chessboard_corners_results = [chessboard_corners_results_left, chessboard_corners_results_right]        
    image_points_left = calibration.get_image_points(lr_images[0], lr_chessboard_corners_results[0])
    image_points_right = calibration.get_image_points(lr_images[1], lr_chessboard_corners_results[1])
    
    lr_image_points = [image_points_left, image_points_right]
    
    lr_camera_matrices = [intrinsics_left[0], intrinsics_right[0]]
    lr_dist_coefs = [intrinsics_left[1], intrinsics_right[1]]
    
    image_size = images.get_image_size(images_left[0])
    
    ''' 
    Performing stereo calibration    
    '''
    res = cv2.stereoCalibrate(object_points, lr_image_points[0], lr_image_points[1], image_size, lr_camera_matrices[0], lr_dist_coefs[0], lr_camera_matrices[1], lr_dist_coefs[1])
    return res
    
def stereo_rectify(intrinsics_left, intrinsics_right, image_size, rotation_matrix, translation_vector):
    camera_matrix_left, dist_coefs_left = intrinsics_left    
    camera_matrix_right, dist_coefs_right = intrinsics_right
    print 'Performing stereo rectification'        
    res = cv2.stereoRectify(camera_matrix_left, dist_coefs_left, camera_matrix_right, dist_coefs_right, image_size, rotation_matrix, translation_vector)
    return res
    
def undistort_and_rectify():
    

    
    
    
    
    
    
    
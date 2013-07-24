# -*- coding: utf-8 -*-

import numpy as np
import cv2
from cvhelpers.images import get_image_size

def undistort_images(images, intrinsics):
        
    camera_matrix, dist_coefs = intrinsics
    r = np.eye(3)
    image_size = get_image_size(images[0])
    m1type = cv2.CV_16SC2
    
    mapx, mapy = cv2.initUndistortRectifyMap(camera_matrix, dist_coefs, r, camera_matrix, image_size, m1type)
    interp_method = cv2.INTER_LINEAR
    undistorted_images = [cv2.remap(img, mapx, mapy, interp_method) for img in images]
    
    return undistorted_images

def undistort_and_rectify_images_stereo(images_left, images_right, intrinsics_left, intrinsics_right, r_rect, p_rect):
    ''' 
    Conducts undistortion and rectification processes on two sets of images
    (from left and right cameras of the stereo vision system)    
    
    Agruments:
    intrinsics_left -- a tuple (camera_matrix_left, dist_coefs_left)
                       containing left camera intrinsic parameters: 
                       camera matrix and distortion coeffitient     
    intrinsics_right -- a tuple (camera_matrix_right, dist_coefs_right)
                        containing right camera intrinsic parameters: 
                        camera matrix and distortion coeffitient
    r_rect -- a tuple containing rectification rotation matrices for left and 
              right image planes
    p_rect -- a tuple containing left and right projection equation matrices
    
    Returns tuple (images_left_rect, images_right_rect) containing lists of 
    undistorted and rectified images (for left and right cameras respectively)
    in matrix form
    '''
    
    lr_camera_matrices = [intrinsics_left[0], intrinsics_right[0]]
    lr_dist_coefs = [intrinsics_left[1], intrinsics_right[1]]
    
    image_size = get_image_size(images_left[0])    
    m1type = cv2.CV_16SC2
    lr_maps = [cv2.initUndistortRectifyMap(lr_camera_matrices[i], lr_dist_coefs[i], r_rect[i], p_rect[i], image_size, m1type) for i in range(2)]
    maps_left, maps_right = lr_maps    
    
    interp_method = cv2.INTER_LINEAR
    images_left_rect = [cv2.remap(img, maps_left[0], maps_left[1], interp_method) for img in images_left]    
    images_right_rect = [cv2.remap(img, maps_right[0], maps_right[1], interp_method) for img in images_right]    
    
    return (images_left_rect, images_right_rect)
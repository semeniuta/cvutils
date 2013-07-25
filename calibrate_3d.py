# -*- coding: utf-8 -*-

import cPickle as pickle
from params import DataDirs, ImageSets, Directories
from cvfunctions import stereovision as sv
from cvfunctions import images
from cvfunctions import chessboard
from cvfunctions import calibration
from cvfunctions import transform
import os
import time
import cv2
from cvclasses.stereovisionsystem import StereoVisionSystem

def unpickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def open_images(imageset_left, imageset_right):
    images_left = images.open_images_from_mask(imageset_left[0])
    images_right = images.open_images_from_mask(imageset_right[0])
    return (images_left, images_right)
    
def unpickle_intrinsics():

    intrinsics_left = unpickle_data(os.path.join(DataDirs.left, 'intrinsics.pickle'))
    intrinsics_right = unpickle_data(os.path.join(DataDirs.right, 'intrinsics.pickle'))         
    return (intrinsics_left, intrinsics_right)

def calculate_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size):
    intrinsics_left = calibration.calibrate_camera(images_left, pattern_size, square_size, corners_left)[1:3]    
    intrinsics_right = calibration.calibrate_camera(images_right, pattern_size, square_size, corners_right)[1:3]
    return (intrinsics_left, intrinsics_right)
    
def rectify_uncalibrated(intrinsics_left, intrinsics_right, corners_left, corners_right, image_size):
    cm_left, dc_left = intrinsics_left
    cm_right, dc_right = intrinsics_right
    points_left = cv2.undistortPoints(corners_left[0][1], cm_left, dc_left)
    points_right = cv2.undistortPoints(corners_right[0][1], cm_right, dc_right)
    R1_uc, R2_uc = sv.compute_rectification_transforms_uncalibrated(cm_left, cm_right, points_left, points_right, image_size)    
    
def save_rectified_images(new_images):
    timelabel = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))        
    savedir = Directories.rectified_images
    savedir_left = os.path.join(savedir, timelabel + '_LEFT')
    savedir_right = os.path.join(savedir, timelabel + '_RIGHT')
            
    rectimg_left, rectimg_right = new_images
    images.save_images_to_dir(rectimg_left, savedir_left)
    images.save_images_to_dir(rectimg_right, savedir_right)
    
if __name__ == '__main__':
    
    imageset_left = ImageSets.opencv_sample_left
    imageset_right = ImageSets.opencv_sample_right
    
    pattern_size = imageset_left[1]
    square_size = imageset_left[2]    
    
    print 'Opening images'    
    images_left, images_right = open_images(imageset_left, imageset_right)
    
    print 'Finding chessboard corners'
    corners_left = chessboard.find_chessboard_corners(images_left, pattern_size)    
    corners_right = chessboard.find_chessboard_corners(images_right, pattern_size)
    corners_left, corners_right, images_left, images_right = chessboard.filter_chessboard_corners_results_stereo(corners_left, corners_right, images_left, images_right)
    
    print "Determining cameras' intrinsic parameters"
    lr_intrinsics = calculate_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size)    
    intrinsics_left, intrinsics_right = lr_intrinsics
            
    print 'Performing stereo calibration'
    svs = StereoVisionSystem()    
    res = sv.calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right, corners_left, corners_right)
    print 'Calibration error: %f' % res[0]
    svs.set_calibration_parameters(res)
        
    print 'Performing stereo rectification'
    image_size = images.get_image_size(images_left[0])
    rect_res = sv.compute_rectification_transforms(intrinsics_left, intrinsics_right, image_size, svs.R, svs.T)
    svs.set_rectification_transforms(rect_res)    
    new_images = transform.undistort_and_rectify_images_stereo(images_left, images_right, intrinsics_left, intrinsics_right, svs.rotation_matrices, svs.projection_matrices)
    
    print 'Saving images'
    save_rectified_images(new_images)
        
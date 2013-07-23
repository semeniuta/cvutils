# -*- coding: utf-8 -*-

import cPickle as pickle
from params import DataDirs, ImageSets, Directories
from cvhelpers import stereovision as sv
from cvhelpers import images
from cvhelpers import chessboard
from cvhelpers import calibration
import os
import time

def unpickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data

def open_images(imageset_left, imageset_right):
    images_left = images.open_images_from_mask(imageset_left[0])
    images_right = images.open_images_from_mask(imageset_right[0])
    return (images_left, images_right)
    
def unpickle_intrinsics(unpickle=False):

    intrinsics_left = unpickle_data(os.path.join(DataDirs.left, 'intrinsics.pickle'))
    intrinsics_right = unpickle_data(os.path.join(DataDirs.right, 'intrinsics.pickle'))         
    return (intrinsics_left, intrinsics_right)

def calculate_intrinsics(images_left, images_right, corners_left, corners_right, pattern_size, square_size):
    intrinsics_left = calibration.calibrate_camera(images_left, pattern_size, square_size, corners_left)[1:3]    
    intrinsics_right = calibration.calibrate_camera(images_right, pattern_size, square_size, corners_right)[1:3]
    return (intrinsics_left, intrinsics_right)
    
def save_rectified_images(new_images):
    timelabel = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))        
    savedir = Directories.rectified_images
    savedir_left = os.path.join(savedir, timelabel + '_LEFT')
    savedir_right = os.path.join(savedir, timelabel + '_RIGHT')
        
    os.makedirs(savedir_left)
    os.makedirs(savedir_right)
        
    rectimg_left, rectimg_right = new_images
    for i in range(len(rectimg_left)):
        images.save_image(rectimg_left[i], os.path.join(savedir_left, '%d.jpg' % i))
    for i in range(len(rectimg_right)):
        images.save_image(rectimg_right[i], os.path.join(savedir_right, '%d.jpg' % i))
    
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
    res = sv.calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right, corners_left, corners_right)
    print 'Calibration error: %f' % res[0]
    R, T, E, F = res[5:]
        
    print 'Performing stereo rectification'
    image_size = images.get_image_size(images_left[0])
    rect_res = sv.stereo_rectify(intrinsics_left, intrinsics_right, image_size, R, T)
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = rect_res
    
    new_images = sv.undistort_and_rectify(images_left, images_right, intrinsics_left, intrinsics_right, (R1, R2), (P1, P2))
    
    print 'Saving images'
    save_rectified_images(new_images)
        
# -*- coding: utf-8 -*-

import cPickle as pickle
from params import DataDirs, ImageSets, Directories
from cvhelpers import stereovision as sv
from cvhelpers import images
from cvhelpers import chessboard
from cvhelpers import calibration
import os
import cv2
import time

def unpickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data
    
if __name__ == '__main__':
    
    imageset_left = ImageSets.new_set_1
    imageset_right = ImageSets.new_set_2
    
    print 'Opening images'    
    images_left = images.open_images_from_mask(imageset_left[0])[:]
    images_right = images.open_images_from_mask(imageset_right[0])[:]
    
    pattern_size = imageset_left[1]
    square_size = imageset_left[2]
    
    intrinsics_left = unpickle_data(os.path.join(DataDirs.left, 'intrinsics.pickle'))
    intrinsics_right = unpickle_data(os.path.join(DataDirs.right, 'intrinsics.pickle'))    
    
    print 'Finding chessboard corners'
    corners_left = [cv2.findChessboardCorners(img, pattern_size) for img in images_left]    
    corners_right = [cv2.findChessboardCorners(img, pattern_size) for img in images_right]
    corners_left_f, corners_right_f, images_left_f, images_right_f = chessboard.filter_chessboard_corners_results_stereo(corners_left, corners_right, images_left, images_right)
    
    #intrinsics_left_1 = calibration.calibrate_camera(images_left_f, pattern_size, square_size, corners_left_f)[1:3]    
    #intrinsics_right_1 = calibration.calibrate_camera(images_right_f, pattern_size, square_size, corners_right_f)[1:3]
    
    ''' STEREO CALIBRATION '''    
    print 'Performing stereo calibration'    
    res = sv.calibrate_stereo_vision_system(images_left_f, images_right_f, pattern_size, square_size, intrinsics_left, intrinsics_right, corners_left_f, corners_right_f)
    #res_1 = sv.calibrate_stereo_vision_system(images_left_f, images_right_f, pattern_size, square_size, intrinsics_left_1, intrinsics_right_1, corners_left_f, corners_right_f)
    print res[0]
    #print res_1[0]    
    R, T, E, F = res[5:]

    fm1 = cv2.findFundamentalMat(corners_left_f[0][1], corners_right_f[0][1])
    fm2 = cv2.findFundamentalMat(corners_left_f[0][1], corners_right_f[0][1])
    
    #print F
    #print fm1[0]
    #print fm2[0]
    
    ''' STEREO RECTIFICATION '''
    print 'Performing stereo rectification'
    image_size = images.get_image_size(images_left_f[0])
    rect_res = sv.stereo_rectify(intrinsics_left, intrinsics_right, image_size, R, T)
    R1, R2, P1, P2, Q, validPixROI1, validPixROI2 = rect_res
    
    new_images = sv.undistort_and_rectify(images_left_f, images_right_f, intrinsics_left, intrinsics_right, (R1, R2), (P1, P2))
    
    ''' SAVING IMAGES '''
    print 'Saving images'
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
        
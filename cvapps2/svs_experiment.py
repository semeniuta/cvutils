# -*- coding: utf-8 -*-

import cPickle as pickle
from cvfunctions import stereovision as sv
from cvapplications.confmanager import ConfigManager
from cvfunctions import images
from cvfunctions import chessboard
from cvfunctions import calibration
from cvfunctions import transform
import os
import time
import cv2
from cvclasses.stereovisionsystem import StereoVisionSystem

cm = ConfigManager()
params = cm.get_svs_parameters() 

def conduct_svs_experiment(images_left, images_right, corners_left, corners_right, intrinsics_data_left, intrinsics_data_right, pattern_size, square_size):
    n = len(intrinsics_data_left)
    
    svs_list = []    
    for i in range(n):
        row_left = intrinsics_data_left[i]
        row_right = intrinsics_data_right[i]
        
        intrinsics_left = (calibration.get_camera_matrix(row_left[1:5]), row_left[5:])
        intrinsics_right = (calibration.get_camera_matrix(row_right[1:5]), row_right[5:])
        
        svs = get_svs(images_left, images_right, corners_left, corners_right, intrinsics_left, intrinsics_right, pattern_size, square_size)
        svs_list.append(svs)
    
    return svs_list

def get_svs(images_left, images_right, corners_left, corners_right, intrinsics_left, intrinsics_right, pattern_size, square_size):
            
    svs = StereoVisionSystem()    
    res = sv.calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right, corners_left, corners_right)
    print '%.3f' % res[0]    
    svs.set_calibration_parameters(res)
        
    image_size = images.get_image_size(images_left[0])
    rect_res = sv.compute_rectification_transforms(intrinsics_left, intrinsics_right, image_size, svs.R, svs.T)
    svs.set_rectification_transforms(rect_res)    
    
#    res_dir = create_results_dir()    
    
#    print 'Saving data'    
#    svs.pickle(os.path.join(res_dir, 'svs.pickle'))
#    svs.save_to_excel_file(os.path.join(res_dir, 'svs_parameters.xlsx'))   
    return svs

#def create_results_dir():
#    timelabel = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(time.time()))        
#    dirname = '%s_%s' % (params['name'], timelabel)
#    res_dir = os.path.join(cm.get_directory('stereo'), dirname)
#    os.makedirs(res_dir)
#    return res_dir
    
#def save_rectified_images(new_images, res_dir):
#    savedir = os.path.join(res_dir, 'rectified_images')            
#    rectimg_left, rectimg_right = new_images
#    images.save_images_to_dir(rectimg_left, savedir, '%d_0.jpg')
#    images.save_images_to_dir(rectimg_right, savedir, '%d_1.jpg')
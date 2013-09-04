# -*- coding: utf-8 -*-

import os
from cvapplications.confmanager import ConfigManager
from cvapplications import fullcalib
from cvapplications import pyramid_measurement as pm
from cvfunctions import chessboard
from cvfunctions import images
from cvfunctions import pyramid
from cvfunctions import transform

cm = ConfigManager()

def measure(mask1, mask2, cam1, cam2, indices, segments):
    
    pyramid_images1 = images.open_images_from_mask(mask1)
    pyramid_images2 = images.open_images_from_mask(mask2)
    
    res = transform.undistort_and_rectify_images_stereo(pyramid_images1, pyramid_images2, cam1.intrinsics, cam2.intrinsics, svs.rotation_matrices, svs.projection_matrices)
    
    ind = 2
    
    im1 = res[0][ind]
    im2 = res[1][ind]
    
    two_images = [im1, im2]
    
    points = []
    blobs_list = []
    for im in two_images:
        blobs, im_t = pyramid.detect_dots(im)
        blobs_list.append(blobs)
        points.append(pyramid.extract_points(blobs))
        
    points1, points2 = points      
    
    d = pm.measure_distances(points1, points2, indices, segments, svs.P1, svs.P2)    
    pm.display_measurements(points1, points2, indices, segments, two_images, blobs_list, d)


if __name__ == '__main__':
    
    sample_size = 12
    nsamples = 100
    findcbc_flags = chessboard.flags['at_or_fq']    
    
    indices = {1:2, 25:33, 10:13, 15:19, 26:34, 8:11, 3:5, 12:15, 13:17, 24:31, 0:1, 2:4, 22:28, 19:25, 21:27, 18:24, 7:10, 4:7, 9:12, 6:9, 14:18, 20:26, 23:30, 5:8, 16:21, 17:22}
    segments = [(15, 10), (1, 25), (25, 26), (10, 8), (1, 3), (12, 13), (26, 24), (0, 2), (22, 20), (21, 18), (7, 4), (22, 24), (9, 6), (14, 19), (15, 14), (10, 9), (14, 9), (25, 23), (23, 21), (18, 15), (3, 5), (5, 8), (17, 16), (16, 13), (4, 2), (1, 0), (1, 17), (25, 17)]
    
    cb_set1 = cm.get_chessboard_imageset('raufoss_set2_left')
    cb_set2 = cm.get_chessboard_imageset('raufoss_set2_right')
    
    pyramid_set1_mask = cm.get_imageset_full_mask('pyramid_left')
    pyramid_set2_mask = cm.get_imageset_full_mask('pyramid_right')
    
    calib_dir = os.path.join(cm.get_directory('calibration'), 'batch')    
    
    svs, cam1, cam2 = fullcalib.get_svs_and_cameras_objects(cb_set1, cb_set2, sample_size, nsamples, findcbc_flags, calib_dir)  
    measure(pyramid_set1_mask, pyramid_set2_mask, cam1, cam2, indices, segments)

    
    









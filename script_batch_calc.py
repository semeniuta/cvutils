# -*- coding: utf-8 -*-

import cv2
import os
from cvapplications.confmanager import ConfigManager
from cvfunctions import chessboard
from cvfunctions import calibration
from cvfunctions import stereovision
from cvfunctions import images
from cvfunctions import pyramid
from cvfunctions import transform
from cvclasses.stereovisionsystem import StereoVisionSystem
from generalfunctions import sampling
from cvclasses.camera import Camera
import numpy as np
from cvfunctions import geometry
import matplotlib.pyplot as plt


cm = ConfigManager()

def calibrate(set1, set2):
        
    findcbc_flags = cv2.CALIB_CB_ADAPTIVE_THRESH | cv2.CALIB_CB_FILTER_QUADS
    pattern_size = set1.pattern_size
    square_size = set1.square_size
    c1, c2, i1, i2, f1, f2 = chessboard.open_images_and_find_corners_universal(set1.imagemask, set1.pattern_size, set2.imagemask, findcbc_flags)
    
    population_size = len(i1)
    sample_size = 12
    nsamples = 30
    samples = sampling.generate_list_of_samples(population_size, sample_size, nsamples)
    
    res1 = []
    res2 = []
    for s in samples:
        
        images1_sample = [i1[num] for num in s]
        images2_sample = [i2[num] for num in s]
        corners1_sample = [c1[num] for num in s]
        corners2_sample = [c2[num] for num in s]
        
        res1_sample = calibration.calibrate_camera(images1_sample, pattern_size, square_size, corners1_sample)
        res2_sample = calibration.calibrate_camera(images2_sample, pattern_size, square_size, corners2_sample)
        
        res1.append(res1_sample)
        res2.append(res2_sample)
    
    min_error_index = 0    
    for i in range(1, nsamples):
        if res1[i][0] < res1[min_error_index][0]:
            min_error_index = i
    print res1[min_error_index][0]
            
    intrinsics1 = res1[min_error_index][1:3]
    intrinsics2 = res2[min_error_index][1:3]
    
    images1 = i1
    images2 = i2
    corners1 = c1
    corners2 = c2
    
    cal_params = stereovision.calibrate_stereo_vision_system(images1, images2, pattern_size, square_size, intrinsics1, intrinsics2, corners1, corners2)
    svs = StereoVisionSystem()
    svs.set_calibration_parameters(cal_params)
    image_size = images.get_image_size(images1[0])
    rt = stereovision.compute_rectification_transforms(intrinsics1, intrinsics2, image_size, svs.R, svs.T)
    svs.set_rectification_transforms(rt)
    
    cam1 = Camera()
    cam2 = Camera()
    
    cam1.set_intrinsics(intrinsics1)
    cam2.set_intrinsics(intrinsics2)
    
    return svs, cam1, cam2    

def measure(set1, set2, cam1, cam2):
    
    pyramid_images1 = images.open_images_from_mask(set1)
    pyramid_images2 = images.open_images_from_mask(set2)
    
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
        
    indices = {1:2, 25:33, 10:13, 15:19, 26:34, 8:11, 3:5, 12:15, 13:17, 24:31, 0:1, 2:4, 22:28, 19:25, 21:27, 18:24, 7:10, 4:7, 9:12, 6:9, 14:18, 20:26, 23:30, 5:8, 16:21, 17:22}
    
    interest_points_1 = np.transpose(np.array([points[0][i1] for i1, i2 in indices.iteritems()]))
    interest_points_2 = np.transpose(np.array([points[1][i2] for i1, i2 in indices.iteritems()]))
    
    res = cv2.triangulatePoints(svs.P1, svs.P2, interest_points_1, interest_points_2)
    
    res = np.transpose(res)
    res_real = np.array([[row[i]/row[3] for i in range(3)] for row in res])
    
    i1_list = list(indices.iterkeys())
    res_dict = {i1_list[i]: res_real[i] for i in range(len(i1_list))}
    
    dist = lambda a, b: geometry.compute_distance(*[res_dict[i] for i in (a, b)])
    
    segments = [(15, 10), (1, 25), (25, 26), (10, 8), (1, 3), (12, 13), (26, 24), (0, 2), (22, 20), (21, 18), (7, 4), (22, 24), (9, 6), (14, 19), (15, 14), (10, 9), (14, 9), (25, 23), (23, 21), (18, 15), (3, 5), (5, 8), (17, 16), (16, 13), (4, 2), (1, 0), (1, 17), (25, 17)]
    d = [dist(a, b) for a, b in segments]
    
    pixel_dict_1 = {i1_list[i]: np.transpose(interest_points_1)[i] for i in range(len(i1_list))}
    pixel_dict_2 = {i1_list[i]: np.transpose(interest_points_2)[i] for i in range(len(i1_list))}
    pd = [pixel_dict_1, pixel_dict_2]
    for i in range(2):
        pyramid.display_dots(two_images[i], blobs_list[i])
        pyramid.display_dots_numbers(blobs_list[i])
        for segm_ind in range(len(segments)):
            a, b = segments[segm_ind]
            p1 = pd[i][a]
            p2 = pd[i][b]
            x = [p1[0], p2[0]]
            y = [p1[1], p2[1]]
            plt.plot(x, y, 'c')
            center = geometry.compute_segment_center(p1, p2)
            plt.text(center[0], center[1], '%.3f' % d[segm_ind], color='#ffff99')



if __name__ == '__main__':
    set1 = cm.get_chessboard_imageset('raufoss_set2_left')
    set2 = cm.get_chessboard_imageset('raufoss_set2_right')
    
    calib_dir = os.path.join(cm.get_directory('calibration'), 'batch')    
    pickles = {name: os.path.join(calib_dir, name + '.pickle') for name in ('svs', 'cam1', 'cam2')}
    if not os.path.exists(calib_dir):
        os.makedirs(calib_dir)
        svs, cam1, cam2  = calibrate(set1, set2)
        svs.pickle(pickles['svs'])
        cam1.pickle(pickles['cam1'])
        cam2.pickle(pickles['cam2'])
    else:
        svs = StereoVisionSystem()
        cam1 = Camera()
        cam2 = Camera()
        svs.unpickle(pickles['svs'])
        cam1.unpickle(pickles['cam1'])
        cam2.unpickle(pickles['cam2'])
    
    pyramid_set1 = cm.get_imageset_full_mask('pyramid_left')
    pyramid_set2 = cm.get_imageset_full_mask('pyramid_right')
    
    measure(pyramid_set1, pyramid_set2, cam1, cam2)

    
    









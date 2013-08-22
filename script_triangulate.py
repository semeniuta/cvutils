# -*- coding: utf-8 -*-

import cv2
from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid, transform
from cvclasses.stereovisionsystem import StereoVisionSystem
from cvclasses.camera import Camera
import os
import numpy as np
from cvfunctions import geometry

cm = ConfigManager()

set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

images1 = images.open_images_from_mask(set1)
images2 = images.open_images_from_mask(set2)

lr_images = [images1, images2]

params = cm.get_pyramid_parameters()
stereo_datadir = params['stereo_dir']
svs = StereoVisionSystem()
svs.unpickle(os.path.join(stereo_datadir, 'svs.pickle'))

intrinsics_left_dir = params['intrinsics_left_dir']
intrinsics_right_dir = params['intrinsics_right_dir']
cam1 = Camera()
cam2 = Camera()
cam1.unpickle(os.path.join(intrinsics_left_dir, 'intrinsics.pickle'))
cam2.unpickle(os.path.join(intrinsics_right_dir, 'intrinsics.pickle'))

res = transform.undistort_and_rectify_images_stereo(images1, images2, cam1.intrinsics, cam2.intrinsics, svs.rotation_matrices, svs.projection_matrices)

ind = 2

im1 = res[0][ind]
im2 = res[1][ind]

two_images = [im1, im2]

points = []
for im in two_images:
    blobs, im_t = pyramid.detect_dots(im)
    pyramid.display_dots(im, blobs)
    pyramid.display_dots_numbers(blobs)
    points.append(pyramid.extract_points(blobs))
    
indices_1 = [1, 25, 10, 15, 26, 8, 3]
indices_2 = [2, 33, 13, 19, 34, 11, 5]

interest_points_1 = np.transpose(np.array([points[0][ind] for ind in indices_1]))
interest_points_2 = np.transpose(np.array([points[1][ind] for ind in indices_2]))

res = cv2.triangulatePoints(svs.P1, svs.P2, interest_points_1, interest_points_2)

res = np.transpose(res)
res_real = np.array([[row[i]/row[3] for i in range(3)] for row in res])

d1 = geometry.compute_distance(*[res_real[i] for i in (2, 3)])
d2 = geometry.compute_distance(*[res_real[i] for i in (0, 1)])
d3 = geometry.compute_distance(*[res_real[i] for i in (1, 4)])        
d4 = geometry.compute_distance(*[res_real[i] for i in (2, 5)])        
h1 = res_real[2][2] - res_real[5][2]
h2 = res_real[0][2] - res_real[6][2]

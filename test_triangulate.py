# -*- coding: utf-8 -*-

import cv2
from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid, transform, output
from cvclasses.stereovisionsystem import StereoVisionSystem
from cvclasses.camera import Camera
import os
import random
from matplotlib import pyplot as plt
import numpy as np

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
    dots, im_t = pyramid.detect_dots(im)
    pyramid.display_dots(im, dots)
    points.append([])

    num = 0
    for d in dots:
        x, y = d.pt
        points[-1].append(np.array([x, y]))
        plt.text(x, y, num, color='w')
        num += 1
        
interest_points_1 = np.transpose(np.array([points[0][1], points[0][25], points[0][10], points[0][15]]))
interest_points_2 = np.transpose(np.array([points[1][2], points[1][33], points[1][13], points[1][19]]))

res = cv2.triangulatePoints(svs.P1, svs.P2, interest_points_1, interest_points_2)

res = np.transpose(res)
res_real = np.array([[row[i]/row[3] for i in range(3)] for row in res])
        



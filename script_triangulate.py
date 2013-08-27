# -*- coding: utf-8 -*-

'''
Script that measures distances in real-world 3D coordinates
using the pyramid images
'''

import cv2
from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid, transform
from cvclasses.stereovisionsystem import StereoVisionSystem
from cvclasses.camera import Camera
import os
import numpy as np
from cvfunctions import geometry
import matplotlib.pyplot as plt

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
blobs_list = []
for im in two_images:
    blobs, im_t = pyramid.detect_dots(im)
    blobs_list.append(blobs)
    points.append(pyramid.extract_points(blobs))
    
indices = {1:2, 25:33, 10:13, 15:19, 26:34, 8:11, 3:5, 12:15, 13:17, 24:31, 0:1, 2:4, 22:28, 19:26, 21:27, 18:24, 7:10, 4:7, 9:12, 6:9, 14:18, 20:25}

interest_points_1 = np.transpose(np.array([points[0][i1] for i1, i2 in indices.iteritems()]))
interest_points_2 = np.transpose(np.array([points[1][i2] for i1, i2 in indices.iteritems()]))

res = cv2.triangulatePoints(svs.P1, svs.P2, interest_points_1, interest_points_2)

res = np.transpose(res)
res_real = np.array([[row[i]/row[3] for i in range(3)] for row in res])

i1_list = list(indices.iterkeys())
res_dict = {i1_list[i]: res_real[i] for i in range(len(i1_list))}

dist = lambda a, b: geometry.compute_distance(*[res_dict[i] for i in (a, b)])

segments = [(15, 10), (1, 25), (25, 26), (10, 8), (1, 3), (12, 13), (26, 24), (0, 2), (22, 19), (21, 18), (7, 4), (22, 24), (9, 6), (14, 20), (15, 14), (10, 9), (14, 9)]
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
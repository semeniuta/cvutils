# -*- coding: utf-8 -*-

''' 
Script that illustrates how the images are rectified and that the pyramid's
dots are not row-aligned on the rectified images 

Open photos of the pyramid taken by two cameras
Perform stereo calibration
Rectify the images
Take specific pair of rectified images and merge them
Find the dots on the merged image
Draw the lines throught each dot's center  
'''

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid, transform, output
from cvclasses.stereovisionsystem import StereoVisionSystem
from cvclasses.camera import Camera
import os
import random
from matplotlib import pyplot as plt

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

im_merged = images.merge_images(im1, im2)

dots, im_t = pyramid.detect_dots(im_merged)
pyramid.display_dots(im_merged, dots)

colors = ['r', 'g', 'b', 'c', 'm', 'y', 'w']

num = 1
for d in dots:
    x, y = d.pt
    plt.text(x, y, num, color='w')
    color = colors[random.randint(0, len(colors) - 1)]
    output.draw_horizontal_line(y, color)
    num += 1


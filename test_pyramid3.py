# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid, transform, output
from cvclasses.stereovisionsystem import StereoVisionSystem
from cvclasses.camera import Camera
import os
import random
from matplotlib import pyplot as plt
import numpy as np

from scipy.cluster.vq import kmeans, vq


cm = ConfigManager()

set_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

images1 = images.open_images_from_mask(set1)
images2 = images.open_images_from_mask(set2)

im = images1[1]
    
dots, im_t = pyramid.detect_dots(im)
    
res = pyramid.get_lines(dots)
res_f = res[res.dist < 100]

data = np.array(res_f.loc[:, ['slope', 'intercept']])
xy = np.array(res_f.loc[:, 'x0':'y1'])

nclusters = 9
centroids, _ = kmeans(data, nclusters)
idx,_ = vq(data,centroids)

colors = ['r', 'g', 'b', 'c', 'm']

for i in range(nclusters):    
    randcolor = colors[random.randint(0, len(colors)-1)]
    xy_current_cluster = xy[idx==i]
    output.plot_image(im)    
    for row in xy_current_cluster:
        x = row[:2]
        y = row[2:]
        plt.plot(x, y, randcolor)

plt.figure()
for i in range(nclusters):    
    output.plot_points(data[idx==i,0], data[idx==i,1], randcolor)
plt.plot(centroids[:,0], centroids[:,1], 'sy')


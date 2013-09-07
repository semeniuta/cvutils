# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid
import cvfunctions.featuredetection as fd
import matplotlib.pyplot as plt
from cvfunctions import output
import cv2

cm = ConfigManager()

def display_pyramid_results(image, blobs):
    pyramid.display_dots(image, blobs)
    pyramid.display_dots_numbers(blobs, display_sizes=False)
    
set_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

images_all = [images.open_images_from_mask(s) for s in (set1, set2, set_phone)]

im1 = images_all[0][-1]
im2 = images_all[1][-1]
imp = images_all[2][-1]

images = (im1, im2, imp)
min_threshold = 15
max_threshold = 100
pre_threshold = False
for im in images:
    if pre_threshold:
        im_t = fd.threshold_binary(im, min_threshold)
    else:
        im_t = im
    
    p = cv2.SimpleBlobDetector_Params()
    p.minCircularity = 0.8
    p.maxCircularity = 1.2
    p.filterByCircularity = True
    
    if not pre_threshold:
        p.minThreshold = min_threshold    
        p.maxThreshold = max_threshold
        
    det = cv2.SimpleBlobDetector(p)
    
    blobs = det.detect(im_t)
    
    plt.figure()
    display_pyramid_results(im_t, blobs)

plt.figure()    
output.plot_several_image_histograms(images, ['im1', 'im2', 'imp'])
        
    
    
    
    
    
    
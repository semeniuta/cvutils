# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid
import cvfunctions.featuredetection as fd
import matplotlib.pyplot as plt
from cvfunctions import output

cm = ConfigManager()

def find_blobs(image, threshold):
    min_circularity = 0.8
    max_circularity = 1.2    
    im_t = fd.threshold_binary(image, threshold)   
    blobs = fd.detect_circles_as_blobs(im_t, min_circularity, max_circularity)
    return im_t, blobs

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
thresholds = [25]
for im in images:    
    
    plt.figure()
    for i in range(len(thresholds)):
        t = thresholds[i]
        im_t, blobs = find_blobs(im, t)
        display_pyramid_results(im_t, blobs)

plt.figure()    
output.plot_several_image_histograms(images, ['im1', 'im2', 'imp'])
        
    
    
    
    
    
    
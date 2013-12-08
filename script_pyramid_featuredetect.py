# -*- coding: utf-8 -*-

''' 
Script for exploring the possibilities for creation of a universal feature
detection algorithms (particularly for detection of pyramid dots)
'''

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid
import matplotlib.pyplot as plt
from cvfunctions import output
import cv2

cm = ConfigManager()

def display_pyramid_results(image, blobs):
    pyramid.display_dots(image, blobs)
    pyramid.display_dots_numbers(blobs, display_sizes=True)
    
set_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

images_all = [images.open_images_from_mask(s) for s in (set1, set2, set_phone)]

im1 = images_all[0][-1]
im2 = images_all[1][-1]
imp = images_all[2][-1]

min_threshold = 20
max_threshold = 150
blur_window = 15
for im in (im1, im2, imp):
    
    #im = pixt.adjust_contrast_and_brightness(im, 3, 1)
    im = cv2.medianBlur(im, blur_window)
    
    p = cv2.SimpleBlobDetector_Params()
    p.minCircularity = 0.8
    p.maxCircularity = 1.2
    p.filterByCircularity = True
    
    p.minThreshold = min_threshold    
    p.maxThreshold = max_threshold
        
    det = cv2.SimpleBlobDetector(p)
    
    blobs = det.detect(im)
    
    print 'Found: %d blobs' % len(blobs)
    
    plt.figure()
    display_pyramid_results(im, blobs)

plt.figure()    
output.plot_several_image_histograms([im1, im2, imp], ['im1', 'im2', 'imp'])
        
    
    
    
    
    
    
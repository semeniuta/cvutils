# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid
import cvfunctions.featuredetection as fd
import cvfunctions.pixeltransform as pixt
import matplotlib.pyplot as plt
from cvfunctions import output
import cv2
from numpy.lib.function_base import average

cm = ConfigManager()

def different_filters(im):
    
    im_median13 = cv2.medianBlur(im, 13)
    im_median15 = cv2.medianBlur(im, 15)
    
    images = [im, im_median13, im_median15]
    for image in images:
        plt.figure()
        output.plot_image(image)
    
    plt.figure()
    output.plot_several_image_histograms(images, ['original', 'median13', 'median15'])
    
def hist_analysis(im):
    blurred_images = []
    plt.figure()
    for i in range(1, 100, 2):
        im_blurred = cv2.medianBlur(im, i)
        blurred_images.append(im_blurred)
        
        hist_res = output.plot_image_histogram(im_blurred)
        n = hist_res[0]
        max_n = max(n)
        w, h = images.get_image_size(im_blurred)
        total_pixels = w * h
        max_ratio = max_n / float(total_pixels)
        
        avg = average(n)
        
        print i, max_ratio, avg/total_pixels
        
def pixel_transform(im):
    plt.figure()
    output.plot_image(im)
    
    plt.figure()
    im_doublecontrast = pixt.adjust_contrast_and_brightness(im, 3, 1)
    output.plot_image(im_doublecontrast)
    
    plt.figure()
    im_blurred = cv2.medianBlur(im_doublecontrast, 3)
    output.plot_image(im_blurred)

    return im_doublecontrast    


set_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

images_all = [images.open_images_from_mask(s) for s in (set1, set2, set_phone)]

im1 = images_all[0][-1]
im2 = images_all[1][-1]
imp = images_all[2][-1]

imgs = (im1, im2, imp)

imdc = pixel_transform(im1)
 
#output.plot_several_image_histograms(imgs, ['im1', 'im2', 'imp'])
 
#different_filters(imp)
 
#hist_analysis(imp)


        
    
    
    
    
    
    
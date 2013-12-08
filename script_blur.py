# -*- coding: utf-8 -*-

'''
Script for testing how different blurring options affect the effectiveness
of finding dots on the pyramid images
'''

import cv2
from cvfunctions import images, pyramid
from cvapplications.confmanager import ConfigManager
import matplotlib.pyplot as plt

cm = ConfigManager()

def test_blur(im):
    im_f = cv2.GaussianBlur(im, (5, 5), 1)
    #im_f = cv2.medianBlur(im, 11)
    
    merged = images.merge_images(im, im_f)
    
    dots, im_t = pyramid.detect_dots(merged, threshold=80, iterate=False)
    pyramid.display_dots(merged, dots)
    
def test_hist(im1, im2):
    plt.figure()    
    plt.subplot(2, 1, 1)
    plt.hist(im1.flatten(), 128)    
    plt.subplot(2, 1, 2)    
    plt.hist(im2.flatten(), 128)    
    
if __name__ == '__main__':
    
    mask_robot = cm.get_imageset_full_mask('pyramid_left')
    mask_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
    
    images_list_robot = images.open_images_from_mask(mask_robot)
    images_list_phone = images.open_images_from_mask(mask_phone)
    
    im1 = images_list_robot[0]
    im2 = images_list_phone[0]

    test_blur(im2)
    test_hist(im1, im2)



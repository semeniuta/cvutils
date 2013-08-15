# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid, transform, output
from cvclasses.stereovisionsystem import StereoVisionSystem
from cvclasses.camera import Camera
import os
import random
from matplotlib import pyplot as plt

cm = ConfigManager()

set_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

print 'Opening images'
images1 = images.open_images_from_mask(set1)
images2 = images.open_images_from_mask(set2)

for im in images1:
    
    print 'Finding dots'
    dots, im_t = pyramid.detect_dots(im)
    pyramid.display_dots(im, dots)
   
    num = 1
    for d in dots:
        x, y = d.pt
        plt.text(x, y, num, color='w')
        num += 1
        
    #pos = 'The pyramid is turned %s' % ('left' if pyramid.pyramid_is_turned_left(dots) else 'right')
    #plt.text(50, 50, pos, color='c')    
    
    #pyramid.draw_extreme_points(dots)    
 
    

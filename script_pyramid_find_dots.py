# -*- coding: utf-8 -*-

''' 
Script that finds dots on the set of pyramid images 
'''

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid
from matplotlib import pyplot as plt

cm = ConfigManager()

set_phone = cm.get_imageset_full_mask('pyramid_withphone_2')
set1 = cm.get_imageset_full_mask('pyramid_left')
set2 = cm.get_imageset_full_mask('pyramid_right')

current_set = set2

print 'Opening images'
images = images.open_images_from_mask(current_set)

for im in images:
    
    print 'Finding dots'
    dots, im_t = pyramid.detect_dots(im)
    plt.figure()
    pyramid.display_dots(im, dots)
   
    num = 1
    for d in dots:
        x, y = d.pt
        plt.text(x, y, num, color='w')
        num += 1
         
 
    

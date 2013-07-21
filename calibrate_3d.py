# -*- coding: utf-8 -*-

import cPickle as pickle
from params import DataDirs, ImageSets
from cvhelpers import stereovision as sv
from cvhelpers import images
import os

def unpickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data
    
if __name__ == '__main__':
    
    '''
    calibrate_stereo_vision_system(images_left, images_right, pattern_size,
    square_size, intrinsics_left, intrinsics_right):    
    '''
    
    imageset_left = ImageSets.new_set_1
    imageset_right = ImageSets.new_set_2
    
    print 'Opening images'    
    images_left = images.open_images_from_mask(imageset_left[0])
    images_right = images.open_images_from_mask(imageset_right[0])
    
    pattern_size = imageset_left[1]
    square_size = imageset_left[2]
    
    intrinsics_left = unpickle_data(os.path.join(DataDirs.left, 'intrinsics.pickle'))
    intrinsics_right = unpickle_data(os.path.join(DataDirs.right, 'intrinsics.pickle'))
    
    res = sv.calibrate_stereo_vision_system(images_left, images_right, pattern_size, square_size, intrinsics_left, intrinsics_right)
    
    
    
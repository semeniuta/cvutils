# -*- coding: utf-8 -*-

import cv2
from cvfunctions import images
from cvapplications.svsparametrize import parametrize_stereo_vision_system
from params import SVSParametrization as p

def get_svs_object():
    lr_imagesets = (p.imageset_left, p.imageset_right)
    imagemasks = (lr_imagesets[0][0], lr_imagesets[1][0])
    pattern_size = lr_imagesets[0][1]
    square_size = lr_imagesets[0][2]
    svs = parametrize_stereo_vision_system(imagemasks, pattern_size, square_size, "compute", False)
    return svs

if __name__ == '__main__':
    svs = get_svs_object()
    
    

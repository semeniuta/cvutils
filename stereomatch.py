# -*- coding: utf-8 -*-

import cv2
from cvfunctions.images import open_image, save_image
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
    
    img_left = open_image(r'D:\Dropbox\SINTEF\rectified\LEFT\5.jpg')
    img_right = open_image(r'D:\Dropbox\SINTEF\rectified\RIGHT\5.jpg')
    
    preset = cv2.STEREO_BM_BASIC_PRESET
    ndisparities = 16 * 5
    sad_winsize = 11
    sbm = cv2.StereoBM(preset, ndisparities, sad_winsize)
    
    disparity = sbm.compute(img_left, img_right, disptype=cv2.CV_16S)
    
    minval, maxval = cv2.minMaxLoc(disparity)[:2]
    
    res = cv2.reprojectImageTo3D(disparity, svs.Q)

    save_image(disparity, 'disp.png')

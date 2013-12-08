# -*- coding: utf-8 -*-

import cv2
from cvfunctions.images import open_image, save_image
from cvapplications.svsparametrize import parametrize_stereo_vision_system
from cvapplications.confmanager import ConfigManager

def get_svs_object():
    import os
    cm = ConfigManager()
    params = cm.get_svs_parameters()
    lr_imagesets = (cm.get_chessboard_imageset(params['imageset_left']), cm.get_chessboard_imageset(params['imageset_right']))
    imagemasks = (lr_imagesets[0].imagemask, lr_imagesets[1].imagemask)
    pattern_size = lr_imagesets[0].pattern_size
    square_size = lr_imagesets[0].square_size
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

# -*- coding: utf-8 -*-

from cvapplications.svsparametrize import parametrize_stereo_vision_system
from cvapplications.confmanager import ConfigManager
import argparse 
from cvclasses.stereovisionsystem import StereoVisionSystem

def initialize_parameters(args=None):
    
    cm = ConfigManager()
    params = cm.get_svs_parameters()

    imageset_left_name = params['imageset_left'] if  args.imageset_left == None else args.imageset_left     
    imageset_right_name = params['imageset_right'] if  args.imageset_right == None else args.imageset_right
    
    imageset_left = cm.get_chessboard_imageset(imageset_left_name)    
    imageset_right = cm.get_chessboard_imageset(imageset_right_name)    
        
    imagemasks = (imageset_left.imagemask, imageset_right.imagemask)
    pattern_size = imageset_left.pattern_size
    square_size = imageset_left.square_size

    get_intrinsics_method = args.intrinsics     
    saverect = args.saverect
    
    return (imagemasks, pattern_size, square_size, get_intrinsics_method, saverect)

def start(args):
    svs = parametrize_stereo_vision_system(*args)
    return svs

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--imageset-left')  
    parser.add_argument('--imageset-right')
    parser.add_argument('--intrinsics', default='read', choices=['compute', 'read'])    
    parser.add_argument('--saverect', action='store_true', default=True)
    args = parser.parse_args()    
    
    parameters = initialize_parameters(args)
    svs = start(parameters)


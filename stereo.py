# -*- coding: utf-8 -*-

from cvapplications.svsparametrize import parametrize_stereo_vision_system
import params
import argparse 

def initialize_parameters(args=None):
    p = params.SVSParametrization    
    
    if args.imageset_left == None:
        imageset_left = p.imageset_left
    else:
        imageset_left = get_imageset(args.imageset_left)
    
    if args.imageset_right == None:
        imageset_right = p.imageset_right
    else:
        imageset_right = get_imageset(args.imageset_rigth)
    
    imagemasks = (imageset_left[0], imageset_right[0])
    pattern_size, square_size = imageset_left[1:3]

    get_intrinsics_method = args.intrinsics     
    saverect = args.saverect
    
    return (imagemasks, pattern_size, square_size, get_intrinsics_method, saverect)

def get_imageset(name):
    return getattr(params.ImageSets, name)

def start(args):
    svs = parametrize_stereo_vision_system(*args)
    return svs

if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--imageset-left')  
    parser.add_argument('--imageset-right')
    parser.add_argument('--intrinsics', default='compute', choices=['compute', 'read'])    
    parser.add_argument('--saverect', action='store_true', default=True)
    args = parser.parse_args()    
    
    parameters = initialize_parameters(args)
    svs = start(parameters)

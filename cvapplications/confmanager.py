# -*- coding: utf-8 -*-

from ConfigParser import ConfigParser
import os
from cvclasses.imageset import CalibrationImageSet
from glob import glob

SYSTEM_CONFIG_FILE = r'conf_system.ini'
IMAGESETS_CONFIG_FILE = r'conf_imagesets.ini'

class ConfigManager:
    def __init__(self):        
        self.imgconfig = ConfigParser()
        self.imgconfig.read(IMAGESETS_CONFIG_FILE)
        self.systemconfig = ConfigParser()
        self.systemconfig.read(SYSTEM_CONFIG_FILE)

    def get_root_directory(self):
        return self.systemconfig.get('system', 'root_directory')        
    
    def get_directory(self, dir_key):
        root_directory = self.get_root_directory()
        dir_name = self.systemconfig.get('directories', dir_key)
        return os.path.join(root_directory, dir_name)
        
    def get_directories(self):
        tuples = self.systemconfig.items('directories')
        dir_dict = {key: os.path.join(self.get_root_directory(), dirname) for key, dirname in tuples}
        return dir_dict
        
    def get_imageset_images_list(self, imageset_name):
        mask = self.get_imageset_full_mask(imageset_name)
        return glob(mask)
    
    def get_imageset_full_mask(self, imageset_name):
        imagemask = self.imgconfig.get(imageset_name, 'mask')
        if '/' not in imagemask and '\\' not in imagemask:
            root_dir = self.get_root_directory()
            img_dir = self.systemconfig.get('directories', 'imagesets')
            imagemask = os.path.join(root_dir, img_dir, imageset_name, imagemask)
        return imagemask
    
    def get_chessboard_imageset(self, imageset_name):
        imagemask = self.get_imageset_full_mask(imageset_name)
        
        width = self.imgconfig.getint(imageset_name, 'width')
        height = self.imgconfig.getint(imageset_name, 'height')
        pattern_size = (width, height)
        square_size = self.imgconfig.getfloat(imageset_name, 'square')
        
        imageset = CalibrationImageSet(imageset_name, imagemask, pattern_size, square_size)
        return imageset
        
    def get_calibration_parameters(self):
        res = {}        
        res['sample_size'] = self.systemconfig.getint('calibration', 'sample_size')        
        res['num_of_samples'] = self.systemconfig.getint('calibration', 'num_of_samples')
        res['imageset'] = self.systemconfig.get('calibration', 'imageset')
        return res
        
    def get_svs_parameters(self):
        res = {}
        res['imageset_left'] = self.systemconfig.get('svs', 'imageset_left')        
        res['imageset_right'] = self.systemconfig.get('svs', 'imageset_right')
        calib_dir = self.get_directory('calibration')        
        res['datadir_left'] = os.path.join(calib_dir, self.systemconfig.get('svs', 'datadir_left'))
        res['datadir_right'] = os.path.join(calib_dir, self.systemconfig.get('svs', 'datadir_right'))
        res['name'] = self.systemconfig.get('svs', 'name')
        return res
        
    def get_pyramid_parameters(self):
        stereo_dir_name = self.systemconfig.get('pyramid', 'stereo_dir')
        intrinsics_left_dir_name = self.systemconfig.get('pyramid', 'intrinsics_left_dir')
        intrinsics_right_dir_name = self.systemconfig.get('pyramid', 'intrinsics_right_dir')
        
        svs_results_dir = self.get_directory('stereo')
        calib_dir = self.get_directory('calibration')
        
        res = {}
        res['stereo_dir'] = os.path.join(svs_results_dir, stereo_dir_name)
        res['intrinsics_left_dir'] = os.path.join(calib_dir, intrinsics_left_dir_name)
        res['intrinsics_right_dir'] = os.path.join(calib_dir, intrinsics_right_dir_name)
        return res
    
    def get_ti_dirs(self):
        calib_dir = self.get_directory('calibration')
        left = os.path.join(calib_dir, self.systemconfig.get('ti', 'left'))
        right = os.path.join(calib_dir, self.systemconfig.get('ti', 'right'))
        return (left, right)
        
        
        
        
        
        
        
        
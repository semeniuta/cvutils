# -*- coding: utf-8 -*-

class Directories:
    experiment_results = r'D:\Dropbox\SINTEF\experiments'
    rectified_images = r'D:\Dropbox\SINTEF\rectified'
    undistortion_test = r'D:\Dropbox\SINTEF\undist'

class ImageSets:
    first_four = (r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp', (7, 7), 2.9, 'first_four')
    opencv_sample_left = (r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg', (9, 6), 1.0, 'opencv_sample_left')
    opencv_sample_right = (r'D:\Dropbox\SINTEF\img\opencv_sample\right*.jpg', (9, 6), 1.0, 'opencv_sample_right')
    raufoss_set1_left = (r'D:\Dropbox\SINTEF\img\Camera1-1\*.bmp', (8, 7), 2.9, 'new_set_left')
    raufoss_set1_right = (r'D:\Dropbox\SINTEF\img\Camera2-1\*.bmp', (8, 7), 2.9, 'new_set_right')
    raufoss_set2_left = (r'D:\Dropbox\SINTEF\img\new\Camera1-2\*.bmp', (10, 8), 2.9, 'new_set_left')
    raufoss_set2_right = (r'D:\Dropbox\SINTEF\img\new\Camera2-2\*.bmp', (10, 8), 2.9, 'new_set_right')
    
class CalibrationExperiment:
    sample_size = 7
    num_of_samples = 300    
    imageset = ImageSets.opencv_sample_left   
    results_dir = Directories.experiment_results

class DataDirsTI:
    left = r'D:\Dropbox\SINTEF\experiments\NEWLEFT2_10x3000'
    right = r'D:\Dropbox\SINTEF\experiments\NEWRIGHT2_10x3000'

class SVSParametrization:
    imageset_left = ImageSets.raufoss_set2_left
    imageset_right = ImageSets.raufoss_set2_right
    datadir_left = r'D:\Dropbox\SINTEF\experiments\NEWLEFT2_10x3000'
    datadir_right = r'D:\Dropbox\SINTEF\experiments\NEWRIGHT2_10x3000'
    rectified_images_dir = Directories.rectified_images

#class SVSParametrization:
#    imageset_left = ImageSets.opencv_sample_left
#    imageset_right = ImageSets.opencv_sample_right
#    datadir_left = r'D:\Dropbox\SINTEF\experiments\opencv_sample_left_7x1000'
#    datadir_right = r'D:\Dropbox\SINTEF\experiments\opencv_sample_right_7x1000'
#    rectified_images_dir = Directories.rectified_images    
    
class StereoMatching:
    pass
    
    
    
    

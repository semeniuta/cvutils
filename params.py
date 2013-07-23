# -*- coding: utf-8 -*-

class Directories:
    pickle_data = r'D:\Dropbox\SINTEF\pickle_data'
    experiment_results = r'D:\Dropbox\SINTEF\experiments'
    rectified_images = r'D:\Dropbox\SINTEF\rectified'

class ImageSets:
    first_four = (r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp', (7, 7), 2.9, 'first_four')
    opencv_sample = (r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg', (9, 6), 1.0, 'opencv_sample')
    new_set_1 = (r'D:\Dropbox\SINTEF\img\Camera1-1\*.bmp', (8, 7), 2.9, 'new_set_left')
    new_set_2 = (r'D:\Dropbox\SINTEF\img\Camera2-1\*.bmp', (8, 7), 2.9, 'new_set_right')

class CalibrationExperiment:
    sample_size = 7
    num_of_samples = 300    
    imageset = ImageSets.opencv_sample    
    results_dir = Directories.experiment_results
    
class DataDirs:
    left = r'D:\Dropbox\SINTEF\experiments\LEFT_20x2000'
    right = r'D:\Dropbox\SINTEF\experiments\RIGHT_20x2000'
# -*- coding: utf-8 -*-

import os

class Directories:
    pickle_data = r'D:\Dropbox\SINTEF\pickle_data'
    experiment_results = r'D:\Dropbox\SINTEF\experiments'

class ImageSets:
    first_four = (r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp', (7, 7), 2.9, os.path.join(Directories.pickle_data, 'first_four.pickle'), 'first_four')
    opencv_sample = (r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg', (9, 6), 1.0, os.path.join(Directories.pickle_data, 'opencv_sample.pickle'), 'opencv_sample')
    new_set_1 = (r'D:\Dropbox\SINTEF\img\Camera1-1\*.bmp', (8, 7), 2.9, os.path.join(Directories.pickle_data, 'new_set_1.pickle'), 'new_set_left')
    new_set_2 = (r'D:\Dropbox\SINTEF\img\Camera2-1\*.bmp', (8, 7), 2.9, os.path.join(Directories.pickle_data, 'new_set_2.pickle'), 'new_set_right')

class CalibrationExperiment:
    sample_size = 7
    num_of_tests = 100    
    imageset = ImageSets.opencv_sample    
    results_dir = Directories.experiment_results
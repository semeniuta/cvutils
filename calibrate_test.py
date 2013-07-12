from cvexperiments import calibration_experiments as calexp

''' Different image sets for testing '''
first_four = (r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp', (7, 7), 2.9, 'data/first_four.pickle')
opencv_sample = (r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg', (9, 6), 1.0, 'data/opencv_sample.pickle')
new_set_1 = (r'D:\Dropbox\SINTEF\img\Camera1-1\*.bmp', (8, 7), 2.9, 'data/new_set_1.pickle')
new_set_2 = (r'D:\Dropbox\SINTEF\img\Camera2-1\*.bmp', (8, 7), 2.9, 'data/new_set_2.pickle')

''' Sample  testing parameters'''
sample_size = 10
num_of_tests = 500

images_mask, pattern_size, square_size, data_file = new_set_2

results_dir = 'D:\Dropbox\SINTEF\experiments'

calexp.different_samples_experiment(images_mask, pattern_size, square_size, data_file, sample_size, num_of_tests, results_dir)
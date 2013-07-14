from cvexperiments import calibration_experiments as calexp

''' Different image sets for testing '''
first_four = (r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp', (7, 7), 2.9, 'data/first_four.pickle', 'first_four')
opencv_sample = (r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg', (9, 6), 1.0, 'data/opencv_sample.pickle', 'opencv_sample')
new_set_1 = (r'D:\Dropbox\SINTEF\img\Camera1-1\*.bmp', (8, 7), 2.9, 'data/new_set_1.pickle', 'new_set_left')
new_set_2 = (r'D:\Dropbox\SINTEF\img\Camera2-1\*.bmp', (8, 7), 2.9, 'data/new_set_2.pickle', 'new_set_right')

''' Sample  testing parameters'''
sample_size = 20
num_of_tests = 2000

images_mask, pattern_size, square_size, data_file, experiment_name = new_set_2

results_dir = 'D:\Dropbox\SINTEF\experiments'

calexp.different_samples_experiment(images_mask, pattern_size, square_size, data_file, sample_size, num_of_tests, results_dir, experiment_name)
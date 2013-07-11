from cvhelpers import calibration
from cvhelpers import images
import random
import numpy as np
import cv2
import os
import cPickle as pickle
import time

start = time.time()

''' Different image sets for testing '''
first_four = (r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp', (7, 7), 2.9, 'data/first_four.pickle')
opencv_sample = (r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg', (9, 6), 1.0, 'data/opencv_sample.pickle')
new_set_1 = (r'D:\Dropbox\SINTEF\img\Camera1-1\*.bmp', (8, 7), 2.9, 'data/new_set_1.pickle')
new_set_2 = (r'D:\Dropbox\SINTEF\img\Camera2-1\*.bmp', (8, 7), 2.9, 'data/new_set_2.pickle')

''' Sample  testing parameters'''
sample_size = 20
num_of_tests = 100

images_mask, pattern_size, square_size, data_file = new_set_1

''' Open the images and find chessboard corners on them '''
if not os.path.exists(data_file):
    opened_images = images.open_images_from_mask(images_mask)
    chessboard_corners_results = [cv2.findChessboardCorners(img, pattern_size) for img in opened_images]
    found = [res[0] for res in chessboard_corners_results]    
    with open(data_file, 'wb') as f:
        pickle.dump(opened_images, f)
        pickle.dump(chessboard_corners_results, f)
else:
    with open(data_file, 'rb') as f:
        print 'Loading from file %s' % data_file
        opened_images = pickle.load(f)
        chessboard_corners_results = pickle.load(f)

''' Filter out the images that failed during the cv2.findChessboardCorners call'''
filtered_images = []
filtered_chessboard_corners_results = []
for i in range(len(found)):
    if found[i]:
        filtered_images.append(opened_images[i])
        filtered_chessboard_corners_results.append(chessboard_corners_results[i])
        
''' Calibrate camera '''
res = calibration.calibrate_camera(filtered_images, pattern_size, square_size, filtered_chessboard_corners_results)
camera_matrix = res[1]

print 'All images:'
print camera_matrix

''' Samples testing ''' 
num_of_images_total = len(filtered_images)
tests = []
for i in range(num_of_tests):
    sample = [random.randint(0, num_of_images_total - 1) for j in range(sample_size)]
    tests.append(sample)
    
camera_matrices = []
for t in tests:
    sample_images = [filtered_images[el] for el in t]
    sample_corners = [filtered_chessboard_corners_results[el] for el in t]
    
    print 'Sample %s:' % t
    res = calibration.calibrate_camera(sample_images, pattern_size, square_size, sample_corners)
    camera_matrix = res[1]
    print camera_matrix    
    
    camera_matrices.append(np.array(camera_matrix))
    
print 'Averaged matrix:'
avg_matrix = camera_matrices[0]
for i in range(1, len(camera_matrices)):
    avg_matrix += camera_matrices[i]
avg_matrix /= num_of_tests
print avg_matrix

finish = time.time()
print 'It took %f seconds to execute' % (finish - start)

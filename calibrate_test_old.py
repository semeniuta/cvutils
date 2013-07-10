from glob import glob
from cvhelpers import calibration
import random
import numpy as np

# PARAMETERS

first_four = (r'D:\Dropbox\SINTEF\img\first_four\*_0.bmp', (7, 7), 2.9)
opencv_sample = (r'D:\Dropbox\SINTEF\img\opencv_sample\left*.jpg', (9, 6), 1.0)
new_set_1 = (r'D:\Dropbox\SINTEF\img\Camera1-1\*.bmp', (8, 7), 2.9)

images_mask, pattern_shape, square_size = new_set_1

image_names = glob(images_mask)

sample_size = 30
num_of_tests = 3
num_of_images_total = len(image_names)
tests = []
for i in range(num_of_tests):
    sample = [random.randint(0, num_of_images_total - 1) for j in range(sample_size)]
    tests.append(sample)
    
camera_matrices = []
for t in tests:
    sample_images = [image_names[el] for el in t]
    
    print 'Calibration sample %s using cvhelpers.calibration' % t
    res, failures = calibration.calibrate_camera_old(sample_images, pattern_shape, square_size)
    print 'Failure indices: %s' % failures
    camera_matrix = res[1]
    print camera_matrix    
    
    camera_matrices.append(np.array(camera_matrix))
    
print 'Averaged matrix:'
avg_matrix = camera_matrices[0]
for i in range(1, len(camera_matrices)):
    avg_matrix += camera_matrices[i]
avg_matrix /= num_of_tests
print avg_matrix
    









     
    






    

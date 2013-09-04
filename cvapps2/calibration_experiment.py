from cvfunctions import calibration
from cvfunctions import chessboard
from cvfunctions import output
from generalfunctions import sampling
import numpy as np
import os
import csv
import time
import sys
import cv2

def conduct_calibration_experiment(imageset, images, corners, samples, findcbc_flags):
    ''' 
    Conducts an experiment on a given set of images with invoking the calibration
    algorithm on a number of samples of randomly chosen images from the set. 

    Arguments:
    images_mask -- a masked string defining the path to the image set
    pattern_size -- dimmension of the chessboard pattern, e.g. (7, 8)
    square_size -- size of a square edge on the chessboard
    data_file -- path to the pickle file for saving/restoring image processing data
    sample_size -- size of the samples taken for calibration
    nsamples -- number of samples to be tested
    experiments_dir -- directory in which the results of the experiment are to be saved
    experiment_name -- short string defining the name of current experiment
    special_flags -- TODo
    ''' 
#    start = time.time()    
#    
#    experiment_start_label = time.strftime('%Y-%m-%d_%H%M%S', time.localtime(start))
#    current_dir = '%dx%d_%s' % (sample_size, nsamples, experiment_name)
#    results_dir = os.path.join(experiments_dir, current_dir)
#    if os.path.exists(results_dir):
#        results_dir += ('_%s' % experiment_start_label) 
#    os.makedirs(results_dir)    
    
  
    ''' Samples testing '''     
#    samples_filename = os.path.join(results_dir, 'samples_combinations.csv')
#    sampling.write_samples_to_file(samples, samples_filename)        
        
    res_table = []
    
    print 'Calibrating the camera using random samples of images:'
    sample_index = 1
    for s in samples:
        sample_images = [images[ind] for ind in s]
        sample_corners = [corners[ind] for ind in s]
        
        res = calibration.calibrate_camera(sample_images, imageset.pattern_size, imageset.square_size, sample_corners)
        res_row = calibration.get_intrinsics_as_a_tuple(res)
        res_table.append(res_row)
        
        sys.stdout.write('%d ' % sample_index)
        sample_index += 1
    print '\n'
    
    return res_table
    
#    with open(os.path.join(results_dir, 'samples_calibration.csv'), 'wb') as calib_res_file:
#        write_calibration_results_to_file(res_table, calib_res_file)

#    ''' Create and save histograms '''
#    res_table_arr = np.array(res_table)
#    fx = res_table_arr[:, 1]
#    fy = res_table_arr[:, 2]
#    cx = res_table_arr[:, 3]
#    cy = res_table_arr[:, 4]
#    k1 = res_table_arr[:, 5]
#    k2 = res_table_arr[:, 6]
#    p1 = res_table_arr[:, 7]
#    p2 = res_table_arr[:, 8]
#    k3 = res_table_arr[:, 9]
# 
#    nbins = 100
#    
#    output.create_and_save_histogram(fx, nbins, 'fx', os.path.join(results_dir, 'fx_hist.png'))
#    output.create_and_save_histogram(fy, nbins, 'fy', os.path.join(results_dir, 'fy_hist.png'))
#    output.create_and_save_histogram(cx, nbins, 'cx', os.path.join(results_dir, 'cx_hist.png'))
#    output.create_and_save_histogram(cy, nbins, 'cy', os.path.join(results_dir, 'cy_hist.png'))
#    output.create_and_save_histogram(k1, nbins, 'k1', os.path.join(results_dir, 'k1_hist.png'))
#    output.create_and_save_histogram(k2, nbins, 'k2', os.path.join(results_dir, 'k2_hist.png'))
#    output.create_and_save_histogram(p1, nbins, 'p1', os.path.join(results_dir, 'p1_hist.png'))
#    output.create_and_save_histogram(p2, nbins, 'p2', os.path.join(results_dir, 'p2_hist.png'))
#    output.create_and_save_histogram(k3, nbins, 'k3', os.path.join(results_dir, 'k3_hist.png'))

#def write_calibration_results_to_file(res_table, f): 
#    ''' 
#    Saves the result of the calibration experiment to the specified CSV file
#    '''
#    columns = ['rms', 'fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']    
#    w = csv.writer(f)
#    w.writerow(columns)
#        
#    for row in res_table:    
#        w.writerow(row)
#        
#def write_images_list_to_file(images_list, f):
#    w = csv.writer(f)    
#    for i in range(len(images_list)):
#        fname = images_list[i]        
#        row = [i, fname]
#        w.writerow(row)    

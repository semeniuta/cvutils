from cvhelpers import calibration
from cvhelpers import images
import random
import numpy as np
import cv2
import os
import cPickle as pickle
import matplotlib.pyplot as plt
import csv
import time

def different_samples_experiment(images_mask, pattern_size, square_size, data_file, sample_size, num_of_tests, experiments_dir, experiment_name):
    
    start = time.time()    
    
    experiment_start_label = time.strftime('%y-%m-%d_%H%M%S', time.localtime(start))
    current_dir = '%s_%s' % (experiment_start_label, experiment_name)
    results_dir = os.path.join(experiments_dir, current_dir)
    os.makedirs(results_dir)
    
    ''' Open the images and find chessboard corners on them '''
    if not os.path.exists(data_file):
        opened_images = images.open_images_from_mask(images_mask)
        chessboard_corners_results = [cv2.findChessboardCorners(img, pattern_size) for img in opened_images]    
        with open(data_file, 'wb') as f:
            pickle.dump(opened_images, f)
            pickle.dump(chessboard_corners_results, f)
    else:
        with open(data_file, 'rb') as f:
            print 'Loading from file %s' % data_file
            opened_images = pickle.load(f)
            chessboard_corners_results = pickle.load(f)
    
    found = [res[0] for res in chessboard_corners_results]
    
    ''' Filter out the images that failed during the cv2.findChessboardCorners call'''
    filtered_images = []
    filtered_chessboard_corners_results = []
    for i in range(len(found)):
        if found[i]:
            filtered_images.append(opened_images[i])
            filtered_chessboard_corners_results.append(chessboard_corners_results[i])
            
    ''' Calibrate camera '''
    res = calibration.calibrate_camera(filtered_images, pattern_size, square_size, filtered_chessboard_corners_results)    
    res_table = [calibration.get_calibration_results_as_a_tuple(res)]     
    with open(os.path.join(results_dir, 'all_images_calibration.csv'), 'wb') as f:    
        write_calibration_results_to_file(res_table, f)
  
    ''' Samples testing ''' 
    num_of_images_total = len(filtered_images)
    tests = []
    for i in range(num_of_tests):
        sample = [random.randint(0, num_of_images_total - 1) for j in range(sample_size)]
        tests.append(sample)

    res_table = []
    
    for t in tests:
        sample_images = [filtered_images[el] for el in t]
        sample_corners = [filtered_chessboard_corners_results[el] for el in t]
        
        res = calibration.calibrate_camera(sample_images, pattern_size, square_size, sample_corners)
        res_row = calibration.get_calibration_results_as_a_tuple(res)
        res_table.append(res_row)
    
    with open(os.path.join(results_dir, 'samples_calibration.csv'), 'wb') as calib_res_file:
        write_calibration_results_to_file(res_table, calib_res_file)

    ''' Create and save histograms '''
    res_table_arr = np.array(res_table)
    fx = res_table_arr[:, 1]
    fy = res_table_arr[:, 2]
    cx = res_table_arr[:, 3]
    cy = res_table_arr[:, 4]
    k1 = res_table_arr[:, 5]
    k2 = res_table_arr[:, 6]
    p1 = res_table_arr[:, 7]
    p2 = res_table_arr[:, 8]
    k3 = res_table_arr[:, 9]
 
    nbins = 100
    
    create_and_save_histogram(fx, nbins, 'fx', os.path.join(results_dir, 'fx_hist.png'))
    create_and_save_histogram(fy, nbins, 'fy', os.path.join(results_dir, 'fy_hist.png'))
    create_and_save_histogram(cx, nbins, 'cx', os.path.join(results_dir, 'cx_hist.png'))
    create_and_save_histogram(cy, nbins, 'cy', os.path.join(results_dir, 'cy_hist.png'))
    create_and_save_histogram(k1, nbins, 'k1', os.path.join(results_dir, 'k1_hist.png'))
    create_and_save_histogram(k2, nbins, 'k2', os.path.join(results_dir, 'k2_hist.png'))
    create_and_save_histogram(p1, nbins, 'p1', os.path.join(results_dir, 'p1_hist.png'))
    create_and_save_histogram(p2, nbins, 'p2', os.path.join(results_dir, 'p2_hist.png'))
    create_and_save_histogram(k3, nbins, 'k3', os.path.join(results_dir, 'k3_hist.png'))
            
def write_calibration_results_to_file(res_table, f): 
    columns = ['rms', 'fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']    
    w = csv.writer(f)
    w.writerow(columns)
        
    for row in res_table:    
        w.writerow(row)
    
def create_and_save_histogram(data, nbins, title, filename):
    plt.figure()    
    plt.hist(data, nbins)
    plt.title(title)
    plt.savefig(filename)

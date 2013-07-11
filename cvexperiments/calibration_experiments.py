from cvhelpers import calibration
from cvhelpers import images
import random
import numpy as np
import cv2
import os
import cPickle as pickle
import time
import matplotlib.pyplot as plt

def different_samples_experiment(images_mask, pattern_size, square_size, data_file, sample_size, num_of_tests, experiments_dir=None):
    
    start = time.time()

    experiment_start_label = time.strftime('%y-%m-%d_%H%M', time.localtime(start))
    results_dir = os.path.join(experiments_dir, experiment_start_label)
    os.makedirs(results_dir)
    crf = open(os.path.join(results_dir, 'calibration_results.txt'), 'w')
    
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
    camera_matrix = res[1]    
    
    crf.write('Calibration results using all the images\n')
    write_calibration_results_to_file(res, crf)
  
    ''' Samples testing ''' 
    num_of_images_total = len(filtered_images)
    tests = []
    for i in range(num_of_tests):
        sample = [random.randint(0, num_of_images_total - 1) for j in range(sample_size)]
        tests.append(sample)
        
    camera_matrices = []
    
    fx_list = []
    fy_list = []
    cx_list = []
    cy_list = []
    
    for t in tests:
        sample_images = [filtered_images[el] for el in t]
        sample_corners = [filtered_chessboard_corners_results[el] for el in t]
        
        res = calibration.calibrate_camera(sample_images, pattern_size, square_size, sample_corners)
        camera_matrix = res[1]        
        
        crf.write('Calibration results using sanple %s\n' % t)
        write_calibration_results_to_file(res, crf)
        
        fx, fy, cx, cy = calibration.get_camera_intrinsic_parameters(camera_matrix)
        fx_list.append(fx)
        fy_list.append(fy)
        cx_list.append(cx)
        cy_list.append(cy)
            
        camera_matrices.append(np.array(camera_matrix))
        
    avg_matrix = camera_matrices[0]
    for i in range(1, len(camera_matrices)):
        avg_matrix += camera_matrices[i]
    avg_matrix /= num_of_tests
    
    crf.write('Averaged matrix:\n')    
    crf.write('%s\n' % avg_matrix)
    
    fxmin, fxmax = min(fx_list), max(fx_list)
    fymin, fymax = min(fy_list), max(fy_list)
    cxmin, cxmax = min(cx_list), max(cx_list)
    cymin, cymax = min(cy_list), max(cy_list)
    
    crf.write('fx: MIN=%f, MAX=%f, SPREAD=%f' % (fxmin, fxmax, fxmax - fxmin))
    crf.write('fy: MIN=%f, MAX=%f, SPREAD=%f' % (fymin, fymax, fymax - fymin))
    crf.write('cx: MIN=%f, MAX=%f, SPREAD=%f' % (cxmin, cxmax, cxmax - cxmin))
    crf.write('cy: MIN=%f, MAX=%f, SPREAD=%f' % (cymin, cymax, cymax - cymin))
    
    nbins = 100
    create_and_save_histogram(fx_list, nbins, 'fx', os.path.join(results_dir, 'fx_hist.png'))
    create_and_save_histogram(fy_list, nbins, 'fy', os.path.join(results_dir, 'fy_hist.png'))
    create_and_save_histogram(cx_list, nbins, 'cx', os.path.join(results_dir, 'cx_hist.png'))
    create_and_save_histogram(cy_list, nbins, 'cy', os.path.join(results_dir, 'cy_hist.png'))
    
    crf.close()    
    
    finish = time.time()
    crf.write('It took %f seconds to execute\n', (finish - start))
    
def write_calibration_results_to_file(res, f):
    rms, camera_matrix, dist_coefs, rvecs, tvecs = res
    f.write('RMS = %f\n' % rms)
    f.write('Camera matrix:\n %s\n' %  camera_matrix)
    f.write('Rotation vectors:\n')    
    #for r in rvecs:
    #    f.write('%s\n' % r)
    #f.write('Translation vectors:\n')        
    #for t in tvecs:
    #    f.write('%s\n' % t)
    f.write('\n')
    
def create_and_save_histogram(data, nbins, title, filename):
    plt.figure()    
    plt.hist(data, nbins)
    plt.title(title)
    plt.savefig(filename)

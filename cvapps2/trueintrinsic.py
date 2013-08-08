# -*- coding: utf-8 -*-

from cvapplications import statsfuncs as sf
from cvfunctions import calibration
from generalfunctions.stats import compute_frequencies
import pandas

def find_true_intrinsics(data, nbins):
    '''
    Finds "true" intrinsic parameters of the camera
    based on experimental data gathered by 
    cvexperiments.calibration_experiment
    
    Arguments:
    d -- dataframe (pandas.DataFrame) object containing the experimental data
    nbins -- TODO
                    
    Returns a tuple containing two elements:
    (1) tuple containing camera matrix and distortion coeffitients (true
    intrinsics)
    (2) pandas.DataFrame object with the colunms rounded in accordance to 
    ndigits_list
    '''        
    
    cols = [col for colname, col in data.iteritems()]
    cols = cols[1:]
        
    ti_values = []
    for c in cols:
        freqs, bins = compute_frequencies(c, nbins)
        max_freq_ind = 0       
        for i in range(1, nbins):
            if freqs[i] > freqs[max_freq_ind]:
                max_freq_ind = i
        ti = bins[max_freq_ind] + (bins[max_freq_ind + 1] - bins[max_freq_ind])/2
        ti_values.append(ti)

    camera_matrix = calibration.get_camera_matrix(ti_values[:4])
    dist_coefs = ti_values[4:]
    res = (camera_matrix, tuple(dist_coefs)) 
    
    return res
    
#    cols = round_dataframe_columns(data, ndigits_list)
#    modes = [sf.calc_mode(c) for c in cols[1:]]
#    
#    camera_matrix = calibration.get_camera_matrix(modes[:4])
#    dist_coefs = modes[4:]
#    
#    colnames = [colname for colname, series in data.iteritems()]    
#    constuctor_dict = dict(zip(colnames, cols))    
#    new_dataframe = pandas.DataFrame(constuctor_dict)
#    

#    
#    return res, new_dataframe
               
    
def expand_ti_tuple(ti_tuple):
    '''
    Expand a tuple that is returned by find_true_intrinsics function to
    tuple containing the following sequence of parameters:
    (fx, fy, cx, cy, k1, k2, p1, p2, k3)
    '''
    camera_matrix, dist_coefs = ti_tuple
    matrix_as_a_tuple = calibration.get_camera_intrinsic_parameters(camera_matrix)
    return matrix_as_a_tuple + dist_coefs
    
def print_statistics(data):
    for colname, series in data.iteritems():
        print colname
        
        maxval = series.max()
        minval = series.min()
        rangeval = maxval - minval        
        
        print minval, maxval, rangeval
        print '%e' % (rangeval / 100)

        


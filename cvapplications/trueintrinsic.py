# -*- coding: utf-8 -*-

from cvapplications import statsfuncs as sf
from cvfunctions import calibration
import pandas

def find_true_intrinsics(data, ndigits_list):
    '''
    Finds "true" intrinsic parameters of the camera
    based on experimental data gathered by 
    cvexperiments.calibration_experiment
    
    Arguments:
    d -- dataframe (pandas.DataFrame) object containing the experimental data
    ndigits_list -- list of number of digits after the decical point to which
                    the numbers will be rounded: each for the dataframe's
                    columns (the first value should be None)
                    
    Returns a tuple containing two elements:
    (1) tuple containing camera matrix and distortion coeffitients (true
    intrinsics)
    (2) pandas.DataFrame object with the colunms rounded in accordance to 
    ndigits_list
    '''        
    
    print_statistics(data)    
    
    cols = round_dataframe_columns(data, ndigits_list)
    modes = [sf.calc_mode(c) for c in cols[1:]]
    
    camera_matrix = calibration.get_camera_matrix(modes[:4])
    dist_coefs = modes[4:]
    
    colnames = [colname for colname, series in data.iteritems()]    
    constuctor_dict = dict(zip(colnames, cols))    
    new_dataframe = pandas.DataFrame(constuctor_dict)
    
    res = (camera_matrix, tuple(dist_coefs))
    
    return res, new_dataframe
    
def round_dataframe_columns(df, ndigits_list): 
    ''' 
    Rounds each column of the dataframes in accordance to the 
    corrsponding number in ndigits_list (number of digits after the
    decimal point). Returns a list of pandas.DataSeries objects    
    '''
    i = 0
    rounded_cols = []
    for colname, series in df.iteritems():
        if ndigits_list[i] == None:
            rounded_cols.append(series)
        else:
            rc = sf.round_dataframe_col(series, ndigits_list[i])
            rounded_cols.append(rc)
        i += 1
    
    return rounded_cols            
    
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


def compute_histogram_nbins(dataseries, ndigits):

    r = dataseries.max() - dataseries.min()
    denom = 1.0 / 10**(ndigits)
    nbins = int(r/denom)
    print nbins
    return nbins
        


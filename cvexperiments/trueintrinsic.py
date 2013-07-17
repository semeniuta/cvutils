# -*- coding: utf-8 -*-

from cvexperiments import statsfuncs as sf
from cvhelpers import calibration
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
    '''        
        
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

def compute_histogram_nbins(dataseries, ndigits):

    r = dataseries.max() - dataseries.min()
    denom = 1.0 / 10**(ndigits)
    nbins = int(r/denom)
    return nbins
    
def expand_ti_tuple(ti_tuple):
    camera_matrix, dist_coefs = ti_tuple
    matrix_as_a_tuple = calibration.get_camera_intrinsic_parameters(camera_matrix)
    return matrix_as_a_tuple + dist_coefs
    

        


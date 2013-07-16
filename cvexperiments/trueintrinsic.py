# -*- coding: utf-8 -*-

from cvexperiments import statsfuncs as sf
from cvhelpers import calibration
import pandas

def find_true_intrinsics(data, ndigits=2):
    '''
    Finds "true" intrinsic parameters of the camera
    based on experimental data gathered by 
    cvexperiments.calibration_experiment
    
    Arguments:
    d -- dataframe (pandas.DataFrame) object containing the experimental data
    ndigits -- number of digits after the decical point to which
               the float numbers will be rounded
    '''        

    rms = data['rms']    
    fx = sf.round_dataframe_col(data['fx'], 0)    
    fy = sf.round_dataframe_col(data['fy'], 0)
    cx = sf.round_dataframe_col(data['cx'], 0)
    cy = sf.round_dataframe_col(data['cy'], 0)    
    k1 = sf.round_dataframe_col(data['k1'], ndigits)
    k2 = sf.round_dataframe_col(data['k2'], ndigits)
    p1 = sf.round_dataframe_col(data['p1'], ndigits)
    p2 = sf.round_dataframe_col(data['p2'], ndigits)
    k3 = sf.round_dataframe_col(data['k3'], ndigits)

    cols = (fx, fy, cx, cy, k1, k2, p1, p2, k3)
    modes = [sf.calc_mode(c) for c in cols]
    
    camera_matrix = calibration.get_camera_matrix(modes[:4])
    dist_coefs = modes[4:]
    
    colnames = [colname for colname, series in data.iteritems()]    
    constuctor_dict = dict(zip(colnames, cols))    
    new_dataframe = pandas.DataFrame(constuctor_dict)
    
    res = (camera_matrix, dist_coefs)
    
    return res, new_dataframe
    
        


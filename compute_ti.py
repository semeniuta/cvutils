# -*- coding: utf-8 -*-
from cvexperiments import trueintrinsic as ti
from cvexperiments import statsfuncs as sf
from cvhelpers import output
import pandas
import os

def read_data(data_dir):
    return pandas.read_csv(os.path.join(data_dir, 'samples_calibration.csv'))  

if __name__ == '__main__':
    ''' Parameters '''
    data_dir_left = r'D:\Dropbox\SINTEF\experiments\LEFT_20x2000' 
    data_dir_right = r'D:\Dropbox\SINTEF\experiments\RIGHT_20x2000' 
    ndigits = 2

    ''' Compute "true intrinsics" for both cameras '''    
    data_dirs = (data_dir_left, data_dir_right)
    dataframes = [read_data(d) for d in data_dirs]
    
    intrinsics = []
    new_dataframes = []

    for df in dataframes:
        res, new_dataframe = ti.find_true_intrinsics(df, ndigits)
        intrinsics.append(res)
        new_dataframes.append(new_dataframe)
    
    ''' Create and save histograms '''
    par = 'k1'
    data = sf.round_dataframe_col(dataframes[0][par], ndigits)
    nbins = 100
    x = intrinsics[0][1][0]
    
    output.create_histogram(data, nbins, par)
    output.draw_vertical_line(x)
    
    
    
    



# -*- coding: utf-8 -*-
from cvexperiments import trueintrinsic as ti
import pandas
import os

def read_data(data_dir):
    return pandas.read_csv(os.path.join(data_dir, 'samples_calibration.csv'))  

if __name__ == '__main__':
    ''' Parameters '''
    data_dir_left = r'D:\Dropbox\SINTEF\experiments\LEFT_20x2000' 
    data_dir_right = r'D:\Dropbox\SINTEF\experiments\RIGHT_20x2000' 
    ndigits = 2

    data_dirs = (data_dir_left, data_dir_right)
    dataframes = [read_data(d) for d in data_dirs]
    intrinsics = [ti.find_true_intrinsics(df, ndigits) for df in dataframes]
    
    
    
    



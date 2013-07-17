# -*- coding: utf-8 -*-
from cvexperiments import trueintrinsic as ti
from cvexperiments import statsfuncs as sf
from cvhelpers import output
import pandas
import os

def read_data(data_dir):
    return pandas.read_csv(os.path.join(data_dir, 'samples_calibration.csv'))  

def create_hist(ndigits, new_dataframes, intrinsics):    
    ''' Create and save histograms '''    
    varnames = ['fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']    
    ndigits_list = [0, 0, 0, 0, ndigits, ndigits, ndigits, ndigits, ndigits]  
      
    lr = ['LEFT', 'RIGHT']
    for j in range(2): 
        cam = lr[j]
        data = new_dataframes[j]
        intr = ti.expand_ti_tuple(intrinsics[j])                 
        for i in range(len(varnames)):
            var = varnames[i]
            series = data[var]            
            nbins = ti.compute_histogram_nbins(series, ndigits_list[i])
            if not nbins == 0:
                output.create_histogram(series, nbins, '%s %s' % (cam, var))
                x = intr[i]               
                output.draw_vertical_line(x)
    
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
    hist_nbins = []
    for df in dataframes:
        res, new_dataframe = ti.find_true_intrinsics(df, ndigits)
        intrinsics.append(res)
        new_dataframes.append(new_dataframe)
    
    #create_hist(ndigits, new_dataframes, intrinsics)

    
    



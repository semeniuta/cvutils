# -*- coding: utf-8 -*-
from cvapplications import trueintrinsic2 as ti
from cvfunctions import output
import pandas
import os
import cPickle as pickle
from params import DataDirsTI

def read_data(data_dir):
    return pandas.read_csv(os.path.join(data_dir, 'samples_calibration.csv'))  

def create_hist(intrinsics, original_dataset, nbibs, imageset_name=''):    
    ''' Create and save histograms '''    
    varnames = ['fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']    
    
    intr = ti.expand_ti_tuple(intrinsics)                 
    for i in range(len(varnames)):
        var = varnames[i]
        series = original_dataset[var]           
        
        output.create_histogram(series, nbins, '%s %s' % (imageset_name, var))
        x = intr[i]               
        output.draw_vertical_line(x)
    
def pickle_results(filename, intrinsics):
    with open(filename, 'wb') as f:
        pickle.dump(intrinsics, f)

def compute_ti(data_dir_left, data_dir_right, nbins, create_histograms):
    ''' Compute "true intrinsics" for both cameras '''    
    data_dirs = {'left': data_dir_left, 'right': data_dir_right}
    
    dataframes = {cam: read_data(ddir) for cam, ddir in data_dirs.iteritems()}
    ti_results = {cam: ti.find_true_intrinsics(dframe, nbins) for cam, dframe in dataframes.iteritems()}
    
    for cam, ti_res in ti_results.iteritems():
        intrinsics = ti_res
        excel_file = os.path.join(data_dirs[cam], 'res_%s.xlsx' % cam)
        pickle_file = os.path.join(data_dirs[cam], 'intrinsics.pickle')        
        output.save_camera_intrinsics_to_excel_file(excel_file, intrinsics)
        pickle_results(pickle_file, intrinsics)
        
    if create_histograms:
        create_hist(ti_results['left'], dataframes['left'], nbins, 'left')
        create_hist(ti_results['right'], dataframes['right'], nbins, 'right')

if __name__ == '__main__':

    create_histograms = True
    nbins = 100
    
    compute_ti(DataDirsTI.left, DataDirsTI.right, nbins, create_histograms)
    
    #data = read_data(DataDirsTI.left)
    #ti.print_statistics(data)

    
    
    



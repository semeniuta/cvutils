# -*- coding: utf-8 -*-
from cvapplications import trueintrinsic as ti
from cvapplications.confmanager import ConfigManager
from cvfunctions import output
import os
from cvclasses.camera import Camera
import shutil
from cvapplications import calibration_experiment as calexp

def create_hist(intrinsics, original_dataset, nbibs, imageset_name, directory):    
    ''' Create and save histograms '''    
    varnames = ['fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']    
    
    hist_dir = os.path.join(directory, 'ti_histograms')
    if not os.path.exists(hist_dir):
        os.makedirs(hist_dir)
    else:
        shutil.rmtree(hist_dir)
        os.makedirs(hist_dir)    
        
    intr = ti.expand_ti_tuple(intrinsics)                 
    for i in range(len(varnames)):
        var = varnames[i]
        series = original_dataset[var]           
        
        title = '%s %s' % (imageset_name, var)  
        filename = os.path.join(hist_dir, '%s_%s.jpg' % (imageset_name, var))
        output.create_histogram(series, nbins, title)
        x = intr[i]               
        output.draw_vertical_line(x)
        output.save_current_figure(filename)

def compute_ti(data_dir_left, data_dir_right, nbins, create_histograms):
    ''' Compute "true intrinsics" for both cameras '''    
    data_dirs = {'left': data_dir_left, 'right': data_dir_right}
    cameras = {'left': Camera(), 'right': Camera()}    
    
    dataframes = {cam: calexp.read_calib_data(ddir) for cam, ddir in data_dirs.iteritems()}
    ti_results = {cam: ti.find_true_intrinsics(dframe, nbins) for cam, dframe in dataframes.iteritems()}
    
    for cam_name, intrinsics in ti_results.iteritems():
        camera = cameras[cam_name]        
        camera.set_intrinsics(intrinsics)
                
        excel_file = os.path.join(data_dirs[cam_name], 'res_%s.xlsx' % cam_name)
        pickle_file = os.path.join(data_dirs[cam_name], 'intrinsics.pickle')        
        
        camera.save_to_excel_file(excel_file)
        camera.pickle(pickle_file)
        
    if create_histograms:
        create_hist(ti_results['left'], dataframes['left'], nbins, 'left', data_dirs['left'])
        create_hist(ti_results['right'], dataframes['right'], nbins, 'right', data_dirs['right'])

if __name__ == '__main__':

    create_histograms = True
    nbins = 100
    
    cm = ConfigManager(conf_dir='..')
    left_dir, right_dir = cm.get_ti_dirs()    
    
    compute_ti(left_dir, right_dir, nbins, create_histograms)


    
    
    



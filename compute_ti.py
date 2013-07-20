# -*- coding: utf-8 -*-
from cvexperiments import trueintrinsic as ti
from cvhelpers import output
import pandas
import os
from xlsxwriter.workbook import Workbook
import cPickle as pickle
from params import DataDirs

def read_data(data_dir):
    return pandas.read_csv(os.path.join(data_dir, 'samples_calibration.csv'))  

def create_hist(intrinsics, original_dataset, imageset_name=''):    
    ''' Create and save histograms '''    
    varnames = ['fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']    
    
    intr = ti.expand_ti_tuple(intrinsics)                 
    for i in range(len(varnames)):
        var = varnames[i]
        series = original_dataset[var]           
        nbins = 100
        
        output.create_histogram(series, nbins, '%s %s' % (imageset_name, var))
        x = intr[i]               
        output.draw_vertical_line(x)

def save_results_to_excel_file(filename, intrinsics):
    wb = Workbook(filename)
    sheet = wb.add_worksheet()
    bold = wb.add_format({'bold': 1})
    sheet.write('B2', 'Camera matrix', bold)
    
    camera_matrix, dist_coefs = intrinsics
    
    rows, cols = camera_matrix.shape
    for i in range(rows):
        for j in range(cols):
            sheet.write(2+i, 1+j, camera_matrix[i, j])
            
    sheet.write('F2', 'Distortion coeffitients', bold)
    for i in range(len(dist_coefs)):
        sheet.write(2, 5+i, dist_coefs[i])
        
    wb.close()
    
def pickle_results(filename, intrinsics):
    with open(filename, 'wb') as f:
        pickle.dump(intrinsics, f)

def compute_ti(data_dir_left, data_dir_right, ndigits_list, create_histograms):
    ''' Compute "true intrinsics" for both cameras '''    
    data_dirs = {'left': data_dir_left, 'right': data_dir_right}
    
    dataframes = {cam: read_data(ddir) for cam, ddir in data_dirs.iteritems()}
    ti_results = {cam: ti.find_true_intrinsics(dframe, ndigits_list) for cam, dframe in dataframes.iteritems()}
    
    for cam, ti_res in ti_results.iteritems():
        intrinsics = ti_res[0]
        excel_file = os.path.join(data_dirs[cam], 'res_%s.xlsx' % cam)
        pickle_file = os.path.join(data_dirs[cam], 'intrinsics.pickle')        
        save_results_to_excel_file(excel_file, intrinsics)
        pickle_results(pickle_file, intrinsics)
        
    if create_histograms:
        create_hist(ti_results['left'][0], dataframes['left'], 'left')

if __name__ == '__main__':
        
    ''' Parameters '''
    ndigits_list = [None, 1, 1, 1, 1, 3, 3, 4, 4, 2]
    create_histograms = False
    
    compute_ti(DataDirs.left, DataDirs.right, ndigits_list, create_histograms)
    
    #data = read_data(DataDirs.left)
    #ti.print_statistics(data)

    
    
    



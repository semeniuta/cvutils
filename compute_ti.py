# -*- coding: utf-8 -*-
from cvexperiments import trueintrinsic as ti
from cvhelpers import output
import pandas
import os
from xlsxwriter.workbook import Workbook

def read_data(data_dir):
    return pandas.read_csv(os.path.join(data_dir, 'samples_calibration.csv'))  

def create_hist(ndigits_list, intrinsics, dataframe, imageset_name=''):    
    ''' Create and save histograms '''    
    varnames = ['fx', 'fy', 'cx', 'cy', 'k1', 'k2', 'p1', 'p2', 'k3']    
    
    intr = ti.expand_ti_tuple(intrinsics)                 
    for i in range(len(varnames)):
        var = varnames[i]
        series = dataframe[var]           
        nbins = ti.compute_histogram_nbins(series, ndigits_list[i])       
        if not nbins == 0:
            output.create_histogram(series, nbins, '%s %s' % (imageset_name, var))
            x = intr[i]               
            output.draw_vertical_line(x)

def find_ti(data_dir, ndigits_list):
    dataframe = read_data(data_dir)
    intrinsics, new_dataframe = ti.find_true_intrinsics(dataframe, ndigits_list)
    return intrinsics, new_dataframe 

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
            
    sheet.write('G2', 'Distortion coeffitients', bold)
    for i in range(len(dist_coefs)):
        sheet.write(2, 6+i, dist_coefs[i])
        
    wb.close()
    
def pickle_results(intrinsics):
    pass
    
if __name__ == '__main__':
        
    ''' Parameters '''
    data_dir_left = r'D:\Dropbox\SINTEF\experiments\LEFT_20x2000' 
    data_dir_right = r'D:\Dropbox\SINTEF\experiments\RIGHT_20x2000' 
    ndigits_list = [None, 2, 2, 2, 2, 3, 3, 3, 3, 3]
    CREATE_HISTOGRAMS = False

    ''' Compute "true intrinsics" for both cameras '''    
    data_dirs = {'left': data_dir_left, 'right': data_dir_right}
    
    ti_results = {cam: find_ti(ddir, ndigits_list) for cam, ddir in data_dirs.iteritems()}
    
    for cam, ti_res in ti_results.iteritems():
        intrinsics = ti_res[0]
        res_file = os.path.join(data_dirs[cam], 'res_%s.xlsx' % cam)
        save_results_to_excel_file(res_file, intrinsics)
        pickle_results(intrinsics)
        
    if CREATE_HISTOGRAMS:
        create_hist(ndigits_list[1:], ti_results['left'][0], ti_results['left'][1], 'left')
    
    



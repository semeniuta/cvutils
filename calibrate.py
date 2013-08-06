# -*- coding: utf-8 -*-

from cvapplications import calibration_experiment as calexp
import argparse
from cvapplications.confmanager import ConfigManager

def initialize_parameters(args=None):
    cm = ConfigManager()    
    
    params = cm.get_calibration_parameters()
    
    sample_size = params['sample_size'] if args.samplesize == None else args.samplesize
    num_of_samples = params['num_of_samples'] if args.nsamples == None else args.nsamples       
    imageset_name = params['imageset'] if  args.imageset == None else args.imageset     
    imageset = cm.get_chessboard_imageset(imageset_name)    
        
    images_mask, pattern_size, square_size, experiment_name = imageset.get_tuple()
    results_dir = cm.get_directory('calibration')
    
    return (images_mask, pattern_size, square_size, sample_size, num_of_samples, results_dir, experiment_name)

def start_experiment(images_mask, pattern_size, square_size, sample_size, num_of_samples, results_dir, experiment_name):
    calexp.different_samples_experiment(images_mask, pattern_size, square_size, sample_size, num_of_samples, results_dir, experiment_name)
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--imageset', help='a masked string defining the path to the image set')  
    parser.add_argument('--samplesize', type=int, help='sample size')
    parser.add_argument('--nsamples', type=int, help='number of samples')  
    args = parser.parse_args()    
    
    parameters = initialize_parameters(args)
    start_experiment(*parameters)


from cvexperiments import calibration_experiments as calexp
import params
import argparse

def initialize_parameters(args=None):
    p = params.CalibrationExperiment    
    
    sample_size = p.sample_size if args.samplesize == None else args.samplesize
    num_of_samples = p.num_of_samples if args.nsamples == None else args.nsamples
    
    if args.imageset == None:
        imageset = p.imageset
    else:
        imageset_name = args.imageset
        imageset = getattr(params.ImageSets, imageset_name)
    
    images_mask, pattern_size, square_size, experiment_name = imageset
    results_dir = p.results_dir
    
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


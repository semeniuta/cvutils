from cvexperiments import calibration_experiments as calexp
import params

def initialize_parameters():
    p = params.CalibrationExperiment    
    
    sample_size = p.sample_size
    num_of_tests = p.num_of_tests    
    images_mask, pattern_size, square_size, data_file, experiment_name = p.imageset
    results_dir = p.results_dir
    
    return (images_mask, pattern_size, square_size, data_file, sample_size, num_of_tests, results_dir, experiment_name)

def start_experiment(images_mask, pattern_size, square_size, data_file, sample_size, num_of_tests, results_dir, experiment_name):
    calexp.different_samples_experiment(images_mask, pattern_size, square_size, data_file, sample_size, num_of_tests, results_dir, experiment_name)
    
if __name__ == '__main__':
    parameters = initialize_parameters()
    start_experiment(*parameters)


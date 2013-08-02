# -*- coding: utf-8 -*-

import random

def generate_list_of_samples(population_size, sample_size, nsamples):
    samples = []
    for i in range(nsamples):
        sample = generate_sample(population_size, sample_size)
        samples.append(sample)
    return samples
        
def generate_sample(population_size, sample_size):
    
    sample = []
    while len(sample) < sample_size:
        rnd = random.randint(0, population_size - 1)
        if rnd not in sample:
            sample.append(rnd)    
    
    return sorted(sample)

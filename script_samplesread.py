# -*- coding: utf-8 -*-

''' 
Script that demonstartes how samples are read 
from CSV file    
'''

import os
from generalfunctions import sampling
from cvapplications.confmanager import ConfigManager

cm = ConfigManager()
params = cm.get_svs_parameters()

samples_filename = os.path.join(params['datadir_left'], 'samples_combinations.csv')
s = sampling.read_samples_from_file(samples_filename)
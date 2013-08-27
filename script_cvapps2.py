# -*- coding: utf-8 -*-

''' 
Script that tests the experimental module cvapps2 
'''

from cvapps2.confmanager import ConfigManager
from cvapps2 import findcbc
from cvapps2 import calibration_experiment as calexp
from cvapps2 import svs_experiment as svsexp

from generalfunctions import sampling

cm = ConfigManager()

''' DATA '''
imageset_left = cm.get_chessboard_imageset('raufoss_set2_left')
imageset_right = cm.get_chessboard_imageset('raufoss_set2_right')

''' VARIABLES '''
findcbc_flags = findcbc.flags_sets['adtresh_or_filquads']
sample_size = 12
nsamples = 15

''' Find chessboard corners and filter out the results '''
res = findcbc.open_images_and_find_corners(imageset_left, imageset_right, findcbc_flags)
corners_left, corners_right, images_left, images_right, filenames_left, filenames_right = res

''' Generate samples '''
nimages = len(images_left)
samples = sampling.generate_list_of_samples(nimages, sample_size, nsamples)

''' Calibration experiment '''
res_left = calexp.conduct_calibration_experiment(imageset_left, images_left, corners_left, samples, findcbc_flags)
res_right = calexp.conduct_calibration_experiment(imageset_right, images_right, corners_right, samples, findcbc_flags)

''' SVS experiment '''
pattern_size = imageset_left.pattern_size
square_size = imageset_left.square_size
svs_res = svsexp.conduct_svs_experiment(images_left, images_right, corners_left, corners_right, res_left, res_right, pattern_size, square_size)


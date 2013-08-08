# -*- coding: utf-8 -*-

import pandas
import os

def read_data(data_dir):
    return pandas.read_csv(os.path.join(data_dir, 'samples_calibration.csv'))  
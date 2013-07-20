# -*- coding: utf-8 -*-

import cPickle as pickle
from params import DataDirs
import os

def unpickle_data(filename):
    with open(filename, 'rb') as f:
        data = pickle.load(f)
    return data
    
if __name__ == '__main__':
    intrinsics_left = unpickle_data(os.path.join(DataDirs.left, 'intrinsics.pickle'))
    intrinsics_right = unpickle_data(os.path.join(DataDirs.right, 'intrinsics.pickle'))
    
    cm = [intrinsics_left[0], intrinsics_right[0]]
    dc = [intrinsics_left[1], intrinsics_right[1]]
    
    
    
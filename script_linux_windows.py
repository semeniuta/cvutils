# -*- coding: utf-8 -*-

''' 
Check whether for the same images OpenCV on different OSes (Linux and Windows)
return the same results
'''

from cvapplications.confmanager import ConfigManager
from cvapplications import cameracalib
from cvfunctions import chessboard
import argparse

cm = ConfigManager()

parser = argparse.ArgumentParser()
parser.add_argument('out')
args = parser.parse_args()

imset = cm.get_chessboard_imageset('raufoss_set2_left')

flags = chessboard.flags['at_or_fq']

res = cameracalib.calibrate_camera(imset, findcbc_flags=flags)

outfile = open('%s.txt' % args.out, 'w')

outfile.writelines([str(obj) + '\n' for obj in res])

outfile.close()
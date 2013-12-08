# -*- coding: utf-8 -*-

''' Scripts display histograms of a set of different images '''

from cvapplications.confmanager import ConfigManager
from cvfunctions import output, images
import os

cm = ConfigManager()

imgdir = os.path.join(cm.get_directory('imagesets'), 'misc_images')

image_files = [os.path.join(imgdir, fname) for fname in os.listdir(imgdir)]
names = [fname.split('.')[0] for fname in os.listdir(imgdir)]
img_list = [images.open_image(fname) for fname in image_files]

output.plot_several_image_histograms(img_list, names)

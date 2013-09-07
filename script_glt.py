# -*- coding: utf-8 -*-

''' Graylevel transofrm '''

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid
import cvfunctions.featuredetection as fd
import cvfunctions.grayleveltransform as glt
import matplotlib.pyplot as plt
from cvfunctions import output
import os

cm = ConfigManager()

imgdir = os.path.join(cm.get_directory('imagesets'), 'misc_images')

image_files = [os.path.join(imgdir, fname) for fname in os.listdir(imgdir)]
names = [fname.split('.')[0] for fname in os.listdir(imgdir)]
img_list = [images.open_image(fname) for fname in image_files]

output.plot_several_image_histograms(img_list, names)

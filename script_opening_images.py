# -*- coding: utf-8 -*-

'''
Evaluating different methods for opening the images

@author Oleksandr Semeniuta
'''

from PIL import Image
import os
from cvfunctions import output

from cvapplications.confmanager import ConfigManager
cm = ConfigManager()

test_imfile = os.path.join(cm.get_directory('imagesets'), 'misc_images', 'kpi.jpg')

im = Image.open(test_imfile)
im_pil_gray = im.convert('L')

output.plot_image(im_pil_gray)



# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager
from cvfunctions import images, pyramid

cm = ConfigManager()

images_left_list = cm.get_imageset_images_list('pyramid_left')
im = images.open_image(images_left_list[3])

dots = pyramid.detect_dots(im)
pyramid.display_dots(im, dots)

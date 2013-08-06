# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager

cm = ConfigManager()

print cm.get_chessboard_imageset('raufoss_set2_left')

print cm.get_calibration_parameters()

print cm.get_ti_dirs()
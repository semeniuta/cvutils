# -*- coding: utf-8 -*-

import os
from cvapplications.confmanager import ConfigManager

def create_directories():
    cm = ConfigManager()
    for key, d in cm.get_directories().iteritems():
        if not os.path.exists(d):        
            os.makedirs(d)
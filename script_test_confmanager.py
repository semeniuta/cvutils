# -*- coding: utf-8 -*-

from cvapplications.confmanager import ConfigManager

cm = ConfigManager()
dirs = cm.get_directories()
d = dirs['imagesets']

print cm.get_root_directory()
print d



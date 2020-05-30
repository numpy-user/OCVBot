import logging as log
import os
import sys

import keyboard

sys.setrecursionlimit(9999)

log.basicConfig(format='%(asctime)s %(filename)s.%(funcName)s - %(message)s'
                , level='INFO')

# TODO: Find a better way to do this.
# Clean up left over screenshots from failed runs.
# sub.Popen(["rm", "./.screenshot2*"])

# Make sure the program's working directory is the directory that this
#   file is located in.
absolute_path = os.path.abspath(__file__)
dir_name = os.path.dirname(absolute_path)
os.chdir(dir_name)


def killer():
    """
    Manually kill script.
    """
    sys.exit(0)


keyboard.add_hotkey('k', killer)

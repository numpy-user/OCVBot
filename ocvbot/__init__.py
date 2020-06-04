"""
Sets up global variables and a few other preparatory checks.
"""
import logging as log
import os
import sys

import pyautogui as pag

sys.setrecursionlimit(9999)

log.basicConfig(format='%(asctime)s %(filename)s.%(funcName)s - %(message)s'
                , level='INFO')

pag.PAUSE = 0

# Make sure the program's working directory is the directory in which
#   this file is located.
absolute_path = os.path.abspath(__file__)
dir_name = os.path.dirname(absolute_path)
os.chdir(dir_name)

# TODO: Find a better way to do this.
# TODO: Add a check to only run this if the OS is Linux.
# Clean up left over screenshots from previous runs.
os.system('rm .screenshot2*.png >/dev/null 2>&1')

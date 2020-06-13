# coding=UTF-8
"""
Sets up global variables and a few other preparatory checks.

"""
import logging as log
import os
import sys

import pyautogui as pag

pag.PAUSE = 0
sys.setrecursionlimit(9999)
log.basicConfig(format='%(asctime)s %(filename)s.%(funcName)s - %(message)s',
                level='INFO')

# Make sure the program's working directory is the directory in which
#   this file is located. If the script is compiled (i.e. "frozen"), a
#   different method must be used.
if hasattr(sys, "frozen"):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))

# TODO: Find a better way to do this.
# Clean up left over screenshots from previous runs.
if os.name == 'posix':
    os.system('rm .screenshot2*.png >/dev/null 2>&1')

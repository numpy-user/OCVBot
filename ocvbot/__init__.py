# coding=UTF-8
"""
Sets up a few global configurations before script is run.

"""
import logging as log
import os
import sys

import pyautogui as pag
import yaml

pag.PAUSE = 0
sys.setrecursionlimit(9999)

with open('./config.yaml') as config:
    config_file = yaml.safe_load(config)

log.basicConfig(format='%(asctime)s %(filename)s.%(funcName)s - %(message)s',
                level=str(config_file['log_level']))

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

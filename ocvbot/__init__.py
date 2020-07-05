# coding=UTF-8
"""
Set up a few global configurations before script is run.

"""
import logging as log
import os
import sys

import pyautogui as pag
import yaml

pag.PAUSE = 0
pag.FAILSAFE = False
sys.setrecursionlimit(9999)

# Make sure the program's working directory is the directory in which
#   this file is located. If the script is compiled (i.e. "frozen"), a
#   different method must be used.
if hasattr(sys, "frozen"):
    os.chdir(os.path.dirname(sys.executable))
else:
    os.chdir(os.path.dirname(__file__))

# Read in the config file.
with open('config.yaml') as config:
    config = yaml.safe_load(config)

log_level = config['main']['log_level']
log.basicConfig(format='%(asctime)s %(filename)s.%(funcName)s - %(message)s',
                level=log_level)

# TODO: Find a better way to do this.
# Clean up left over screenshots from previous runs.
if os.name == 'posix':
    os.system('rm .screenshot2*.png >/dev/null 2>&1')


def kill_script():
    """
    Used to manually terminate the primary thread of execution.

    """
    # TODO: Replace this with psutil.kill().
    os.system('pkill -f main.py')


# This requires sudo privileges, so it's optional.
if config['main']['keyboard_kill'] is True:
    import keyboard
    keyboard.add_hotkey(config['main']['kill_hotkey'], kill_script,)

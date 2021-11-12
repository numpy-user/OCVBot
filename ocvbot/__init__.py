# coding=UTF-8
"""
Setup a few global configurations before script is run.

"""
import logging as log
import os
import sys

import pathlib
import pyautogui as pag
import yaml

pag.PAUSE = 0
pag.FAILSAFE = False
sys.setrecursionlimit(9999)

# Make sure the program's working directory is the directory in which
#   this file is located.
os.chdir(os.path.dirname(__file__))

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)

# Read in the config file.
with open("config.yaml", encoding="utf-8") as config_file:
    config = yaml.safe_load(config_file)

# Configure logging.
log_level = config["main"]["log_level"]
log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level=log_level
)
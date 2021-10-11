# coding=UTF-8
"""
Keeps the OSRS client logged in.

"""
import logging as log
import os
import pathlib
import random as rand
import sys
import yaml

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)

from ocvbot import input, misc, vision as vis

# Focus the client.
input.Mouse(region=vis.chat_menu).click_coord(move_away=True)

with open('../ocvbot/config.yaml') as config:
    config = yaml.safe_load(config)

def kill_script():
    """
    Used to manually terminate the primary thread of execution.

    """
    # TODO: Replace this with psutil.kill().
    os.system('pkill -f main.py')


# This requires sudo privileges, so it's optional.
if config['main']['keyboard_kill'] is True:
    import keyboard
    keyboard.add_hotkey(config['main']['kill_hotkey'], kill_script)

while True:
    # Every 3-5 minutes, hit an arrow key to move the client's camera.
    misc.sleep_rand(180000, 299000)
    key = rand.randint(1, 4)
    log.info('Hitting arrow key')
    if key == 1:
        input.Keyboard().keypress('left')
    elif key == 2:
        input.Keyboard().keypress('right')
    elif key == 3:
        input.Keyboard().keypress('up')
    elif key == 4:
        input.Keyboard().keypress('down')

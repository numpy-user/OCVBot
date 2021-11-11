#!/usr/bin/env python3
# coding=UTF-8
"""
Keeps the OSRS client logged in by randomly pressing an arrow key every
few minutes.

"""
import logging as log
import pathlib
import random as rand
import sys

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)

from ocvbot import inputs
from ocvbot import misc
from ocvbot import vision as vis

vis.init()

def main() -> None:
    # Focus the client by clicking a random spot on the chat menu.
    inputs.Mouse(region=vis.CHAT_MENU).click_coord()

    # Every 100-299 seconds, hit an arrow key to move the client's camera.
    # Auto-logout occurs after 5 minutes (300 seconds) of inactivity.
    while True:
        # Units for sleep_rand() are in miliseconds.
        # 5 min = 300000 miliseconds.
        misc.sleep_rand(100000, 299000)
        roll = rand.randint(1, 4)

        if roll == 1:
            key = "left"
        elif roll == 2:
            key = "right"
        elif roll == 3:
            key = "up"
        else:
            key = "down"

        log.info("Pressing key %s to remain logged in", key)
        inputs.Keyboard().keypress(key)


if __name__ == "__main__":
    main()

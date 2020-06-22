# coding=UTF-8
"""
Keeps the OSRS client logged in.

"""
import random as rand
from ocvbot import input, misc, vision as vis

# Focus the client.
input.Mouse(ltwh=vis.chat_menu).click_coord(move_away=True)

while True:
    # Every 30-120 seconds, hit an arrow key to move the client's camera.
    misc.sleep_rand(30000, 120000)
    key = rand.randint(1, 4)
    if key == 1:
        input.Keyboard().keypress('left')
    elif key == 2:
        input.Keyboard().keypress('right')
    elif key == 3:
        input.Keyboard().keypress('up')
    elif key == 4:
        input.Keyboard().keypress('down')

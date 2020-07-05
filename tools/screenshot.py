# coding=UTF-8
"""
Simple screenshot tool for quickly capturing the OSRS client window.
Linux-only! Requires pngcrush and ImageMagick.

If DEBUG is False, produces an image called
haystack_$(date +%Y-%m-%d_%H:%M:%S).png in the current directory.

Syntax:
    python screnshot.py [DELAY] [DEBUG]

Example:
    python screenshot.py 5 True = Wait 5 seconds before taking screenshot,
                                  enable debugging mode.

Optional positional arguments:

    DELAY (int): The number of seconds to wait before taking the
                 screenshot, default is 0.

    DEBUG (bool): Whether the function will perform extra processing
                  to overlay rectanges onto the screenshot
                  cooresponding to the various coordinate spaces used
                  by the bot, default is False.

"""
import logging as log
import os
import time
import sys

import pyautogui as pag

from ocvbot import vision as vis, startup as start

log.basicConfig(format='%(asctime)s -- %(filename)s.%(funcName)s - %(message)s', level='INFO')
arguments = len(sys.argv)

# If the name of the script is the only argument given, set the optional
#   arguments to their default values.
if arguments == 1:
    delay = 0
    debug = False
elif arguments == 2:
    delay = int(sys.argv[1])
    debug = False
elif arguments == 3:
    delay = int(sys.argv[1])
    debug = bool(sys.argv[2])
else:
    raise Exception('Unsupported arguments!')


def pngcrush():
    log.info('Compressing screenshot...')
    os.system('pngcrush -s /tmp/haystack.tmp2.png /tmp/haystack.tmp.png 2>/dev/null')


def main():
    """
    Takes a screenshot of the OldSchool Runescape client window.

    Automatically censors player's username.

    """
    log.info('Initializing...')
    # Clean up from any previous runs, otherwise the function will break.
    for file in ('/tmp/haystack.tmp.png', '/tmp/haystack.tmp2.png'):
        try:
            os.remove(file)
        except FileNotFoundError:
            pass

    client_status = vis.orient()[0]

    if delay > 0:
        log.info('Waiting %s seconds', delay)
        time.sleep(delay)

    if debug is False:
        pag.screenshot('/tmp/haystack.tmp2.png', region=vis.client)
        pngcrush()

        if client_status == 'logged_in':
            # If the client is logged in, censor the player's username
            #   by drawing a black rectangle over it with ImageMagick.
            os.system('convert /tmp/haystack.tmp.png -fill black -draw "rectangle 7 458 190 473" '
                      '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png"')
        elif client_status == 'logged_out':
            os.system('mv -- "/tmp/haystack.tmp2.png" '
                      '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png"')
        else:
            raise Exception("Could not interpret client_status var!")

    else:
        pag.screenshot('/tmp/haystack.tmp2.png', region=vis.display)
        pngcrush()

        # Import all the coordinate spaces to overlay onto the screenshot.
        # Create a separate file for coordinate space, as some of them
        #   overlap.
        log.info('Creating ocvbot_client.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.client_left)
                  + ' ' + str(vis.client_top)
                  + ' ' + str(vis.client_left + start.CLIENT_WIDTH)
                  + ' ' + str(vis.client_top + start.CLIENT_HEIGHT)
                  + '" ocvbot_client.png')

        log.info('Creating ocvbot_inv.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_left)
                  + ' ' + str(vis.inv_top)
                  + ' ' + str(vis.inv_left + start.INV_WIDTH)
                  + ' ' + str(vis.inv_top + start.INV_HEIGHT)
                  + '" ocvbot_inv.png')

        log.info('Creating inv_bottom_half.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_bottom_left)
                  + ' ' + str(vis.inv_bottom_top)
                  + ' ' + str(vis.inv_bottom_left + start.INV_WIDTH)
                  + ' ' + str(vis.inv_bottom_top + start.INV_HALF_HEIGHT)
                  + '" inv_bottom_half.png')

        log.info('Creating ocvbot_inv_right_half.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_right_half_left)
                  + ' ' + str(vis.inv_right_half_top)
                  + ' ' + str(vis.inv_right_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.inv_right_half_top + start.INV_HEIGHT)
                  + '" ocvbot_inv_right_half.png')

        log.info('Creating ocvbot_inv_left_half.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_left_half_left)
                  + ' ' + str(vis.inv_left_half_top)
                  + ' ' + str(vis.inv_left_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.inv_left_half_top + start.INV_HEIGHT)
                  + '" ocvbot_inv_left_half.png')

        log.info('Creating ocvbot_game_screen.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.game_screen_left)
                  + ' ' + str(vis.game_screen_top)
                  + ' ' + str(vis.game_screen_left + start.GAME_SCREEN_WIDTH)
                  + ' ' + str(vis.game_screen_top + start.GAME_SCREEN_HEIGHT)
                  + '" ocvbot_game_screen.png')

        log.info('Creating ocvbot_side_stones.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.side_stones_left)
                  + ' ' + str(vis.side_stones_top)
                  + ' ' + str(vis.side_stones_left + start.SIDE_STONES_WIDTH)
                  + ' ' + str(vis.side_stones_top + start.SIDE_STONES_HEIGHT)
                  + '" ocvbot_side_stones.png')

        log.info('Creating ocvbot_chat_menu.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.chat_menu_left)
                  + ' ' + str(vis.chat_menu_top)
                  + ' ' + str(vis.chat_menu_left + start.CHAT_MENU_WIDTH)
                  + ' ' + str(vis.chat_menu_top + start.CHAT_MENU_HEIGHT)
                  + '" ocvbot_chat_menu_recent.png')

        log.info('Creating ocvbot_chat_menu_recent.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.chat_menu_recent_left)
                  + ' ' + str(vis.chat_menu_recent_top)
                  + ' ' + str(vis.chat_menu_recent_left + start.CHAT_MENU_RECENT_WIDTH)
                  + ' ' + str(vis.chat_menu_recent_top + start.CHAT_MENU_RECENT_HEIGHT)
                  + '" ocvbot_chat_menu_recent.png')

        log.info('Creating ocvbot_minimap.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.minimap_left)
                  + ' ' + str(vis.minimap_top)
                  + ' ' + str(vis.minimap_left + start.MINIMAP_WIDTH)
                  + ' ' + str(vis.minimap_top + start.MINIMAP_HEIGHT)
                  + '" ocvbot_minimap.png')

        log.info('Creating ocvbot_minimap_slice.png')
        os.system('convert /tmp/haystack.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.minimap_slice_left)
                  + ' ' + str(vis.minimap_slice_top)
                  + ' ' + str(vis.minimap_slice_left + start.MINIMAP_SLICE_WIDTH)
                  + ' ' + str(vis.minimap_slice_top + start.MINIMAP_SLICE_HEIGHT)
                  + '" ocvbot_minimap_slice.png')
    return True


if __name__ == '__main__':
    main()

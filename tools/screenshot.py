# coding=UTF-8
"""
Simple screenshot tool for quickly capturing the OSRS client window.

Linux-only! Requires pngcrush and ImageMagick.

Syntax:
    python screnshot.py [DELAY] [DEBUG]

Example:
    python screenshot.py 5 False = Wait 5 seconds before taking screenshot,
                                   no debugging.

Positional arguments:
    delay (int): The number of seconds to wait before taking the
                 screnshot.

    debug (bool): Whether the function will perform extra processing
                  to overlay rectanges onto the screenshot
                  cooresponding to the various coordinate spaces used
                  by the bot. This takes a second or two, default is
                  false.

                  If set to false, this function produces an image
                  called haystack_$(date +%Y-%m-%d_%H:%M:%S).png in
                  the current directory.

"""
import logging as log
import os
import time
import sys

import pyautogui as pag

from ocvbot import vision as vis, startup as start

log.basicConfig(format='%(asctime)s -- %(filename)s.%(funcName)s - %(message)s', level='INFO')

# If no argument is given, default to 0.
if len(sys.argv) == 1:
    delay = 0
    debug = False
else:
    delay = int(sys.argv[1])
    debug = bool(sys.argv[2])


def main():
    """
    Takes a screenshot of the OldSchool Runescape client window.

    Automatically censors player's username.

    """
    if delay > 0:
        log.info('Waiting %s seconds', delay)
        time.sleep(delay)

    log.info('Initializing...')
    # Remove old screenshots with similar names, otherwise the function
    #   will break.
    os.system('rm -f /tmp/screenshot.tmp*.png')

    if debug is False:
        pag.screenshot('/tmp/screenshot.tmp.png', region=vis.client)
        log.info('Processing screenshot...')

        if vis.client_status == 'logged_in':
            # If the client is logged in, censor the player's username
            #   by drawing a black box over it with ImageMagick.
            os.system('pngcrush -s "/tmp/screenshot.tmp.png" "/tmp/screenshot.tmp2.png" 2>/dev/null '
                      '&& '
                      'convert /tmp/screenshot.tmp2.png -fill black -draw "rectangle 7 458 190 473" '
                      '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png" '
                      '&& '
                      'rm -f /tmp/screenshot.tmp*')
        elif vis.client_status == 'logged_out':
            os.system('pngcrush -s "/tmp/screenshot.tmp.png" '
                      '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png" '
                      '2>/dev/null '
                      '&& '
                      'rm -f /tmp/screenshot.tmp*')
        else:
            raise Exception("Could not interpret client_status var!")

    else:
        pag.screenshot('/tmp/screenshot.tmp2.png', region=vis.display)
        log.info('Processing screenshot...')
        os.system('pngcrush -s /tmp/screenshot.tmp2.png /tmp/screenshot.tmp.png')

        # Import all the coordinate spaces to overlay onto the screenshot.
        # Create a separate file for coordinate space, as some of them
        #   overlap.
        log.info('Creating ocvbot_client.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.client_left)
                  + ' ' + str(vis.client_top)
                  + ' ' + str(vis.client_left + start.CLIENT_WIDTH)
                  + ' ' + str(vis.client_top + start.CLIENT_HEIGHT)
                  + '" ocvbot_client.png')

        log.info('Creating ocvbot_inv.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_left)
                  + ' ' + str(vis.inv_top)
                  + ' ' + str(vis.inv_left + start.INV_WIDTH)
                  + ' ' + str(vis.inv_top + start.INV_HEIGHT)
                  + '" ocvbot_inv.png')

        log.info('Creating inv_bottom_half.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_bottom_left)
                  + ' ' + str(vis.inv_bottom_top)
                  + ' ' + str(vis.inv_bottom_left + start.INV_WIDTH)
                  + ' ' + str(vis.inv_bottom_top + start.INV_HALF_HEIGHT)
                  + '" inv_bottom_half.png')

        log.info('Creating ocvbot_inv_right_half.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_right_half_left)
                  + ' ' + str(vis.inv_right_half_top)
                  + ' ' + str(vis.inv_right_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.inv_right_half_top + start.INV_HEIGHT)
                  + '" ocvbot_inv_right_half.png')

        log.info('Creating ocvbot_inv_left_half.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_left_half_left)
                  + ' ' + str(vis.inv_left_half_top)
                  + ' ' + str(vis.inv_left_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.inv_left_half_top + start.INV_HEIGHT)
                  + '" ocvbot_inv_left_half.png')

        log.info('Creating ocvbot_game_screen.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.game_screen_left)
                  + ' ' + str(vis.game_screen_top)
                  + ' ' + str(vis.game_screen_left + start.GAME_SCREEN_WIDTH)
                  + ' ' + str(vis.game_screen_top + start.GAME_SCREEN_HEIGHT)
                  + '" ocvbot_game_screen.png')

        log.info('Creating ocvbot_side_stones.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.side_stones_left)
                  + ' ' + str(vis.side_stones_top)
                  + ' ' + str(vis.side_stones_left + start.SIDE_STONES_WIDTH)
                  + ' ' + str(vis.side_stones_top + start.SIDE_STONES_HEIGHT)
                  + '" ocvbot_side_stones.png')

        log.info('Creating ocvbot_chat_menu.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.chat_menu_left)
                  + ' ' + str(vis.chat_menu_top)
                  + ' ' + str(vis.chat_menu_left + start.CHAT_MENU_WIDTH)
                  + ' ' + str(vis.chat_menu_top + start.CHAT_MENU_HEIGHT)
                  + '" ocvbot_chat_menu_recent.png')

        log.info('Creating ocvbot_chat_menu_recent.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.chat_menu_recent_left)
                  + ' ' + str(vis.chat_menu_recent_top)
                  + ' ' + str(vis.chat_menu_recent_left + start.CHAT_MENU_RECENT_WIDTH)
                  + ' ' + str(vis.chat_menu_recent_top + start.CHAT_MENU_RECENT_HEIGHT)
                  + '" ocvbot_chat_menu_recent.png')

        log.info('Creating ocvbot_minimap.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.minimap_left)
                  + ' ' + str(vis.minimap_top)
                  + ' ' + str(vis.minimap_left + start.MINIMAP_WIDTH)
                  + ' ' + str(vis.minimap_top + start.MINIMAP_HEIGHT)
                  + '" ocvbot_minimap.png')

        log.info('Creating ocvbot_minimap_slice.png')
        os.system('convert /tmp/screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.minimap_slice_left)
                  + ' ' + str(vis.minimap_slice_top)
                  + ' ' + str(vis.minimap_slice_left + start.MINIMAP_SLICE_WIDTH)
                  + ' ' + str(vis.minimap_slice_top + start.MINIMAP_SLICE_HEIGHT)
                  + '" ocvbot_minimap_slice.png')

        os.system('rm /tmp/screenshot.tmp*.png '
                  '&& '
                  'notify-send -u low "Debug screenshots taken!" 2>/dev/null')
    return True


if __name__ == '__main__':
    main()

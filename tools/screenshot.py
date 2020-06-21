# coding=UTF-8
"""
Simple screenshot tool for quickly capturing the OSRS client window.
Linux-only. Requires pngcrush and ImageMagick.

Optionally allows you to specify the number of seconds to wait before
taking the screenshot on the commandline, default is 0.

"""
import logging as log
import os
import time
import sys

import pyautogui as pag

from ocvbot import vision as vis, startup as start

log.basicConfig(format='%(asctime)s -- %(filename)s.%(funcName)s - %(message)s'
                , level='INFO')

# If no argument is given, default to 0.
if len(sys.argv) == 1:
    delay = 0
else:
    delay = int(sys.argv[1])


def main(debug=False):
    """
    Takes a screenshot of the OldSchool Runescape client window.

    Automatically censors player's username.

    Optionally overlays the coordinates of Vision objects, which can be
    useful for debugging.

    Args:
        debug (bool): Whether the function will perform extra processing
                      to overlay rectanges cooresponding to Vision
                      object coordinates on the screenshot, which takes
                      a second or two, default is False.

                      If set to False, the function produces an image
                      called haystack_$(date +%Y-%m-%d_%H:%M:%S).png in
                      the current directory.

    """
    if delay > 0:
        log.info('Waiting %s seconds', delay)
        time.sleep(delay)

    log.info('Initializing...')
    # Remove old screenshots with similar names, otherwise it will break.
    os.system('rm -f /tmp/screenshot.tmp*')
    pag.screenshot('/tmp/screenshot.tmp.png', region=(vis.client_left,
                                                      vis.client_top,
                                                      start.CLIENT_WIDTH,
                                                      start.CLIENT_HEIGHT))

    if debug is False:
        log.info('Processing screenshot...')
        if vis.client_status == 'logged_in':
            # If the client is logged in, censor the player's username
            #   by drawing a black box over it with ImageMagick.
            os.system(
                'pngcrush -s "/tmp/screenshot.tmp.png" '
                '"/tmp/screenshot.tmp2.png" '
                '2>/dev/null '
                '&& '
                'convert /tmp/screenshot.tmp2.png '
                '-fill black '
                '-draw "rectangle 7 458 190 473" '
                '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png" '
                '&& '
                'rm -f /tmp/screenshot.tmp*')
        elif vis.client_status == 'logged_out':
            os.system('pngcrush -s '
                      '"/tmp/screenshot.tmp.png" '
                      '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png" '
                      '2>/dev/null '
                      '&& '
                      'rm -f /tmp/screenshot.tmp*')
        else:
            raise Exception("Could not interpret client_status var!")

    elif debug is True:
        # Import all the Vision objects to overlay onto the screenshot.

        pag.screenshot('.screenshot.tmp2.png', region=(0, 0,
                                                       start.DISPLAY_WIDTH,
                                                       start.DISPLAY_HEIGHT))
        log.info('Compressing screenshot...')
        os.system('pngcrush -s .screenshot.tmp2.png .screenshot.tmp.png'
                  '&>/dev/null')

        # Create a separate edited file for each Vision object, as some
        #   of the objects' coordinates overlap.
        log.info('Creating client.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.client_left)
                  + ' ' + str(vis.client_top)
                  + ' ' + str(vis.client_left + start.CLIENT_WIDTH)
                  + ' ' + str(vis.client_top + start.CLIENT_HEIGHT)
                  + '" client.png')

        log.info('Creating inv.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_left)
                  + ' ' + str(vis.inv_top)
                  + ' ' + str(vis.inv_left + start.INV_WIDTH)
                  + ' ' + str(vis.inv_top + start.INV_HEIGHT)
                  + '" inv.png')

        log.info('Creating inv_bottom_half.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_bottom_left)
                  + ' ' + str(vis.inv_bottom_top)
                  + ' ' + str(vis.inv_bottom_left + start.INV_WIDTH)
                  + ' ' + str(vis.inv_bottom_top + start.INV_HALF_HEIGHT)
                  + '" inv_bottom_half.png')

        log.info('Creating inv_right_half.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_right_half_left)
                  + ' ' + str(vis.inv_right_half_top)
                  + ' ' + str(vis.inv_right_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.inv_right_half_top + start.INV_HEIGHT)
                  + '" inv_right_half.png')

        log.info('Creating inv_left_half.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.inv_left_half_left)
                  + ' ' + str(vis.inv_left_half_top)
                  + ' ' + str(vis.inv_left_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.inv_left_half_top + start.INV_HEIGHT)
                  + '" inv_left_half.png')

        log.info('Creating game_screen.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.game_screen_left)
                  + ' ' + str(vis.game_screen_top)
                  + ' ' + str(vis.game_screen_left + start.GAME_SCREEN_WIDTH)
                  + ' ' + str(vis.game_screen_top + start.GAME_SCREEN_HEIGHT)
                  + '" game_screen.png')

        log.info('Creating chat_menu.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.chat_menu_left)
                  + ' ' + str(vis.chat_menu_top)
                  + ' ' + str(vis.chat_menu_left + start.CHAT_MENU_WIDTH)
                  + ' ' + str(vis.chat_menu_top + start.CHAT_MENU_HEIGHT)
                  + '" chat_menu_recent.png')

        log.info('Creating chat_menu_recent.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.chat_menu_recent_left)
                  + ' ' + str(vis.chat_menu_recent_top)
                  + ' ' + str(vis.chat_menu_recent_left +
                              start.CHAT_MENU_RECENT_WIDTH)
                  + ' ' + str(vis.chat_menu_recent_top +
                              start.CHAT_MENU_RECENT_HEIGHT)
                  + '" chat_menu_recent.png')

        os.system('rm .screenshot.tmp*.png && '
                  'notify-send -u low "Debug screenshots taken!"')
        return True
    return True


if __name__ == '__main__':
    main()

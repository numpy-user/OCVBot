import logging as log
import os

import pyautogui as pag

from ocvbot import vision as vis, startup as start

log.basicConfig(format='%(asctime)s -- %(filename)s.%(funcName)s - %(message)s'
                , level='INFO')


def main(debug=False):
    """
    Takes a screenshot of the OldSchool Runescape client window.

    Automatically censors player's username.

    Optionally overlays the coordinates of Vision objects, which can be
    useful for debugging. This function is designed to be run manually.


    Args:
        debug (bool): Whether the function will perform extra processing
                      to overlay rectanges cooresponding to Vision
                      object coordinates on the screenshot, which takes
                      a second or two, default is False. If set to
                      False, the function produces an image called
                      haystack_$(date +%Y-%m-%d_%H:%M:%S).png in the
                      current directory.

    Returns:
        Always returns 0.
    """

    log.info('Initializing')

    pag.screenshot('/tmp/screenshot.tmp.png', region=(vis.vclient_left,
                                                      vis.vclient_top,
                                                      start.CLIENT_WIDTH,
                                                      start.CLIENT_HEIGHT))

    if debug is False:
        log.info('Processing screenshot')
        if vis.client_status == 'logged_in':
            # If the client is logged in, censor the player's username
            #   by drawing a black box over it with ImageMagick.
            import time
            time.sleep(1)
            os.system('pngcrush -s '
                      '"/tmp/screenshot.tmp.png" '
                      '"/tmp/screenshot.tmp2.png" '
                      '2>/dev/null '
                      '&& convert /tmp/screenshot.tmp2.png '
                      '-fill black '
                      '-draw "rectangle 7 458 190 473" '
                      '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png"')
        elif vis.client_status == 'logged_out':
            os.system('pngcrush -s '
                      '/tmp/screenshot.tmp.png" '
                      '"$(pwd)/haystack_$(date +%Y-%m-%d_%H:%M:%S).png" '
                      '2>/dev/null')
        else:
            raise RuntimeError("Could not interpret client_status var!")

    elif debug is True:
        # Import all the Vision objects to overlay onto the screenshot.

        pag.screenshot('.screenshot.tmp2.png', region=(0, 0,
                                                       start.DISPLAY_WIDTH,
                                                       start.DISPLAY_HEIGHT))
        log.info('Compressing screenshot')
        os.system('pngcrush -s .screenshot.tmp2.png .screenshot.tmp.png'
                  '&>/dev/null')

        # Create a separate edited file for each Vision object, as some
        #   of the objects' coordinates overlap.
        log.info('Creating client.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vclient_left)
                  + ' ' + str(vis.vclient_top)
                  + ' ' + str(vis.vclient_left + start.CLIENT_WIDTH)
                  + ' ' + str(vis.vclient_top + start.CLIENT_HEIGHT)
                  + '" client.png')

        log.info('Creating inv.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vinv_left)
                  + ' ' + str(vis.vinv_top)
                  + ' ' + str(vis.vinv_left + start.INV_WIDTH)
                  + ' ' + str(vis.vinv_top + start.INV_HEIGHT)
                  + '" inv.png')

        log.info('Creating inv_bottom_half.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vinv_bottom_left)
                  + ' ' + str(vis.vinv_bottom_top)
                  + ' ' + str(vis.vinv_bottom_left + start.INV_WIDTH)
                  + ' ' + str(vis.vinv_bottom_top + start.INV_HALF_HEIGHT)
                  + '" inv_bottom_half.png')

        log.info('Creating inv_right_half.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vinv_right_half_left)
                  + ' ' + str(vis.vinv_right_half_top)
                  + ' ' + str(vis.vinv_right_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.vinv_right_half_top + start.INV_HEIGHT)
                  + '" inv_right_half.png')

        log.info('Creating inv_left_half.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vinv_left_half_left)
                  + ' ' + str(vis.vinv_left_half_top)
                  + ' ' + str(vis.vinv_left_half_left + start.INV_HALF_WIDTH)
                  + ' ' + str(vis.vinv_left_half_top + start.INV_HEIGHT)
                  + '" inv_left_half.png')

        log.info('Creating game_screen.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vgame_screen_left)
                  + ' ' + str(vis.vgame_screen_top)
                  + ' ' + str(vis.vgame_screen_left + start.GAME_SCREEN_WIDTH)
                  + ' ' + str(vis.vgame_screen_top + start.GAME_SCREEN_HEIGHT)
                  + '" game_screen.png')

        log.info('Creating chat_menu.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vchat_menu_left)
                  + ' ' + str(vis.vchat_menu_top)
                  + ' ' + str(vis.vchat_menu_left + start.CHAT_MENU_WIDTH)
                  + ' ' + str(vis.vchat_menu_top + start.CHAT_MENU_HEIGHT)
                  + '" chat_menu_recent.png')

        log.info('Creating chat_menu_recent.png')
        os.system('convert .screenshot.tmp.png '
                  '-fill red '
                  '-draw "rectangle '
                  + str(vis.vchat_menu_recent_left)
                  + ' ' + str(vis.vchat_menu_recent_top)
                  + ' ' + str(vis.vchat_menu_recent_left + start.CHAT_MENU_RECENT_WIDTH)
                  + ' ' + str(vis.vchat_menu_recent_top + start.CHAT_MENU_RECENT_HEIGHT)
                  + '" chat_menu_recent.png')

        os.system('rm .screenshot.tmp*.png && '
                  'notify-send -u low "Debug screenshots taken!"')
        return 0

    return 0


if __name__ == '__main__':
    main()

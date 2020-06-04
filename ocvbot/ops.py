# The OSRS Positioning System

import logging as log
import os

import pyautogui

from ocvbot import input


def main():
    os.chdir('/home/austin/ocvbot/ocvbot')
    # Find chunk within world
    # chunk = pyautogui.locate('./world3-6.png',
    # './world.png', confidence=0.9)
    # Break up chunk tuple
    # (chunk_left, chunk_top, chunk_width, chunk_height) = chunk
    chunk_left = 4608
    chunk_top = 2304

    # Find needle within chunk
    needle = pyautogui.locate('./minimap-slice.png',
                              './world3-6.png', confidence=0.7)
    print("needle is", needle)
    (needle_chunk_left, needle_chunk_top, needle_width, needle_height) = needle

    # Get needle coordinates relative to world
    needle_world_left = needle_chunk_left + chunk_left
    needle_world_top = needle_chunk_top + chunk_top

    # Get center of needle within world
    needle_world_center_x = int(
        (needle_world_left + needle_width) - (needle_width / 2))
    needle_world_center_y = int(
        (needle_world_top + needle_height) - (needle_height / 2))

    # Get center of needle within client window
    from ocvbot.vision import client
    print("vclient is", client)
    needle_client_center = client.wait_for_image(loctype='center',
                                                 needle='/home/austin/ocvbot/'
                                                  'ocvbot/minimap-slice.png',
                                                 loop_num=1)
    (needle_client_center_x, needle_client_center_y) = needle_client_center

    # Get destination
    dest_world_center_x = 4986
    dest_world_center_y = 2892

    # Figure out how far the destination is from the current location
    dest_distance_x = dest_world_center_x - needle_world_center_x
    dest_distance_y = dest_world_center_y - needle_world_center_y

    # If the destination distance is larger than the size of the minimap,
    #   reduce the current click distance to the edge of the minimap
    if dest_distance_x >= 30:
        log.info("dest distance X is over value")
        click_pos_x = needle_client_center_x + 30
    elif dest_distance_x >= (-30):
        log.info("dest distance X is under value")
        click_pos_x = needle_client_center_x - 30
    else:
        click_pos_x = needle_client_center_x + dest_distance_x

    if dest_distance_y >= 30:
        log.info("dest distance Y is over value")
        click_pos_y = needle_client_center_y + 30
    elif dest_distance_x >= (-30):
        log.info("dest distance Y is under value")
        click_pos_y = needle_client_center_y - 30
    else:
        click_pos_y = needle_client_center_y + dest_distance_y

    # Now, make the click
    input.click_coord(click_pos_x, click_pos_y, width=0, height=0)


if __name__ == '__main__':
    main()

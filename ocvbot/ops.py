# The OSRS Positioning System

#import os

#import sys
#import pyautogui

import os
import time

import cv2
import numpy as np
import pyautogui

from ocvbot import input, vision

'''
match current minimap (needle) against:
    world-map.png
        rgb
        grayscale - 6.2s
    world-map-pngcrush.png
        rgb - 18.7s
        grayscale - 6.3s
    world-map-no-zeah.png
        rgb - 9.4s
        grayscale - 3.4s
    world-map-mainland-only.png
        grayscale - 2.9s
    world-map-oceans-deleted.png
        grayscale - 2.9s
    world-map-f2p-no-karamja-no-corsair.png
        rgb - 1.74s
        grayscale - 0.60s
    world-map-f2p-no-wild-no-karamja-no-corsair.png
        rgb - 0.9s
        grayscale - 0.38s
'''

haystack = cv2.imread('varrock-east-mine.png', cv2.IMREAD_GRAYSCALE)

def ocv_find_location():
    global haystack
    needle = pyautogui.screenshot(region=vision.minimap_slice)
    needle = cv2.cvtColor(np.array(needle), cv2.COLOR_RGB2GRAY)
    w, h = needle.shape[::-1]
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(result)
    max_x = loc[3]
    return max_x[0], max_x[1], w, h

def main():
    # Find chunk within world
    # world-map-f2-no-wildy-no-karamja-no-corsair.png
    chunk_left = 6891
    chunk_top = 2158
    # set destination relative to world's coordinates
    # to bank:
    destination_list = [(8558, 2670, 20, 5),
                        (8408, 2670, 20, 5),
                        (8411, 2703, 4, 5),]
    # from bank:
    #destination_list = [(8408, 2670, 20, 5),
                         #(8558, 2670, 15, 5),
                        #(8540, 2912, 3, 10)]
    for destination in destination_list:
        while True:

            dest_world_center_x, dest_world_center_y, tolerance, refresh = destination
            # Find current minimap position within the haystack
            os.system('rm -f current-pos*.png')
            current_pos = pyautogui.screenshot('current-pos.png', region=vision.minimap_slice)
            coordinates = ocv_find_location()
            #print("minimap relative to haystack is", coordinates)
            (needle_chunk_left, needle_chunk_top, needle_width, needle_height) = coordinates

            # Now get the minimap coordinates coordinates relative to world
            needle_world_left = needle_chunk_left + chunk_left
            needle_world_top = needle_chunk_top + chunk_top

            # Get center of minimap coordinates within world
            needle_world_center_x = int(
                (needle_world_left + needle_width) - (needle_width / 2))
            needle_world_center_y = int(
                (needle_world_top + needle_height) - (needle_height / 2))
            print("minimap relative to world is", needle_world_center_x, ' ', needle_world_center_y)

            # Get center of minimap slice within client window
            #print("client is", client)
            #os.system('rm -f /tmp/current-pos*.png')
            #current_pos = pyautogui.screenshot('/tmp/current-pos.png', region=vision.minimap_slice)
            #needle_client_center = vision.Vision(ltwh=vision.minimap,
                                                 #loctype='center',
                                                  #needle='/tmp/current-pos.png',
                                                 #conf=0.9,
                                                  #loop_num=5).wait_for_image(get_tuple=True)
            #print('minimap relative to client is', needle_client_center)
            #(needle_client_center_x, needle_client_center_y) = needle_client_center
            needle_client_center_x = vision.client[0] + 642
            needle_client_center_y = vision.client[1] + 86


            # Figure out how far the destination is from the current location
            dest_distance_x = dest_world_center_x - needle_world_center_x
            dest_distance_y = dest_world_center_y - needle_world_center_y
            print('dest_distance x is', dest_distance_x)
            print('dest_distance y is', dest_distance_y)

            # If the destination distance is larger than the size of the minimap,
            #   reduce the current click distance to the edge of the minimap
            if dest_distance_x >= 50:
                #log.info("dest distance X is over value")
                click_pos_x = needle_client_center_x + 50
            elif abs(dest_distance_x) >= 50:
                #log.info("dest distance X is under value")
                click_pos_x = needle_client_center_x - 50
            else:
                click_pos_x = needle_client_center_x + dest_distance_x

            if dest_distance_y >= 50:
                #log.info("dest distance Y is over value")
                click_pos_y = needle_client_center_y + 50
                # Since the minimap is circular, if the Y-distance is low
                #   engouh, we can make the click-position for the X-coordinate
                #   farther down the minimap to take advantage of the extra space
                if dest_distance_y >= 10:
                    click_pos_y = needle_client_center_y + 70

            elif abs(dest_distance_y) >= 50:
                #log.info("dest distance Y is under value")
                click_pos_y = needle_client_center_y - 50

                if abs(dest_distance_y) >= 10:
                    click_pos_y = needle_client_center_y - 70
            else:
                click_pos_y = needle_client_center_y + dest_distance_y

            # Now, make the click
            click_pos_y = abs(click_pos_y)
            click_pos_x = abs(click_pos_x)
            input.Mouse(ltwh=(click_pos_x, click_pos_y, 0, 0), sleep_range=(0, 1, 100, 200),
                        move_duration_range=(0, 1)).click_coord()
            #print('click pos x is ', click_pos_x)
            #print('click pos y is ', click_pos_y)
            time.sleep(refresh)

            if (abs(dest_distance_y) <= tolerance and abs(dest_distance_x) <= tolerance):
                print('arrived at dest!')
                break
            else:
                print('havent arrived at dest yet')
                pass



if __name__ == '__main__':
    main()

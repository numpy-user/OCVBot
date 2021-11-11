#!/usr/bin/env python3
# coding=UTF-8
"""
Captures a screenshot of the OSRS client and overlays rectangles onto the
screenshot cooresponding to the various coordinate spaces used by the bot.

This is only useful for debugging or development purposes.

"""
import logging as log
import pathlib
import subprocess
import sys

import screenshot

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)

from ocvbot import vision as vis, startup as start

vis.init()

log.basicConfig(
    format="%(asctime)s -- %(filename)s.%(funcName)s - %(message)s", level="INFO"
)

# We must take a screenshot of the entire display instead of only the client
#   because the Vision objects (e.g. vis.client_left and vis.client_top, etc.)
#   use coordinates that are relative to the entire display.
# Cropping is performed after the Vision object regions have been highlighted.
SCREENSHOT_PATH = str(screenshot.main(region=vis.display))


def crop_to_client(file_name: str) -> None:
    log.info("Creating %s", file_name)
    try:
        subprocess.run(
            "convert"
            + " "
            + file_name
            + " -crop"
            + " "
            + str(start.CLIENT_WIDTH)
            + "x"
            + str(start.CLIENT_HEIGHT)
            + "+"
            + str(vis.client_left)
            + "+"
            + str(vis.client_top)
            + " "
            + file_name,
            check=True,
            shell=True,
        )
    except FileNotFoundError:
        log.critical("ImageMagick not found!")


def mark_region(
    region_name: str,
    region_left: int,
    region_top: int,
    region_width: int,
    region_height: int,
) -> None:
    file_name = "ocvbot_" + region_name + ".png"
    log.info("Creating %s", file_name)

    region_coordinates = (
        str(region_left)
        + " "
        + str(region_top)
        + " "
        + str(region_left + region_width)
        + " "
        + str(region_top + region_height)
    )
    convert_rectangle_arg = ' -draw "rectangle ' + region_coordinates + '"'

    try:
        subprocess.run(
            "convert "
            + SCREENSHOT_PATH
            + ' -fill "rgba(255,0,0,0.5)"'
            + convert_rectangle_arg
            + " "
            + file_name,
            check=True,
            shell=True,
        )
    except FileNotFoundError:
        log.critical("ImageMagick not found!")

    crop_to_client(file_name)
    pngcrush(file_name)


def pngcrush(filename: str) -> None:
    try:
        subprocess.call(["pngcrush", "-ow ", filename])
    except FileNotFoundError:
        log.warning("pngcrush not present!")


def main() -> None:
    # Import all the coordinate spaces to overlay onto the screenshot.
    # Create a separate file for coordinate space, as some of them
    #   overlap.
    mark_region(
        "client",
        vis.client_left,
        vis.client_top,
        start.CLIENT_WIDTH,
        start.CLIENT_HEIGHT,
    )
    mark_region(
        "inv",
        vis.inv_left,
        vis.inv_top,
        start.INV_WIDTH,
        start.INV_HEIGHT,
    )
    mark_region(
        "inv_bottom",
        vis.inv_bottom_left,
        vis.inv_bottom_top,
        start.INV_WIDTH,
        start.INV_HALF_HEIGHT,
    )
    mark_region(
        "inv_right_half",
        vis.inv_right_half_left,
        vis.inv_right_half_top,
        start.INV_HALF_WIDTH,
        start.INV_HEIGHT,
    )
    mark_region(
        "inv_left_half",
        vis.inv_left_half_left,
        vis.inv_left_half_top,
        start.INV_HALF_WIDTH,
        start.INV_HEIGHT,
    )
    mark_region(
        "game_screen",
        vis.game_screen_left,
        vis.game_screen_top,
        start.GAME_SCREEN_WIDTH,
        start.GAME_SCREEN_HEIGHT,
    )
    mark_region(
        "bank_items_window",
        vis.bank_items_window_left,
        vis.bank_items_window_top,
        start.BANK_ITEMS_WINDOW_WIDTH,
        start.BANK_ITEMS_WINDOW_HEIGHT,
    )
    mark_region(
        "side_stones",
        vis.side_stones_left,
        vis.side_stones_top,
        start.SIDE_STONES_WIDTH,
        start.SIDE_STONES_HEIGHT,
    )
    mark_region(
        "chat_menu",
        vis.chat_menu_left,
        vis.chat_menu_top,
        start.CHAT_MENU_WIDTH,
        start.CHAT_MENU_HEIGHT,
    )
    mark_region(
        "chat_menu_recent",
        vis.chat_menu_recent_left,
        vis.chat_menu_recent_top,
        start.CHAT_MENU_RECENT_WIDTH,
        start.CHAT_MENU_RECENT_HEIGHT,
    )
    mark_region(
        "minimap",
        vis.minimap_left,
        vis.minimap_top,
        start.MINIMAP_WIDTH,
        start.MINIMAP_HEIGHT,
    )
    mark_region(
        "minimap_slice",
        vis.minimap_slice_left,
        vis.minimap_slice_top,
        start.MINIMAP_SLICE_WIDTH,
        start.MINIMAP_SLICE_HEIGHT,
    )


if __name__ == "__main__":
    main()

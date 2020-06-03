import logging as log
import random as rand

import pyautogui as pag
import pyclick as pyc

from ocvbot import misc

# initialize HumanClicker object
hc = pyc.HumanClicker()


def click_coord(left, top, width, height, button='left'):
    """
    Clicks within the provided coordinates. If width and height are both
    0, then this function will click in the exact same location every
    time.

    Args:
        left (int): The left edge (x) of the coordinate space to click
                    within.
        top (int): The top edge (y) of the coordinate space to click
                   within.
        width (int): The x width of the coordinate space to randomize
                     the click within.
        height (int): The y height of the coordinate space to randomize
                      the click within.
        button (str): The mouse button to click with, default is left.
    """

    move_to(x=left, y=top,
            xmin=0, xmax=width,
            ymin=0, ymax=height)

    click(button=button)
    return


def move_to(x, y,
            xmax, ymax,
            xmin=0, ymin=0,
            durmin=50, durmax=1500):
    """
    Moves the mouse pointer to the specified coordinates. Coordinates
    are relative to the display's dimensions. Units are in pixels.

    Args:
        x (int): The X coordinate to move the mouse to.
        y (int): The Y coordinate to move the mouse to.
        xmax (int): The maximum random pixel offset from x.
        ymax (int): The maximum random pixel offset from y.
        xmin  (int): The minimum random pixel offset from x, default is
                     0.
        ymin (int): The minimum random pixel offset from y, default is
                     0.
        durmin (int): The minumum number of miliseconds to take to move
                      the mouse cursor to its destination, default is
                      50.
        durmax (int): The maximum number of miliseconds to take to move
                       the mouse cursor to its destination, default is
                       1500.
    """

    xrand = rand.randint(xmin, xmax)
    yrand = rand.randint(ymin, ymax)

    hc.move((x + xrand), (y + yrand),
            move_duration(durmin=durmin, durmax=durmax))
    return


def moverel(xmin, xmax, ymin, ymax, durmin=50, durmax=1000):
    """
    Moves the mouse relative to its current position.

    Args;
        xmin (int): The mininum X distance to move the mouse.
        xmax (int): The maximum X distance to move the mouse.
        ymin (int): The mininum Y distance to move the mouse.
        ymax (int): The maximum Y distance to move the mouse.
        durmin (int): See move_duration()'s docstring.
        durmax (int): See move_duration()'s docstring.
    """
    # Current position.
    (x_pos, y_pos) = pag.position()

    # Distance to move.
    x_dist = rand.randint(xmin, xmax)
    y_dist = rand.randint(ymin, ymax)

    # Destination positions.
    x_dest = x_pos + x_dist
    y_dest = y_pos + y_dist

    hc.move(x_dest, y_dest, move_duration(durmin=durmin, durmax=durmax))
    return


def move_to_neutral(x, y,
                    xmin=50, xmax=300,
                    ymin=300, ymax=500):
    """
    Moves the mouse to a 'neutral zone', away from any buttons or
    tooltop icons that could get in the way of the script. Units are in
    pixels.

    Args:
        x (int): The x coordinate to move to.
        y (int): The y coordinate to move to.
        xmin (int): The minimum X-distance away from x to move, default
                    is 50.
        xmax (int): The maximum X-distance away from x to move, default
                    is 300.
        ymin (int): The minimum Y-distance away from y to move, default
                    is 300.
        ymax (int): The maximum X-distance away from y to move, default
                    is 500.
    """

    log.debug('Moving mouse towards neutral area.')

    move_to(x=x, y=y, xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)
    return


def click(button='left',
          sleep_befmin=0, sleep_befmax=500,
          sleep_afmin=0, sleep_afmax=500,
          click_durmin=0, click_durmax=100):
    """
    Clicks the left or right mouse button, waiting before and after
    for a randomized period of time.

    Args:
        button (str): Which mouse button to click, default is left.
        sleep_befmin (int): Minimum number of miliseconds to wait before
                            clicking, default is 0.
        sleep_befmax (int): Maximum number of miliseconds to wait before
                            clicking, default is 500.
        sleep_afmin (int): Minimum number of miliseconds to wait after
                           clicking, default is 0.
        sleep_afmax (int): Maximum number of miliseconds to wait after
                           clicking, default is 500.
        click_durmin (int): Minimum number of miliseconds to hold down
                            the mouse button, default is 0.
        click_durmax (int): Maximum number of miliseconds to hold down
                            the mouse button, default is 100.
    """

    misc.sleep_rand(rmin=sleep_befmin, rmax=sleep_befmax)

    duration = misc.rand_seconds(rmin=click_durmin, rmax=click_durmax)

    #log.debug('Holding down ' + button + ' mouse button for ' + str(duration) +
              #' seconds.')

    pag.click(button=button, duration=duration)
    misc.sleep_rand(rmin=sleep_afmin, rmax=sleep_afmax)
    return


def move_duration(durmin=50, durmax=1500):
    """
    Randomizes the amount of time the mouse cursor takes to move to a
    new location. Input arguments are in miliseconds but return value is
    in seconds.

    Args:
        durmin (int): Minimum number of miliseconds the mouse
                      pointer will take to move to its destination,
                      default is 50.
        durmax (int): Maximum number of miliseconds the mouse pointer
                      will take to move to its destination, default is
                      1500.
    Returns:
        Returns a float.
    """

    move_duration_var = misc.rand_seconds(rmin=durmin, rmax=durmax)
    return move_duration_var


def keypress(key,
             durmin=1, durmax=180,
             sleep_befmin=50, sleep_befmax=1000,
             sleep_afmin=50, sleep_afmax=1000):
    """
    Holds down the specified key for a random period of time. All
    values are in miliseconds.

    Args:
        key (str): The key on the keyboard to press, according to
                   PyAutoGUI.
        durmin (int): The shortest time the key can be down, default is
                      1.
        durmax (int): The longest time the key can be down, default is
                      180.
        sleep_befmin (int): The shortest time to wait before pressing
                            the key down, default is 50.
        sleep_befmax (int): The longest time to wait before pressing the
                            key down, default is 1000.
        sleep_afmin (int): The shortest time to wait after releasing the
                           key, default is 50.
        sleep_afmax (int): The longest time to wait after releasing the
                           key, default is 1000.
    """

    log.debug('Pressing key: ' + str(key) + '.')
    misc.sleep_rand(rmin=sleep_befmin, rmax=sleep_befmax)
    pag.keyDown(key)
    misc.sleep_rand(rmin=durmin, rmax=durmax)
    pag.keyUp(key)
    misc.sleep_rand(rmin=sleep_afmin, rmax=sleep_afmax)
    return


def double_hotkey_press(key1, key2,
                        durmin=5, durmax=190,
                        sleep_befmin=500, sleep_befmax=1000,
                        sleep_afmin=500, sleep_afmax=1000):
    """
    Performs a two-key hotkey shortcut, such as Ctrl-c for copying
    text.

    Args:
        key1 (str): The first hotkey used in the two-hotkey shortcut,
                    sometimes also called the modifier key.
        key2 (str): The second hotkey used in the two-hotkey shortcut.
        durmin (int): See keypress()'s docstring, default is 5.
        durmax (int): See keypress()'s docstring, default is 190.
        sleep_befmin (int): See keypress()'s docstring, default is 500.
        sleep_befmax (int): See keypress()'s docstring, default is 1000.
        sleep_afmin (int): See keypress()'s docstring, default is 500.
        sleep_afmax (int): See keypress()'s docstring, default is 1000.
    """

    log.debug('Pressing hotkeys: ' + str(key1) + ' + ' + str(key2))
    misc.sleep_rand(rmin=sleep_befmin, rmax=sleep_befmax)
    pag.keyDown(key1)
    misc.sleep_rand(rmin=durmin, rmax=durmax)
    pag.keyDown(key2)
    misc.sleep_rand(rmin=durmin, rmax=durmax)
    pag.keyUp(key1)
    misc.sleep_rand(rmin=durmin, rmax=durmax)
    pag.keyUp(key2)
    misc.sleep_rand(rmin=sleep_afmin, rmax=sleep_afmax)
    return

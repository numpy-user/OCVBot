import logging as log
import random as rand

import pyautogui as pag
import pyclick as pyc

from ocvbot import misc

# initialize HumanClicker object
hc = pyc.HumanClicker()


class Mouse:
    """
    left (int): X coordinate of the left edge to move the mouse cursor
                to.
    top (int): Y coordinte of the The top edge to move the mouse cursor
               to.
    width (int): The width of the coordinate space to randomize the
                 mouse cursor within.
    height (int): The height of the coordinate space to randomize the
                  mouse cursor within.
    sleep_befmin (int): Minimum number of miliseconds to wait before
                        performing action, default is 0.
    sleep_befmax (int): Maximum number of miliseconds to wait before
                        performing action, default is 500.
    sleep_afmin (int): Minimum number of miliseconds to wait after
                       performing action, default is 0.
    sleep_afmax (int): Maximum number of miliseconds to wait after
                       performing action, default is 500.
    click_durmin (int): Minimum number of miliseconds to hold down
                        the mouse button, default is 0.
    click_durmax (int): Maximum number of miliseconds to hold down
                        the mouse button, default is 100.
    move_durmin (int): The minumum number of miliseconds to take to move
                       the mouse cursor to its destination, default is
                       50.
    move_durmax (int): The maximum number of miliseconds to take to move
                       the mouse cursor to its destination, default is
                       1500.
    button (str): The mouse button to click with, default is left.

    """
    def __init__(self,
                 left, top, width, height,
                 sleep_befmin=0, sleep_befmax=500,
                 sleep_afmin=0, sleep_afmax=500,
                 move_durmin=50, move_durmax=1000,
                 durmin=1, durmax=100,
                 button='left'):

        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.sleep_befmin = sleep_befmin
        self.sleep_befmax = sleep_befmax
        self.sleep_afmin = sleep_afmin
        self.sleep_afmax = sleep_afmax
        self.move_durmin = move_durmin
        self.move_durmax = move_durmax
        self.durmin = durmin
        self.durmax = durmax
        self.button = button

    def click_coord(self):
        """
        Clicks within the provided coordinates. If width and height are
        both 0, then this function will click in the exact same location
        every time.

        """
        self.move_to()
        self.click()

    def move_to(self):
        """
        Moves the mouse pointer to the specified coordinates. Coordinates
        are based on the display's dimensions. Units are in pixels. Uses
        Bezier curves to make mouse movement appear more human-like.

        """
        xmin = self.left
        xmax = self.left + self.width
        ymin = self.top
        ymax = self.top + self.height

        x_coord = rand.randint(xmin, xmax)
        y_coord = rand.randint(ymin, ymax)

        hc.move((x_coord, y_coord), self.move_duration())

    def moverel(self):
        """
        Moves the mouse relative to its current position. This function
        interprets its object parameters a little differently:

        self.left is minimum X distance to move the mouse.
        self.width is maximum X distance to move the mouse.
        self.top is the minimum Y distance to move the mouse.
        self.height is the maximum Y distance to move the mouse.

        """
        if self.left < self.width or self.top < self.height:
            raise Exception("Width and Height must be greater than or equal to"
                            "Left andnTop when using the moverel() function!")

        (x_position, y_position) = pag.position()

        x_distance = rand.randint(self.left, self.width)
        y_distance = rand.randint(self.top, self.height)

        x_destination = x_position + x_distance
        y_destination = y_position + y_distance

        hc.move((x_destination, y_destination), self.move_duration())

    def move_duration(self):
        """
        Randomizes the amount of time the mouse cursor takes to move to
        a new location.

        Returns:
            Returns a float containing a number in seconds.

        """
        move_duration_var = misc.rand_seconds(rmin=self.move_durmin,
                                              rmax=self.move_durmax)
        return move_duration_var

    def click(self):
        """
        Clicks the left or right mouse button, waiting both before and
        after for a randomized period of time.

        """
        misc.sleep_rand(rmin=self.sleep_befmin,
                        rmax=self.sleep_befmax)

        duration = misc.rand_seconds(rmin=self.durmin,
                                     rmax=self.durmax)
        pag.click(button=self.button,
                  duration=duration)

        misc.sleep_rand(rmin=self.sleep_afmin,
                        rmax=self.sleep_afmax)


class Keyboard:
    """
    sleep_befmin (int): The minimum number of miliseconds to wait before
                        performing action, default is 50.
    sleep_befmax (int): The maximum number of miliseconds to wait before
                        performing action default is 1000.
    sleep_afmin (int): The minimum number of miliseconds to wait after
                        performing action, default is 50.
    sleep_afmax (int): The minimum number of miliseconds to wait after
                        performing action, default is 1000.
    durmin (int): The minimum number of miliseconds to hold the key down,
                  default is 1.
    durmax (int): The maximum number of miliseconds to hold the key down,
                  default is 180.

    """
    def __init__(self,
                 sleep_befmin=0, sleep_befmax=500,
                 sleep_afmin=0, sleep_afmax=500,
                 durmin=1, durmax=100):

        self.sleep_befmin = sleep_befmin
        self.sleep_befmax = sleep_befmax
        self.sleep_afmin = sleep_afmin
        self.sleep_afmax = sleep_afmax
        self.durmin = durmin
        self.durmax = durmax

    def keypress(self, key):
        """
        Presses the specified key.

        Args:
            key (str): The key on the keyboard to press, according to
                       PyAutoGUI.

        """
        log.debug('Pressing key: ' + str(key) + '.')
        misc.sleep_rand(rmin=self.sleep_befmin, rmax=self.sleep_befmax)
        pag.keyDown(key)
        misc.sleep_rand(rmin=self.durmin, rmax=self.durmax)
        pag.keyUp(key)
        misc.sleep_rand(rmin=self.sleep_afmin, rmax=self.sleep_afmax)

    def double_hotkey_press(self, key1, key2):
        """
        Performs a two-key hotkey shortcut, such as Ctrl-c for copying
        text.

        Args:
            key1 (str): The first hotkey used in the two-hotkey shortcut,
                        sometimes also called the modifier key.
            key2 (str): The second hotkey used in the two-hotkey shortcut.

        """
        log.debug('Pressing hotkeys: ' + str(key1) + ' + ' + str(key2))
        misc.sleep_rand(rmin=self.sleep_befmin, rmax=self.sleep_befmax)
        pag.keyDown(key1)
        misc.sleep_rand(rmin=self.durmin, rmax=self.durmax)
        pag.keyDown(key2)
        misc.sleep_rand(rmin=self.durmin, rmax=self.durmax)
        pag.keyUp(key1)
        misc.sleep_rand(rmin=self.durmin, rmax=self.durmax)
        pag.keyUp(key2)
        misc.sleep_rand(rmin=self.sleep_afmin, rmax=self.sleep_afmax)

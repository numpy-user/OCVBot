# coding=UTF-8
"""
Controls the mouse and keyboard.

"""
import logging as log
import random as rand

import pyautogui as pag
import pyclick as pyc

from ocvbot import misc

# initialize HumanClicker object
hc = pyc.HumanClicker()


class Mouse:
    """
    Class to move and click the mouse cursor.

    Args:
        ltwh (tuple): A 4-tuple containing the left, top, width, and
                      height coordinates. The width and height values
                      are used for randomizing the location of the mouse
                      cursor.
        sleep_range (tuple): A 4-tuple containing the minimum and maximum
                             number of miliseconds to wait before
                             performing the action, and the minimum and
                             maximum number of miliseconds to wait after
                             performing the action, default is
                             (0, 500, 0, 500).
        action_duration_range (tuple): A 2-tuple containing the
                                       minimum and maximum number of
                                       miliseconds during which the
                                       action will be performed, such as
                                       holding down the mouse button,
                                       default is (1, 100).
        move_duration_range (tuple): A 2-tuple containing the
                                     minimum and maximum number of
                                     miliseconds to take to move the
                                     mouse cursor to its destination,
                                     default is (50, 1500).
        button (str): The mouse button to click with, default is left.

    """
    def __init__(self,
                 ltwh,  # "left, top, width, height"
                 sleep_range=(0, 500, 0, 500),
                 move_duration_range=(50, 1500),
                 action_duration_range=(1, 100),
                 button='left'):

        self.ltwh = ltwh
        self.sleep_range = sleep_range
        self.move_duration_range = move_duration_range
        self.action_duration_range = action_duration_range
        self.button = button

    def click_coord(self, move_away=False):
        """
        Clicks within the provided coordinates. If width and height are
        both 0, then this function will click in the exact same location
        every time.

        Args:
            move_away (bool): Whether to move the mouse cursor a short
                              distance away from the coordinates that
                              were just clicked on, default is False.

        """
        self.move_to()
        self.click()
        if move_away is True:
            self.ltwh = (15, 15, 100, 100)
            self.move_duration_range = (0, 500)
            self.moverel()
        return True

    def move_to(self):
        """
        Moves the mouse pointer to the specified coordinates. Coordinates
        are based on the display's dimensions. Units are in pixels. Uses
        Bezier curves to make mouse movement appear more human-like.

        """
        left, top, width, height = self.ltwh

        # hc.move uses a (x1, x2, y1, y2) coordinate format instead of a
        #   (left, top, width, height) format.
        # x2 and y2 are obtained by adding width to left and height to top.
        x_coord = rand.randint(left, (left + width))
        y_coord = rand.randint(top, (top + height))

        hc.move((x_coord, y_coord), self.move_duration())
        return True

    def moverel(self):
        """
        Moves the mouse in a random direction, relative to its current
        position. Uses left/width to determinie the minimum and maximum
        X distance to move and top/height to determine the minimum and
        maximum Y distance to move.

        Whichever of the two left/width values is lower will be used as
        the minimum X distance and whichever of the two values is higher
        will be used as the maximum X distance. Same for top/height.

        """
        left, top, width, height = self.ltwh
        (x_position, y_position) = pag.position()

        # Get min and max values based on the provided ltwh coordinates.
        x_min = min(left, width)
        x_max = max(left, width)
        y_min = min(top, height)
        y_max = max(top, height)

        # Get a random distance to move based on min and max values.
        x_distance = rand.randint(x_min, x_max)
        y_distance = rand.randint(y_min, y_max)

        y_destination = y_position + y_distance
        x_destination = x_position + x_distance

        # Roll for a chance to reverse the direction the mouse moves in.
        if (rand.randint(1, 2)) == 2:
            x_destination = x_position - x_distance
        if (rand.randint(1, 2)) == 2:
            y_destination = y_position - y_distance

        hc.move((x_destination, y_destination), self.move_duration())
        return True

    def move_duration(self):
        """
        Randomizes the amount of time the mouse cursor takes to move to
        a new location.

        Returns:
            Returns a float containing a number in seconds.

        """
        move_durmin, move_durmax = self.move_duration_range
        move_duration_var = misc.rand_seconds(rmin=move_durmin, rmax=move_durmax)
        return move_duration_var

    def click(self, hold=False):
        """
        Clicks the left or right mouse button, waiting both before and
        after for a randomized period of time.

        Args:
            hold (bool): Whether to hold down the mouse button rather
                         than just clicking it.
                         Uses self.action_duration_range to determine
                         the minimum and maximum duration to hold down
                         the mouse button.

        """
        # Random sleep before click.
        misc.sleep_rand(rmin=self.sleep_range[0], rmax=self.sleep_range[1])

        if hold is True:
            duration = misc.rand_seconds(rmin=self.action_duration_range[0],
                                         rmax=self.action_duration_range[1])
            pag.click(button=self.button, duration=duration)
        else:
            pag.click(button=self.button)

        # Random sleep after click.
        misc.sleep_rand(rmin=self.sleep_range[2], rmax=self.sleep_range[3])
        return True


class Keyboard:
    """
    Manipulates the keyboard.

    Args:
        sleep_range (tuple): A 4-tuple containing the minimum and
                             maximum number of miliseconds to wait
                             before performing the action, and the
                             minimum and maximum number of miliseconds
                             to wait after performing the action,
                             default is (0, 500, 0, 500).
        action_duration_range (tuple): A 2-tuple containing the
                                       minimum and maximum number of
                                       miliseconds during which the
                                       action will be performed, such as
                                       holding down a key, default is
                                       (1, 100).
        log_keys (bool): Whether to log keystrokes at DEBUG level. This
                         is always set to False when entering user
                         credentials, default is True.

    """
    def __init__(self,
                 sleep_range=(0, 500, 0, 500),
                 action_duration_range=(1, 100),
                 log_keys=True):

        self.sleep_range = sleep_range
        self.action_duration_range = action_duration_range
        self.log = log_keys

    def typewriter(self, message):
        """
        Types out the specified message with a randomized delay between
        each key press.

        Args:
            message (str): The message to type.

        """
        self.sleep_range = (0, 20, 0, 20)
        self.action_duration_range = (1, 50)
        for key in message:
            self.keypress(key)
        return True

    def keypress(self, key):
        """
        Presses the specified key.

        Args:
            key (str): The key on the keyboard to press, according to
                       PyAutoGUI.

        """
        if self.log is True:
            log.debug('Pressing key: %s.', key)

        misc.sleep_rand(rmin=self.sleep_range[0], rmax=self.sleep_range[1])
        pag.keyDown(key)
        misc.sleep_rand(rmin=self.action_duration_range[0],
                        rmax=self.action_duration_range[1])
        pag.keyUp(key)
        misc.sleep_rand(rmin=self.sleep_range[2], rmax=self.sleep_range[3])
        return True

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
        sleep_before_min, sleep_before_max, sleep_after_min, sleep_after_max = \
            self.sleep_range
        action_duration_min, action_duration_max = self.action_duration_range

        misc.sleep_rand(rmin=sleep_before_min, rmax=sleep_before_max)
        pag.keyDown(key1)
        misc.sleep_rand(rmin=action_duration_min, rmax=action_duration_max)
        pag.keyDown(key2)
        misc.sleep_rand(rmin=action_duration_min, rmax=action_duration_max)
        pag.keyUp(key1)
        misc.sleep_rand(rmin=action_duration_min, rmax=action_duration_max)
        pag.keyUp(key2)
        misc.sleep_rand(rmin=sleep_after_min, rmax=sleep_after_max)
        return True

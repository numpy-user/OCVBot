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
        ltwh (tuple): A 4-member tuple containing the left, top, width,
                      and height coordinates. The width and height
                      values are used for randomizing the location of
                      the mouse cursor.
        sleep_range (tuple): A 4-member tuple containing the minimum
                             and maximum number of miliseconds to wait
                             before performing the action, and the
                             minimum and maximum number of miliseconds
                             to wait after performing the action,
                             default is (0, 500, 0, 500).
        action_duration_range (tuple): A 2-member tuple containing the
                                       minimum and maximum number of
                                       miliseconds during which the
                                       action will be performed, such as
                                       holding down the mouse button,
                                       default is (1, 100).
        move_duration_range (tuple): A 2-member tuple containing the
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

        """
        self.move_to()
        self.click()
        if move_away is True:
            self.ltwh = (25, 150, 25, 150)
            self.move_duration_range = (5, 300)
            self.moverel()
        return True

    def move_to(self):
        """
        Moves the mouse pointer to the specified coordinates. Coordinates
        are based on the display's dimensions. Units are in pixels. Uses
        Bezier curves to make mouse movement appear more human-like.

        """
        xmin, ymin, xmax, ymax = self.ltwh

        x_coord = rand.randint(xmin, (xmin + xmax))
        y_coord = rand.randint(ymin, (ymin + ymax))

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

        x_distance = rand.randint(min(left, width), max(left, width))
        y_distance = rand.randint(min(top, height), max(top, height))

        x_destination = x_position + x_distance
        y_destination = y_position + y_distance

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
        move_duration_var = misc.rand_seconds(rmin=move_durmin,
                                              rmax=move_durmax)
        return move_duration_var

    def click(self, hold=False):
        """
        Clicks the left or right mouse button, waiting both before and
        after for a randomized period of time.

        Args:
            hold (bool): Whether to hold down the mouse button rather
                         than just clicking it.
                         Uses self.action_duration_range to determine
                         min and max duration.

        """
        misc.sleep_rand(rmin=self.sleep_range[0],
                        rmax=self.sleep_range[1])

        if hold is True:
            duration = misc.rand_seconds(rmin=self.action_duration_range[0],
                                         rmax=self.action_duration_range[1])
            pag.click(button=self.button,
                      duration=duration)
        else:
            pag.click(button=self.button)

        misc.sleep_rand(rmin=self.sleep_range[2],
                        rmax=self.sleep_range[3])
        return True


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
                 sleep_range=(0, 500, 0, 500),
                 action_duration_range=(1, 100)):
        self.sleep_range = sleep_range
        self.action_duration_range = action_duration_range

    def typewriter(self, message):
        """
        Types out the specified message with a randomized delay between
        key presses.

        Args:
            message (str): The message to type.

        """
        self.sleep_range = (0, 20, 0, 20)
        self.action_duration_range = (1, 100)
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
        log.debug('Pressing key: ' + str(key) + '.')

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

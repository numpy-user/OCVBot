# coding=UTF-8
"""
Module for "seeing" the client.

"""
import logging as log
import pathlib

import pyautogui as pag
from ocvbot import inputs
from ocvbot import misc
from ocvbot import startup as start


# Set initial values for vision regions.
#
# See ./docs/client_anatomy.png for more info.
#
# Capture the width and height of various different elements within the
#   game client. Values of tuples start at (0, 0, 0, 0) until they are defined
#   by the init() function. Units are in pixels.

BANK_ITEMS_WINDOW_WIDTH = 375
BANK_ITEMS_WINDOW_HEIGHT = 215
BANK_ITEMS_WINDOW = (0, 0, 0, 0)

CHAT_MENU_WIDTH = 506
CHAT_MENU_HEIGHT = 129
CHAT_MENU = (0, 0, 0, 0)

CHAT_MENU_RECENT_WIDTH = 490
CHAT_MENU_RECENT_HEIGHT = 17
CHAT_MENU_RECENT = (0, 0, 0, 0)

CLIENT_WIDTH = 765
CLIENT_HEIGHT = 503
CLIENT = (0, 0, 0, 0)

DISPLAY_WIDTH = pag.size().width
DISPLAY_HEIGHT = pag.size().height
DISPLAY = (0, 0, DISPLAY_WIDTH, DISPLAY_HEIGHT)

GAME_SCREEN_WIDTH = 512
GAME_SCREEN_HEIGHT = 340
GAME_SCREEN = (0, 0, 0, 0)

INV_WIDTH = 186
INV_HEIGHT = 262
INV_HALF_WIDTH = round((INV_WIDTH / 2) + 5)
INV_HALF_HEIGHT = round(INV_HEIGHT / 2)
INV = (0, 0, 0, 0)
INV_BOTTOM = (0, 0, 0, 0)
INV_RIGHT_HALF = (0, 0, 0, 0)
INV_LEFT_HALF = (0, 0, 0, 0)

LOGIN_FIELD_WIDTH = 258
LOGIN_FIELD_HEIGHT = 12
LOGIN_FIELD = (0, 0, 0, 0)
PASS_FIELD = (0, 0, 0, 0)

MINIMAP_WIDTH = 146
MINIMAP_HEIGHT = 151
MINIMAP = (0, 0, 0, 0)

MINIMAP_SLICE_WIDTH = 85
MINIMAP_SLICE_HEIGHT = 85
MINIMAP_SLICE = (0, 0, 0, 0)

SIDE_STONES_WIDTH = 249
SIDE_STONES_HEIGHT = 366
SIDE_STONES = (0, 0, 0, 0)

# TODO
def wait_for_needle_list(
    loops: int,
    needle_list: list[tuple[str, tuple[int, int, int, int]]],
    sleep_range: tuple[int, int],
):
    """
    Works like vision.wait_for_needle(), except multiple needles can be
    searched for simultaneously.

    Args:
        loops: The number of tries to look for each needle in needle_list.
        needle_list: A list of filepaths to the needles to look for. Each
                     item in the list is a 2-tuple containing:
                     - The filepath to the needle.
                     - The region in which to search for that needle.
        sleep_range: A 2-tuple containing the minimum and maximum number
                     of miliseconds to wait after each loop.

    Returns:
        If a needle in needle_list is found, returns a 2-tuple containing
        the ltwh dimensions of the needle and the index of the needle in
        needle_list (This is so the function knows which needle was found).

        Returns false if no needles in needle_list could be found.

    """
    for _ in range(1, loops):

        for item in needle_list:
            needle, region = item

            needle_found = Vision(
                region=region, needle=needle, loop_num=1
            ).wait_for_needle(get_tuple=True)
            if needle_found is True:
                return needle_found, needle_list.index(needle)

        misc.sleep_rand(sleep_range[0], sleep_range[1])

    return False


# TODO: Add examples of usage.
# TODO: Rename to "Needle" or "Image". Create another class for pixel matching
#   called "Pixel".
class Vision:
    """
    Main class locating and clicking on images on the display.
    All coordinates are relative to the top left corner of the display.
    All coordinates are in a (left, top, width, height) format.

    Args:
        region (tuple): A 4-tuple containing the Left, Top, Width, and
                        Height of the region in which to look for the
                        needle. This typically will be one of the tuples
                        defined at the top of this file like `INV` or
                        `GAME_SCREEN`.
        needle (file): A filepath to an the image to search for within the
                       `region` tuple.
        loctype (str): Whether to return the needle's (ltwh) coordinates
                       or its (X, Y) center. Available values are `regular`
                       and `center`.
            regular = Returns the needle's left, top, width, and height
                      as a 4-tuple.
            center = Returns the (X, Y) coordinates of the needle's
                     center as a 2-tuple (relative to the display's
                     dimensions).
        conf (float): The confidence value required to match the needle
                      successfully, expressed as a decimal <= 1. This is
                      used by PyAutoGUI. Default is 0.95.
        loop_num (int): The number of times wait_for_needle() will search
                        the given coordinates for the needle. Default is
                        10.
        loop_sleep_range (tuple): A 2-tuple containing the minimum and
                                  maximum number of miliseconds to wait
                                  between image-search loops. Used by
                                  the wait_for_needle() method. Default
                                  is (0, 100).
        grayscale (bool): Converts the haystack to grayscale before
                          searching within it. Speeds up searching by
                          about 30%. Default is False.

    """

    def __init__(
        self,
        region: tuple[int, int, int, int],
        needle: str,
        loctype: str = "regular",
        conf: float = 0.95,
        # TODO: Move to a parameter of wait_for_needle().
        loop_num: int = 10,
        # TODO: Move to a parameter of wait_for_needle().
        loop_sleep_range: tuple[int, int] = (0, 100),
        grayscale: bool = False,
    ):
        self.grayscale = grayscale
        self.region = region
        self.needle = needle
        self.loctype = loctype
        self.conf = conf
        self.loop_num = loop_num
        self.loop_sleep_range = loop_sleep_range

    # TODO: Add examples of usage.
    def find_needle(self):
        """
        Searches within the self.ltwh coordinates for self.needle.

        Returns:
            If the needle is found and self.loctype is `regular`, returns
            the needle's left/top/width/height dimensions as a 4-tuple.

            If the needle is found and self.loctype is `center`, returns
            coordinates of the needle's (X, Y) center as a 2-tuple.

            If the needle is not found, returns False.

        """
        if self.loctype == "regular":
            needle_coords = pag.locateOnScreen(
                self.needle,
                confidence=self.conf,
                grayscale=self.grayscale,
                region=self.region,
            )
            if needle_coords is not None:
                log.debug("Found regular image %s, %s", self.needle, needle_coords)
                return needle_coords
            raise start.NeedleError("Could not find needle!", self.needle)

        elif self.loctype == "center":
            needle_coords = pag.locateCenterOnScreen(
                self.needle,
                confidence=self.conf,
                grayscale=self.grayscale,
                region=self.region,
            )
            if needle_coords is not None:
                log.debug("Found center of image %s, %s", self.needle, needle_coords)
                return needle_coords
            raise start.NeedleError("Could not find needle!", self.needle)

        raise RuntimeError(
            "self.loctype must be 'regular' or 'center', got '%s'", self.loctype
        )

    # TODO: Add examples of usage.
    def wait_for_needle(self):
        """
        Repeatedly searches within the self.ltwh coordinates for the needle.

        Returns:
            If self.loctype is `regular`, returns a 4-tuple containing the
            (left, top, width, height) coordinates of the needle.
            
            If self.loctype is `center`, returns a 2-tuple containing the
            (X, Y) center of the needle.

        Raises:
            Raises start.NeedleError if the needle could not be found.
        """
        # Add 1 to self.loop_num because if loop_num=1, it won't loop at
        #   all.
        for tries in range(1, (self.loop_num + 1)):

            try:
                needle_coords = Vision.find_needle(self)
                log.debug("Found %s after trying %s times.", self.needle, tries)
                return needle_coords
            except start.NeedleError:
                log.debug("Cannot find %s, tried %s times.", self.needle, tries)
                misc.sleep_rand(self.loop_sleep_range[0], self.loop_sleep_range[1])

        raise start.NeedleError("Timed out looking for needle!", self.needle)

    # TODO: Add examples of usage.
    def click_needle(
        self,
        sleep_range: tuple[int, int, int, int] = (50, 200, 50, 200),
        move_duration_range: tuple[int, int] = (1, 50),
        button: str = "left",
        move_away: bool = False,
        number_of_clicks: int = 1,
    ) -> bool:
        """
        Moves the mouse to the provided needle image and clicks on
        it. Automatically randomizes the location the mouse cursor
        will click to based on the dimensions of the needle image.

        Args:
            sleep_range (tuple): Passed to the Mouse class in inputs.py,
                                 see its docstring for more info.
            move_duration_range (tuple): Passed to the Mouse class in
                                         inputs.py, see its docstring for
                                         more info.
            button (str): The mouse button to use when clicking on the
                          needle, default is `left`.
            move_away (bool): Whether to move the mouse out of the way
                              after clicking on the needle. Useful when
                              we needs to determine the status of a button
                              that the mouse just clicked.
            number_of_clicks (int): Passed to the click_coord() function of the
                                    Mouse class, see its docstring for more
                                    info. Default is 1.

        Returns:
            Returns True if the needle was clicked on successfully,
            returns False otherwise.

        """
        log.debug("Looking for %s to click on.", self.needle)

        needle_coords = self.wait_for_needle()

        # Randomize the location the mouse cursor will move to using
        #   the dimensions of needle image.
        # The mouse will click anywhere within the needle image.
        inputs.Mouse(
            region=needle_coords,
            sleep_range=sleep_range,
            move_duration_range=move_duration_range,
            button=button,
        ).click_coord(number_of_clicks=number_of_clicks)

        log.debug("Clicking on %s", self.needle)

        if move_away is True:
            inputs.Mouse(
                region=(25, 25, 100, 100), move_duration_range=(50, 200)
            ).moverel()

    def count_needles(self):
        """
        Counts the number of needles found within the region specified.

        Examples:
            Count the number of iron bars in the player's inventory:
            vision.Vision(region=vis.inv, needle="./needles/items/iron-bar.png").count_needles()

        Returns:
            Returns an int.
        """
        # Make sure file path is OS-agnostic.
        needle = str(pathlib.Path(self.needle))

        try:
            needles_coords = pag.locateAllOnScreen(
                needle,
                confidence=self.conf,
                grayscale=self.grayscale,
                region=self.region,
            )
            needles_coords_list = list(needles_coords)
            number_of_needles = len(needles_coords_list)
            return number_of_needles

        # If no needles can be found, then the number of needles is 0.
        except ImageNotFoundException:
            return 0


# TODO: Add examples of usage.
# TODO: Break out an "is_logged_in" function.
def orient(
    region: tuple[int, int, int, int] = (DISPLAY),
    launch_client: bool = False,
):
    """
    Looks for an icon to orient the client. If it's found, use its
    location within the game client to determine the coordinates of the
    game client relative to the display's coordinates.

    This function is also used to determine if the client is logged out.
    This is generally one of the first functions that is run upon script
    startup.

    Args:
        region (tuple): A 4-tuple containing the left, top, width, and
                      height of the coordinate space to search within,
                      relative to the display's coordinates. By default
                      uses the entire display.

    Raises:
       Raises an exception if the client cannot be found, or if the
       function can't determine if the client is logged in or logged
       out.

    Returns:
         If client is logged in, returns a 2-tuple containing a string
         with the text "logged_in" and a 2-tuple of the center (X, Y)
         coordinates of the orient needle.

         If client is logged out, returns a 2-tuple containing a string
         with the text "logged_out" and a 2-tuple of the center (X, Y)
         coordinates of the orient-logged-out needle.

    """
    try:
        logged_in = Vision(
            region=region,
            needle="needles/minimap/orient.png",
            loctype="center",
            loop_num=1,
            conf=0.8,
        ).wait_for_needle()
        log.info("Client is logged in.")
        return "logged_in", logged_in
    except start.NeedleError:
        pass
    
    try:
        # If the client is not logged in, check if it's logged out.
        logged_out = Vision(
            region=region,
            needle="needles/login-menu/orient-logged-out.png",
            loctype="center",
            loop_num=1,
            conf=0.8,
        ).wait_for_needle()
        log.info("Client is logged out.")
        return "logged_out", logged_out
    except start.NeedleError
        raise RuntimeError("Unable to locate client!")


# TODO: add 'configure camera' function that clicks on compass, zooms in camera, and holds down up arrow
#       only click on the compass if it isn't perfectly aligned


def init() -> None:
    """
    Locates the client and sets the value of the vision regions.
    This function MUST be run before OCVBot can do anything else.
    """

    (client_status, anchor) = orient(region=DISPLAY)
    (client_left, client_top) = anchor

    if client_status == "logged_in":
        client_left -= 735
        client_top -= 21
    elif client_status == "logged_out":
        client_left -= 183
        client_top -= 59

    # Each of these tuples contains coordinates for the "region" parameter
    #   of PyAutoGUI's Locate() functions. These tuples are used by methods
    #   in the Vision class to look for needles within the specified set of
    #   coordinates, rather than within the entire display's coordinates,
    #   which is much faster.

    # All coordinates are in a (left, top, width, height) format, to match
    #   PyAutoGUI.

    # The fixed-width game client.
    global CLIENT
    CLIENT = (client_left, client_top, CLIENT_WIDTH, CLIENT_HEIGHT)

    # The player's inventory.
    inv_left = client_left + 548
    inv_top = client_top + 205
    global INV
    INV = (inv_left, inv_top, INV_WIDTH, INV_HEIGHT)

    # Bottom half of the player's inventory.
    inv_bottom_left = inv_left
    inv_bottom_top = inv_top + INV_HALF_HEIGHT
    global INV_BOTTOM
    INV_BOTTOM = (
        inv_bottom_left,
        inv_bottom_top,
        INV_WIDTH,
        INV_HALF_HEIGHT,
    )

    # Right half of the player's inventory.
    inv_right_half_left = (inv_left + INV_HALF_WIDTH) - 5
    inv_right_half_top = inv_top
    global INV_RIGHT_HALF
    INV_RIGHT_HALF = (
        inv_right_half_left,
        inv_right_half_top,
        INV_HALF_WIDTH,
        INV_HEIGHT,
    )

    # Left half of the player's inventory.
    inv_left_half_left = inv_left
    inv_left_half_top = inv_top
    global INV_LEFT_HALF
    INV_LEFT_HALF = (
        inv_left_half_left,
        inv_left_half_top,
        INV_HALF_WIDTH,
        INV_HEIGHT,
    )

    # The "gameplay screen". This is the screen that displays the player
    #   character and the game world.
    game_screen_left = client_left + 4
    game_screen_top = client_top + 4
    global GAME_SCREEN
    GAME_SCREEN = (
        game_screen_left,
        game_screen_top,
        GAME_SCREEN_WIDTH,
        GAME_SCREEN_HEIGHT,
    )

    # Banking window, minus the tabs at the top and other surrounding elements.
    # This is done to prevent the bot from attempting to withdrawal items by
    #   clicking on their tab icons
    bank_items_window_left = game_screen_left + 68
    bank_items_window_top = game_screen_top + 77
    global BANK_ITEMS_WINDOW
    BANK_ITEMS_WINDOW = (
        bank_items_window_left,
        bank_items_window_top,
        BANK_ITEMS_WINDOW_WIDTH,
        BANK_ITEMS_WINDOW_HEIGHT,
    )

    # The player's inventory, plus the top and bottom "side stone" tabs that
    #   open all the different menus.
    side_stones_left = client_left + 516
    side_stones_top = client_top + 166
    global SIDE_STONES
    SIDE_STONES = (
        side_stones_left,
        side_stones_top,
        SIDE_STONES_WIDTH,
        SIDE_STONES_HEIGHT,
    )

    # Chat menu.
    chat_menu_left = client_left + 7
    chat_menu_top = client_top + 345
    global CHAT_MENU
    CHAT_MENU = (
        chat_menu_left,
        chat_menu_top,
        CHAT_MENU_WIDTH,
        CHAT_MENU_HEIGHT,
    )

    # The most recent chat message.
    chat_menu_recent_left = chat_menu_left - 3
    chat_menu_recent_top = chat_menu_top + 98
    global CHAT_MENU_RECENT
    CHAT_MENU_RECENT = (
        chat_menu_recent_left,
        chat_menu_recent_top,
        CHAT_MENU_RECENT_WIDTH,
        CHAT_MENU_RECENT_HEIGHT,
    )

    # The "Login" field on the main login screen.
    login_field_left = client_left + 273
    login_field_top = client_top + 242
    global LOGIN_FIELD
    LOGIN_FIELD = (
        login_field_left,
        login_field_top,
        LOGIN_FIELD_WIDTH,
        LOGIN_FIELD_HEIGHT,
    )

    # The "Password" field on the main login screen.
    pass_field_left = client_left + 275
    pass_field_top = client_top + 258
    global PASS_FIELD
    PASS_FIELD = (
        pass_field_left,
        pass_field_top,
        LOGIN_FIELD_WIDTH,
        LOGIN_FIELD_HEIGHT,
    )

    # The entire minimap.
    minimap_left = client_left + 571
    minimap_top = client_top + 11
    global MINIMAP
    MINIMAP = (minimap_left, minimap_top, MINIMAP_WIDTH, MINIMAP_HEIGHT)

    # The current minimap "slice" for locating the player on the world map.
    # The largest area of the minimap, centered on the player, that can be
    #   used to determine the player's location for the travel() function.
    minimap_slice_left = client_left + 599
    minimap_slice_top = client_top + 43
    global MINIMAP_SLICE
    MINIMAP_SLICE = (
        minimap_slice_left,
        minimap_slice_top,
        MINIMAP_SLICE_WIDTH,
        MINIMAP_SLICE_HEIGHT,
    )

# coding=UTF-8
"""
Contains non-skilling player behaviors.

"""
import logging as log
import pathlib
import random as rand
import sys
import time

import cv2
import numpy as np
import pyautogui as pag
from ocvbot import banking
from ocvbot import inputs
from ocvbot import interface
from ocvbot import misc
from ocvbot import startup as start
from ocvbot import vision as vis


# TODO: Move login and world-switcher functions to login_menu.py.
# TODO: Add switch_worlds_logged_in()


# TODO: Add tests.
# TODO: Move to login_menu.py
def switch_worlds_logged_out(world: str, attempts=5) -> bool:
    MAX_COLUMNS = 7
    X_OFFSET = 93
    Y_OFFSET = 19

    # Get world's row and col
    world_info = start.worlds[world]
    column = world_info["column"]
    row = world_info["row"]

    # Click world switch button
    switcher_clicked = vis.Vision(
        region=vis.CLIENT, needle="needles/login-menu/world-switcher-logged-out.png"
    ).click_needle()

    if switcher_clicked is False:
        log.error("Unable to find world switcher!")
        return False

    # Wait for green world filter button, fails if filter is not set correctly
    world_filter = vis.Vision(
        region=vis.CLIENT, needle="needles/login-menu/world-filter-enabled.png"
    ).wait_for_needle()

    if world_filter is False:
        enabled_filter = interface.enable_button(
            "needles/login-menu/world-filter-disabled.png",
            vis.CLIENT,
            "needles/login-menu/world-filter-enabled.png",
            vis.CLIENT,
        )
        if enabled_filter is False:
            return False

    # If the world is off screen
    if column > MAX_COLUMNS:
        # Click next page until the world is on screen
        times_to_click = column % MAX_COLUMNS
        next_page_button = vis.Vision(
            region=vis.CLIENT, needle="needles/login-menu/next-page.png"
        ).click_needle(number_of_clicks=times_to_click)

        if next_page_button is False:
            log.error("Unable to find next page button!")
            return False

        # Set the world's col to max, it'll always be in the last col
        # after it's visible
        col = MAX_COLUMNS

    # Coordinates for the first world
    first_world_x = vis.client_left + 110
    first_world_y = vis.client_top + 43

    # Apply offsets using the first world as a base
    x = first_world_x + ((col - 1) * X_OFFSET)
    y = first_world_y + ((row - 1) * Y_OFFSET)

    # Click a random spot in the world's button
    for _ in range(attempts):
        inputs.Mouse(region=(x, y, 32, 6), move_duration_range=(50, 200)).click_coord()

        # Wait for login screen
        login_screen = vis.Vision(
            region=vis.CLIENT, needle="needles/login-menu/orient-logged-out.png"
        ).wait_for_needle()
        if login_screen is True:
            return True

    log.error("Timed out waiting for login screen!")
    return False


# TODO: Move to inventory.py
def check_skills() -> None:
    """
    Used to mimic human-like behavior. Checks the stats of a random
    skill.

    Returns:
        Returns after hovering mouse over skill.

    """
    open_side_stone("skills")
    inputs.Mouse(region=vis.INV).move_to()
    misc.sleep_rand(1000, 7000)
    return


# TODO: Move to inventory.py
def drop_item(
    item,
    random_wait: bool = True,
    shift_click: bool = True,
) -> None:
    """
    Drops all instances of the provided item from the inventory.
    The "Shift+Click" setting to drop items MUST be enabled in the OSRS
    client.

    Args:
       item (file): Filepath to an image of the item to drop, as it
                    appears in the player's inventory.
       random_wait (bool): Whether to roll for a chance to randomly wait
                           while dropping items. Default is True.
       shift_click (bool): Whether to hold down Shift before clicking the
                           item. This arg only exists because it must be
                           disabled when running unit tests with PyTest and
                           feh -- don't change it unless you know what
                           you're doing. Default is True.

    Examples:
        drop_item("./needles/items/iron-ore.png")

    Returns:
        Returns when all instances of the given item have been dropped, or when
        there were already zero instances of the given item in the inventory.

    Raises:
        Raises start.InventoryError if not all instances of the given item could
        be dropped.
    """
    # TODO: Create four objects, one for each quadrant of the inventory
    #   and rotate dropping items randomly among each quadrant to make
    #   item-dropping more randomized.

    open_side_stone("inventory")

    number_of_items = vis.Vision(region=vis.INV, needle=item).count_needles()
    if number_of_items == 0:
        log.info("No instances of item %s exist in the inventory", item)
        return

    log.info("Dropping %s instances of %s", number_of_items, item)
    for _ in range(35):

        if shift_click:
            pag.keyDown("shift")
        # Alternate between searching for the item in left half and the
        #   right half of the player's inventory. This helps reduce the
        #   chances the bot will click on the same item twice.
        vis.Vision(region=vis.INV_RIGHT_HALF, needle=item, loop_num=1).click_needle(
            sleep_range=(10, 50, 10, 50)
        )
        vis.Vision(region=vis.INV_LEFT_HALF, needle=item, loop_num=1).click_needle(
            sleep_range=(10, 50, 10, 50)
        )

        # Search the entire inventory to check if the item is still
        #   there.
        item_remains = vis.Vision(
            region=vis.INV, loop_num=1, needle=item
        ).wait_for_needle()

        # Chance to sleep while dropping items.
        if random_wait:
            misc.sleep_rand_roll(chance_range=(30, 40), sleep_range=(1000, 20000))

        if shift_click:
            pag.keyUp("shift")
        if item_remains is False:
            return

    raise start.InventoryError("Tried dropping item too many times!")


def human_behavior_rand(chance) -> None:
    """
    Randomly chooses from a list of human behaviors if the roll passes.
    This is done to make the bot appear more human.

    Args:
        chance (int): The number that must be rolled for a random
                      behavior to be triggered. For example, if this
                      parameter is 25, then there is a 1 in 25 chance
                      for the roll to pass.

    Returns:
        Returns after random human behavior has been completed.
    """
    roll = rand.randint(1, chance)
    log.debug("Human behavior rolled %s", roll)

    if roll == chance:
        log.info("Attempting to act human.")
        roll = rand.randint(1, 2)
        if roll == 1:
            check_skills()
        elif roll == 2:
            roll = rand.randint(1, 8)
            if roll == 1:
                open_side_stone("attacks")
            elif roll == 2:
                open_side_stone("quests")
            elif roll == 3:
                open_side_stone("equipment")
            elif roll == 4:
                open_side_stone("prayers")
            elif roll == 5:
                open_side_stone("spellbook")
            elif roll == 6:
                open_side_stone("music")
            elif roll == 7:
                open_side_stone("friends")
            elif roll == 8:
                open_side_stone("settings")


# TODO: Move to login_menu.py
def login_basic(
    username_file=start.config["main"]["username_file"],
    password_file=start.config["main"]["password_file"],
    cred_sleep_range: tuple[int, int] = (800, 5000),
) -> bool:
    """
    Performs a login without checking if the login was successful.

    Advances to the user credentials screen, enters the user's
    credentials, and submits the user's credentials, that's it.

    Args;
        username_file (file): The path to a file containing the user's
                              username login, by default reads the
                              `username_file` field in the main config
                              file.
        password_file (file): The path to a file containing the user's
                              password, by default reads the
                              `password_file` field in the main config
                              file.
        cred_sleep_range (tuple): A 2-tuple containing the minimum and
                                  maximum number of miliseconds to wait
                                  between actions while entering account
                                  credentials, default is (800, 5000).
    Returns:
        Returns True if credentials were entered and a login was
        initiated. Returns False otherwise.

    """
    # Remove line breaks from credential files to make logging in more
    #   predictable.
    username = open(username_file, "r", encoding="utf-8").read()
    username = str(username.replace("\n", ""))
    password = open(password_file, "r", encoding="utf-8").read()
    password = str(password.replace("\n", ""))

    for _ in range(1, 3):
        log.info("Logging in.")

        # Click the "Ok" button if it's present at the login screen.
        # This button appears if the user was disconnected due to
        #   inactivity.
        ok_button = vis.Vision(
            region=vis.CLIENT, needle="./needles/login-menu/ok-button.png", loop_num=1
        ).click_needle()
        # If the "Ok" button isn't found, look for the "Existing user"
        #   button.
        existing_user_button = vis.Vision(
            region=vis.CLIENT,
            needle="./needles/login-menu/existing-user-button.png",
            loop_num=1,
        ).click_needle()

        if existing_user_button is True or ok_button is True:
            credential_screen = vis.Vision(
                region=vis.CLIENT,
                needle="./needles/login-menu/login-cancel-buttons.png",
                loop_num=5,
            ).wait_for_needle()

            if credential_screen is True:
                # Click to make sure the "Login" field is active.
                inputs.Mouse(region=(vis.LOGIN_FIELD)).click_coord()
                # Enter login field credentials.
                misc.sleep_rand(cred_sleep_range[0], cred_sleep_range[1])
                inputs.Keyboard(log_keys=False).typewriter(username)
                misc.sleep_rand(cred_sleep_range[0], cred_sleep_range[1])

                # Click to make sure the "Password" field is active.
                inputs.Mouse(region=(vis.PASS_FIELD)).click_coord()
                # Enter password field credentials and login.
                inputs.Keyboard(log_keys=False).typewriter(password)
                misc.sleep_rand(cred_sleep_range[0], cred_sleep_range[1])

                inputs.Keyboard().keypress(key="enter")
                return True

    log.critical("Could not perform login!")
    return False


# TODO: Move to login_menu.py
def login_full(
    login_sleep_range: tuple[int, int] = (500, 5000),
    postlogin_sleep_range: tuple[int, int] = (500, 5000),
    username_file=start.config["main"]["username_file"],
    password_file=start.config["main"]["password_file"],
) -> bool:
    """
    Logs into the client using the credentials specified in the main
    config file. Waits until the login is successful before returning.

    Args:
        login_sleep_range (tuple): A 2-tuple containing the minimum and
                                   maximum number of miliseconds to wait
                                   after hitting "Enter" to login,
                                   default is (500, 5000).
        postlogin_sleep_range (tuple): The minimum and maximum number of
                                       miliseconds to wait after clicking
                                       the "Click here to play" button,
                                       default is (500, 5000).

    Raises:
        Raises an exception if the login was not successful for any
        reason.

    Returns:
        Returns True if the login was successful.

    """
    log.info("Attempting to login.")
    for _ in range(1, 3):

        login = login_basic(username_file, password_file)
        if login is False:
            raise Exception("Could not perform initial login!")

        misc.sleep_rand(login_sleep_range[0], login_sleep_range[1])
        postlogin_screen_button = vis.Vision(
            region=vis.CLIENT,
            needle="./needles/login-menu/orient-postlogin.png",
            conf=0.8,
            loop_num=10,
            loop_sleep_range=(1000, 2000),
        ).click_needle()

        if postlogin_screen_button is True:
            misc.sleep_rand(postlogin_sleep_range[0], postlogin_sleep_range[1])

            # Wait for the orient function to return true in order to
            #    confirm the login.
            logged_in = vis.Vision(
                region=vis.CLIENT,
                needle="./needles/minimap/orient.png",
                loop_num=50,
                loop_sleep_range=(1000, 2000),
            ).wait_for_needle()
            if logged_in is True:
                # Reset the timer that's used to count the number of
                #   seconds the bot has been running for.
                start.start_time = time.time()
                # Make sure client camera is oriented correctly after
                #   logging in.
                # TODO: move this to a 'configure_camera' function
                pag.keyDown("Up")
                misc.sleep_rand(3000, 7000)
                pag.keyUp("Up")
                return True
            raise Exception("Could not detect login after postlogin screen!")
        # Begin checking for the various non-successful login messages.
        #   This includes messages like "invalid credentials",
        #   "you must be a member to use this world", "cannot
        #   connect to server," etc.
        log.warning("Cannot find postlogin screen!")

        # TODO: Add additional checks to other login messages.
        invalid_credentials = vis.Vision(
            region=vis.CLIENT,
            needle="./needles/login-menu/invalid-credentials.png",
            loop_num=1,
        ).wait_for_needle()
        if invalid_credentials is True:
            raise Exception("Invalid user credentials!")
        log.critical("Cannot find postlogin screen!")

    raise Exception("Unable to login!")


# TODO: Move to inventory.py
def logout() -> None:
    """
    If the client is logged in, logs out.

    Raises:
        Raises an exception if the client could not logout.

    Returns:
        Returns if the logout was successful, or the client is already logged
        out.

    """
    # Make sure the client is logged in.
    if vis.orient()[0] == "logged_out":
        log.warning("Client already logged out!")
        return

    log.info("Attempting to logout.")
    banking.close_bank()
    open_side_stone("logout")

    def is_logged_out() -> bool:
        logged_out = vis.Vision(
            region=vis.CLIENT,
            needle="./needles/login-menu/orient-logged-out.png",
            loop_num=5,
            loop_sleep_range=(1000, 1200),
        ).wait_for_needle()
        if logged_out is True:
            return True

    # Look for any one of the three possible logout buttons.
    for _ in range(5):

        # The standard logout button.
        logout_button = vis.Vision(
            region=vis.INV,
            needle="./needles/side-stones/logout/logout.png",
            conf=0.9,
            loop_num=1,
        ).click_needle(move_away=True)
        if logout_button is True:
            if is_logged_out() is True:
                return

        # The logout button as it appears when the mouse is over it.
        logout_button_highlighted = vis.Vision(
            region=vis.INV,
            needle="./needles/side-stones/logout/logout-highlighted.png",
            conf=0.9,
            loop_num=1,
        ).click_needle(move_away=True)
        if logout_button_highlighted is True:
            if is_logged_out() is True:
                return

        # The logout button when the world switcher is open.
        logout_button_world_switcher = vis.Vision(
            region=vis.SIDE_STONES,
            needle="./needles/side-stones/logout/logout-world-switcher.png",
            conf=0.95,
            loop_num=1,
        ).click_needle(move_away=True)
        if logout_button_world_switcher is True:
            if is_logged_out() is True:
                return

    raise Exception("Could not logout!")


# TODO: Move to misc.py
def logout_break_range() -> None:
    """
    Triggers a random logout within a specific range of times, set by the user
    in the main config file. Additional configuration for this function is set
    by variables in startup.py.

    To determine when a logout roll should occur, this function creates five
    evenly-spaced timestamps at which to roll for a logout. These timestamps
    are called "checkpoints". Each roll has a 1/5 chance to pass. The first and
    last checkpoints are based on the user-defined minimum and maximum session
    duration. As a result of this, the last checkpoint's roll always has a 100%
    chance of success. All variables set by this function are reset if a logout
    roll passes.

    When called, this function checks if an checkpoint's timestamp has passed
    and hasn't yet been rolled. If true, it rolls for that checkpoint and marks
    it (so it's not rolled again). If the roll passes, a logout is called and
    all checkpoints are reset. If the roll fails or a checkpoint's timestamp
    hasn't yet passed, the function does nothing and returns.

    """
    current_time = round(time.time())

    # If a checkpoint's timestamp has passed, roll for a logout, then set
    #   a global variable so that checkpoint isn't rolled again.
    if current_time >= start.checkpoint_1 and start.checkpoint_1_checked is False:
        log.info("Rolling for checkpoint 1...")
        start.checkpoint_1_checked = True
        logout_break_roll(5)

    elif current_time >= start.checkpoint_2 and start.checkpoint_2_checked is False:
        log.info("Rolling for checkpoint 2...")
        start.checkpoint_2_checked = True
        logout_break_roll(5)

    elif current_time >= start.checkpoint_3 and start.checkpoint_3_checked is False:
        log.info("Rolling for checkpoint 3...")
        start.checkpoint_3_checked = True
        logout_break_roll(5)

    elif current_time >= start.checkpoint_4 and start.checkpoint_4_checked is False:
        log.info("Rolling for checkpoint 4...")
        start.checkpoint_4_checked = True
        logout_break_roll(5)

    # The last checkpoint's timestamp is based on the maximum session
    #   duration, so force a logout and reset all the other checkpoints.
    elif current_time >= start.checkpoint_5:
        start.checkpoint_1_checked = False
        start.checkpoint_2_checked = False
        start.checkpoint_3_checked = False
        start.checkpoint_4_checked = False
        logout_break_roll(1)

    # Print the correct logging information according to which checkpoint(s)
    #   have been rolled for.
    else:
        if start.checkpoint_1_checked is False:
            log.info("Checkpoint 1 is at %s", time.ctime(start.checkpoint_1))
        elif start.checkpoint_1_checked is True and start.checkpoint_2_checked is False:
            log.info("Checkpoint 2 is at %s", time.ctime(start.checkpoint_2))
        elif start.checkpoint_2_checked is True and start.checkpoint_3_checked is False:
            log.info("Checkpoint 3 is at %s", time.ctime(start.checkpoint_3))
        elif start.checkpoint_3_checked is True and start.checkpoint_4_checked is False:
            log.info("Checkpoint 4 is at %s", time.ctime(start.checkpoint_4))
        elif start.checkpoint_4_checked is True:
            log.info("Checkpoint 5 is at %s", time.ctime(start.checkpoint_5))


# TODO: Move to misc.py
def logout_break_roll(
    chance,
    min_break_duration=int(start.config["main"]["min_break_duration"]),
    max_break_duration=int(start.config["main"]["max_break_duration"]),
) -> None:
    """
    Rolls for a chance to take a logout break.

    Args:
        chance (int): See wait_rand()'s docstring.
        min_break_duration (int): The minimum number of minutes to wait
                                  if the roll passes, by default reads
                                  the config file.
        max_break_duration (int): The maximum number of minutes to wait
                                  if the roll passes, by default reads
                                  the config file.

    """
    logout_roll = rand.randint(1, chance)
    log.info("Logout roll was %s, needed %s", logout_roll, chance)

    if logout_roll == chance:
        log.info("Random logout called.")
        logout()
        # Make sure all checkpoints are reset.
        start.checkpoint_1_checked = False
        start.checkpoint_2_checked = False
        start.checkpoint_3_checked = False
        start.checkpoint_4_checked = False

        # Track the number of play sessions that have occurred so far.
        start.session_num += 1
        log.info("Completed session %s/%s", start.session_num, start.session_total)

        # If the maximum number of sessions has been reached, kill the bot.
        if start.session_num >= start.session_total:
            log.info("Final session completed! Script done.")
            sys.exit(0)

        else:
            # Convert from minutes to miliseconds.
            min_break_duration *= 60000
            max_break_duration *= 60000
            wait_time_seconds = misc.rand_seconds(
                min_break_duration, max_break_duration
            )

            # Convert back to human-readable format for logging.
            wait_time_minutes = wait_time_seconds / 60
            log.info("Sleeping for %s minutes.", round(wait_time_minutes))

            time.sleep(wait_time_seconds)
            login_full()
    else:
        return


# TODO: Move to inventory.py
def open_side_stone(side_stone) -> bool:
    """
    Opens a side stone menu.

    Args:
        side_stone (str): The name of the side stone to open. Available
                          options are `attacks`, `skills`, `quests`,
                          `inventory`, `equipment`, `prayers`, `spellbook`,
                          `clan`, `friends`, `account`, `logout`,
                          `settings`, `emotes`, and `music`.

    Returns:
        Returns True if desired side stone was opened or is already open.

    Raises:
        Raises an exception if side stone could not be opened.

    """
    side_stone_open = "./needles/side-stones/open/" + side_stone + ".png"
    side_stone_closed = "./needles/side-stones/closed/" + side_stone + ".png"

    try:
        banking.close_bank()
        log.debug("Ensuring side stone %s is open", side_stone)
        interface.enable_button(
            button_disabled=side_stone_closed,
            button_disabled_region=vis.SIDE_STONES,
            button_enabled=side_stone_open,
            button_enabled_region=vis.SIDE_STONES,
            conf=0.98,
        )
    except Exception as error:
        raise Exception("Could not open side stone!") from error
    return True


# TODO: Update the terminology used in this function. Make sure to
#   distinguish between "waypoint" and "destination". Probably going to
#   redefine "waypoint" to be "the coordinates that you click on the
#   minimap to tell your character to walk to", and "destination" to be
#   "the desired coordinates you want your character to be at".
def travel(param_list, haystack_map, attempts=100) -> bool:
    """
    Clicks on the minimap until the player has arrived at the desired
    coordinates.

    Here's an example of what the arguments might look like for this
    function:

        ([((240, 399), 1, (4, 4), (5, 10)),   <- This is the first waypoint.
        ((420, 401),  3, (25, 25), (5, 10))], <- This is the second waypoint.
        haystack.png, 150)

        (240, 399) = The first waypoint is at X=240 Y=399, relative to
                     haystack.png.
        1 = Issued "walk" or "run" commands will vary by 1 coordinate
            when travelling to the waypoint.
        (4, 4) = The player will have arrived at the waypoint when they're
                 within 4 coordinates of the waypoint's coordinates.
        (5, 10) = The function will wait between 5 and 10 seconds between
                  each "walk" or "run" command.
        150 = The function will issue a total of 150 "walk" or "run"
              commands before giving up.

    Args:
        param_list (list): A list of tuples containing the parameters that
                           describe how to get the player to the wapoint(s).
                           Each tuple in the list describes a single
                           waypoint with its associated parameters.
                           Each tuple in the list containes three tuples
                           and an integer in the following order:
                           - A 2-tuple of the desired (X, Y) coordinates
                             to travel to. This is the waypoint's coordinates
                             relative to the haystack map's coordinates.
                           - An integer of the coordinate tolerance for
                             each minimap click.
                           - A 2-tuple of the (X, Y) tolerance allowed
                             for determining if the player has reached
                             the waypoint.
                           - A 2-tuple of the minimum and maximum number of
                             seconds to sleep before re-checking position
                             while going to that waypoint.
        haystack_map (file): Filepath to the map to use to navigate.
                             All waypoint coordinates are relative to
                             this map.
        attempts (int): The number of "walk" or "run" commands the function
                        will issue to the player before giving up.

    Raises:
        Logs out if any errors occur.

    """
    # TODO: Make this function travel to a single waypoint only.
    #   Create a separate function if multiple waypoints need to be
    #   joined together.

    # Make sure file path is OS-agnostic.
    haystack_map = str(pathlib.Path(haystack_map))
    haystack = cv2.imread(haystack_map, cv2.IMREAD_GRAYSCALE)

    # Loop through each waypoint.
    # TODO: Change param_list to a dictionary so parameter names can be
    #   seen when this function is called.
    log.info("Travelling to location.")
    for params in param_list:

        # Break down the parameters for the current waypoint.
        waypoint, coord_tolerance, waypoint_tolerance, sleep_range = params

        for attempt in range(1, attempts):

            if attempt > attempts:
                log.error("Could not reach destination!")
                return False

            # Find the minimap position within the haystack map.
            coords = ocv_find_location(haystack)
            (
                coords_map_left,
                coords_map_top,
                coords_map_width,
                coords_map_height,
            ) = coords

            # Get center of minimap coordinates within haystack map.
            coords_map_x = int(coords_map_left + (coords_map_width / 2))
            coords_map_y = int(coords_map_top + (coords_map_height / 2))

            # Get center of minimap coordinates within client.
            # Absolute coordinates are used rather than using an image
            #   search to speed things up.
            coords_client_x = vis.CLIENT[0] + 642
            coords_client_y = vis.CLIENT[1] + 85

            # Figure out how far the waypoint is from the current location.
            waypoint_distance_x = waypoint[0] - coords_map_x
            waypoint_distance_y = waypoint[1] - coords_map_y
            log.debug(
                "dest_distance is (x=%s, y=%s)",
                waypoint_distance_x,
                waypoint_distance_y,
            )

            # Check if player has reached waypoint before making the click.
            if (
                abs(waypoint_distance_x) <= waypoint_tolerance[0]
                and abs(waypoint_distance_y) <= waypoint_tolerance[1]
            ):
                break

            # Generate random click coordinate variation.
            coord_rand = rand.randint(-coord_tolerance, coord_tolerance)
            # If the waypoint's distance is larger than the size of the
            #   minimap (about 50 pixels in either direction), reduce
            #   the click distance to the edge of the minimap.
            if waypoint_distance_x >= 50:
                click_pos_x = coords_client_x + 50 + coord_rand
                # Since the minimap is circular, if the Y-distance is low
                #   enough, we can make the click-position for the X-coordinate
                #   farther left/right to take advantage of the extra space.
                if waypoint_distance_y <= 10:
                    click_pos_x += 13

            # If the waypoint's X distance is negative, we know we
            #   need to subtract X coordinates.
            elif abs(waypoint_distance_x) >= 50:
                click_pos_x = coords_client_x - 50 + coord_rand
                if abs(waypoint_distance_y) <= 10:
                    click_pos_x -= 13
            else:
                click_pos_x = coords_client_x + waypoint_distance_x + coord_rand

            # Do the same thing, but for the Y coordinates.
            coord_rand = rand.randint(-coord_tolerance, coord_tolerance)
            if waypoint_distance_y >= 50:
                click_pos_y = coords_client_y + 50 + coord_rand
                if waypoint_distance_x <= 10:
                    click_pos_y += 13
            elif abs(waypoint_distance_y) >= 50:
                click_pos_y = coords_client_y - 50 + coord_rand
                if abs(waypoint_distance_x) <= 10:
                    click_pos_y -= 13
            else:
                click_pos_y = coords_client_y + waypoint_distance_y + coord_rand

            click_pos_y = abs(click_pos_y)
            click_pos_x = abs(click_pos_x)
            # Holding down CTRL while clicking will cause character to
            #   run.

            if start.config["main"]["ctrl_click_run"] is True:
                pag.keyDown("ctrl")
            inputs.Mouse(
                region=(click_pos_x, click_pos_y, 0, 0),
                sleep_range=(50, 100, 100, 200),
                move_duration_range=(0, 300),
            ).click_coord()
            if start.config["main"]["ctrl_click_run"] is True:
                pag.keyUp("ctrl")
            misc.sleep_rand((sleep_range[0] * 1000), (sleep_range[1] * 1000))

            if (
                abs(waypoint_distance_x) <= waypoint_tolerance[0]
                and abs(waypoint_distance_y) <= waypoint_tolerance[1]
            ):
                break
    # logout()
    # raise Exception('Could not reach destination!')
    return True


def ocv_find_location(haystack) -> tuple[int, int, int, int]:
    """
    OpenCV helper function used by travel() to find the minimap within
    the haystack map.

    Currently hard-coded to using the travel() function, so it's not
    very flexible.

    Args:
        haystack: The haystack to match the needle within. Must be
                  an OpenCV vision object.

    Returns:
        Returns the (left, top, width, height) coordinates of the
        needle within the haystack.

    """
    needle = pag.screenshot(region=vis.MINIMAP_SLICE)
    needle = cv2.cvtColor(np.array(needle), cv2.COLOR_RGB2GRAY)
    w, h = needle.shape[::-1]
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(result)
    match = loc[3]
    return match[0], match[1], w, h

# coding=UTF-8
"""
Contains non-skilling player behaviors.

"""
import logging as log
import random as rand
import sys
import time

import cv2
import numpy as np
import pathlib
import pyautogui as pag

from ocvbot import input, vision as vis, startup as start, vision, misc


# TODO
def switch_worlds_logged_in(members=False, free_to_play=True, safe=True):
    if members is False and free_to_play is False:
        raise Exception('A world type must be selected!')


# TODO
def switch_worlds_logged_out():
    pass


def login_basic(username_file=start.config.get('main', 'username_file'),
                password_file=start.config.get('main', 'password_file'),
                cred_sleep_range=(800, 5000)):
    """
    Performs a login without checking if the login was successful.

    Advances to the user credentials screen, enters the user's
    credentials, and submits the user's credentials, that's it.

    Args;
        username_file (file): The path to a file containing the user's
                              username login, by default reads the
                              'username_file' field in the main config
                              file.
        password_file (file): The path to a file containing the user's
                              password, by default reads the
                              'password_file' field in the main config
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
    username = open(username_file, 'r').read()
    username = str(username.replace('\n', ''))
    password = open(password_file, 'r').read()
    password = str(password.replace('\n', ''))

    for _ in range(3):
        log.info('Logging in.')

        # Click the "Ok" button if it's present at the login screen.
        # This button appears if the user was disconnected due to
        #   inactivity.
        ok_button = vis.Vision(ltwh=vis.client,
                               needle='./needles/login-menu/ok-button.png',
                               loop_num=1).click_image()
        # If the "Ok" button isn't found, look for the "Existing user"
        #   button.
        existing_user_button = vis.Vision(ltwh=vis.client,
                                          needle='./needles/login-menu/existing-user-button.png',
                                          loop_num=1).click_image()

        if existing_user_button is True or ok_button is True:
            credential_screen = vis.Vision(ltwh=vis.client,
                                           needle='./needles/login-menu/login-cancel-buttons.png',
                                           loop_num=5).wait_for_image()

            if credential_screen is True:
                # Click to make sure the "Login" field is active.
                input.Mouse(ltwh=(vis.login_field_left, vis.login_field_top,
                                  start.LOGIN_FIELD_WIDTH, start.LOGIN_FIELD_HEIGHT)).click_coord()
                # Enter login field credentials.
                misc.sleep_rand(cred_sleep_range[0], cred_sleep_range[1])
                input.Keyboard(log_keys=False).typewriter(username)
                misc.sleep_rand(cred_sleep_range[0], cred_sleep_range[1])

                # Click to make sure the "Password" field is active.
                input.Mouse(ltwh=(vis.pass_field_left, vis.pass_field_top,
                                  start.LOGIN_FIELD_WIDTH, start.LOGIN_FIELD_HEIGHT)).click_coord()
                # Enter password field credentials and login.
                input.Keyboard(log_keys=False).typewriter(password)
                misc.sleep_rand(cred_sleep_range[0], cred_sleep_range[1])

                input.Keyboard().keypress(key='enter')
                return True

    log.error('Could perform login!')
    return False


def login_full(login_sleep_range=(500, 5000), postlogin_sleep_range=(500, 5000),
               username_file=start.config.get('main', 'username_file'),
               password_file=start.config.get('main', 'password_file')):
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
    for _ in range(3):

        login = login_basic(username_file, password_file)
        if login is False:
            raise Exception('Could not perform initial login!')

        misc.sleep_rand(login_sleep_range[0], login_sleep_range[1])
        postlogin_screen_button = vis.Vision(ltwh=vis.display,
                                             needle='./needles/login-menu/orient-postlogin.png',
                                             conf=0.8, loop_num=10, loop_sleep_range=(1000, 2000)).click_image()

        if postlogin_screen_button is True:
            misc.sleep_rand(postlogin_sleep_range[0], postlogin_sleep_range[1])

            # Wait for the orient function to return true in order to
            #    confirm the login.
            logged_in = vis.Vision(ltwh=vis.display,
                                   needle='./needles/minimap/orient.png',
                                   loop_num=50, loop_sleep_range=(1000, 2000)).wait_for_image()
            if logged_in is True:
                # Reset the timer that's used to count the number of
                #   seconds the bot has been running for.
                start.start_time = time.time()
                # Make sure client camera is oriented correctly after
                #   logging in.
                pag.keyDown('Up')
                misc.sleep_rand(3000, 7000)
                pag.keyUp('Up')
                return True
            else:
                raise Exception('Could not detect login after postlogin screen!')

        else:
            # Begin checking for the various non-successful login messages.
            #   This includes messages like "invalid credentials",
            #   "you must be a member to use this world", "cannot
            #   connect to server," etc.
            log.warning('Cannot find postlogin screen!')

            # TODO: add additional checks to other login messages
            invalid_credentials = vis.Vision(ltwh=vis.display,
                                             needle='./needles/login-menu/invalid-credentials.png',
                                             loop_num=1).wait_for_image()
            if invalid_credentials is True:
                raise Exception('Invalid user credentials!')
            log.error('Cannot find postlogin screen!')

    raise Exception('Unable to login!')


def logout():
    """
    If the client is logged in, logs out.

    Raises:
        Raises an exception if the client could not logout.

    Returns:
        Returns True if the logout was successful.

    """
    # Make sure the client is logged in.
    if vis.orient()[0] == 'logged_out':
        log.warning('Client already logged out!')
        return True

    open_side_stone('logout')

    logout_button_world_switcher = False
    logout_button_highlighted = False
    logout_button = False

    # Look for any of the three possible logout buttons.
    for _ in range(5):
        # The standard logout button.
        logout_button = vis.Vision(ltwh=vis.inv,
                                   needle='./needles/side-stones/logout/logout.png',
                                   conf=0.9, loop_num=1).wait_for_image(get_tuple=True)
        if isinstance(logout_button, tuple) is True:
            # Break out of the loop if any of the buttons was found.
            break

        # The logout button as it appears when the mouse is over it.
        logout_button_highlighted = vis.Vision(ltwh=vis.inv,
                                               needle='./needles/side-stones/logout/logout-highlighted.png',
                                               conf=0.9, loop_num=1).wait_for_image(get_tuple=True)
        if isinstance(logout_button_highlighted, tuple) is True:
            logout_button = logout_button_highlighted
            break

        # TODO: fix missing logout-world-switcher.png
        # The logout button when the world switcher is open.
        logout_button_world_switcher = vis.Vision(ltwh=vis.side_stones,
                                                  needle='./needles/side-stones/logout/logout-world-switcher.png',
                                                  conf=0.9, loop_num=1).wait_for_image(get_tuple=True)
        if isinstance(logout_button_world_switcher, tuple) is True:
            logout_button = logout_button_world_switcher
            break

    if logout_button is False and logout_button_highlighted is False \
            and logout_button_world_switcher is False:
        raise Exception("Failed to find logout button!")

    # Once a logout button has been found, click on its coordinates
    #   and wait for the logout to complete.
    # If a logout is not detected after the first try, keep clicking
    #   on the location of the detected logout button and try again.
    input.Mouse(ltwh=logout_button).click_coord(move_away=True)
    for tries in range(5):
        logged_out = vis.Vision(ltwh=vis.client,
                                needle='./needles/login-menu/orient-logged-out.png',
                                loop_num=5, loop_sleep_range=(1000, 1200)).wait_for_image()
        if logged_out is True:
            log.info('Logged out after trying %s times(s)', tries)
            return True
        else:
            log.info('Unable to log out, trying again.')
            input.Mouse(ltwh=logout_button).click_coord(move_away=True)

    raise Exception('Could not logout!')


def logout_break_range():
    """
    Triggers a random logout within a specific range of times, set
    by the user in the main config file. Additional configuration for
    this function is set by variables in startup.py.

    To determine when a logout roll should occur, this function creates
    five evenly-spaced timestamps at which to roll for a logout. These
    timestamps are called "checkpoints" interanally. Each roll has a
    1/5 chance to pass. The first and last checkpoints are based on the
    user-defined minimum and maximum session duration. As a result of
    this, the last checkpoint's roll always has a 100% chance of
    success.
    All variables set by this function are reset if a logout roll passes.

    When called, this function checks if an checkpoint's timestamp has
    passed and hasn't yet been rolled. If true, it rolls for that checkpoint
    and marks it (so it's not rolled again). If the roll passes, a logout
    is called and all checkpoints are reset. If the roll fails or a
    checkpoint's timestamp hasn't yet passed, the function does nothing
    and returns.

    """
    # TODO: there's probably a way to refactor all these near-duplicate
    #   if-statements into a single for-loop
    current_time = round(time.time())

    # If a checkpoint's timestamp has passed, roll for a logout, then set
    #   a global variable so that checkpoint isn't rolled again.
    if current_time >= start.checkpoint_1 and start.checkpoint_1_checked is False:
        log.info('Rolling for checkpoint 1...')
        start.checkpoint_1_checked = True
        logout_break_roll(5)

    elif current_time >= start.checkpoint_2 and start.checkpoint_2_checked is False:
        log.info('Rolling for checkpoint 2...')
        start.checkpoint_2_checked = True
        logout_break_roll(5)

    elif current_time >= start.checkpoint_3 and start.checkpoint_3_checked is False:
        log.info('Rolling for checkpoint 3...')
        start.checkpoint_3_checked = True
        logout_break_roll(5)

    elif current_time >= start.checkpoint_4 and start.checkpoint_4_checked is False:
        log.info('Rolling checkpoint 4...')
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
            log.info('Checkpoint 1 is at %s', time.ctime(start.checkpoint_1))
        elif start.checkpoint_1_checked is True and start.checkpoint_2_checked is False:
            log.info('Checkpoint 2 is at %s', time.ctime(start.checkpoint_2))
        elif start.checkpoint_2_checked is True and start.checkpoint_3_checked is False:
            log.info('Checkpoint 3 is at %s', time.ctime(start.checkpoint_3))
        elif start.checkpoint_3_checked is True and start.checkpoint_4_checked is False:
            log.info('Checkpoint 4 is at %s', time.ctime(start.checkpoint_4))
        elif start.checkpoint_4_checked is True:
            log.info('Checkpoint 5 is at %s', time.ctime(start.checkpoint_5))
    return True


def logout_break_roll(chance,
                      wait_min=int(start.config.get('main', 'min_break_duration')),
                      wait_max=int(start.config.get('main', 'max_break_duration'))):
    """
    Rolls for a chance to logout and wait.

    Args:
        chance (int): See wait_rand()'s docstring.
        wait_min (int): The minimum number of minutes to wait if the
                        roll passes, by default reads the config file.
        wait_max (int): The maximum number of minutes to wait if the
                        roll passes, by default reads the config file.

    """
    logout_roll = rand.randint(1, chance)
    log.info('Logout roll was %s', logout_roll)

    if logout_roll == chance:
        log.info('Random logout called.')
        logout()

        # Track the number of play sessions that have occurred so far.
        start.session_num += 1
        log.info('Completed session %s/%s', start.session_num, start.session_total)

        # If the maximum number of sessions has been reached, kill the bot.
        if start.session_num >= start.session_total:
            log.info('Final session completed! Script done.')
            sys.exit(0)

        else:
            # Convert from minutes to miliseconds.
            wait_min *= 60000
            wait_max *= 60000
            wait_time_seconds = misc.rand_seconds(wait_min, wait_max)

            # Convert back to human-readable format for logging.
            wait_time_minutes = wait_time_seconds / 60
            current_time = time.time()
            # Determine the time the break will be done.
            stop_time = current_time + (current_time + wait_time_seconds)
            # Convert from Epoch seconds to tuple for a human-readable
            #   format.
            stop_time_human = time.localtime(stop_time)

            log.info('Sleeping for %s minutes. Break will be over at %s:%s:%s',
                     round(wait_time_minutes), stop_time_human[3],
                     stop_time_human[4], stop_time_human[5])

            time.sleep(wait_time_seconds)
    else:
        return


def open_side_stone(side_stone):
    """
    Opens a side stone menu.

    Args:
        side_stone (str): The name of the side stone to open. Available
                          options are 'attacks', 'skills', 'quests',
                          'inventory', 'equipment', 'prayers', 'spellbook',
                          'clan', 'friends', 'account', 'logout',
                          'settings', emotes', and 'music'.

    Returns:
        Returns True if desired side stone was opened or is already open.

    Raises:
        Raises an exception if side stone could not be opened.

    """
    side_stone_open = ('./needles/side-stones/open/' + side_stone + '.png')
    side_stone_closed = ('./needles/side-stones/closed/' + side_stone + '.png')

    # Some side stones need a higher than default confidence to determine
    #   if they're open.
    stone_open = vis.Vision(ltwh=vis.side_stones, needle=side_stone_open,
                            loop_num=1, conf=0.98).wait_for_image()
    if stone_open is True:
        log.debug('Side stone already open.')
        return True
    else:
        log.debug('Opening side stone...')

    # Try a total of 5 times to open the desired side stone menu using
    #   the mouse.
    for tries in range(6):
        # Move mouse out of the way after clicking so the function can
        #   tell if the stone is open.
        vis.Vision(ltwh=vis.side_stones, needle=side_stone_closed,
                   loop_num=3, loop_sleep_range=(100, 300)). \
            click_image(sleep_range=(0, 200, 0, 200), move_away=True)

        stone_open = vis.Vision(ltwh=vis.side_stones, needle=side_stone_open,
                                loop_num=3, conf=0.98, loop_sleep_range=(100, 200)). \
            wait_for_image()

        if stone_open is True:
            log.info('Opened side stone after %s tries.', tries)
            return True
        # Make sure the bank window isn't open, which would block
        #   access to the side stones.
        vis.Vision(ltwh=vis.game_screen, needle='./needles/buttons/close.png',
                   loop_num=1).click_image()
    raise Exception('Could not open side stone!')


def check_skills():
    """
    Used to mimic human-like behavior. Checks the stats of a random
    skill.

    """
    open_side_stone('skills')
    input.Mouse(ltwh=vis.inv).move_to()
    misc.sleep_rand(1000, 7000)


def human_behavior_rand(chance):
    """
    Randomly chooses from a list of human behaviors if the roll passes.
    This is done to make the bot appear more human.

    Args:
        chance (int): The number that must be rolled for a random
                      behavior to be triggered. For example, if this
                      parameter is 25, then there is a 1 in 25 chance
                      for the roll to pass.

    """
    roll = rand.randint(1, chance)
    log.info('Human behavior rolled %s', roll)
    if roll == chance:
        log.info('Attempting to act human.')
        roll = rand.randint(1, 2)
        if roll == 1:
            check_skills()
        elif roll == 2:
            roll = rand.randint(1, 8)
            if roll == 1:
                open_side_stone('attacks')
            elif roll == 2:
                open_side_stone('quests')
            elif roll == 3:
                open_side_stone('equipment')
            elif roll == 4:
                open_side_stone('prayers')
            elif roll == 5:
                open_side_stone('spellbook')
            elif roll == 6:
                open_side_stone('music')
            elif roll == 7:
                open_side_stone('friends')
            elif roll == 8:
                open_side_stone('settings')
        return
    return


def drop_item(item, track=True, wait_chance=120, wait_min=5000, wait_max=20000):
    """
    Drops all instances of the provided item from the inventory.
    Shift+Click to drop item MUST be enabled.

    Args:
       item (file): Filepath to an image of the item to drop, as it
                    appears in the player's inventory.
       track (bool): Keep track of the number of items dropped in a
                     global variable, default is True.
       wait_chance (int): Chance to wait randomly while dropping item,
                          see wait_rand()'s docstring for more info,
                          default is 50.
       wait_min (int): Minimum number of miliseconds to wait if
                       a wait is triggered, default is 5000.
       wait_max (int): Maximum number of miliseconds to wait if
                       a wait is triggered, default is 20000.
    """
    # TODO: create four objects, one for each quadrant of the inventory
    #   and rotate dropping items randomly among each quadrant to make
    #   item-dropping more randomized.

    # Make sure the inventory tab is selected in the main menu.
    log.debug('Making sure inventory is selected')
    open_side_stone('inventory')

    item_remains = vis.inv.wait_for_image(loop_num=1, needle=item)
    if item_remains is False:
        log.info('Could not find %s', item)
        return False

    log.info('Dropping all instances of %s', item)
    for tries in range(40):

        pag.keyDown('shift')
        # Alternate between searching for the item in left half and the
        #   right half of the player's inventory. This helps reduce the
        #   chances the bot will click on the same item twice.
        item_on_right = \
            vis.inv_right_half(needle=item).click_image(loop_num=1,
                                                        sleep_range=(10, 50, 50, 300),
                                                        move_duration_range=(50, 800))
        # TODO: this "track" parameter is for stats. implement stats!
        if item_on_right is True and track is True:
            start.items_gathered += 1

        item_on_left = \
            vis.inv_left_half(needle=item).click_image(loop_num=1,
                                                       sleep_range=(10, 50, 50, 300),
                                                       move_duration_range=(50, 800))
        if item_on_left is True and track is True:
            start.items_gathered += 1

        # Search the entire inventory to check if the item is still
        #   there.
        item_remains = vis.inv.wait_for_image(loop_num=1, needle=item)

        # Chance to briefly wait while dropping items.
        misc.wait_rand(wait_chance, wait_min, wait_max)

        pag.keyUp('shift')
        if item_remains is False:
            return True

    log.error('Tried dropping item too many times!')
    return False


# TODO:
def bank_config_check(config, status):
    """
    Checks for specific bank configurations in the bank window, such
    as the "All" button being highlighted.

    Args:
        config:
        status:

    Returns:

    """
    if config == 'quantity':
        if status == 'all':
            quantity_all_enabled = vis.Vision(ltwh=vis.game_screen,
                                              needle='./needles/buttons/'
                                                     'bank-preset-all.png',
                                              loop_num=2).wait_for_image()
            if quantity_all_enabled is False:
                quantity_all_disabled = vis.Vision(ltwh)
                return


def open_bank(direction):
    """
    Opens the bank, assuming the player is within a 2 tiles of the booth.

    Args:
        direction (str): The direction of the bank booth. Must be 'north',
                         'south', 'east', or 'west'.

    Returns:

    """
    for _ in range(10):
        one_tile = vis.Vision(ltwh=vis.game_screen,
                              needle='./needles/game-screen/bank/bank-booth-' + direction + '-1-tile.png',
                              loop_num=1, conf=0.85).click_image()

        two_tiles = vis.Vision(ltwh=vis.game_screen,
                               needle='./needles/game-screen/bank/bank-booth-' + direction + '-2-tiles.png',
                               loop_num=1, conf=0.85).click_image()

        if one_tile is True or two_tiles is True:
            bank_open = vis.Vision(ltwh=vis.game_screen,
                                   needle='./needles/buttons/close.png',
                                   loop_num=50).wait_for_image()
            if bank_open is True:
                return True

        misc.sleep_rand(1000, 3000)

    raise Exception('Could not find bank booth!')


def enable_run():
    """
    If run is turned off but energy is full, turns running on.

    """
    # TODO: turn run on when over 75%
    for _ in range(5):
        run_full_off = vis.Vision(ltwh=vis.client,
                                  needle='./needles/buttons/run-full-off.png',
                                  loop_num=1).click_image(move_away=True)
        if run_full_off is True:
            misc.sleep_rand(300, 1000)
            run_full_on = vis.Vision(ltwh=vis.client,
                                     needle='./needles/buttons/run-full-on.png',
                                     loop_num=1).wait_for_image()
            if run_full_on is True:
                return True
        else:
            return False
    log.error('Unable to turn on running!')


def travel(param_list, haystack_map):
    """
    Clicks on the minimap until the plater has arrived at the desired
    coordinates.

    Here's an example of what the arguments might look like for this
    function:
        [((240, 399), 1, (4, 4), (5, 10))], haystack.png
        (240, 399) = The X and Y coordinates of the waypoint on
                     haystack.png.
        1 = The X and Y variation in coordinates that will be used when
            clicking on the minimap.
        (4, 4) = The X and Y variation in coordinates the function will
                 allow when checking if the player has reached the
                 waypoint.
        (5, 10) = The minimum and maximum number of seconds to wait for
                  the player to walk/run to the location clicked on in
                  the minimap.

    Args:
        param_list (list): A list of the coordinates to move the player
                           to, among a few other parameters.
                           Each item in the list containes three tuples
                           and an integer in the following order:
                           - A 2-tuple of the desired XY coordinates.
                           - An integer of the coordinate tolerance for
                             each minimap click.
                           - A 2-tuple of the X and Y tolerance allowed
                             for determining if the player has reached
                             the waypoint.
                           - A 2-tuple of the minimum and maximum number of
                             seconds to sleep before re-checking position
                             while going to that waypoint.
        haystack_map (file): Filepath to the map to use to navigate.
                             All waypoint coordinates are relative to
                             this map.

    Raises:
        Logs out if any errors occur.

    """
    # Make sure file path is OS-agnostic.
    haystack_map = str(pathlib.Path(haystack_map))
    haystack = cv2.imread(haystack_map, cv2.IMREAD_GRAYSCALE)

    # Disable failsafe for now.
    pag.FAILSAFE = False

    # Get the first waypoint.
    for params in param_list:
        # Break down the parameters for that waypoint.
        waypoint, coord_tolerance, waypoint_tolerance, sleep_range = params
        for _ in range(500):

            # Find the minimap position within the haystack map.
            coords = ocv_find_location(haystack)
            (coords_map_left, coords_map_top, coords_map_width, coords_map_height) = coords

            # Get center of minimap coordinates within haystack map.
            coords_map_x = int(coords_map_left + (coords_map_width / 2))
            coords_map_y = int(coords_map_top + (coords_map_height / 2))

            # Get center of minimap coordinates within client.
            # Absolute coordinates are used rather than using an image
            #   search to speed things up.
            coords_client_x = vision.client[0] + 642
            coords_client_y = vision.client[1] + 85

            # Figure out how far the waypoint is from the current location.
            waypoint_distance_x = waypoint[0] - coords_map_x
            waypoint_distance_y = waypoint[1] - coords_map_y
            log.debug('dest_distance x is %s.', waypoint_distance_x)
            log.debug('dest_distance y is %s.', waypoint_distance_y)

            # Check if player has reached waypoint before making the click.
            if (abs(waypoint_distance_x) <= waypoint_tolerance[0] and
                    abs(waypoint_distance_y) <= waypoint_tolerance[1]):
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

            # If the waypoint's X distance is "negative", we know we
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
            # Holding down ctrl while clicking will cause character to
            #   run.
            pag.keyDown('ctrl')
            input.Mouse(ltwh=(click_pos_x, click_pos_y, 0, 0),
                        sleep_range=(50, 100, 100, 200),
                        move_duration_range=(0, 300)).click_coord()
            pag.keyUp('ctrl')
            misc.sleep_rand((sleep_range[0] * 1000), (sleep_range[1] * 1000))

            if (abs(waypoint_distance_x) <= waypoint_tolerance[0] and
                    abs(waypoint_distance_y) <= waypoint_tolerance[1]):
                break
    # logout()
    # raise Exception('Could not reach destination!')
    return True


def ocv_find_location(haystack):
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
    needle = pag.screenshot(region=vision.minimap_slice)
    needle = cv2.cvtColor(np.array(needle), cv2.COLOR_RGB2GRAY)
    w, h = needle.shape[::-1]
    result = cv2.matchTemplate(haystack, needle, cv2.TM_CCOEFF_NORMED)
    loc = cv2.minMaxLoc(result)
    match = loc[3]
    return match[0], match[1], w, h

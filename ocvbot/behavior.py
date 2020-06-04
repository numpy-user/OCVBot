import logging as log
import random as rand
import sys
import time

import pyautogui as pag

from ocvbot import input, misc, vision as vis, startup as start


def switch_worlds_logged_in(members=False, free_to_play=True, safe=True):
    # TODO
    if members is False and free_to_play is False:
        raise Exception("A world type must be selected!")


def switch_worlds_logged_out():
    # TODO
    pass


def login(cred_sleep_min=800, cred_sleep_max=5000,
          login_sleep_min=500, login_sleep_max=5000,
          postlogin_sleep_min=500, postlogin_sleep_max=5000):
    """
    Logs in in using the credentials specified the main config file.

    Args:
        cred_sleep_min (int): The minimum number of miliseconds to wait
                              between actions while entering account
                              credentials, default is 800.
        cred_sleep_max (int): The maximum number of miliseconds to wait
                              between actions while entering account
                              credentials, default is 5000.
        login_sleep_min (int): The minimum number of miliseconds to wait
                               after hitting "Enter" to login, default
                               is 5000.
        login_sleep_max (int): The maximum number of miliseconds to wait
                               after hitting "Enter" to login, default
                               is 15000.
        postlogin_sleep_min (int): The minimum number of miliseconds to
                                   wait after clicking the "Click here
                                   to play" button, default is 5000.
        postlogin_sleep_max (int): The maximum number of miliseconds to
                                   wait after clicking the "Click here
                                   to play" button, default is 10000.

    Raises:
        Raises a runtime error if the login menu cannot be found, the
        postlogin screen cannot be found, or the logged-in client cannot
        be found.
    """

    # Make sure the client is logged out.
    # TODO: use orient() for this, not wait_for_image
    logged_out = vis.display.wait_for_image(needle='./needles/login-menu/'
                                                   'orient-logged-out.png',
                                            loop_num=3,
                                            loop_sleep_min=1000,
                                            loop_sleep_max=2000)
    if logged_out is False:
        raise RuntimeError("Cannot find client or client is not logged out!")

    log.info('Logging in.')

    # Click the "Ok" button if it's present at the login screen.
    # This button appears if the user was disconnected due to idle
    #   activity.
    ok_button = vis.display.click_image(needle='./needles/login-menu/'
                                               'ok-button.png',
                                        loop_num=1)
    # If the "Ok" button isn't found, look for the "Existing user"
    #   button.
    existing_user_button = vis.display.click_image(
        needle='./needles/login-menu/'
               'existing-user-button.png',
        loop_num=1)

    if existing_user_button is True or ok_button is True:
        # Click to make sure the "Login" field is active.
        input.Mouse(left=vis.login_field_left,
                    top=vis.login_field_top,
                    width=start.LOGIN_FIELD_WIDTH,
                    height=start.LOGIN_FIELD_HEIGHT).click_coord()
        # Enter login field credentials.
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        username_file = start.config_file['username_file']
        pag.typewrite(open(username_file, 'r').read(), interval=0.1)
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)

        # Click to make sure the "Password" field is active.
        input.Mouse(left=vis.pass_field_left,
                    top=vis.pass_field_top,
                    width=start.LOGIN_FIELD_WIDTH,
                    height=start.LOGIN_FIELD_HEIGHT).click_coord()
        # Enter password field credentials and login.
        password_file = start.config_file['password_file']
        pag.typewrite(open(password_file, 'r').read(), interval=0.1)
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)

        input.Keyboard().keypress(key='enter')
        misc.sleep_rand(login_sleep_min, login_sleep_max)

        postlogin_screen_button = vis.display. \
            click_image(needle='./needles/login-menu/orient-postlogin.png',
                        conf=0.8,
                        loop_num=50,
                        loop_sleep_min=1000,
                        loop_sleep_max=2000)

        if postlogin_screen_button is True:
            misc.sleep_rand(postlogin_sleep_min, postlogin_sleep_max)
            # Wait for the orient.png to appear in the client window.
            logged_in = vis.display.wait_for_image(needle='./needles/minimap/'
                                                          'orient.png',
                                                   loop_num=50,
                                                   loop_sleep_min=1000,
                                                   loop_sleep_max=3000)
            if logged_in is True:
                # Reset the timer that's used to count the number of
                #   seconds the bot has been running for.
                start.start_time = time.time()
                # Make sure client camera is oriented correctly after
                #   logging in.
                pag.keyDown('Up')
                misc.sleep_rand(3000, 7000)
                pag.keyUp('Up')
                return
            raise RuntimeError("Did not detect login after postlogin!")
        raise RuntimeError("Cannot find postlogin screen!")
    raise RuntimeError("Cannot find existing user or OK button!")


def open_side_stone(side_stone):
    """
    Opens a side stone menu.

    Args:
        side_stone (str): The name of the side stone to open.

    Returns:
        Returns True if desired side stone was opened or is already open.

    Raises:
        Raises an exception if side stone could not be opened.

    """
    side_stone_open = ('./needles/side-stones/open/' + side_stone + '.png')
    side_stone_closed = ('./needles/side-stones/closed/' + side_stone + '.png')

    stone_open = vis.side_stones.wait_for_image(needle=side_stone_open,
                                                loop_num=1)
    if stone_open is True:
        log.debug('Side stone already open.')
        return True
    log.debug('Opening side stone.')

    # Try a total of 5 times to open the desired side stone menu using
    #   the mouse.
    for tries in range(1, 5):
        vis.side_stones.click_image(needle=side_stone_closed,
                                    loop_num=3,
                                    loop_sleep_min=100, loop_sleep_max=300,
                                    sleep_befmax=200, sleep_afmax=200)
        # Move mouse out of the way so the function can tell if the
        #   stone is open.
        input.Mouse(25, 150, 25, 150, move_durmax=100).moverel()
        stone_open = vis.side_stones.wait_for_image(needle=side_stone_open,
                                                    loop_num=3,
                                                    loop_sleep_min=100,
                                                    loop_sleep_max=200)
        if stone_open is True:
            log.info('Opened side stone after ' + str(tries) + ' tries.')
            return True
        # Make sure the bank window isn't open, which would block
        #   access to the side stones.
        vis.game_screen.click_image(
            needle='./needles/buttons/bank-window-close.png', loop_num=1)
    raise Exception('Could not open side stone! Is the hotkey correct?')


def logout():
    """
    If the client is logged in, logs out. Side stone hotkeys MUST be
    enabled.

    Raises:
        Raises a runtime error if the logout side stone is opened but
        the logout button cannot be found.
        Raises a runtime error if the logout button was clicked but the
        logout could not be confirmed.
    """
    # TODO: Check if the world-switcher is open in the logout menu
    #  and close it.

    # First, make sure the client is logged in.
    orient = vis.orient(display_height=start.DISPLAY_HEIGHT,
                        display_width=start.DISPLAY_WIDTH)
    (client_status, unused_var) = orient

    if client_status == 'logged_in':
        open_side_stone('logout')

        logout_button = vis.client.click_image(
            needle='./needles/buttons/logout.png', conf=0.9, loop_num=3)
        logout_button_highlighted = vis.client.click_image(
            needle='./needles/buttons/logout.png', conf=0.9, loop_num=3)

        if logout_button is True or logout_button_highlighted is True:
            for tries in range(1, 10):
                logged_out = vis.client.wait_for_image(
                    needle='./needles/login-menu/orient-logged-out.png',
                    loop_num=30,
                    loop_sleep_min=1000,
                    loop_sleep_max=1500)
                if logged_out is True:
                    log.info('Logged out after trying ' + str(tries) +
                             ' time(s).')
                    return
                log.info('Unable to log out after trying ' + str(tries) +
                         ' time(s).')
                vis.client.click_image(needle='./needles/buttons/'
                                              'logout.png')
            raise RuntimeError("Could not logout!")
        raise RuntimeError("Could not find logout button!")
    log.warning("Client already logged out!")
    return


def logout_rand_range():
    """
    Triggers a random logout within a specific range of time, set
    by the user in the main config file. Additional configuration for
    this function is set by variables in startup.py.

    To determine when a logout roll should occur, this function creates
    five evenly-spaced timestamps at which to roll for a logout.
    Each roll has a 1/5 chance to pass. The first and last timestamps
    are based on the desired minimum and maximum session duration, set
    by the user. The function forces a logout on the fifth and final
    timestamp (aka "checkpoint"). All variables are reset if a logout
    roll passes.

    When called, this function checks if an checkpoint has occurred that
    hasn't yet been rolled. If true, it rolls for that checkpoint and
    marks it (so it's not rolled again). If the roll passes, a logout is
    called and all checkpoints are reset. If it's not time to roll for a
    checkpoint, the function does nothing and returns.
    """

    current_time = round(time.time())

    # If a checkpoint's timestamp has passed, roll for a logout, then set
    #   a global variable so another roll doesn't occur between that
    #   checkpoint and the next checkpoint.
    if current_time >= start.checkpoint_1 and \
            start.checkpoint_1_checked is False:
        log.info('Rolling checkpoint 1')
        start.checkpoint_1_checked = True
        logout_rand(5)

    elif current_time >= start.checkpoint_2 and \
            start.checkpoint_2_checked is False:
        log.info('Rolling checkpoint 2')
        start.checkpoint_2_checked = True
        logout_rand(5)

    elif current_time >= start.checkpoint_3 and \
            start.checkpoint_3_checked is False:
        log.info('Rolling checkpoint 3')
        start.checkpoint_3_checked = True
        logout_rand(5)

    elif current_time >= start.checkpoint_4 and \
            start.checkpoint_4_checked is False:
        log.info('Rolling checkpoint 4')
        start.checkpoint_4_checked = True
        logout_rand(5)

    # The last checkpoint's timestamp is the start time of the session
    #   plus the maximum session duration, so force a logout and
    #   reset all the other checkpoints.
    elif current_time >= start.checkpoint_5:
        start.checkpoint_1_checked = False
        start.checkpoint_2_checked = False
        start.checkpoint_3_checked = False
        start.checkpoint_4_checked = False
        logout_rand(1)

    else:
        log.info('time is ' + str(current_time))
        log.info('Checkpoint 1 is at ' + str(start.checkpoint_1))
        log.info('Checkpoint 2 is at ' + str(start.checkpoint_2))
        log.info('Checkpoint 3 is at ' + str(start.checkpoint_3))
        log.info('Checkpoint 4 is at ' + str(start.checkpoint_4))
        log.info('Checkpoint 5 is at ' + str(start.checkpoint_5))
        log.info('Not time for a logout roll')
        return
    return


def logout_rand(chance,
                wait_min=int(start.config_file['min_break_duration']),
                wait_max=int(start.config_file['max_break_duration'])):
    """
    Rolls for a chance to logout of the client and wait.

    Args:
        chance (int): See wait_rand()'s docstring.
        wait_min (int): The minimum number of minutes to wait if the
                        roll passes, by default reads a config file.
        wait_max (int): The maximum number of minutes to wait if the
                        roll passes, by default reads a config file.
    """

    logout_roll = rand.randint(1, chance)
    log.info('Logout roll was ' + str(logout_roll))
    if logout_roll == chance:
        log.info('Random logout called.')

        # Reset all the logout checkpoints for the next session.
        start.checkpoint_1_checked = False
        start.checkpoint_2_checked = False
        start.checkpoint_3_checked = False
        start.checkpoint_4_checked = False

        logout()

        # Track the number of play sessions that have occurred so far.
        start.session_num += 1
        log.info('Completed session ' + str(start.session_num) + '/'
                 + str(start.session_total))
        # If the maximum number of sessions has been reached, kill the
        #   bot.
        if start.session_num >= start.session_total:
            log.info('Final session completed! Script done.')
            sys.exit(0)

        elif start.session_num < start.session_total:
            # Convert from minutes to miliseconds.
            wait_min *= 60000
            wait_max *= 60000
            wait_time_seconds = misc.rand_seconds(wait_min, wait_max)

            # Convert back to human-readable format for logging.
            wait_time_minutes = wait_time_seconds / 600
            current_time = time.time()
            # Determine the time the break will be done.
            stop_time = current_time + (current_time + wait_time_seconds)
            # Convert from Epoch seconds to tuple for a human-readable
            #   format.
            stop_time_human = time.localtime(stop_time)
            log.info('Sleeping for ' + str(stop_time_human[4]) + ' minutes.' +
                     ' Break will be over at ' + str(stop_time_human[3]) + ':' + str(minute)
                     + ':' + str(second))

            time.sleep(wait_time_seconds)
        else:
            raise RuntimeError('Error with session numbers!')
    else:
        return


def check_skills():
    """
    Used to mimic human-like behavior. Checks the stats of a random
    skill.
    """

    open_side_stone('skills')
    input.Mouse(vis.inv_left, vis.inv_top,
                start.INV_WIDTH, start.INV_HEIGHT).move_to()
    misc.sleep_rand(500, 5000)


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
    log.info('Human behavior rolled ' + str(roll))
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
                open_side_stone('spellbooks')
            elif roll == 6:
                open_side_stone('music')
            elif roll == 7:
                open_side_stone('friends')
            elif roll == 8:
                open_side_stone('settings')
        return
    return


def drop_item(item, track=True,
              wait_chance=120, wait_min=5000, wait_max=20000):
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
        log.info('Could not find ' + str(item) + '.')
        return False

    log.info('Dropping ' + str(item) + '.')
    tries = 0
    while item_remains is True and tries <= 40:

        tries += 1
        pag.keyDown('shift')
        # Alternate between searching for the item in left half and the
        #   right half of the player's inventory. This helps reduce the
        #   chances the bot will click on the same item twice.
        item_on_right = vis.inv_right_half.click_image(loop_num=1,
                                                       sleep_befmin=10,
                                                       sleep_befmax=50,
                                                       sleep_afmin=50,
                                                       sleep_afmax=300,
                                                       move_durmin=50,
                                                       move_durmax=800,
                                                       needle=item)
        if item_on_right is True and track is True:
            start.items_gathered += 1
        item_on_left = vis.inv_left_half.click_image(loop_num=1,
                                                     sleep_befmin=10,
                                                     sleep_befmax=50,
                                                     sleep_afmin=50,
                                                     sleep_afmax=300,
                                                     move_durmin=50,
                                                     move_durmax=800,
                                                     needle=item)
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

    if tries > 40:
        log.error('Tried dropping item too many times!')
        return False
    return True

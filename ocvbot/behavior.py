import logging as log
import random as rand
import sys
import time

import pyautogui as pag

from ocvbot import input, misc, vision as vis, startup as start
# TODO
from ocvbot.misc import wait_rand

"""
def chat(context)
  if context == 'smelting'
    type 'option 1'
    type 'option 2'
  
  elif context == 'blablabla'
  
def move_camera_rand(chance=3,down_min=200,down_max=2000)
    down_arrow_roll = rand.randint(1, chance)
    if down_arrow_roll == chance:
       input.keyDown('Down')
       time.sleep(float(rand.randint(down_min, down_max)))
       input.keyUp('Down')
    left
    right arrow roll
 
def switch_worlds()
"""


def login(username_file='username.txt', password_file='password.txt',
          cred_sleep_min=800, cred_sleep_max=5000,
          login_sleep_min=500, login_sleep_max=5000,
          postlogin_sleep_min=500, postlogin_sleep_max=5000):
    """
    Logs in in using credentials specified in two files.

    Args:
        username_file (file): The filepath of the file containing the
                              user's username. Filepath is relative to
                              the directory this file is in, default is
                              a file simply called "username".
        password_file (file): The filepath of the file containing the
                              user's password. Filepath is relative to
                              the directory this file is in, default is
                              a file simply called "password".
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

    Returns:
        Always returns 0.
    """
    # TODO: fix issue is "password" field is displayed first

    # Check to make extra sure the client is logged out.
    logged_out = vis.vdisplay.click_image(needle='./needles/login-menu/'
                                                 'orient-logged-out.png',
                                          loop_num=1)
    if logged_out == 1:
        raise RuntimeError("Cannot find client!")

    log.info('Logging in.')

    # Click the "Ok" button if it's present at the login screen.
    ok_button = vis.vdisplay.click_image(needle='./needles/login-menu/'
                                                'ok-button.png',
                                         loop_num=1)

    misc.sleep_rand(cred_sleep_min, cred_sleep_max)

    # Make sure the "Existing user" button is present.
    existing_user = vis.vdisplay.wait_for_image(needle='./needles/login-menu/'
                                                'existing-user-button.png',
                                                loop_num=1)
    if existing_user != 1:
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        input.keypress('enter')

    if existing_user != 1 or ok_button != 1:
        # Enter credentials.
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        pag.typewrite(open(username_file, 'r').read())
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        pag.typewrite(open(password_file, 'r').read())
        misc.sleep_rand(cred_sleep_min, cred_sleep_max)
        input.keypress('enter')
        misc.sleep_rand(login_sleep_min, login_sleep_max)

        #try_again = vis.vdisplay.click_image(needle='./needles/'
                                             #'login-menu/try-again-button.png',
                                             #conf=0.9,
                                             #loop_num=30,
                                             #loop_sleep_max=1000)
        #if try_again != 1:
            #pag.keyDown('backspace')
            #misc.sleep_rand(2000, 4000)
            #pag.keyUp('backspace')
            #input.keypress('tab')
            ##pag.keyDown('backspace')
            #misc.sleep_rand(2000, 4000)
            #pag.keyUp('backspace')
#
        # Click the 'click here to play' button in the postlogin menu.
        postlogin = vis.vdisplay.click_image(needle='./needles/'
                                             'login-menu/orient-postlogin.png',
                                             conf=0.8,
                                             loop_num=50,
                                             loop_sleep_min=1000,
                                             loop_sleep_max=3000)
        if postlogin != 1:
            misc.sleep_rand(postlogin_sleep_min, postlogin_sleep_max)
            # Wait for the orient.png to appear in the client window.
            logged_in = vis.vdisplay.wait_for_image(needle='./needles/minimap/'
                                                           'orient.png',
                                                    loop_num=50,
                                                    loop_sleep_min=1000,
                                                    loop_sleep_max=3000)
            if logged_in != 1:
                # Reset the timer that's used to count the number of
                #   seconds the bot has been running for.
                start.start_time = time.time()
                # Make sure client camera is oriented correctly after
                #   logging in.
                pag.keyDown('Up')
                misc.sleep_rand(3000, 7000)
                pag.keyUp('Up')
                return 0
            else:
                raise RuntimeError("Cannot login!")

        else:
            raise RuntimeError("Cannot find postlogin screen!")

    elif existing_user == 1:
        raise RuntimeError("Cannot find existing user button!")


def open_side_stone(side_stone, hotkey):
    """
    Open the specific side stone menu.

    Args:
        side_stone (file): Filepath to an image of the desired side
                           stone in its "closed" state (i.e. with a
                           standard grey background).
        hotkey (str): The key used to open the desired side stone. This
                      is not set by default in the native client and
                      must be enabled.

    Returns:
        Returns 0 if desired side stone was opened or is already open.
        Returns 1 in any other situation.
    """

    stone_closed = vis.vside_stones.wait_for_image(needle=side_stone,
                                                   loop_num=1)
    if stone_closed == 1:
        log.debug('Side stone already open.')
        return 0
    elif stone_closed != 1:
        log.debug('Opening side stone.')
        input.keypress(hotkey)

    # Try a total of 5 times to open the desired side stone menu using
    #   the hotkey.
    for tries in range(1, 5):
        stone_closed = vis.vside_stones.wait_for_image(needle=side_stone,
                                                       loop_num=5,
                                                       loop_sleep_min=100,
                                                       loop_sleep_max=500)
        if stone_closed == 1:
            log.info('Opened side stone')
            return 0
        elif stone_closed != 1:
            # Make sure the bank window isn't open, which would block
            #   access to the side stones.
            vis.vgame_screen.click_image(
                needle='./needles/buttons/bank-window-close.png', loop_num=1)

    # TODO: Click on the side stone with the mouse if it won't open with
    #   the hotkey.

    raise RuntimeError('Could not open side stone! Is the hotkey correct?')


def logout():
    """
    If the client is logged in, logs out. Side stone hotkeys MUST be
    enabled.

    Raises:
        Raises a runtime error if the logout side stone is opened but
        the logout button cannot be found.
        Raises a runtime error if the logout button was clicked but the
        logout could not be confirmed.

    Returns:
        Returns 0 if the client has logged out.
        Returns 1 if the client is already logged out.
    """
    # TODO: Check if the world-switcher is open in the logout menu
    #  and close it.

    # First, make sure the client is logged in.
    orient = vis.orient(display_height=start.DISPLAY_HEIGHT,
                        display_width=start.DISPLAY_WIDTH)
    (client_status, unused_var) = orient

    if client_status == 'logged_in':
        open_side_stone('./needles/side-stones/logout.png',
                        hotkey=start.config_file['side_stone_logout'])

        logout_button = vis.vclient.click_image(
            needle='./needles/buttons/logout.png', conf=0.9, loop_num=10)
        logout_button_highlighted = vis.vclient.click_image(
            needle='./needles/buttons/logout.png', conf=0.9, loop_num=10)

        if logout_button == 0 or logout_button_highlighted == 0:
            for tries in range(1, 10):
                logged_out = vis.vclient.wait_for_image(
                    needle='./needles/login-menu/orient-logged-out.png',
                    loop_num=30,
                    loop_sleep_min=1000,
                    loop_sleep_max=1500)
                if logged_out != 1:
                    log.info('Logged out after trying ' + str(tries) +
                             ' time(s).')
                    return 0
                elif logged_out == 1:
                    log.info('Unable to log out after trying ' + str(tries) +
                             ' time(s).')
                    vis.vclient.click_image(needle='./needles/buttons/'
                                                   'logout.png')
            raise RuntimeError("Could not logout!")

        elif logout_button == 1 and logout_button_highlighted == 1:
            raise RuntimeError("Could not find logout button!")

    elif client_status == 'logged_out':
        log.warning("Client already logged out!")
        return 1
    else:
        return 1


def logout_rand_range():
    """
    Triggers a random logout within a specific range of timestamps, set
    by the user in the main config file. Additional configuration for
    this function is set by variables in startup.py

    Create five evenly-spaced timestamps at which to roll for a logout
    (each roll has a 1/5 chance to pass), based on the desired minimum
    session duration and the desired maximum session duration.
    Everything is reset if a logout roll passes.

    When called, this function checks if it's time to roll for a logout
    and performs the roll if true. If not, it simply does nothing and
    returns.

    Returns:
        Always returns 0
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

    # The last checkpoint's time is the start time plus max_run_duration,
    #   so force a logout and reset all the other checkpoints.
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
        return 0
    return 0

    # TODO: Allow the user to specify a "termination point" after a random
    #  number of logout breaks in which the script will stop completely.
    #
    # config:
    # min_run_duration:  <-- in minutes
    # max_run_duration:
    #
    # min_number_of_runs:
    # max_number_of_runs:
    #
    # Might be better to use the term "sessions" instead of "runs" so as to not
    #   cause confusion with bank runs


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

    Returns:
        Always returns 0.
    """

    logout_roll = rand.randint(1, chance)
    log.info('Logout roll was ' + str(logout_roll))
    if logout_roll == chance:
        log.info('Random logout called.')
        logout()

        # Track the number of play sessions that have occurred so far.
        start.session_num += 1
        log.info('Completed session ' + str(start.session_num) + '/'
                 + str(start.session_total))
        # If the maximum has been reached, kill the bot.
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
            stop_time = time.localtime(stop_time)
            (yr, mon, day, hour, minute, second, wkday, yrday, dls) = stop_time
            log.info('Sleeping for ' + str(wait_time_minutes) + ' minutes.' +
                     ' Break will be over at ' + str(hour) + ':' + str(minute)
                     + ':' + str(second))

            time.sleep(wait_time_seconds)
        else:
            raise RuntimeError('Error with session numbers!')
    return 0


def check_skills():
    """
    Used to mimic human-like behavior. Checks the stats of a random
    skill.
    """

    open_side_stone('./needles/side-stones/skills.png',
                    start.config_file['side_stone_skills'])
    input.move_to(vis.vinv_left, vis.vinv_top,
                  xmin=0, xmax=start.INV_WIDTH,
                  ymin=0, ymax=start.INV_HEIGHT)
    misc.sleep_rand(500, 5000)
    return 0


def human_behavior_rand(chance):
    """
    Randomly chooses from a list of human behaviors if the roll passes.
    This is done to make the bot appear more human.

    Args:
        chance (int): The number that must be rolled for a random
                      behavior to be triggered. For example, if this
                      parameter is 25, then there is a 1 in 25 chance
                      for the roll to pass.
    Returns:
        Always returns 0.
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
                open_side_stone('./needles/side-stones/attacks.png',
                                start.config_file['side_stone_attacks'])
            elif roll == 2:
                open_side_stone('./needles/side-stones/quests.png',
                                start.config_file['side_stone_quests'])
            elif roll == 3:
                open_side_stone('./needles/side-stones/equipment.png',
                                start.config_file['side_stone_equipment'])
            elif roll == 4:
                open_side_stone('./needles/side-stones/prayers.png',
                                start.config_file['side_stone_prayers'])
            elif roll == 5:
                open_side_stone('./needles/side-stones/spellbooks.png',
                                start.config_file['side_stone_spellbook'])
            elif roll == 6:
                open_side_stone('./needles/side-stones/music.png',
                                start.config_file['side_stone_music'])
            elif roll == 7:
                open_side_stone('./needles/side-stones/friends.png',
                                start.config_file['side_stone_friends'])
            elif roll == 8:
                open_side_stone('./needles/side-stones/settings.png',
                                start.config_file['side_stone_settings'])
        else:
            return 0
    elif roll != chance:
        return 0
    return 0


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
    open_side_stone('./needles/side-stones/inventory.png', 'Escape')

    item_remains = vis.vinv.wait_for_image(loop_num=1, needle=item)

    if item_remains != 1:
        log.info('Dropping ' + str(item) + '.')
    elif item_remains == 1:
        log.info('Could not find ' + str(item) + '.')
        return 1

    tries = 0
    while item_remains != 1 and tries <= 40:

        tries += 1
        pag.keyDown('shift')
        # Alternate between searching for the item in left half and the
        #   right half of the player's inventory. This helps reduce the
        #   chances the bot will click on the same item twice.
        item_on_right = vis.vinv_right_half.click_image(loop_num=1,
                                                        click_sleep_befmin=10,
                                                        click_sleep_befmax=50,
                                                        click_sleep_afmin=50,
                                                        click_sleep_afmax=300,
                                                        move_durmin=50,
                                                        move_durmax=800,
                                                        needle=item)
        if item_on_right != 1 and track is True:
            start.items_gathered += 1
        item_on_left = vis.vinv_left_half.click_image(loop_num=1,
                                                      click_sleep_befmin=10,
                                                      click_sleep_befmax=50,
                                                      click_sleep_afmin=50,
                                                      click_sleep_afmax=300,
                                                      move_durmin=50,
                                                      move_durmax=800,
                                                      needle=item)
        if item_on_left != 1 and track is True:
            start.items_gathered += 1

        # Search the entire inventory to check if the item is still
        #   there.
        item_remains = vis.vinv.wait_for_image(loop_num=1, needle=item)

        # Chance to briefly wait while dropping items.
        wait_rand(chance=wait_chance, wait_min=wait_min, wait_max=wait_max)

        pag.keyUp('shift')
        if item_remains == 1:
            return 0

    if tries > 40:
        log.error('Tried dropping item too many times!')
        return 1
    else:
        return 0

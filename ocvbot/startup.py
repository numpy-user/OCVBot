# coding=UTF-8
"""
Sets global variables and constants.

"""
import logging as log
import random as rand
import time

import configparser
import pyautogui as pag

# Read the config file.
config = configparser.ConfigParser()
config.read('./config.ini')

# Constants ------------------------------------------------------------

# See ./docs/client_anatomy.png for more info.
# Captures the width and height of various different elements within the
#  game client. Units are in pixels.

# The entire OSRS game client (in fixed-size mode).
CLIENT_WIDTH = 765
CLIENT_HEIGHT = 503

# The player's inventory.
INV_WIDTH = 186
INV_HEIGHT = 262
INV_HALF_WIDTH = round((INV_WIDTH / 2) + 5)
INV_HALF_HEIGHT = round(INV_HEIGHT / 2)

# The player's inventory plus the top and bottom rows of side stones.
SIDE_STONES_WIDTH = 249
SIDE_STONES_HEIGHT = 366

# The "gameplay screen". This is the screen that displays the player
#   character and the game world.
GAME_SCREEN_WIDTH = 512
GAME_SCREEN_HEIGHT = 334

# The bottom chat menu pane.
CHAT_MENU_WIDTH = 506
CHAT_MENU_HEIGHT = 129

# The most recent "line" in the chat menu's chat history.
CHAT_MENU_RECENT_WIDTH = 490
CHAT_MENU_RECENT_HEIGHT = 17

# The entire display.
DISPLAY_WIDTH = pag.size().width
DISPLAY_HEIGHT = pag.size().height

# The "Login" and "Password" fields on the main login screen.
LOGIN_FIELD_WIDTH = 258
LOGIN_FIELD_HEIGHT = 12

# The entire minimap.
MINIMAP_WIDTH = 146
MINIMAP_HEIGHT = 151

# The largest area of the minimap, centered on the player, that can be
#   used to determine the player's location for the travel() function.
MINIMAP_SLICE_WIDTH = 110
MINIMAP_SLICE_HEIGHT = 73

# TODO: Finish stats
# Stats ----------------------------------------------------------------

# Used for tracking how long the script has been running.
start_time = round(time.time())

# The number of inventories a script has gone through.
inventories = 0
# The number of items gathered, approximately.
items_gathered = 0
# The amount of experience gained since the script started, approximately.
xp_gained = 0
# The amount of experience gained since installing this package
xp_per_hour = 0

ore_xp_dict = {
    'copper': 16.5,
    'iron': 35.5
}

# ----------------------------------------------------------------------
# These variables are used to setup behavior.logout_rand_range(). ------
# ----------------------------------------------------------------------

# Reset initial checkpoint_checked values.
checkpoint_1_checked = False
checkpoint_2_checked = False
checkpoint_3_checked = False
checkpoint_4_checked = False

# Convert run duration within config file from minutes to seconds.
min_session_duration_sec = (int(config.get('main', 'min_session_duration'))) * 60
max_session_duration_sec = (int(config.get('main', 'max_session_duration'))) * 60

# Break the duration of time between the minimum and maximum duration
#   into a set of evenly-sized durations of time. These chunks of time
#   are consecutively added to the start time to create "checkpoints".
#   Checkpoints are timestamps at which a logout roll will occur.
checkpoint_interval = ((max_session_duration_sec - min_session_duration_sec) / 4)

# Space each checkpoint evenly between the min duration and the max
#   duration.
checkpoint_1 = round(start_time + min_session_duration_sec)
checkpoint_2 = round(start_time + min_session_duration_sec + checkpoint_interval)
checkpoint_3 = round(start_time + min_session_duration_sec + (checkpoint_interval * 2))
checkpoint_4 = round(start_time + min_session_duration_sec + (checkpoint_interval * 3))
checkpoint_5 = round(start_time + max_session_duration_sec)

# Determine how many sessions the bot will run for before quitting.
min_sessions = int(config.get('main', 'min_sessions'))
max_sessions = int(config.get('main', 'max_sessions'))
session_total = rand.randint(min_sessions, max_sessions)
log.info('Checkpoint 1 is at %s, session_total is %s', time.ctime(checkpoint_1), session_total)

# The current number of sessions that have been completed.
session_num = 0

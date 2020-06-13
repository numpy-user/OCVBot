# coding=UTF-8
"""
Sets global variables and constants.

"""
import logging as log
import random as rand
import time

import pyautogui as pag
import yaml

# Constants ------------------------------------------------------------

# See ./docs/client_anatomy.png for more info.
# Width and height of the entire game client.
CLIENT_WIDTH = 765
CLIENT_HEIGHT = 503

# Width and height of the inventory screen, in pixels.
INV_WIDTH = 186
INV_HEIGHT = 262
INV_HALF_WIDTH = round((INV_WIDTH / 2) + 5)
INV_HALF_HEIGHT = round(INV_HEIGHT / 2)

SIDE_STONES_WIDTH = 248
SIDE_STONES_HEIGHT = 366

# Width and height of just the game screen in the game client.
GAME_SCREEN_WIDTH = 512
GAME_SCREEN_HEIGHT = 334

CHAT_MENU_WIDTH = 506
CHAT_MENU_HEIGHT = 129

# Dimensions of the most recent "line" in the chat history.
CHAT_MENU_RECENT_WIDTH = 490
CHAT_MENU_RECENT_HEIGHT = 17

# Get the display size in pixels.
DISPLAY_WIDTH = pag.size().width
DISPLAY_HEIGHT = pag.size().height

# Dimensions of the "Login" and "Password" fields on the main login
#   screen.
LOGIN_FIELD_WIDTH = 258
LOGIN_FIELD_HEIGHT = 14

with open('./config.yaml') as config:
    config_file = yaml.safe_load(config)

# Stats ----------------------------------------------------------------

# Used for tracking how long the script has been running.
start_time = round(time.time())

# The number of inventories a script has gone through.
inventories = 0
# The number of items gathered, approximately.
items_gathered = 0
# The amount of experience gained since the script started, approximately.
xp_gained = 0
# TODO:
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
min_session_duration_sec = \
    (int(config_file['min_session_duration'])) * 60
max_session_duration_sec = \
    (int(config_file['max_session_duration'])) * 60

# Break the duration of time between the minimum and maximum duration
#   into a set of evenly-sized durations of time. These chunks of time
#   are consecutively added to the start time to create "checkpoints".
#   Checkpoints are timestamps at which a logout roll will occur.
checkpoint_interval = ((max_session_duration_sec -
                        min_session_duration_sec) / 4)

# Space each checkpoint evenly between the min duration and the max
#   duration.
checkpoint_1 = round(start_time + min_session_duration_sec)
checkpoint_2 = round(start_time + min_session_duration_sec +
                     checkpoint_interval)
checkpoint_3 = round(start_time + min_session_duration_sec +
                     (checkpoint_interval * 2))
checkpoint_4 = round(start_time + min_session_duration_sec +
                     (checkpoint_interval * 3))
checkpoint_5 = round(start_time + max_session_duration_sec)

log.info('Checkpoint 1 is at %s', time.ctime(checkpoint_1))
log.info('Checkpoint 2 is at %s', time.ctime(checkpoint_2))
log.info('Checkpoint 3 is at %s', time.ctime(checkpoint_3))
log.info('Checkpoint 4 is at %s', time.ctime(checkpoint_4))
log.info('Checkpoint 5 is at %s', time.ctime(checkpoint_5))
# log.info('Time between checkpoint 1 and 2 is ' +
# str(checkpoint_2 - checkpoint_1))
# log.info('Time between checkpoint 3 and 2 is ' +
# str(checkpoint_3 - checkpoint_2))
# log.info('Time between checkpoint 4 and 3 is ' +
# str(checkpoint_4 - checkpoint_3))
# log.info('Time between checkpoint 5 and 4 is ' +
# str(checkpoint_5 - checkpoint_4))

# Determine how many sessions the bot will run for before quitting.
min_sessions = int(config_file['min_sessions'])
max_sessions = int(config_file['max_sessions'])
session_total = rand.randint(min_sessions, max_sessions)
log.info('session_total is %s', session_total)

# The current number of sessions that have been completed.
session_num = 0

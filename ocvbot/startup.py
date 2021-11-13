# coding=UTF-8
"""
Sets global variables and constants.

"""
import json
import logging as log
import random as rand
import time

import pyautogui as pag
from ocvbot import config

# TODO: Finish implementing stats.
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

ore_xp_dict = {"copper": 16.5, "iron": 35.5}

# ----------------------------------------------------------------------
# These variables are used to setup behavior.logout_rand_range(). ------
# ----------------------------------------------------------------------

# Set initial checkpoint_checked values.
checkpoint_1_checked = False
checkpoint_2_checked = False
checkpoint_3_checked = False
checkpoint_4_checked = False

# Convert run duration within config file from minutes to seconds.
min_session_duration_sec = (int(config["main"]["min_session_duration"])) * 60
max_session_duration_sec = (int(config["main"]["max_session_duration"])) * 60

if min_session_duration_sec > max_session_duration_sec:
    raise Exception("min_session_duration must be less than max_session_duration!")

min_break_duration = int(config["main"]["min_break_duration"])
max_break_duration = int(config["main"]["max_break_duration"])

if min_break_duration > max_break_duration:
    raise Exception("min_break_duration must be less than max_break_duration!")

# Break the duration of time between the minimum and maximum duration
#   into a set of evenly-sized durations of time. These chunks of time
#   are consecutively added to the start time to create "checkpoints".
#   Checkpoints are timestamps at which a logout roll will occur.
checkpoint_interval = (max_session_duration_sec - min_session_duration_sec) / 4

# Space each checkpoint evenly between the min duration and the max
#   duration.
checkpoint_1 = round(start_time + min_session_duration_sec)
checkpoint_2 = round(start_time + min_session_duration_sec + checkpoint_interval)
checkpoint_3 = round(start_time + min_session_duration_sec + (checkpoint_interval * 2))
checkpoint_4 = round(start_time + min_session_duration_sec + (checkpoint_interval * 3))
checkpoint_5 = round(start_time + max_session_duration_sec)

# Determine how many sessions the bot will run for before quitting.
min_sessions = int(config["main"]["min_sessions"])
max_sessions = int(config["main"]["max_sessions"])

if min_sessions > max_sessions:
    raise Exception("min_sessions must be less than max_sessions!")

session_total = rand.randint(min_sessions, max_sessions)
log.info(
    "Checkpoint 1 is at %s, session_total is %s",
    time.ctime(checkpoint_1),
    session_total,
)

# The current number of sessions that have been completed.
session_num = 0

with open("worlds.json") as f:
    worlds = json.load(f)


# Define custom exception types. ------------------------------------------------------------------


class BankingError(Exception):
    """
    Raised when an unexpected or unrecoverable situation occurs in the
     banking window.
    """


class InefficientUseOfInventory(Exception):
    """
    Raised when the number of free inventory spaces available would result in
     inefficient or overly arduous gameplay. For example, this exception is
     raised when attempting to drop-mine with only 4 free inventory spaces.
    """


class InventoryError(Exception):
    """
    Raised when an unexpected or unrecoverable situation occurs with the
     player's inventory.
    """


class InventoryFull(Exception):
    """
    Raised whenever the player's inventory is too full to perform the desired
     action.
    """


class NeedleError(Exception):
    """
    A generic exception raised when a necessary needle could not be found.
    """


class RockEmpty(Exception):
    """
    Raised by skills.Miner when the given rock is empty.
    """


class TimeoutException(Exception):
    """
    Raised whenever an action takes longer than expected and times out.
    """

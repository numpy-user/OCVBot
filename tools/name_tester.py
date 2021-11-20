#!/usr/bin/env python3
# coding=UTF-8
"""
Reads a list of possible usernames and tests whether they're available.
Usernames are tested at a rate of about 10 per minute.

NOTE:
   You MUST use the fixed-size client display mode. If your client is not in
   fixed-size mode, login to another account, set the client to fixed-size mode,
   then log back into your account on Tutorial Island.

SETUP:
1. Create a file in this directory called `possible-usernames.txt`
2. Add desired possible usernames to the file, one per line. The file should
   look something like this:
```
username1
username2
username3
```
3. Login to your new account on Tutorial Island.

RUNNING:
1. Run this script.
2. A file called `unavailable-usernames.txt` will be created in this directory
   with all the invalid usernames from the `possible-usernames.txt` file.
2. A file called `available-usernames.txt` will be created in this directory
   with all the valid usernames from the `possible-usernames.txt` file.
"""
import logging as log
import pathlib
import sys

script_dir = str(pathlib.Path(__file__).parent.absolute())

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)

from ocvbot import vision as vis
from ocvbot import behavior as behav
from ocvbot import startup as start
from ocvbot import inputs

vis.init()

unavailable_usernames = []
available_usernames = []
possible_usernames = []


def ingest_possible_usernames(file):
    """
    Read the possible usernames file into a list.
    """
    with open(file, "r", encoding="UTF-8") as possible_usernames_file:
        for line in possible_usernames_file:
            line = line.rstrip()
            line = line.lstrip()
            possible_usernames.append(line)


def record_available_username(username):
    """
    Notify the user of a valid username and write it to
    ./available-usernames.txt
    """
    log.info("Name %s is available!", username)
    available_usernames.append(username)
    print(f"{available_usernames=}")

    with open(
        f"{script_dir}/available-usernames.txt", "a", encoding="UTF-8"
    ) as available_usernames_file:
        available_usernames_file.write(username)
        available_usernames_file.write("\n")


def record_unavailable_username(username):
    """
    Notify the user of an invalid username and write it to
    ./unavailable-usernames.txt
    """
    log.debug("Name %s is NOT available!", username)
    unavailable_usernames.append(username)

    with open(
        f"{script_dir}/unavailable-usernames.txt", "a", encoding="UTF-8"
    ) as unavailable_usernames_file:
        unavailable_usernames_file.write(username)
        unavailable_usernames_file.write("\n")


def check_availability(username):
    """
    After entering username into input field, check its availability and call
    record_available_username() or record_unavailable_username() accordingly.
    """

    for _ in range(50):
        # The "Look up name" button becomes "Set name" if the name is available.
        name_available = vis.Vision(
            region=vis.GAME_SCREEN,
            needle="./needles/tutorial-island/set-name-button.png",
            loop_num=1,
        ).wait_for_needle()
        if name_available is True:
            record_available_username(username)
            return

        # The "Look up name" button becomes greyed out if the name is not
        #   available.
        name_unavailable = vis.Vision(
            region=vis.GAME_SCREEN,
            needle="./needles/tutorial-island/name-lookup-complete.png",
            loop_num=1,
        ).wait_for_needle()
        if name_unavailable is True:
            record_unavailable_username(username)
            return
    raise start.TimeoutException("Timed out waiting for name validity!")


def main():
    ingest_possible_usernames(f"{script_dir}/possible-usernames.txt")
    log.info("Testing %s possible usernames", len(possible_usernames))

    # Look for the display name window.
    set_display_name_window = vis.Vision(
        region=vis.GAME_SCREEN,
        needle="./needles/tutorial-island/set-display-name.png",
        loop_num=10,
    ).wait_for_needle()
    if set_display_name_window is False:
        raise start.TimeoutException("Timed out waiting for Display Name Window!")

    # Start testing usernames.
    for username in possible_usernames:
        if len(username) > 12:
            log.info("Username %s is too long! Names must be <=12 characters", username)
            record_unavailable_username(username)
        else:
            # Focus the display name field.
            display_name_input_field = vis.Vision(
                region=vis.GAME_SCREEN,
                needle="./needles/tutorial-island/display-name-field.png",
                loop_num=1,
            ).click_needle(sleep_range=(0, 10, 0, 10), move_duration_range=(1, 10))
            if display_name_input_field is False:
                raise start.NeedleError("Could not find Display Name input field!")

            # Blank out field.
            inputs.Keyboard(
                sleep_range=(0, 1, 0, 1), action_duration_range=(1000, 1500)
            ).keypress(key="Backspace")
            # Type username into the field.
            inputs.Keyboard().typewriter(message=username)
            # Confirm field.
            inputs.Keyboard().keypress(key="Enter")
            check_availability(username)


if __name__ == "__main__":
    main()

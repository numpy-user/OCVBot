#!/usr/bin/env python3
# coding=UTF-8
"""
Prints a list of unique one-word usernames.

Names are generated using a {prefix + infix(es) + suffix} method.

Use the variables at the top of this file to edit parameters.

Prefixes, infixes, and suffixes are obtained by reading these files in the
current directory:
    `possible-prefixes.txt`
    `possible-infixes.txt`
    `possible-suffixes.txt`
"""
import logging as log
import pathlib
import random as rand

# The number of names to generate and print.
NUMBER_OF_NAMES = 10
# All names shorter than this length will be regenerated.
MINIMUM_NAME_LENGTH = 3
# The minimum and maximum number of infix elements.
MIN_INFIXES = 0
MAX_INFIXES = 2

# Set this to "DEBUG" to print debugging information.
LOG_LEVEL = "INFO"
log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level=LOG_LEVEL
)

possible_prefixes = []
possible_infixes = []
possible_suffixes = []

# Get the path the script is in.
SCRIPTPATH = str(pathlib.Path(__file__).parent.absolute())

# Read prefix/infix/suffix files into a list.
with open(
    f"{SCRIPTPATH}/possible-prefixes.txt", "r", encoding="UTF-8"
) as possible_prefixes_file:
    for line in possible_prefixes_file:
        # Strip leading and trailing spaces.
        line = line.strip()
        # Ignore blank lines.
        if len(line.split()) == 0:
            continue
        possible_prefixes.append(line)
with open(
    f"{SCRIPTPATH}/possible-infixes.txt", "r", encoding="UTF-8"
) as possible_infixes_file:
    for line in possible_infixes_file:
        line = line.strip()
        if len(line.split()) == 0:
            continue
        possible_infixes.append(line)
with open(
    f"{SCRIPTPATH}/possible-suffixes.txt", "r", encoding="UTF-8"
) as possible_suffixes_file:
    for line in possible_suffixes_file:
        line = line.strip()
        if len(line.split()) == 0:
            continue
        possible_suffixes.append(line)


def select_prefix():
    """
    Randomly choose a prefix from the list and return it.
    """
    roll = rand.randrange(len(possible_prefixes))
    prefix = possible_prefixes[roll]
    return prefix


def select_infix():
    """
    Randomly choose an infix from the list and return it.
    """
    roll = rand.randrange(len(possible_infixes))
    infix = possible_infixes[roll]
    return infix


def select_suffix():
    """
    Randomly choose a suffix from the list and return it.
    """
    roll = rand.randrange(len(possible_suffixes))
    suffix = possible_suffixes[roll]
    return suffix


def main():
    prefix = select_prefix()
    log.debug("Selected %s as prefix", prefix)

    # Use a random number of infixes.
    infix_number = rand.randint(MIN_INFIXES, MAX_INFIXES)
    log.debug("Using %s infixes", infix_number)
    infix_list = []
    for _ in range(infix_number):
        infix_list.append(select_infix())
    infixes = "".join(infix_list)
    if infix_number > 0:
        log.debug("Using infix(es) of %s", infixes)

    suffix = select_suffix()
    log.debug("Selected %s as suffix", suffix)

    username = f"{prefix}{infixes}{suffix}"

    # Regenerate the name if it's too short.
    if len(username) > MINIMUM_NAME_LENGTH:
        print(username)
    else:
        log.debug("Username %s is too short! Regenerating", username)
        main()


if __name__ == "__main__":
    for _ in range(NUMBER_OF_NAMES):
        main()

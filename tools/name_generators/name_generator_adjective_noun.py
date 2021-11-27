#!/usr/bin/env python3
# coding=UTF-8
"""
Prints out a list of two-word usernames.

Names are generated using an {adjective + noun} method.

Use the variables at the top of this file to edit parameters.

Adjectives and nouns are obtained by reading these files in the current
directory:
    `possible-adjectives.txt`
    `possible-nouns.txt`

All nouns and adjectives over 8 characters long are ignored due to the
   difficulty of finding adjective/noun pairs <12 characters long.
"""
import logging as log
import pathlib
import random as rand
import sys

# The number of names to generate. Due to the way name generation works, this
#   is an approximation and not exact.
NUMBER_OF_NAMES = 21

# Set this to "DEBUG" to get more info.
LOG_LEVEL = "INFO"
log.basicConfig(format="%(asctime)s %(funcName)s - %(message)s", level=LOG_LEVEL)

possible_adjectives = []
possible_nouns = []

adjective = None
noun = None

sys.setrecursionlimit(9999999)

# Get the path the script is in.
SCRIPTPATH = str(pathlib.Path(__file__).parent.absolute())

# Read adjective and noun files into a list.
with open(
    f"{SCRIPTPATH}/possible-adjectives.txt", "r", encoding="UTF-8"
) as possible_adjectives_file:
    for line in possible_adjectives_file:
        # Strip leading and trailing spaces.
        line = line.strip()
        # Ignore blank lines.
        if len(line.split()) == 0:
            continue
        possible_adjectives.append(line)
with open(
    f"{SCRIPTPATH}/possible-nouns.txt", "r", encoding="UTF-8"
) as possible_nouns_file:
    for line in possible_nouns_file:
        line = line.strip()
        if len(line.split()) == 0:
            continue
        possible_nouns.append(line)


def select_random_adjective():
    """
    Randomly choose an applicable adjective from the list and return it.

    Since usernames are limited to 12 characters in length, if a noun has
    already been selected, then an adjective of appropriate length is found.
    """
    global adjective
    roll = rand.randrange(len(possible_adjectives))
    adjective = possible_adjectives[roll]

    # If the adjective is over 8 character in length, then only nouns of <=3
    #   letters will fit.
    if len(adjective) > 8:
        log.debug("Adjective %s is too long", adjective)
        select_random_adjective()

    # If the noun has already been chosen, choose an adjective that fits its length.
    if noun is not None:
        # Add 1 to the length since there's a space between both words.
        if (len(adjective) + len(noun) + 1) > 12:
            log.debug("Generated adjective %s is too long for noun %s", adjective, noun)
            # Randomly regenerating the word until one of sufficient length
            #   is found is obviously not ideal. However, it's still fast enough
            #   that it's not too much of an issue.
            select_random_adjective()

    return adjective


def select_random_noun():
    """
    Randomly choose an applicable noun from the list and return it.

    Since usernames are limited to 12 characters in length, if an adjective has
    already been selected, then a noun of appropriate length is found.
    """
    global noun
    roll = rand.randrange(len(possible_nouns))
    noun = possible_nouns[roll]

    # If the noun is over 8 character in length, then only adjectives of <=3
    #   letters will fit.
    if len(noun) > 8:
        log.debug("Noun %s is too long", noun)
        select_random_noun()

    # If the adjective has already been chosen, choose a noun that fits its length.
    if adjective is not None:
        # Add 1 to the length since there's a space between both words.
        if (len(adjective) + len(noun) + 1) > 12:
            log.debug("Generated noun %s is too long for adjective %s", noun, adjective)
            select_random_noun()
    return noun


def main():
    global adjective
    global noun

    # Alternate between selecting the noun first and the adjective first.
    # If we only generate the adjective first, we'll end up with a list of long
    #   adjectives followed by short nouns on average.

    adjective = None
    noun = None

    adjective = select_random_adjective()
    noun = select_random_noun()
    username = f"{adjective} {noun}"
    print(username)

    adjective = None
    noun = None

    noun = select_random_noun()
    adjective = select_random_adjective()
    username = f"{adjective} {noun}"
    print(username)

    adjective = None
    noun = None

    # Also try using noun + noun pairs for extra variety.
    adjective = select_random_noun()
    noun = select_random_noun()
    username = f"{adjective} {noun}"
    print(username)


if __name__ == "__main__":
    for _ in range(round(int(NUMBER_OF_NAMES / 3))):
        main()

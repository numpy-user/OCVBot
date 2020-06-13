# coding=UTF-8
"""
Miscellaneous functions, mostly related to random sleeps.

"""
import datetime
import logging as log
import random as rand
import time

from ocvbot import startup as start


def rand_seconds(rmin=0, rmax=100):
    """
    Gets a random integer between two values. Input arguments are in
    miliseconds but output is in seconds. For example, if this function
    generates a random value of 391, it will return a value of 0.391.

    Args:
        rmin (int): The minimum number of miliseconds, default is 0.
        rmax (int): The maximum number of miliseconds, default
                    is 100.
    Returns:
        Returns a float.
    """

    randval = rand.randint(rmin, rmax)
    randval = float(randval / 1000)
    # log.debug('Got random value of %s.', randval)
    return randval


def sleep_rand(rmin=0, rmax=100):
    """
    Does nothing for a random period of time. Input arguments are in
    miliseconds.

    Args:
        rmin (int): The minimum number of miliseconds to wait, default
                    is 0.
        rmax (int): The maximum number of miliseconds to wait, default
                    is 100.
    """

    sleeptime = rand_seconds(rmin=rmin, rmax=rmax)
    # log.debug('Sleeping for %s seconds.', sleeptime)
    time.sleep(sleeptime)


def run_duration(human_readable=False):
    """
    Determines how many seconds the current "run" has been running. This
    timer is reset when the bot logs in, or when the bot restarts.

    Args:
        human_readable (bool): Whether to return the number of seconds
                               the bot has been running, or the amount
                               of time in a HH:MM:SS format, default is
                               false.

    Returns:
          Returns an int containing the number of seconds the bot has
          been running since its last logon.
    """
    current_time = time.time()
    elapsed_time_seconds = round(current_time - start.start_time)

    if human_readable is False:
        return elapsed_time_seconds

    elapsed_time_human_readable = datetime.timedelta(
        seconds=elapsed_time_seconds)
    return elapsed_time_human_readable


def wait_rand(chance, second_chance=10,
              wait_min=10000, wait_max=60000):
    """
    Roll for a chance to do nothing for the specified period of time.

    Args:
        chance (int): The number that must be rolled for the wait to be
                      called. For example, if chance is 25, then there
                      is a 1 in 25 chance for the roll to pass.
        second_chance (int): The number that must be rolled for an
                             additional wait to be called if the first
                             roll passes, default is 10. By default,
                             this means that 10% of waits that pass the
                             first roll wait for an additional period of
                             time.
        wait_min (int): The minimum number of miliseconds to wait if the
                        roll passes, default is 10000.
        wait_max (int): The maximum number of miliseconds to wait if the
                        roll passes, default is 60000.
    """

    wait_roll = rand.randint(1, chance)
    if wait_roll == chance:
        log.info('Random wait called.')
        sleeptime = rand_seconds(wait_min, wait_max)
        log.info('Sleeping for %s seconds.', round(sleeptime))
        time.sleep(sleeptime)

        # Perform an additional wait roll so that (1/second_chance)
        #   waits are extra long.
        wait_roll = rand.randint(1, second_chance)
        if wait_roll == 10:
            log.info('Additional random wait called.')
            sleeptime = rand_seconds(wait_min, wait_max)
            log.info('Sleeping for %s seconds.', round(sleeptime))
            time.sleep(sleeptime)

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
    # log.debug('Got random value of ' + str(randval) + '.')
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

    Returns:
        Always returns 0.
    """

    sleeptime = rand_seconds(rmin=rmin, rmax=rmax)
    # log.debug('Sleeping for ' + str(sleeptime) + ' seconds.')
    time.sleep(sleeptime)
    return 0


def bot_duration():
    """
    Determines how many seconds the bot has been running for. This timer
    will be reset after every logout break.

    Returns:
          Returns an int containing the number of seconds the bot has
          been running since its last logon.
    """
    current_time = time.time()
    elapsed_time = start.start_time - current_time
    elapsed_time = round(elapsed_time)
    return elapsed_time

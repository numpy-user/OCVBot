import logging as log
import subprocess as sub
import time

import psutil
import pytest

# Used by feh to shorten its function parameters.
directory = "../tests/test_behavior/"
# Some waiting is required after opening images before template matching
#   is reliable.
interval = 0.1

log.basicConfig(format='%(asctime)s %(filename)s.%(funcName)s - %(message)s'
                , level='DEBUG')


def kill_feh():
    """
    Kills feh so the next set of images can be displayed.
    """
    for proc in psutil.process_iter():
        if proc.name() == 'feh':
            proc.kill()
    return


def feh(test_name, test_type, test_number):
    """
    Runs the feh image viewer using the specified parameters.

    Args:
        test_name (str): The name of the test being run. This is the
                         name of the directory immediately beneath the
                         "directory" variable at the top of this file.
                         Ignore the "test_" in the directory's name.
        test_number (str): Which test to run for test_name. This is the
                           name of the directory immediately beneath
                           the "test_name" parameter. Ignore the "test"
                           in the directory's name
    """
    kill_feh()
    time.sleep(interval)
    test = sub.Popen(['feh', directory + 'test_' + test_name + '/' + test_type
                      + '/test' + test_number + '/'])
    print("TEST IS ", test)
    time.sleep(interval)
    return


# Provide an image for the client to orient itself. Currently any imports
#   from ocvbot require an image to match first, or they will fail.
feh('open_side_stone', 'pass', '01')
from ocvbot import behavior

# ----------------------------------------------------------------------
# PARAMETERS
# ----------------------------------------------------------------------

# Pass in parameters as a tuple. The first item in the tuple is the side
#   stone to open, the second is so feh() knows which test album to open.
open_side_stone_pass_params = (
    ('attacks', '01'),
    ('skills', '02'),
    ('quests', '03'),
    ('inventory', '04'),
    ('equipment', '05'),
    ('prayers', '06'),
    ('spellbook', '07'),
    ('logout', '08'),
)
# Test passing conditions, then test failing conditions.
open_side_stone_fail_params = (
    ('settings', '01'),
    ('logout', '02'),
)

# ----------------------------------------------------------------------
# TESTS
# ----------------------------------------------------------------------


@pytest.mark.parametrize('params', open_side_stone_pass_params)
def test_open_side_stone_pass(params):
    side_stone, test_number = params
    feh('open_side_stone', 'pass', test_number)
    result = behavior.open_side_stone(side_stone)
    assert result is True


#@pytest.mark.parametrize('params', open_side_stone_fail_params)
#def test_open_side_stone_fail(params):
    #side_stone, test_number = params
    #feh('open_side_stone', 'fail', test_number)
    #with pytest.raises(Exception, match='Could not open side stone!'):
        #behavior.open_side_stone(side_stone)
    #kill_feh()


#def test_test():
    #with pytest.raises(ZeroDivisionError):
        #test()


# def test_login():
# time.sleep(interval)
# feh('login', '01')
# time.sleep(interval)
# result = behavior.login()
# kill_feh()
# assert result, True


# def test_logout():
# Function recognizes when client is already logged out.
# time.sleep(interval)
# feh('logout', '01')
# time.sleep(interval)
# result = behavior.logout()
# kill_feh()
# assert (result, 1)

# def test_logout_02(self):
# Function recognizes when client is logged in but "logout"
#   side stone is not active.
# time.sleep(interval)
# kill('feh')
# sub.Popen(["feh", "../tests/needles/"
# "test_behavior/"
# "image_003.png"])
# time.sleep(interval)
# result = behavior.logout()
# kill('feh')
# self.assertRaises(result, RuntimeError)

# def test_logout_03():
# Function recognizes when client is logged in and "logout"
#   side stone is active.
# time.sleep(interval)
# kill('feh')
# sub.Popen(["feh", "../tests/needles/"
# "test_behavior/"
# "image_004.png"])
# time.sleep(interval)
# result = behavior.logout()
# kill('feh')
# assert (result, 0)

import logging as log
import subprocess as sub
import time

import psutil
import pytest

# Used by feh to shorten its function parameters.
directory = "../tests/haystacks/test_behavior/"
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


def feh(test_name, test_number):
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
    sub.Popen(['feh', directory + 'test_' + test_name
               + '/test' + test_number + '/'])
    time.sleep(interval)
    return


# Provide an image for the client to orient itself. Currently any imports
#   from ocvbot require an image to match first, or they will fail.
feh('logout', '01')
from ocvbot import behavior

# Pass in parameters as a tuple. The first item in the tuple is the side
#   stone to open, the second is so feh() knows which test album to open.
open_side_stone_params = (
        # Open the Attacks side stone with no issues.
        ('attacks', '01'),
        # Open the Inventory side stone when it doesn't open on the
        #   first attempt.
        ('inventory', '02'),
)


@pytest.mark.parametrize('params', open_side_stone_params)
def test_open_side_stone(params):
    side_stone, test_number = params
    feh('open_side_stone', test_number)
    result = behavior.open_side_stone(side_stone)
    assert result is True

#def test_login():
    #time.sleep(interval)
    #feh('login', '01')
    #time.sleep(interval)
    #result = behavior.login()
    #kill_feh()
    #assert result, True


#def test_logout():
    # Function recognizes when client is already logged out.
    #time.sleep(interval)
    #feh('logout', '01')
    #time.sleep(interval)
    #result = behavior.logout()
    #kill_feh()
    #assert (result, 1)

#def test_logout_02(self):
    # Function recognizes when client is logged in but "logout"
    #   side stone is not active.
    #time.sleep(interval)
    #kill('feh')
    #sub.Popen(["feh", "../tests/needles/"
                      #"test_behavior/"
                      #"image_003.png"])
    #time.sleep(interval)
    #result = behavior.logout()
    #kill('feh')
    #self.assertRaises(result, RuntimeError)

#def test_logout_03():
    # Function recognizes when client is logged in and "logout"
    #   side stone is active.
    #time.sleep(interval)
    #kill('feh')
    #sub.Popen(["feh", "../tests/needles/"
                      #"test_behavior/"
                      #"image_004.png"])
    #time.sleep(interval)
    #result = behavior.logout()
    #kill('feh')
    #assert (result, 0)


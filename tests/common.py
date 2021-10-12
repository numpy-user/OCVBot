# coding=UTF-8
"""
Common functions used by unit testing files.

"""
import os
import pathlib
import subprocess as sub
import sys
import time

import psutil

# Make sure the program's working directory is the directory in which
#   this file is located.
os.chdir(os.path.dirname(__file__))

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)


def kill_feh() -> None:
    """
    Kills feh so the next slideshow of images can be displayed.

    """
    for proc in psutil.process_iter():
        if proc.name() == 'feh':
            proc.kill()


def feh(test_name, test_type, test_number, directory, interval=0.1) -> None:
    """
    Runs the feh image viewer using the specified parameters.

    Args:
        test_name (str): The name of the test being run. This is the
                         name of the directory immediately beneath the
                         "directory" variable at the top of this file.
                         Ignore the "test_" in the directory's name.
        test_type (str): Whether to test for passing conditions or
                         failing conditions. This value must be either
                         'pass' or 'fail'.
        test_number (str): Which test to run for test_name. This is the
                           name of the directory immediately beneath
                           the "test_name" parameter. Ignore the "test"
                           in the directory's name

    """
    kill_feh()
    # Some waiting is required after opening images before template matching
    #   is reliable.
    time.sleep(interval)
    test = sub.Popen(['feh', directory + 'test_' + test_name + '/' + test_type
                      + '/test' + test_number + '/'])
    print("TEST IS ", test)
    time.sleep(interval)

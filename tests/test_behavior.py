# coding=UTF-8
"""
Unit tests for the behavior.py module.

Linux only. Requires feh.

"""
import logging as log
import os

import psutil
import pytest

import common

image_directory = (os.path.dirname(__file__)) + "/test_behavior/"

log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level="DEBUG"
)

# Provide an image for the client to orient itself. Currently any imports
#   from ocvbot require an image to match first, or they will fail.

# ----------------------------------------------------------------------
# PARAMETERS ###########################################################
# ----------------------------------------------------------------------
common.feh("orient", "pass", "01", image_directory)
from ocvbot import behavior

# Pass in parameters as a tuple. The first item in the tuple is the side
#   stone to open, the second is so feh() knows which test album to open.
open_side_stone_pass_params = (
    ("attacks", "01"),
    ("skills", "02"),
    ("quests", "03"),
    ("inventory", "04"),
    ("equipment", "05"),
    ("prayers", "06"),
    ("spellbook", "07"),
    ("logout", "08"),
)
# Test passing conditions, then test failing conditions.
open_side_stone_fail_params = (
    ("settings", "01"),
    ("logout", "02"),
)

logout_pass_params = (
    "01",  # Standard logout.
    "02",  # Logout button doesn't work the first time.
    "03",  # World switcher open.
    "04",  # World switcher logout button doesn't work the first time.
    "05",  # Logout button is highlighted already.
    "06",  # Already logged out
)

logout_fail_params = ("01",)  # Unable to find the logout button.

login_pass_params = (
    "01",  # Standard login.
    "02",  # Login in which "Ok" button is missed.
)

login_fail_params = (
    "01",  # Invalid user credentials.
    "02",  # Client is already logged in.
)


drop_item_pass_params = (("iron_ore.png", "01"),)

# ----------------------------------------------------------------------
# TESTS ################################################################
# ----------------------------------------------------------------------


# OPEN SIDE STONE ------------------------------------------------------


@pytest.mark.parametrize("params", open_side_stone_pass_params)
def test_open_side_stone_pass(params) -> None:
    side_stone, test_number = params
    common.feh("open_side_stone", "pass", test_number, image_directory)
    result = behavior.open_side_stone(side_stone)
    assert result is True


@pytest.mark.parametrize("params", open_side_stone_fail_params)
def test_open_side_stone_fail(params) -> None:
    side_stone, test_number = params
    common.feh("open_side_stone", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not open side stone!"):
        behavior.open_side_stone(side_stone)
        common.kill_feh()


# LOGOUT ---------------------------------------------------------------


@pytest.mark.parametrize("params", logout_pass_params)
def test_logout_pass(params) -> None:
    test_number = params
    common.feh("logout", "pass", test_number, image_directory)
    result = behavior.logout()
    assert result is True


@pytest.mark.parametrize("params", logout_fail_params)
def test_logout_fail(params) -> None:
    test_number = params
    common.feh("logout", "fail", test_number, image_directory)
    with pytest.raises(Exception, match=".*"):
        behavior.logout()
        common.kill_feh()


# LOGIN ----------------------------------------------------------------


# BROKEN
#  @pytest.mark.parametrize("params", login_pass_params)
#  def test_login_pass(params) -> None:
#      test_number = params
#      common.feh("login", "pass", test_number, image_directory)
#      import os

#      os.system("pwd")
#      result = behavior.login_full(
#          username_file=(image_directory + "./test_login/sampleu.txt"),
#          password_file=(image_directory + "./test_login/samplep.txt"),
#      )
#      assert result is True


# BROKEN
#  @pytest.mark.parametrize("params", login_fail_params)
#  def test_login_fail(params) -> None:
#      test_number = params
#      common.feh("login", "fail", test_number, image_directory)
#      with pytest.raises(Exception, match=".*"):
#          behavior.login_full(
#              username_file=(image_directory + "./test_login/sampleu.txt"),
#              password_file=(image_directory + "./test_login/samplep.txt"),
#          )
#          common.kill_feh()

# CHECK_SKILLS ---------------------------------------------------------

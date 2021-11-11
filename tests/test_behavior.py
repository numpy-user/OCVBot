# coding=UTF-8
"""
Unit tests for the behavior.py module.

Linux only. Requires feh.

"""
import logging as log
import os

import pytest

import common
from ocvbot import behavior
from ocvbot import vision as vis

image_directory = (os.path.dirname(__file__)) + "/test_behavior/"

log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level="DEBUG"
)

# Provide an image for the client to orient itself, then initialize the
#   vision regions.
common.feh("orient", "pass", "01", ((os.path.dirname(__file__)) + "/test_vision/"))
vis.init()

# CHECK_SKILLS ------------------------------------------------------------------------------------

check_skills_pass_params = ("01",)


@pytest.mark.parametrize("params", check_skills_pass_params)
def test_check_skills_pass(params) -> None:
    test_number = params
    common.feh("check_skills", "pass", test_number, image_directory)
    result = behavior.check_skills()
    assert result is True
    common.kill_feh()


# DROP_ITEM ---------------------------------------------------------------------------------------

drop_item_pass_params = (("./needles/items/iron-ore.png", "01"),)


@pytest.mark.parametrize("params", drop_item_pass_params)
def test_drop_item_pass(params) -> None:
    item, test_number = params
    common.feh("drop_item", "pass", test_number, image_directory)
    result = behavior.drop_item(item=item, shift_click=False)
    assert result is True
    common.kill_feh()


# LOGOUT ------------------------------------------------------------------------------------------

logout_pass_params = (
    "01",  # Logout tab is already open.
    "02",  # Logout tab is already open, button highlighted.
    "03",  # Logout tab is already open, world switcher open.
    "04",  # Already logged out
    "05",  # Attack tab is open, switching tabs doesn't work at first.
)


@pytest.mark.parametrize("params", logout_pass_params)
def test_logout_pass(params) -> None:
    test_number = params
    common.feh("logout", "pass", test_number, image_directory)
    result = behavior.logout()
    assert result is True
    common.kill_feh()


logout_fail_params = ("01",)  # Unable to find the logout button.


@pytest.mark.parametrize("params", logout_fail_params)
def test_logout_fail(params) -> None:
    test_number = params
    common.feh("logout", "fail", test_number, image_directory)
    with pytest.raises(Exception, match=".*"):
        behavior.logout()
        common.kill_feh()


# OPEN SIDE STONE ---------------------------------------------------------------------------------

open_side_stone_pass_params = (
    ("attacks", "01"),  # Bank window must be closed first, stone already open.
    ("skills", "02"),  # Must try multiple times to open stone.
    ("quests", "03"),
    ("inventory", "04"),
    ("equipment", "05"),
    ("prayers", "06"),
    ("spellbook", "07"),
    ("logout", "08"),
)


@pytest.mark.parametrize("params", open_side_stone_pass_params)
def test_open_side_stone_pass(params) -> None:
    side_stone, test_number = params
    common.feh("open_side_stone", "pass", test_number, image_directory)
    result = behavior.open_side_stone(side_stone)
    assert result is True
    common.kill_feh()


open_side_stone_fail_params = (("settings", "01"),)


@pytest.mark.parametrize("params", open_side_stone_fail_params)
def test_open_side_stone_fail(params) -> None:
    side_stone, test_number = params
    common.feh("open_side_stone", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not open side stone!"):
        behavior.open_side_stone(side_stone)
        common.kill_feh()

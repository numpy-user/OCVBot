# coding=UTF-8
"""
Unit tests for the behavior.py module.

Linux only. Requires feh.

"""
import os

import pytest

import init_tests

# This statement exists to prevent the OCVBot imports from being re-ordered.
pass

# OCVBot modules must be imported after init_tests.
from ocvbot import behavior
from ocvbot import startup as start

image_directory = (os.path.dirname(__file__)) + "/test_behavior/"


# CHECK_SKILLS ------------------------------------------------------------------------------------

check_skills_pass_params = ("01",)


@pytest.mark.parametrize("params", check_skills_pass_params)
def test_check_skills_pass(params) -> None:
    test_number = params
    init_tests.feh("check_skills", "pass", test_number, image_directory)
    result = behavior.check_skills()
    assert result is True
    init_tests.kill_feh()


# DROP_ITEM ---------------------------------------------------------------------------------------

drop_item_pass_params = (
    # Must open side stone first.
    ("./needles/items/iron-ore.png", "01"),
    # No items exist in inventory.
    ("./needles/items/iron-ore.png", "02"),
)


@pytest.mark.parametrize("params", drop_item_pass_params)
def test_drop_item_pass(params) -> None:
    item, test_number = params
    init_tests.feh("drop_item", "pass", test_number, image_directory)
    result = behavior.drop_item(item=item, random_wait=False, shift_click=False)
    assert result is None
    init_tests.kill_feh()


# Try dropping item too many times.
drop_item_fail_params = (("./needles/items/iron-ore.png", "01"),)


@pytest.mark.parametrize("params", drop_item_fail_params)
def test_drop_item_fail(params) -> None:
    item, test_number = params
    init_tests.feh("drop_item", "fail", test_number, image_directory)
    with pytest.raises(start.InventoryError, match="Tried dropping item too many"):
        behavior.drop_item(item=item, random_wait=False, shift_click=False)
    init_tests.kill_feh()


# LOGOUT ------------------------------------------------------------------------------------------

logout_pass_params = (
    "01",  # Logout tab is already open.
    "02",  # Logout tab is already open, button highlighted.
    "03",  # Logout tab is already open, world switcher open.
    "04",  # Already logged out
    "05",  # Attack tab is open, switching tabs doesn't work at first.
    "06",  # Must click logout button multiple times.
)


@pytest.mark.parametrize("params", logout_pass_params)
def test_logout_pass(params) -> None:
    test_number = params
    init_tests.feh("logout", "pass", test_number, image_directory)
    result = behavior.logout()
    assert result is None
    init_tests.kill_feh()


# Try too many times to click on logout button.
logout_fail_params = ("01",)


@pytest.mark.parametrize("params", logout_fail_params)
def test_logout_fail(params) -> None:
    test_number = params
    init_tests.feh("logout", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not logout"):
        behavior.logout()
    init_tests.kill_feh()


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
    init_tests.feh("open_side_stone", "pass", test_number, image_directory)
    result = behavior.open_side_stone(side_stone)
    assert result is True
    init_tests.kill_feh()


open_side_stone_fail_params = (("settings", "01"),)


@pytest.mark.parametrize("params", open_side_stone_fail_params)
def test_open_side_stone_fail(params) -> None:
    side_stone, test_number = params
    init_tests.feh("open_side_stone", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not open side stone!"):
        behavior.open_side_stone(side_stone)
        init_tests.kill_feh()

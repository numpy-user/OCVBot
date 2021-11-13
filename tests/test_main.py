# coding=UTF-8
"""
Integration tests for the scenarios in main.py.

Linux only. Requires feh.

"""
import os

import pytest

import init_tests

# This statement exists to prevent the OCVBot imports from being re-ordered.
pass

# OCVBot modules must be imported after init_tests.
from ocvbot import main

image_directory = (os.path.dirname(__file__)) + "/test_main/"


# CHEF --------------------------------------------------------------------------------------------

chef_pass_params = (("raw-anchovies", "al-kharid", "01"),) # Level-up occurs halfway through


@pytest.mark.parametrize("params", chef_pass_params)
def test_chef_pass(params) -> None:
    item, location, test_number = params
    init_tests.feh("chef", "pass", test_number, image_directory)
    result = main.chef(item=item, location=location, loops=1)
    assert result is None
    init_tests.kill_feh()


# Pass an unsupported location.
chef_fail_01_params = (("raw-anchovies", "unsupported-location", "00"),)


@pytest.mark.parametrize("params", chef_fail_01_params)
def test_chef_fail_01(params) -> None:
    item, location, test_number = params
    with pytest.raises(ValueError, match="Unsupported value for location"):
        main.chef(item=item, location=location, loops=1)
    init_tests.kill_feh()


# SMITH -------------------------------------------------------------------------------------------

smith_pass_params = (("iron-bar", "iron-platebody", "varrock", "01"),)


@pytest.mark.parametrize("params", smith_pass_params)
def test_smith_pass(params) -> None:
    bar_type, item, location, test_number = params
    init_tests.feh("smith", "pass", test_number, image_directory)
    result = main.smith(bar=bar_type, item=item, location=location, loops=1)
    assert result is True
    init_tests.kill_feh()


# ALCHEMIST ---------------------------------------------------------------------------------------

alchemist_pass_params = (
    ("bank-note", "01"),  # Item is in top left.
    ("bank-note", "02"),  # Item is at bottom.
    ("bank-note", "03"),  # Item is at bottom, side stone must be opened.
)

alchemist_fail_params = (
    ("bank-note", "01"),  # Item on the right side of inventory.
    ("bank-note", "02"),  # Item on the right side of inventory, near center.
)


@pytest.mark.parametrize("params", alchemist_pass_params)
def test_alchemist_pass(params) -> None:
    alch_item_type, test_number = params
    init_tests.feh("alchemist", "pass", test_number, image_directory)
    result = main.alchemist(alch_item_type=alch_item_type, loops=1)
    assert result is None
    init_tests.kill_feh()


@pytest.mark.parametrize("params", alchemist_fail_params)
def test_alchemist_fail(params) -> None:
    alch_item_type, test_number = params
    init_tests.feh("alchemist", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not find target"):
        main.alchemist(alch_item_type=alch_item_type, loops=1)
    init_tests.kill_feh()


# SPELLCASTER -------------------------------------------------------------------------------------

spellcaster_pass_params = (("curse-varrock-castle", "01"),)


@pytest.mark.parametrize("params", spellcaster_pass_params)
def test_spellcaster_pass(params) -> None:
    scenario, test_number = params
    init_tests.feh("spellcaster", "pass", test_number, image_directory)
    result = main.spellcaster(scenario=scenario, loops=1)
    assert result is None
    init_tests.kill_feh()

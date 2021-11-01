# coding=UTF-8
"""
Integration tests for the primary scenarios in main.py.

Linux only. Requires feh.

"""
import logging as log
import os

import pytest

import common

image_directory = (os.path.dirname(__file__)) + "/test_main_integration/"

log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level="INFO"
)

# Provide an image for the client to orient itself. Currently any imports
#   from ocvbot require an image to match first, or they will fail.
common.feh("orient", "pass", "01", image_directory)
from ocvbot import main


# CHEF ------------------------------------------------------

chef_pass_params = (("raw-anchovies", "al-kharid", "01"),)


@pytest.mark.parametrize("params", chef_pass_params)
def test_chef_pass(params) -> None:
    item, location, test_number = params
    common.feh("chef", "pass", test_number, image_directory)
    result = main.chef(item=item, location=location, loops=1)
    assert result is True


# SMITH -----------------------------------------------------

smith_pass_params = (("iron-bar", "iron-platebody", "varrock", "01"),)


@pytest.mark.parametrize("params", smith_pass_params)
def test_smith_pass(params) -> None:
    bar, item, location, test_number = params
    common.feh("smith", "pass", test_number, image_directory)
    result = main.smith(bar=bar, item=item, location=location, loops=1)
    assert result is True

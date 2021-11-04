# coding=UTF-8
"""
Unit tests for the vision.py module.

Linux only. Requires feh.

"""
import logging as log
import os

import psutil
import pytest

import common

image_directory = (os.path.dirname(__file__)) + "/test_vision/"

log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level="DEBUG"
)

# Provide an image for the client to orient itself. Currently any imports
#   from ocvbot require an image to match first, or they will fail.
common.feh("orient", "pass", "01", ((os.path.dirname(__file__)) + "/test_vision/"))
from ocvbot import vision as vis

# COUNT_NEEDLES -----------------------------------------------------------------------------------

count_needles_pass_params = (
    ("./needles/items/iron-bar.png", 27, "01"),
    ("./needles/items/raw-anchovies.png", 8, "02"),
    ("./needles/items/raw-anchovies.png", 0, "03"),
    ("./needles/items/raw-anchovies.png", 18, "04"),
)


@pytest.mark.parametrize("params", count_needles_pass_params)
def test_count_needles_pass(params) -> None:
    needle_path, correct_number_of_needles, test_number = params
    common.feh("count_needles", "pass", test_number, image_directory)
    result = vis.Vision(region=vis.inv, needle=needle_path, conf=0.988).count_needles()
    assert result == correct_number_of_needles

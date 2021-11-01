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

image_directory = (os.path.dirname(__file__)) + "/test_banking/"

log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level="DEBUG"
)

# Provide an image for the client to orient itself. Currently any imports
#   from ocvbot require an image to match first, or they will fail.
common.feh("orient", "pass", "01", image_directory)
from ocvbot import banking

# ----------------------------------------------------------------------
# PARAMETERS ###########################################################
# ----------------------------------------------------------------------

open_bank_pass_params = (
    ("south", "01"),  # 1 tile south.
    ("south", "02"),  # 2 tiles south.
    ("west", "03"),  # 1 tile west.
    ("west", "04"),  # 2 tiles west.
)

close_bank_pass_params = ("01",)
close_bank_fail_params = ("01",)

bank_settings_check_pass_params = (
    ("quantity", "all", "01"),
    ("quantity", "1", "02"),
)

# ----------------------------------------------------------------------
# TESTS ################################################################
# ----------------------------------------------------------------------


# OPEN_BANK ------------------------------------------------------------

@pytest.mark.parametrize("params", open_bank_pass_params)
def test_open_bank_pass(params):
    direction, test_number = params
    common.feh("open_bank", "pass", test_number, image_directory)
    result = banking.open_bank(direction)
    assert result is True


# CLOSE BANK -----------------------------------------------------------

@pytest.mark.parametrize("params", close_bank_pass_params)
def test_close_bank_pass(params) -> None:
    test_number = params
    common.feh("close_bank", "pass", test_number, image_directory)
    result = banking.close_bank()
    assert result is True

@pytest.mark.parametrize("params", close_bank_fail_params)
def test_close_bank_fail(params) -> None:
    test_number = params
    common.feh("close_bank", "fail", test_number, image_directory)
    result = banking.close_bank()
    assert result is False


# BANK_SETTINGS_CHECK --------------------------------------------------

@pytest.mark.parametrize("params", bank_settings_check_pass_params)
def test_bank_settings_check(params):
    setting, value, test_number = params
    common.feh("bank_settings_check", "pass", test_number, image_directory)
    result = banking.bank_settings_check(setting, value)
    assert result is True

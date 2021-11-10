# coding=UTF-8
"""
Unit tests for the banking.py module.

Linux only. Requires feh.

"""
import logging as log
import os

import pytest

import common

image_directory = (os.path.dirname(__file__)) + "/test_banking/"

log.basicConfig(
    format="%(asctime)s %(filename)s.%(funcName)s - %(message)s", level="DEBUG"
)

# Provide an image for the client to orient itself. Currently any imports
#   from ocvbot require an image to match first, or they will fail.
common.feh("orient", "pass", "01", ((os.path.dirname(__file__)) + "/test_vision/"))
from ocvbot import banking


# BANK_SETTINGS_CHECK -----------------------------------------------------------------------------

bank_settings_check_pass_params = (
    ("quantity", "all", "01"),
    ("quantity", "all", "02"),
    ("quantity", "1", "03"),
    ("quantity", "5", "04"),
    ("quantity", "10", "05"),
    ("placeholder", "unset", "06"),
    ("placeholder", "set", "07"),
)


@pytest.mark.parametrize("params", bank_settings_check_pass_params)
def test_bank_settings_check_pass(params):
    setting, value, test_number = params
    common.feh("bank_settings_check", "pass", test_number, image_directory)
    result = banking.bank_settings_check(setting, value)
    assert result is None


bank_settings_check_fail_params = (("note", "all", "00"),)


@pytest.mark.parametrize("params", bank_settings_check_fail_params)
def test_bank_settings_check_fail(params):
    setting, value, test_number = params
    common.feh("bank_settings_check", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not set bank setting|Unsupported"):
        banking.bank_settings_check(setting, value)
    common.kill_feh()


# CLOSE BANK --------------------------------------------------------------------------------------

close_bank_pass_params = ("01",)


@pytest.mark.parametrize("params", close_bank_pass_params)
def test_close_bank_pass(params) -> None:
    test_number = params
    common.feh("close_bank", "pass", test_number, image_directory)
    result = banking.close_bank()
    assert result is None
    common.kill_feh()


close_bank_fail_params = ("01",)


@pytest.mark.parametrize("params", close_bank_fail_params)
def test_close_bank_fail(params) -> None:
    test_number = params
    common.feh("close_bank", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not close bank window"):
        banking.close_bank()
    common.kill_feh()


# DEPOSIT_INVENTORY -------------------------------------------------------------------------------

deposit_inventory_pass_params = (("01"),)


@pytest.mark.parametrize("params", deposit_inventory_pass_params)
def test_deposit_inventory_pass(params):
    test_number = params
    common.feh("deposit_inventory", "pass", test_number, image_directory)
    result = banking.deposit_inventory()
    assert result is None
    common.kill_feh()


deposit_inventory_fail_params = (("01"),)


@pytest.mark.parametrize("params", deposit_inventory_fail_params)
def test_deposit_inventory_fail(params) -> None:
    test_number = params
    common.feh("deposit_inventory", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not deposit inventory"):
        banking.deposit_inventory()
    common.kill_feh()


# DEPOSIT_ITEM ------------------------------------------------------------------------------------

deposit_item_pass_params = (("./needles/items/raw-anchovies.png", "all", "01"),)


@pytest.mark.parametrize("params", deposit_item_pass_params)
def test_deposit_item_pass(params):
    item, quantity, test_number = params
    common.feh("deposit_item", "pass", test_number, image_directory)
    result = banking.deposit_item(item, quantity)
    assert result is None
    common.kill_feh()


# OPEN_BANK ---------------------------------------------------------------------------------------

open_bank_pass_params = (
    ("south", "01"),  # 1 tile south.
    ("south", "02"),  # 2 tiles south.
    ("west", "03"),  # 1 tile west.
    ("west", "04"),  # 2 tiles west.
    ("east", "05"),  # 1 tile east.
)


@pytest.mark.parametrize("params", open_bank_pass_params)
def test_open_bank_pass(params):
    direction, test_number = params
    common.feh("open_bank", "pass", test_number, image_directory)
    result = banking.open_bank(direction)
    assert result is True
    common.kill_feh()


# WITHDRAWAL_ITEM ---------------------------------------------------------------------------------

withdrawal_item_pass_params = (
    (
        "./needles/items/raw-anchovies-bank.png",
        "./needles/items/raw-anchovies.png",
        0.99,
        "all",
        "01",
    ),
)


@pytest.mark.parametrize("params", withdrawal_item_pass_params)
def test_withdrawal_item_pass(params):
    item_bank, item_inv, conf, quantity, test_number = params
    common.feh("withdrawal_item", "pass", test_number, image_directory)
    result = banking.withdrawal_item(item_bank, item_inv, conf, quantity)
    assert result is None
    common.kill_feh()


withdrawal_item_fail_params = (
    (
        "./needles/items/raw-anchovies-bank.png",
        "./needles/items/raw-anchovies.png",
        0.99,
        "all",
        "01",
    ),
)


@pytest.mark.parametrize("params", withdrawal_item_fail_params)
def test_withdrawal_item_fail(params) -> None:
    item_bank, item_inv, conf, quantity, test_number = params
    common.feh("withdrawal_item", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not withdrawal item"):
        banking.withdrawal_item(item_bank, item_inv, conf, quantity)
    common.kill_feh()

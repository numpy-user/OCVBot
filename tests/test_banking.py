# coding=UTF-8
"""
Unit tests for the banking.py module.

Linux only. Requires feh.

"""
import os

import pytest

import init_tests

# This statement exists to prevent the OCVBot imports from being re-ordered.
pass

# OCVBot modules must be imported after init_tests.
from ocvbot import banking
from ocvbot import startup as start

image_directory = (os.path.dirname(__file__)) + "/test_banking/"


# BANK_SETTINGS_CHECK -----------------------------------------------------------------------------

bank_settings_check_pass_params = (
    ("quantity", "all", "01"),  # Set quantity, must try 2 times.
    ("quantity", "all", "02"),  # Quantity already set.
    ("quantity", "1", "03"),  # Set quantity.
    ("quantity", "5", "04"),  # Set quantity.
    ("quantity", "10", "05"),  # Set quantity, must try 2 times.
    ("placeholder", "unset", "06"),  # Set placeholder.
    ("placeholder", "set", "07"),  # Unset placeholder, must try 2 times.
    ("placeholder", "unset", "08"),  # Placeholder already unset.
)


@pytest.mark.parametrize("params", bank_settings_check_pass_params)
def test_bank_settings_check_pass(params):
    setting, value, test_number = params
    init_tests.feh("bank_settings_check", "pass", test_number, image_directory)
    result = banking.bank_settings_check(setting, value)
    assert result is None


# Test unsupported function arguments.
bank_settings_check_fail_01_params = (
    ("note", "all"),  # Try setting a non-existent setting.
    ("quantity", "100"),  # Try setting a non-existent value.
    ("placeholder", "enabled"),  # Try setting a non-existent value.
)


@pytest.mark.parametrize("params", bank_settings_check_fail_01_params)
def test_bank_settings_check_fail_01(params):
    setting, value = params
    with pytest.raises(Exception, match="Unsupported"):
        banking.bank_settings_check(setting, value)
    init_tests.kill_feh()


# Test failure due to too many attempts.
bank_settings_check_fail_02_params = (("quantity", "10", "01"),)  # Try too many times.


@pytest.mark.parametrize("params", bank_settings_check_fail_02_params)
def test_bank_settings_check_fail_02(params) -> None:
    setting, value, test_number = params
    init_tests.feh("bank_settings_check", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not set bank setting"):
        banking.bank_settings_check(setting, value)
    init_tests.kill_feh()


# CLOSE BANK --------------------------------------------------------------------------------------

close_bank_pass_params = (
    "01",  # Must try 2 times.
    "02",  # Bank already closed.
)


@pytest.mark.parametrize("params", close_bank_pass_params)
def test_close_bank_pass(params) -> None:
    test_number = params
    init_tests.feh("close_bank", "pass", test_number, image_directory)
    result = banking.close_bank()
    assert result is None
    init_tests.kill_feh()


close_bank_fail_params = ("01",)  # Try too many times


@pytest.mark.parametrize("params", close_bank_fail_params)
def test_close_bank_fail(params) -> None:
    test_number = params
    init_tests.feh("close_bank", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not close bank window"):
        banking.close_bank()
    init_tests.kill_feh()


# DEPOSIT_INVENTORY -------------------------------------------------------------------------------

deposit_inventory_pass_params = (("01"),)  # Must try 3 times.


@pytest.mark.parametrize("params", deposit_inventory_pass_params)
def test_deposit_inventory_pass(params):
    test_number = params
    init_tests.feh("deposit_inventory", "pass", test_number, image_directory)
    result = banking.deposit_inventory()
    assert result is None
    init_tests.kill_feh()


deposit_inventory_fail_params = (("01"),)  # Try too many times.


@pytest.mark.parametrize("params", deposit_inventory_fail_params)
def test_deposit_inventory_fail(params) -> None:
    test_number = params
    init_tests.feh("deposit_inventory", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Could not deposit inventory"):
        banking.deposit_inventory()
    init_tests.kill_feh()


# DEPOSIT_ITEM ------------------------------------------------------------------------------------

deposit_item_pass_params = (
    ("./needles/items/raw-anchovies.png", "all", "01"),  # Must try 2 times.
    ("./needles/items/iron-ore.png", "10", "02"),  # Must set quantity first.
    ("./needles/items/iron-ore.png", "5", "03"),  # Must set quantity first.
    ("./needles/items/iron-ore.png", "1", "04"),  # Must set quantity first.
    ("./needles/items/iron-ore.png", "1", "05"),  # No items to deposit.
)


@pytest.mark.parametrize("params", deposit_item_pass_params)
def test_deposit_item_pass(params):
    item, quantity, test_number = params
    init_tests.feh("deposit_item", "pass", test_number, image_directory)
    result = banking.deposit_item(item, quantity)
    assert result is None
    init_tests.kill_feh()


# Deposit too many times.
deposit_item_fail_01_params = (("./needles/items/iron-ore.png", "10", "01"),)


@pytest.mark.parametrize("params", deposit_item_fail_01_params)
def test_deposit_item_fail_01(params) -> None:
    item, quantity, test_number = params
    init_tests.feh("deposit_item", "fail", test_number, image_directory)
    with pytest.raises(start.BankingError, match="Deposited too many items"):
        banking.deposit_item(item, quantity)
    init_tests.kill_feh()


# Deposit unsupported quantity.
deposit_item_fail_02_params = (("./needles/items/iron-ore.png", "100", "02"),)


@pytest.mark.parametrize("params", deposit_item_fail_02_params)
def test_deposit_item_fail_02(params) -> None:
    item, quantity, test_number = params
    init_tests.feh("deposit_item", "fail", test_number, image_directory)
    with pytest.raises(ValueError, match="Unsupported value for quantity"):
        banking.deposit_item(item, quantity)
    init_tests.kill_feh()


# Try too many times.
deposit_item_fail_03_params = (("./needles/items/iron-ore.png", "all", "03"),)


@pytest.mark.parametrize("params", deposit_item_fail_03_params)
def test_deposit_item_fail_03(params) -> None:
    item, quantity, test_number = params
    init_tests.feh("deposit_item", "fail", test_number, image_directory)
    with pytest.raises(start.BankingError, match="Could not deposit items"):
        banking.deposit_item(item, quantity)
    init_tests.kill_feh()


# OPEN_BANK ---------------------------------------------------------------------------------------

open_bank_pass_params = (
    ("south", "01"),  # 1 tile south.
    ("south", "02"),  # 2 tiles south.
    ("west", "03"),  # 1 tile west.
    ("west", "04"),  # 2 tiles west.
    ("east", "05"),  # 1 tile east.
    ("east", "07"),  # Bank window already open.
)


@pytest.mark.parametrize("params", open_bank_pass_params)
def test_open_bank_pass(params):
    direction, test_number = params
    init_tests.feh("open_bank", "pass", test_number, image_directory)
    result = banking.open_bank(direction)
    assert result is None
    init_tests.kill_feh()


# Provide an invalid direction.
open_bank_fail_01_params = (("not_a_valid_direction"),)


@pytest.mark.parametrize("params", open_bank_fail_01_params)
def test_open_bank_fail_01(params) -> None:
    direction = params
    with pytest.raises(ValueError, match="Must provide a cardinal direction"):
        banking.open_bank(direction)
    init_tests.kill_feh()


# Unable to open bank window.
open_bank_fail_02_params = (("east", "01"),)


@pytest.mark.parametrize("params", open_bank_fail_02_params)
def test_open_bank_fail_02(params) -> None:
    direction, test_number = params
    init_tests.feh("open_bank", "fail", test_number, image_directory)
    with pytest.raises(Exception, match="Unable to open bank"):
        banking.open_bank(direction)
    init_tests.kill_feh()


# WITHDRAWAL_ITEM ---------------------------------------------------------------------------------

withdrawal_item_pass_params = (
    (
        "./needles/items/raw-anchovies-bank.png",
        "./needles/items/raw-anchovies.png",
        0.99,
        "all",
        "01",
    ),
    # Must set quantity and try 2 times.
    (
        "./needles/items/raw-anchovies-bank.png",
        "./needles/items/raw-anchovies.png",
        0.95,
        "10",
        "02",
    ),
)


@pytest.mark.parametrize("params", withdrawal_item_pass_params)
def test_withdrawal_item_pass(params):
    item_bank, item_inv, conf, quantity, test_number = params
    init_tests.feh("withdrawal_item", "pass", test_number, image_directory)
    result = banking.withdrawal_item(item_bank, item_inv, conf, quantity)
    assert result is None
    init_tests.kill_feh()


# Try too many times to withdrawal item.
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
    init_tests.feh("withdrawal_item", "fail", test_number, image_directory)
    with pytest.raises(start.BankingError, match="Could not withdrawal item"):
        banking.withdrawal_item(item_bank, item_inv, conf, quantity)
    init_tests.kill_feh()

# coding=UTF-8
"""
Functions for interacting with the banking window.

Used for:
  - opening the bank
  - closing the bank
  - withdrawing items
  - depositing items

"""
import logging as log

from ocvbot import interface
from ocvbot import misc
from ocvbot import startup as start
from ocvbot import vision as vis

# TODO: Add search_for_item() function.
# TODO: bank_settings_check(): Add option to disable setting item placeholders.
# TODO: Finish enter_bank_pin() function.


def bank_settings_check(setting: str, value: str) -> None:
    """
    Checks for specific bank window configuration settings.
    Currently only the `quantity` setting is supported.

    Args:
        setting (str): The setting you wish to configure.
            quantity = Sets the value of the `quantity` setting. Available
                       values are `1`, `5`, `10`, and `all`.
            placeholder = Sets the value of the `placeholder` setting.
                          Available values are `set` and `unset`.
        value (str): The value you wish the setting to have.

    Examples:
        bank_settings_check("quantity", "all")
        bank_settings_check("placeholder", "unset")

    Raises:
        Raises an exception if the setting could not be set, or the setting is
        not supported.

    """
    if setting == "quantity":
        if value not in ("1", "5", "10", "all"):
            raise Exception("Unsupported value for quantity setting: ", value)
        setting_unset = (
            "./needles/bank/settings/" + setting + "/" + value + "-unset.png"
        )
        setting_set = "./needles/bank/settings/" + setting + "/" + value + "-set.png"

    elif setting == "placeholder":
        if value == "set":
            setting_unset = "./needles/bank/settings/placeholder/placeholder-unset.png"
            setting_set = "./needles/bank/settings/placeholder/placeholder-set.png"
        elif value == "unset":
            setting_unset = "./needles/bank/settings/placeholder/placeholder-set.png"
            setting_set = "./needles/bank/settings/placeholder/placeholder-unset.png"
        else:
            raise Exception("Unsupported value for placeholder setting: ", value)

    else:
        raise Exception("Unsupported setting: ", setting)

    try:
        log.debug("Checking if bank setting %s is set to %s", setting, value)
        interface.enable_button(
            button_disabled=setting_unset,
            button_disabled_region=vis.game_screen,
            button_enabled=setting_set,
            button_enabled_region=vis.game_screen,
        )
    except Exception as error:
        raise Exception("Could not set bank setting!") from error


def close_bank():
    """
    Closes the bank window if it is open.

    Raises:
        Raises an exception if the bank window could not be closed.

    """
    # Must use invert_match here because we want to check for the absence of
    #   the `close` button.
    try:
        interface.enable_button(
            button_disabled="./needles/buttons/close.png",
            button_disabled_region=vis.game_screen,
            button_enabled="./needles/buttons/close.png",
            button_enabled_region=vis.game_screen,
            invert_match=True,
        )
    except Exception as error:
        raise Exception("Could not close bank window!") from error


def deposit_inventory() -> None:
    """
    Deposits entire inventory into the bank. Assumes the bank window is
    open and the "deposit inventory" button is visible.

    Raises:
        Raises an exception if the inventory could not be deposited.

    """
    try:
        interface.enable_button(
            button_disabled="./needles/bank/deposit-inventory.png",
            button_disabled_region=vis.game_screen,
            button_enabled="./needles/side-stones/inventory/empty-inventory.png",
            button_enabled_region=vis.inv,
        )
    except Exception as error:
        raise Exception("Could not deposit inventory!") from error


def deposit_item(item, quantity) -> None:
    """
    Deposits the given item into the bank. Assumes the bank window is
    open.

    Args:
        item (str): Filepath to an image of the item to deposit as it
                    appears in the player's inventory.
        quantity (str): Quantity of the item to deposit. Available
                        values are `1`, `5`, `10`, and `all`.

    Returns:
        Returns when item was successfully deposited into bank, or there were
        no items of that type in the inventory to begin with.

    Raises:
        Raises a ValueError if `quantity` doesn't match the available values.

        Raises an Exception if the item could not be deposited.

    """
    # Count the initial number of the given item in the inventory.
    initial_number_of_items = vis.Vision(region=vis.inv, needle=item).count_needles()
    # If there are no matching items in the inventory to begin with, return.
    if initial_number_of_items == 0:
        log.debug("No items of type %s to deposit", item)
        return

    # Determine the number of of items that should be removed from the inventory.
    if quantity == "1":
        items_to_deposit = 1
    elif quantity == "5":
        items_to_deposit = 5
    elif quantity == "10":
        items_to_deposit = 10
    elif quantity == "all":
        items_to_deposit = initial_number_of_items
    else:
        raise ValueError("Unsupported value for quantity argument!")

    log.info("Attempting to deposit %s of item %s", quantity, item)

    # Make sure the correct quantity is deposited.
    bank_settings_check("quantity", str(quantity))

    # Try clicking on the item multiple times.
    for _ in range(5):
        vis.Vision(
            region=vis.inv,
            needle=item,
            loop_num=3,
        ).click_needle(sleep_range=(0, 100, 0, 100), move_away=True)

        # Loop and wait until the item has been deposited.
        for _ in range(10):
            misc.sleep_rand(200, 700)
            final_number_of_items = vis.Vision(
                region=vis.inv, needle=item
            ).count_needles()
            if (initial_number_of_items - items_to_deposit) == final_number_of_items:
                log.debug("Deposited item %s", item)
                return

    raise Exception("Could not deposit items!")


def enter_bank_pin(pin=(start.config["main"]["bank_pin"])) -> bool:
    """
    Enters the user's bank PIN. Assumes the bank window is open.

    Args:
        pin (tuple): A 4-tuple of the player's PIN.

    Examples:
        enter_bank_pin(pin=1234)

    Returns:
        Returns True if the bank PIN was successfully entered or PIN
        window could not be found, returns False if PIN was incorrect

    """
    pin = tuple(str(pin))
    # Confirm that the bank PIN screen is actually present.
    bank_pin_screen = vis.Vision(
        region=vis.game_screen, needle="./needles/.png", loop_num=1
    ).wait_for_needle(get_tuple=False)
    if bank_pin_screen is False:
        return True

    # Loop through the different PIN screens for each of the 4 digits.
    for pin_ordinal in range(1, 4):

        # Wait for the first/second/third/fourth PIN prompt screen to
        #   appear.
        pin_ordinal_prompt = vis.Vision(
            region=vis.game_screen, needle="./needles/" + str(pin_ordinal), loop_num=1
        ).wait_for_needle(get_tuple=False)

        # Enter the first/second/third/fourth digit of the PIN.
        if pin_ordinal_prompt is True:
            enter_digit = vis.Vision(
                region=vis.game_screen,
                needle="./needles/" + pin[pin_ordinal],
                loop_num=1,
            ).click_needle()
    return True


def open_bank(direction) -> bool:
    """
    Opens the bank. Assumes the player is within 2 empty tiles of a bank booth.

    Args:
        direction (str): The cardinal direction of the bank booth relative to
                         the player.  Must be `north`, `south`, `east`, or
                         `west`.

    Examples:
        open_bank("west")

    Returns:
        Returns True if bank was opened successfully or is already open,
        returns False otherwise

    """
    bank_open = vis.Vision(
        region=vis.game_screen, needle="./needles/buttons/close.png", loop_num=1
    ).wait_for_needle()
    if bank_open is True:
        log.info("Bank window is already open.")
        return True

    log.info("Attempting to open bank window.")
    for _ in range(5):
        one_tile = vis.Vision(
            region=vis.game_screen,
            needle="./needles/game-screen/bank/bank-booth-" + direction + "-1-tile.png",
            loop_num=1,
            conf=0.85,
        ).click_needle()

        two_tiles = vis.Vision(
            region=vis.game_screen,
            needle="./needles/game-screen/bank/bank-booth-"
            + direction
            + "-2-tiles.png",
            loop_num=1,
            conf=0.85,
        ).click_needle()

        if one_tile is True or two_tiles is True:
            bank_open = vis.Vision(
                region=vis.game_screen,
                needle="./needles/buttons/close.png",
                loop_num=10,
            ).wait_for_needle()
            if bank_open is True:
                return True
        misc.sleep_rand(1000, 3000)

    log.warning("Unable to open bank!")
    return False


def withdrawal_item(
    item_bank: str, item_inv: str, conf: float = 0.95, quantity: str = "all"
) -> None:
    """
    Withdrawals an item from the bank. Assumes the bank window is open and
    the item to withdrawal is visible.

    Args:
        item_bank (str): Filepath to an image of the item to withdrawal as it
                         appears in the bank window.
        item_inv (str): Filepath to an image of the item to withdrawal as it
                        appears in the player's inventory.
        conf (float): See the `conf` arg of the vision.Vision class. Default is
                      0.95
        quantity (str): The number of items to withdrawal. Available
                        options are `1`, `5`, `10`, or `all`. Default is `all`.

    Examples:
        withdrawal_item(item_bank="./needles/items/raw-anchovies-bank.png",
                        item_inv="./needles/items/raw-anchovies.png",
                        conf=0.98)

    Returns:
        Returns True if the item was successfully withdrawn from bank,
        returns False otherwise.

    """
    log.info("Attempting to withdrawal item: %s", item_bank)
    try:
        # Ensure the correct quantity is withdrawn.
        bank_settings_check("quantity", str(quantity))
        # Make sure no placeholders are left behind, as this makes image
        #   matching much more difficult -- placeholders look very similar
        #   to regular "real" items.
        bank_settings_check("placeholder", "unset")
        interface.enable_button(
            button_disabled=item_bank,
            button_disabled_region=vis.bank_items_window,
            button_enabled=item_inv,
            button_enabled_region=vis.inv,
            loop_num=10,
            conf=conf,
        )
    except Exception as error:
        raise Exception("Could not withdrawal item!") from error

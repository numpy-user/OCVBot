# coding=utf-8
"""
Module for invoking main bot scripts.

Most main scripts define a preset list of `scenarios` from which the user
must choose from. Each scenario has a predetermined configuration that will
used for training that skill. For example, the `varrock-east-mine` scenario
for the `miner` script is configured to only mine two specific iron rocks
within Varrock East Mine.

See `config.yaml.example` for more info.
See `docs/scenarios/` for the required client configuration settings in
each scenario.

"""
import logging as log
import os
import pathlib
import sys

# Global TODOs:
# TODO: Transition to use proper exceptions rather than checking for a False return value.

# Make sure the program's working directory is the directory in which
#   this file is located.
os.chdir(os.path.dirname(__file__))

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)

from ocvbot import banking
from ocvbot import behavior
from ocvbot import misc
from ocvbot import skills
from ocvbot import startup as start
from ocvbot import vision as vis


def miner(scenario: str) -> None:
    """
    Script for mining rocks in a handful of locations. Banking support is
    limited.

    Supported scenarios:
        `lumbridge-mine` = Mines copper in Lumbridge Swamp.
        `varrock-east-mine` = Mines iron in Varrock East mine. Banking
                              supported.

        See `/docs/scenarios/` for the required client
        configuration settings for each scenario.

    Raises:
        Raises an exception if an unsupported scenario is passed.

    """
    # TODO: Function is too large. Refactor.

    log.info("Launching miner script with scenario %s.", scenario)
    # Determine if the player will be dropping the ore or banking it.
    # This var is forced to True in scenarios where banking is not
    #   supported.
    drop_ore = start.config["mining"]["drop_ore"]
    # Make the path to the rock needles shorter.
    prefix = "./needles/game-screen/" + scenario + "/"
    haystack_map = "./haystacks/" + scenario + ".png"

    # Set initial waypoint coordinates.
    bank_from_mine = None
    mine_from_bank = None

    while True:

        # Ensure the client is logged in.
        client_status = vis.orient()
        if client_status[0] == "logged_out":
            behavior.login_full()

        if scenario == "varrock-east-mine":
            mining = skills.Mining(
                rocks=[
                    (prefix + "north-full2.png", prefix + "north-empty.png"),
                    (prefix + "west-full.png", prefix + "west-empty.png"),
                ],
                ore="./needles/items/iron-ore.png",
                position=(
                    [((240, 399), 1, (4, 4), (5, 10))],
                    "./haystacks/varrock-east-mine.png",
                ),
            )

            bank_from_mine = [
                ((253, 181), 5, (35, 35), (1, 6)),
                ((112, 158), 5, (20, 20), (1, 6)),
                ((108, 194), 1, (10, 4), (3, 8)),
            ]

            mine_from_bank = [
                ((240, 161), 5, (35, 35), (1, 6)),
                ((262, 365), 5, (25, 25), (1, 6)),
                ((240, 399), 1, (4, 4), (3, 8)),
            ]

        elif scenario == "lumbridge-mine":
            drop_ore = True  # Banking not supported.
            mining = skills.Mining(
                rocks=[
                    (prefix + "east-full.png", prefix + "east-empty.png"),
                    (prefix + "south-full.png", prefix + "south-empty.png"),
                ],
                ore="./needles/items/copper-ore.png",
            )

        elif scenario == "al-kharid-mine":
            drop_ore = True  # Banking not supported.
            mining = skills.Mining(
                rocks=[
                    (prefix + "north-full.png", prefix + "north-empty.png"),
                    (prefix + "west-full.png", prefix + "west-empty.png"),
                    (prefix + "south-full.png", prefix + "south-empty.png"),
                ],
                ore="./needles/items/iron-ore.png",
                conf=(0.95, 0.95),
            )
        else:
            raise Exception("Scenario not supported!")

        if mining.mine_rocks() == "inventory-full":

            elapsed_time = misc.session_duration(human_readable=True)
            log.info("Script has been running for %s (HH:MM:SS)", elapsed_time)

            if drop_ore is True:
                mining.drop_inv_ore()

            behavior.travel(bank_from_mine, haystack_map)
            behavior.open_side_stone("inventory")
            banking.open_bank("south")
            vis.Vision(region=vis.inv, needle=mining.ore).click_needle()
            for item in mining.drop_items:
                vis.Vision(region=vis.inv, needle=item[1], loop_num=1).click_needle()
            # TODO: Instead of waiting a hard-coded period of time,
            #   wait until the item can no longer be found in the
            #   player's inventory.
            misc.sleep_rand(500, 3000)
            # Mining spot from bank.
            behavior.travel(mine_from_bank, haystack_map)
            misc.sleep_rand(300, 800)

        else:
            # Roll for randomized actions when the script returns.
            behavior.logout_break_range()


def alchemist(alch_item_type, loops: int = 10000) -> None:
    """
    Script for training high alchemy.

    Args:
        alch_item_type (str): See the `magic` section of `config.yaml.example`
                              for the available options.
        loops (int): Number of loops to run the given scenario. Changing this
                     is only useful for testing purposes. Default is 10000.

    """
    spell = "./needles/side-stones/spellbook/high-alchemy.png"
    if alch_item_type == "bank-note":
        target = "./needles/items/bank-note.png"
    else:
        target = "./needles/items/" + alch_item_type + ".png"

    behavior.open_side_stone("spellbook")
    for _ in range(loops):
        skills.Magic(
            spell=spell,
            target=target,
            inventory=True,
            conf=0.5,
            region=vis.inv_left_half,
            move_duration_range=(0, 200),
        ).cast_spell()
        misc.sleep_rand_roll(chance_range=(10, 20), sleep_range=(100, 10000))


def spellcaster(scenario: str, loops: int = 10000) -> None:
    """
    Script for training magic with combat spells.

    Args:
        scenario (str): See the `magic` section of `config.yaml.example` for
                        the available options.
        loops (int): Number of loops to run the given scenario. Changing this
                     is only useful for testing purposes. Default is 10000.

    Raises:
        Raises an exception if an unsupported scenario is passed.

    """
    log.info("Launching spellcaster script with scenario %s.", scenario)

    if scenario == "curse-varrock-castle":
        spell = "./needles/side-stones/spellbook/curse.png"
        target = "./needles/game-screen/varrock/monk-of-zamorak.png"
        haystack_map = "./haystacks/varrock-castle.png"
        behavior.travel([((75, 128), 1, (4, 4), (5, 10))], haystack_map)
    else:
        raise Exception("Scenario not supported!")

    behavior.open_side_stone("spellbook")
    for _ in range(loops):
        skills.Magic(
            spell=spell,
            target=target,
            conf=0.75,
            region=vis.game_screen,
        ).cast_spell()
        misc.sleep_rand_roll(chance_range=(10, 20), sleep_range=(100, 10000))


def chef(item: str, location: str, loops: int = 10000) -> bool:
    """
    Cooks a given item at a given location.

    Args:
        item (str): See the `cooking` section of `config.yaml.example` for
                    the available options.
        location (str): See the `cooking` section of `config.yaml.example` for
                       the available options.
        loops (int): Number of loops to run the given scenario. Changing this
                     is only useful for testing purposes. Default is 10000.

    Returns:

    """
    if location == "al-kharid":
        bank_coords = [((91, 207), 3, (4, 7), (3, 9))]
        range_coords = [((103, 148), 1, (5, 5), (8, 12))]
        heat_source = "./needles/game-screen/al-kharid/range.png"
        # Assumes starting location is the bank.
        banking.open_bank("west")
    else:
        log.critical("Unsupported value for location!")
        raise RuntimeError("Unsupported value for location!")

    log.info("Launching chef script with item %s and location %s.", item, location)
    # Must have staff of water equipped!
    # TODO: In Al Kharid, deal with the door to the house with the range
    #   possibly being shut.
    haystack_map = "./haystacks/" + location + ".png"
    item_inv = "./needles/items/" + item + ".png"
    item_bank = "./needles/items/" + item + "-bank.png"

    for _ in range(loops):
        # Conf is higher than default because raw food looks very
        #   similar to cooked food.
        banking.withdrawal_item(item_bank=item_bank, item_inv=item_inv, conf=0.99)
        log.info("Withdrawing raw food.")
        misc.sleep_rand_roll(chance_range=(10, 20), sleep_range=(100, 10000))
        # Go to range.
        behavior.travel(range_coords, haystack_map)
        # Cook food.
        skills.Cooking(item_inv, item_bank, heat_source).cook_item()
        # Go back to bank and deposit cooked food.
        behavior.travel(bank_coords, haystack_map)
        banking.open_bank("west")
        misc.sleep_rand_roll(chance_range=(10, 20), sleep_range=(100, 10000))
        banking.deposit_inventory()
    return True


def smith(bar: str, item: str, location: str, loops: int = 10000):
    """
    Smiths bars at an anvil.

    Args:
        bar (str): See the `smithing` section of `config.yaml.example` for
                   the available options.
        location (str): See the `smithing` section of `config.yaml.example` for
                       the available options.
        loops (int): Number of loops to run the given scenario. Changing this
                     is only useful for testing purposes. Default is 10000.

    """
    if location == "varrock":
        haystack_map = "./haystacks/varrock-west-bank.png"
        bank_coords = [((88, 93), 1, (4, 5), (7, 9))]
        anvil_coords = [((97, 130), 1, (3, 3), (7, 9))]
        anvil = "./needles/game-screen/varrock/anvil.png"
    else:
        raise Exception("Unsupported value for location!")

    # We can use banked versions of the smith item because the smithing menu
    #   has the same background as the bank menu.
    bar = "./needles/items/" + bar + ".png"
    item = "./needles/items/" + item + "-bank.png"
    hammer_inv = "./needles/items/hammer.png"
    hammer_bank = "./needles/items/hammer-bank.png"

    # Determine how many bars are needed to smith the given item.
    if "platebody" in item:
        bars_required = 5
    elif "scimitar" in item:
        bars_required = 2
    elif "axe" in item or "warhammer" in item:
        bars_required = 3
    else:

    smithing = skills.Smithing(
        item_in_menu=item,
        bar_type=bar,
        bars_required=bars_required,
        anvil=anvil,
    )

    if behavior.open_side_stone("inventory") is False:
        return False
        raise Exception("Unsupported value of item!")

    for _ in range(loops):

        if location == "varrock":
            banking.open_bank("east")
        banking.deposit_inventory()
        misc.sleep_rand_roll()

        # Ensure we have bars in the bank
        have_bars = vis.Vision(
            region=vis.game_screen, needle=bar, conf=0.9999
        ).find_needle()
        # Stop script if we don't
        if have_bars is False:
            log.info("Out of bars, stopping script.")
            break

        withdrew_hammer = banking.withdrawal_item(
            item_bank=hammer_bank, item_inv=hammer_inv, quantity="1"
        )
        if withdrew_hammer is False:
            log.error("Unable to withdrawal hammer!")
            break
        misc.sleep_rand_roll()
        withdrew_bars = banking.withdrawal_item(item_bank=bar, item_inv=bar)
        if withdrew_bars is False:
            log.error("Unable to withdrawal bars!")
            break
        misc.sleep_rand_roll()

        # Check if we withdrew a full inventory of bars.
        bars_in_inventory = vis.Vision(region=vis.inv, needle=bar).count_needles()
        # Stop script if we didn't
        if bars_in_inventory != 27:
            log.warning("Out of bars, stopping script.")
            break

        behavior.travel(anvil_coords, haystack_map)
        misc.sleep_rand_roll()
        smithing.smith_items()
        misc.sleep_rand_roll()
        behavior.travel(bank_coords, haystack_map)
        misc.sleep_rand_roll()

    return True


def test():
    banking.deposit_inventory()


# TODO: Add basic firemaking script that starts at a bank booth and
#   creates 27 fires, all in a straight line, then returns to the booth.

# TODO: Add oak woodcutting script that waits by an oak tree, clicks on
#   it when it appears, and empties inventory when full -- super simple.

# TODO: Possible location for starting a fishing script where the
#  "fishing tiles" don't change much is fly fishing at barbarian village.


script = start.config["main"]["script"]


def main():
    """
    Calls the main botting script defined in the config file.

    """
    if script == "mining":
        miner(start.config[script]["location"])

    elif script == "magic":
        if start.config[script]["scenario"] == "high-alchemy":
            alchemist(start.config[script]["alch_item_type"])
        else:
            spellcaster(start.config[script]["scenario"])

    elif script == "cooking":
        chef(
            item=start.config[script]["item"],
            location=start.config[script]["location"],
        )

    elif script == "smithing":
        smith(
            bar=start.config[script]["bar"],
            item=start.config[script]["item"],
            location=start.config[script]["location"],
        )

    elif script == "test":
        test()

    else:
        log.critical("Unknown value provided for 'script' key in config file!")
        raise RuntimeError("Unknown value provided for 'script' key in config file!")

    sys.exit(0)


if __name__ == "__main__":
    main()

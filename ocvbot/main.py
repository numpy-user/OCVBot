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


def spellcaster(scenario: str) -> None:
    """
    Script for training magic, either with combat spells or alchemy.

    Supported scenarios:
        `curse-varrock-castle` = Casts curse against the Monk of Zamorak
                                 in varrock castle.
        `high-alchemy` = Casts high alchemy on all noted items within the
                         left half of the player's inventory.

    Raises:
        Raises an exception if an unsupported scenario is passed.

    """
    log.info("Launching spellcaster script with scenario %s.", scenario)
    # TODO: Ensure spellbook side-stone is open before starting loop.
    if scenario == "curse-varrock-castle":
        spell = "./needles/side-stones/spellbook/curse.png"
        target = "./needles/game-screen/varrock/monk-of-zamorak.png"
        haystack_map = "./haystacks/varrock-castle.png"
        behavior.travel([((75, 128), 1, (4, 4), (5, 10))], haystack_map)
        for _ in range(10000):
            skills.Magic(
                spell=spell,
                target=target,
                logout=True,
                conf=0.75,
                region=vis.game_screen,
            ).cast_spell()

    # Casts high-level alchemy on all noted items in the left half of the
    #   player's inventory.
    elif scenario == "high-alchemy":
        spell = "./needles/side-stones/spellbook/high-alchemy.png"
        item = start.config["magic"]["alch_item_type"]
        if item == "bank-note":
            target = "./needles/items/bank-note.png"
        else:
            target = "./needles/items/" + item + ".png"
        behavior.open_side_stone("spellbook")
        for _ in range(10000):
            spell_cast = skills.Magic(
                spell=spell,
                target=target,
                inventory=True,
                logout=False,
                conf=0.5,
                region=vis.inv_left_half,
                move_duration_range=(0, 200),
            ).cast_spell()
            if spell_cast is False:
                if start.config["magic"]["logout"] is True:
                    behavior.logout()
                sys.exit(0)
                #  check inv for nature runes
                #  if nature runes = 0
                #      open inv
                #      get cash stack
                #      purchase nature runes equal to 10% cash stack

                #  check inv for alched item
                #  if item = 0
                #      open inv
                #      get cash stack
                #      search for item on GE to get price
                #      determine how many of that item can be bought
                #      buy that many nature runes
                #      get new cash stack
                #      buy item
            misc.sleep_rand_roll(chance_range=(10, 30), sleep_range=(0, 3000))

        behavior.logout()
    else:
        raise Exception("Scenario not supported!")


def chef(item: str, location: str, loops: int) -> bool:
    """
    Cooks a given item at a given location.

    Args:
        item:
        location:
        loops: The number of iterations to run.

    Returns:

    """
    log.info("Launching chef script with item %s and location %s.", item, location)
    # Must have staff of water equipped!
    # TODO: In Al Kharid, deal with the door to the house with the range
    #   possibly being shut.
    haystack_map = "./haystacks/" + location + ".png"
    item_inv = "./needles/items/" + item + ".png"
    item_bank = "./needles/items/" + item + "-bank.png"

    bank_coords = [((91, 207), 3, (4, 7), (3, 9))]
    range_coords = [((107, 152), 1, (5, 5), (8, 12))]
    heat_source = "./needles/game-screen/al-kharid/range.png"

    # Assumes starting location is the bank.
    banking.open_bank("west")

    for _ in range(loops):
        # Conf is higher than default because raw food looks very
        #   similar to cooked food.
        banking.withdrawal_item(item_bank=item_bank, item_inv=item_inv, conf=0.98)
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




def smither(bar: str, smith: str, bars_per_item: int):
    haystack_map = "./haystacks/varrock-west-bank.png"

    # These are used to figure out when we're done smithing.
    # Smithing items that take multiple bars may lead to 1 or 2 bars remaining.
    inv_3_remaining = "./needles/side-stones/inventory/iron-bars-3.png"
    inv_2_remaining = "./needles/side-stones/inventory/iron-bars-2.png"
    inv_1_remaining = "./needles/items/iron-bar.png"

    inv_full = "./needles/side-stones/inventory/iron-bars-full.png"

    # We can use banked versions of the smith item because the smithing menu
    # has the same background as the bank menu
    bar = "./needles/items/" + bar + ".png"
    smith = "./needles/items/" + smith + "-bank.png"
    anvil = "./needles/game-screen/varrock/anvil.png"

    hammer_inv = "./needles/items/hammer.png"
    hammer_bank = "./needles/items/hammer-bank.png"

    bank_coords = [((88, 95), 1, (4, 7), (8, 10))]
    anvil_coords = [((98, 132), 1, (3, 3), (8, 10))]

    # Determine which needle to use by bars per item.
    # For example, if we smith a full inventory of platebodies (5 bars per item),
    #   we'll have 2 bars remaining once we reach the end. We then know we're
    #   done smithing if we can't find 3 bars in our inventory.
    if bars_per_item == 5:
        uncompleted_inv = inv_3_remaining
    elif bars_per_item == 2:
        uncompleted_inv = inv_2_remaining
    elif bars_per_item in (1, 3):
        uncompleted_inv = inv_1_remaining
    else:
        log.critical("Unsupported value of bars_per_item!")
        raise RuntimeError("Unsupported value of bars_per_item!")

    smithing = skills.Smithing(smith, anvil, uncompleted_inv)

    while True:

        # Ensure the client is logged in.
        client_status = vis.orient()
        if client_status[0] == "logged_out":
            behavior.login_full()

        # Assumes starting location is Varrock west bank.
        banking.open_bank("east")
        banking.deposit_inventory()

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

        withdrew_bars = banking.withdrawal_item(item_bank=bar, item_inv=bar)
        if withdrew_bars is False:
            log.error("Unable to withdrawal bars!")
            break

        # Check if we withdrew a full inventory of bars
        full_inv = vis.Vision(region=vis.inv, needle=inv_full).wait_for_needle()

        # Stop script if we didn't
        if full_inv is False:
            log.info("Out of bars, stopping script.")
            break

        behavior.travel(anvil_coords, haystack_map)
        smithing.smith_items()
        behavior.travel(bank_coords, haystack_map)


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
    if script == "mining":
        miner(start.config[script]["location"])
        sys.exit(0)

    elif script == "magic":
        spellcaster(start.config[script]["scenario"])
        sys.exit(0)

    elif script == "chef":
        chef(
            item=start.config[script]["item"],
            location=start.config[script]["location"],
            loops=1000,
        )
        sys.exit(0)
    elif script == "smithing":
        smither(
            bar=start.config[script]["bar"],
            smith=start.config[script]["smith"],
            bars_per_item=start.config[script]["bars_per_item"],
        )
        sys.exit(0)
    elif script == "test":
        test()
        sys.exit(0)
    else:
        log.critical("Unknown value provided for 'script' key in config file!")
        raise RuntimeError("Unknown value provided for 'script' key in config file!")


if __name__ == "__main__":
    main()

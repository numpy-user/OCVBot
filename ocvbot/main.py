# coding=utf-8
"""
Module for invoking main bot scripts.

Most main scripts define a preset list of 'scenarios' from which the user
can choose from. Each scenario has a predetermined configuration that will
used for training that skill. For example, the 'varrock-east-mine' scenario
for the 'miner' script is configured to only mine two specific iron rocks
within Varrock East Mine.

Some scripts, however, are a little more flexible and don't define any
rigid scenarios to which the user must adhere. The 'chef' script, for
example, allows the user to specify both the item to be cooked as well as
the location to use.

See '/docs/client-configuration/' for the required client
configuration settings in each scenario.

"""
import logging as log
import sys

from ocvbot import skills, behavior, vision as vis, startup as start, misc


def miner(scenario):
    """
    Script for mining rocks in a handful of locations. Banking support is
    limited.

    Supported scenarios:
        'lumbridge-mine' = Mines copper in Lumbridge Swamp.
        'varrock-east-mine' = Mines iron in Varrock East mine. Banking
                              supported.
        'al-kharid-mine' = Mines iron in Al Kharid mine.

        See '/docs/client-configuration/' for the required client
        configuration settings for each scenario.

    Raises:
        Raises an exception if an unsupported scenario is passed.

    """
    # Determine if the player will be dropping the ore or banking it.
    # This var is forced to True in scenarios where banking is not
    #   supported.
    drop_ore = start.config['mining']['drop_ore']
    # Make the path to the rock needles shorter.
    prefix = './needles/game-screen/' + scenario + '/'
    haystack_map = './haystacks/' + scenario + '.png'

    # Set initial waypoint coordinates.
    bank_from_mine = None
    mine_from_bank = None

    while True:

        # Ensure the client is logged in.
        client_status = vis.orient()
        if client_status[0] == 'logged_out':
            behavior.login_full()

        if scenario == 'varrock-east-mine':
            mining = skills.Mining(rocks=[(prefix + 'north-full2.png',
                                           prefix + 'north-empty.png'),
                                          (prefix + 'west-full.png',
                                           prefix + 'west-empty.png')],
                                   ore='./needles/items/iron-ore.png',
                                   position=([((240, 399), 1, (4, 4), (5, 10))],
                                             './haystacks/varrock-east-mine.png'))

            bank_from_mine = ([((253, 181), 5, (35, 35), (1, 6)),
                               ((112, 158), 5, (20, 20), (1, 6)),
                               ((108, 194), 1, (10, 4), (3, 8))])

            mine_from_bank = ([((240, 161), 5, (35, 35), (1, 6)),
                               ((262, 365), 5, (25, 25), (1, 6)),
                               ((240, 399), 1, (4, 4), (3, 8))])

        elif scenario == 'lumbridge-mine':
            drop_ore = True  # Banking not supported.
            mining = skills.Mining(rocks=[(prefix + 'east-full.png',
                                           prefix + 'east-empty.png'),
                                          (prefix + 'south-full.png',
                                           prefix + 'south-empty.png')],
                                   ore='./needles/items/copper-ore.png')

        elif scenario == 'al-kharid-mine':
            drop_ore = True  # Banking not supported.
            mining = skills.Mining(rocks=[(prefix + 'north-full.png',
                                           prefix + 'north-empty.png'),
                                          (prefix + 'west-full.png',
                                           prefix + 'west-empty.png'),
                                          (prefix + 'south-full.png',
                                           prefix + 'south-empty.png')],
                                   ore='./needles/items/iron-ore.png',
                                   conf=(0.95, 0.95))
        else:
            raise Exception('Scenario not supported!')

        if mining.mine_rocks() == 'inventory-full':

            elapsed_time = misc.session_duration(human_readable=True)
            log.info('Script has been running for %s (HH:MM:SS)', elapsed_time)

            if drop_ore is True:
                mining.drop_inv_ore()

            behavior.travel(bank_from_mine, haystack_map)
            behavior.open_side_stone('inventory')
            behavior.open_bank('south')
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


def spellcaster(scenario):
    """
    Script for training magic, either with combat spells or alchemy.

    Supported scenarios:
        'curse-varrock-castle' = Casts curse against the Monk of Zamorak
                                 in varrock castle.
        'high-alchemy' = Casts high alchemy on all noted items within the
                         left half of the player's inventory.

    Raises:
        Raises an exception if an unsupported scenario is passed.

    """
    if scenario == 'curse-varrock-castle':
        spell = './needles/side-stones/spellbook/curse.png'
        target = './needles/game-screen/varrock/monk-of-zamorak.png'
        haystack_map = './haystacks/varrock-castle.png'
        for _ in range(10000):
            behavior.travel([((75, 128), 1, (4, 4), (5, 10))], haystack_map)
            skills.Magic(spell=spell, target=target, logout=True,
                         conf=0.75, region=vis.game_screen).cast_spell()

    # Casts high-level alchemy on all noted items in the left half of the
    #   player's inventory
    elif scenario == 'high-alchemy':
        spell = './needles/side-stones/spellbook/high-alchemy.png'
        item = start.config['magic']['alch_item_type']
        if item == 'bank-note':
            target = './needles/items/bank-note.png'
        else:
            target = './needles/items/' + item + '.png'
        behavior.open_side_stone('spellbook')
        for _ in range(10000):
            spell_cast = skills.Magic(spell=spell, target=target,
                                      inventory=True, logout=False,
                                      conf=0.45, region=vis.inv_left_half,
                                      move_duration_range=(0, 500)).cast_spell()
            if spell_cast is False:
                sys.exit(0)
            misc.sleep_rand_roll(chance_range=(10, 30), sleep_range=(0, 3000))

    else:
        raise Exception('Scenario not supported!')


def chef(item, location):
    """
    Cooks a given item at a given location.

    Args:
        item:
        location:

    Returns:

    """
    # Must have staff of water equipped!
    # TODO: In Al Kharid, deal with the door to the house with the range
    #   possibly being shut.
    haystack_map = './haystacks/' + location + '.png'
    item_inv = './needles/items/' + item + '.png'
    item_bank = './needles/items/' + item + '-bank.png'

    bank_coords = [((91, 207), 3, (4, 7), (3, 9))]
    range_coords = [((107, 152), 1, (5, 5), (8, 12))]
    heat_source = './needles/game-screen/al-kharid/range.png'

    # Assumes starting location is the bank.
    behavior.open_bank('west')

    for _ in range(1000):
        # Withdraw raw food from bank.
        # Conf is higher than default because raw food looks very
        #   similar to cooked food.
        # TODO: If item cannot be found in the bank, click the down arrow
        #   in the bank window until item is found.
        raw_food_withdraw = vis.Vision(region=vis.game_screen,
                                       needle=item_bank,
                                       loop_num=3, conf=0.98).click_needle()
        if raw_food_withdraw is False:
            raise Exception('Cannot find raw food in bank!')
        # Wait for raw food to appear in inventory
        raw_food_in_inv = vis.Vision(region=vis.inv,
                                     needle=item_inv,
                                     loop_num=30, conf=0.99).wait_for_needle()
        misc.sleep_rand_roll(chance_range=(10, 20), sleep_range=(100, 10000))
        if raw_food_in_inv is False:
            raise Exception('Cannot find items in inventory!')
        # Go to range.
        behavior.travel(range_coords, haystack_map)
        # Cook food.
        skills.Cooking(item_inv, item_bank, heat_source).cook_item()
        # Go back to bank.
        behavior.travel(bank_coords, haystack_map)
        # Open bank window.
        behavior.open_bank('west')
        misc.sleep_rand_roll(chance_range=(10, 20), sleep_range=(100, 10000))
        # Deposit cooked food. Try multiple times if not successful on
        #   the first attempt.
        inv_full = True
        for _ in range(1, 5):
            vis.Vision(region=vis.game_screen,
                       needle='./needles/bank/deposit-inventory.png',
                       loop_num=3).click_needle()
            misc.sleep_rand(500, 1000)
            misc.sleep_rand_roll(chance_range=(10, 20), sleep_range=(100, 10000))
            # Make sure inventory is empty.
            inv_full = vis.Vision(region=vis.inv,
                                  needle=item_inv,
                                  loop_sleep_range=(100, 300),
                                  loop_num=3, conf=0.8).wait_for_needle()
            # Only continue if the inventory is empty.
            if inv_full is False:
                break
        if inv_full is True:
            raise Exception('Could not empty inventory!')


# TODO: Add basic firemaking script that starts at a bank booth and
#   creates 27 fires, all in a straight line, then returns to the booth.

# TODO: Add oak woodcutting script that waits by an oak tree, clicks on
#   it when it appears, and empties inventory when full -- super simple.

# TODO: Possible location for starting a fishing script where the
#  "fishing tiles" don't change much is fly fishing at barbarian village.


script = start.config['main']['script']

if script == 'mining':
    miner(start.config[script]['location'])
    sys.exit(0)

elif script == 'magic':
    spellcaster(start.config[script]['scenario'])
    sys.exit(0)

elif script == 'chef':
    chef(start.config[script]['item'],
         start.config[script]['location'])
    sys.exit(0)

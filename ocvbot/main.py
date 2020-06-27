# coding=utf-8
"""
Invokes main bot scripts.

"""
import sys

from ocvbot import skills, behavior, vision as vis, startup as start, misc


def miner(scenario):
    """
    Script for mining in a variety of locations, based on preset
    "scenarios".

    Supported scenarios:
        'lumbridge-swamp' = Mines copper in Lumbridge Swamp. Banking is
                            not supported for this scenario.
        'varrock-east' = Mines iron in Varrock East mine.

        See "/docs/client-configuration/" for the required client
        configuration settings for each scenario.

    Args:
        scenario (str): The scenario to use. See above for supported
                        scenario types.

    Raises:
        Raises an exception if an unsupported scenario is passed.

    """
    while True:
        # Ensure the client is logged in.
        client_status = vis.orient()
        if client_status[0] == 'logged_out':
            behavior.login_full()

        if scenario == 'varrock-east-mine':
            skills.mine(rocks=[('./needles/game-screen/varrock-east-mine/north-full2.png',
                                './needles/game-screen/varrock-east-mine/north-empty.png'),
                               ('./needles/game-screen/varrock-east-mine/west-full.png',
                                './needles/game-screen/varrock-east-mine/west-empty.png')],
                        ore='./needles/items/iron-ore.png',
                        ore_type='iron',
                        drop_ore=start.config.get('mining', 'drop_ore'),
                        position=([((240, 399), 1, (4, 4), (5, 10))], './haystacks/varrock-east-mine.png'))

        elif scenario == 'lumbridge-mine':
            skills.mine(rocks=[('./needles/game-screen/lumbridge-mine/east-full.png',
                                './needles/game-screen/lumbridge-mine/east-empty.png'),
                               ('./needles/game-screen/lumbridge-mine/south-full.png',
                                './needles/game-screen/lumbridge-mine/south-empty.png')],
                        ore='./needles/items/copper-ore.png',
                        ore_type='copper',
                        drop_ore=True)  # Banking ore not supported.

        elif scenario == 'al-kharid-mine':
            skills.mine(rocks=[('./needles/game-screen/al-kharid-mine/north-full.png',
                                './needles/game-screen/al-kharid-mine/north-empty.png'),
                               ('./needles/game-screen/al-kharid-mine/west-full.png',
                                './needles/game-screen/al-kharid-mine/west-empty.png'),
                               ('./needles/game-screen/al-kharid-mine/south-full.png',
                                './needles/game-screen/al-kharid-mine/south-empty.png')],
                        ore='./needles/items/iron-ore.png',
                        ore_type='iron',
                        drop_ore=True,
                        conf=(0.95, 0.95))  # Banking ore not supported.

        else:
            raise Exception('Scenario not supported!')

        # Roll for randomized actions when the script returns.
        behavior.logout_break_range()


def spellcaster(scenario):
    """
    Defines a set of "scenarios" to use for magic training. Each
    scenario has a preset spell, target, and haystack that the
    cast_spell() function will use.

    Supported scenarios:
        'curse-varrock-castle' = Casts curse against the Monk of Zamorak
                                 in varrock castle.

        See "/docs/client-configuration/" for the required client
        configuration settings for each scenario.

    Args:
        scenario (str): The scenario to use. See above for supported
                        scenario types.

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
                         conf=0.75, haystack=vis.game_screen).cast_spell()

    # Casts high-level alchemy on all noted items in the left half of the
    #   player's inventory
    elif scenario == 'high-alchemy':
        spell = './needles/side-stones/spellbook/high-alchemy.png'
        target = './needles/items/bank-note.png'
        for _ in range(10000):
            spell_cast = skills.Magic(spell=spell, target=target, logout=False,
                                      conf=0.45, haystack=vis.inv_left_half).cast_spell()
            if spell_cast is False:
                sys.exit(0)

    else:
        raise Exception('Scenario not supported!')


def chef(item, location):
    # TODO: In Al Kharid, deal with the door to the house with the range
    #   possibly being shut.
    haystack_map = './haystacks/' + location + '.png'
    item_inv = './needles/items/' + item + '.png'
    item_bank = './needles/items/' + item + '-bank.png'

    bank_coords = [((91, 203), 3, (4, 9), (3, 9))]
    range_coords = [((105, 151), 1, (5, 5), (5, 10))]
    heat_source = './needles/game-screen/range.png'

    # Assumes starting location is the bank.
    for _ in range(1000):
        # Go to range.
        behavior.travel(range_coords, haystack_map)
        # Cook food.
        skills.Cooking(item_inv, item_bank, heat_source).cook_item()
        # Go back to bank.
        behavior.travel(bank_coords, haystack_map)
        # Open bank window.
        behavior.open_bank('west')
        misc.wait_rand(20, 100, 10000)
        # Deposit cooked food. Try multiple times if not successful on
        #   the first attempt.
        inv_full = True
        for _ in range(1, 5):
            vis.Vision(region=vis.game_screen,
                       needle='./needles/bank/deposit-inventory.png',
                       loop_num=3).click_needle()
            misc.sleep_rand(500, 1000)
            misc.wait_rand(20, 100, 10000)
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
        # Withdraw raw food from bank.
        # Conf is higher than default because raw food looks very
        #   similar to cooked food.
        raw_food_withdraw = vis.Vision(region=vis.game_screen,
                                       needle=item_bank,
                                       loop_num=3, conf=0.98).click_needle()
        if raw_food_withdraw is False:
            raise Exception('Cannot find raw food in bank!')
        # Wait for raw food to appear in inventory
        raw_food_in_inv = vis.Vision(region=vis.inv,
                                     needle=item_inv,
                                     loop_num=30, conf=0.99).wait_for_needle()
        misc.wait_rand(20, 100, 10000)
        if raw_food_in_inv is False:
            raise Exception('Cannot find items in inventory!')


# TODO: Add basic firemaking script that starts at a bank booth and
#   creates 27 fires, all in a straight line, then returns to the booth.

# TODO: Add oak woodcutting script that waits by an oak tree, clicks on
#   it when it appears, and empties inventory when full -- super simple.

# TODO: Possible location for starting a fishing script where the
#  "fishing tiles" don't change much is fly fishing at barbarian village.


script = start.config.get('main', 'script')

if script == 'mining':
    miner(start.config.get(script, 'location'))
    sys.exit(0)

elif script == 'magic':
    spellcaster(start.config.get(script, 'scenario'))
    sys.exit(0)

elif script == 'chef':
    chef(start.config.get(script, 'item'),
         start.config.get(script, 'location'))
    sys.exit(0)

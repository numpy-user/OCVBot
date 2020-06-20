# coding=utf-8
"""
Invokes main bot scripts.

"""
import sys

from ocvbot import skilling, behavior, vision as vis, startup as start


def mining_lumbridge_swamp():
    """
    Script for mining copper in the mine in Lumbridge swamp.

    See "/docs/client-configuration/" for the required client
    configuration settings.

    """
    while True:
        # Ensure the client is logged in before starting.
        client_status = vis.orient()
        if client_status[0] == 'logged_out':
            behavior.login_full()

        skilling.miner(
            rocks=[('./needles/game-screen/lumbridge-mine/east-full.png',
                    './needles/game-screen/lumbridge-mine/east-empty.png'),
                   ('./needles/game-screen/lumbridge-mine/south-full.png',
                    './needles/game-screen/lumbridge-mine/south-empty.png')],
            ore='./needles/items/copper-ore.png',
            ore_type='copper', drop_ore=False)

        # Roll for randomized actions when the script returns.
        behavior.human_behavior_rand(chance=100)
        behavior.logout_rand_range()


def mining_varrock_east():
    """
    Script for mining iron in the eastern Varrock mine.

    See "/docs/client-configuration/" for the required client
    configuration settings.

    """
    while True:
        # Ensure the client is logged in.
        client_status = vis.orient()
        if client_status[0] == 'logged_out':
            behavior.login_full()
        skilling.miner(
            rocks=[('./needles/game-screen/varrock-east-mine/north-full2.png',
                    './needles/game-screen/varrock-east-mine/north-empty.png'),
                   ('./needles/game-screen/varrock-east-mine/west-full.png',
                    './needles/game-screen/varrock-east-mine/west-empty.png')],
            ore='./needles/items/iron-ore.png',
            ore_type='iron',
            drop_ore=start.config_file['drop_ore'])

        # Roll for randomized actions when the script returns.
        behavior.logout_rand_range()


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
        spell = './needles/buttons/curse.png'
        target = './needles/game-screen/monk-of-zamorak.png'
        haystack = './haystacks/varrock-castle.png'
        for _ in range(10000):
            skilling.cast_spell(spell, target, haystack)

    else:
        raise Exception('Scenario not supported!')


# TODO: Add basic firemaking script that starts at a bank booth and
#   creates 27 fires, all in a straight line, then returns to the booth.

# TODO: Add oak woodcutting script that waits by an oak tree, clicks on
#   it when it appears, and empties inventory when full -- super simple.

# TODO: Possible location for starting a fishing script where the
#  "fishing tiles" don't change much is fly fishing at barbarian village.


if start.config_file['script'] == '1':
    mining_lumbridge_swamp()
    sys.exit(0)
elif start.config_file['script'] == '2':
    mining_varrock_east()
    sys.exit(0)
elif start.config_file['script'] == '3':
    spellcaster('curse-varrock-castle')
    sys.exit(0)

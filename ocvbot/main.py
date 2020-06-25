# coding=utf-8
"""
Invokes main bot scripts.

"""
import sys

from ocvbot import skills, behavior, vision as vis, startup as start


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
    haystack_map = './haystacks/' + location + '.png'
    item_inv = './needles/items/' + item + '_inv.png'
    item_bank = './needles/items/' + item + '_bank.png'

    if location == 'al-kharid':
        bank_coords = [((75, 128), 1, (4, 4), (5, 10))]
        range_coords = []
        heat_source = './needles/game_screen/'

    for _ in range(1000):
        # assumes starting location is the bank
        behavior.travel(range_coords, haystack_map)
        items_cooked = skills.Cooking(item_inv, item_bank, heat_source).chef
        behavior.travel(bank_coords, haystack_map)
        # Deposit cooked inventory.
        behavior.open_bank('west')
        vis.Vision(region=vis.game_screen,
                   needle='./needles/bank/deposit-all.png',
                   loop_num=3).click_needle()
        # Withdraw raw items from bank.
        vis.Vision(region=vis.game_screen,
                   needle='./needles/items/' + item + 'bank.png',
                   loop_num=3).click_needle()


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

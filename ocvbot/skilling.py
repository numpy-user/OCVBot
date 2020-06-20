# coding=UTF-8
"""
Contains skilling-related functions.

"""
import logging as log
import time

from ocvbot import behavior, vision as vis, misc, startup as start


def spellcast(scenario):
    if scenario == 'curse-varrock-castle':
        spell = './needles/buttons/curse.png'
        target = './needles/game-screen/monk-of-zamorak.png'
        haystack = './haystacks/varrock-castle.png'
    else:
        raise Exception('Scenario not supported!')

    behavior.open_side_stone('spellbook')

    # Make sure character is in right spot.
    behavior.travel([((75, 128), 1, (4, 4), (5, 10))], haystack)

    for _ in range(10000):
        # Look for spell.
        spell_needle = vis.Vision(ltwh=vis.inv, loop_num=1, needle=spell) \
            .click_image(sleep_range=(10, 500, 10, 500,), move_duration_range=(10, 1000))
        if spell_needle is True:
            # Look for target.
            for _ in range(5):
                target_needle = vis.Vision(needle=target, ltwh=vis.game_screen, loop_num=1, conf=0.75) \
                    .click_image(sleep_range=(10, 500, 10, 500,), move_duration_range=(10, 1000))
                if target_needle is True:
                    break
                else:
                    # If target cannot be found, check to see if character
                    #   moved accidentally.
                    # Click the spell again to de-activate it.
                    vis.Vision(ltwh=vis.inv, loop_num=1, needle=spell) \
                        .click_image(sleep_range=(10, 500, 10, 500,), move_duration_range=(10, 1000))
                    behavior.travel([((75, 128), 1, (4, 4), (5, 10))], haystack)
            else:
                log.critical('Could not find %s target! Logging out in 10 seconds!', target)
                time.sleep(10)
                behavior.logout()
        else:
            log.critical('Could not find %s spell! Logging out in 10 seconds!', spell)
            time.sleep(10)
            behavior.logout()

        # Wait for spell to be cast.
        misc.sleep_rand(900, 1800)
        # Roll for random wait.
        misc.wait_rand(chance=200, wait_min=10000, wait_max=60000)
        # Roll for logout after the configured period of time.
        behavior.logout_rand_range()

    log.critical('Out of iterations! Logging out in 10 seconds!')
    time.sleep(10)
    behavior.logout()


def miner(rocks, ore, ore_type, drop_ore):
    """
    A mining function.

    This function alternates mining among the rocks that were provided
    (it can mine one rock, two rocks, or many rocks at once).
    All rocks must be of the same ore type. All mined ore, gems, and
    clue geodes are dropped by default when the inventory is full.

    Args:
        rocks (list): A list containing an arbitrary number of 2-tuples.
                       Each tuple must contain two filepaths:
                       The first filepath must be a needle of the
                       rock in its "full" state. The second filepath
                       must be a needle of the same rock in its "empty"
                       state.
        ore (file): Filepath to a needle of the item icon of the ore
                    being mined, as it appears in the player's
                    inventory.
        ore_type (str): The type of ore being mined, used for generating
                        stats. Available options are: "copper", "iron"
        drop_ore (bool): Whether to drop the ore or bank it. Setting
                         this to 'False' only works for Varrock East
                         bank.

    Raises:
        Raises a runtime error if the player's inventory is full but
        the function can't find any ore in the player's inventory to
        drop.

    """
    gems = ['./needles/items/uncut-sapphire.png',
            './needles/items/uncut-emerald.png',
            './needles/items/uncut-ruby.png',
            './needles/items/uncut-diamond.png',
            './needles/items/clue-geode.png']

    # Vision objects have to be imported within functions because the
    #   init_vision() function has to run before the objects get valid
    #   values.

    # TODO: count the number of items in the inventory to make sure
    #   the function never receives an "inventory is already full" message

    # Make sure inventory is selected.
    behavior.open_side_stone('inventory')

    for tries in range(100):

        # Confirm player is in the correct mining spot. This is also
        #   used to re-adjust the player if a mis-click moves the player
        #   out of position.
        # Applies to Varrock East mine only.
        behavior.travel([((240, 399), 1, (4, 4), (5, 10))], './haystacks/varrock-east-mine.png')

        for rock_needle in rocks:
            # Unpack each tuple in the rocks[] list to obtain the "full"
            #   and "empty" versions of each ore.
            (full_rock_needle, empty_rock_needle) = rock_needle

            log.debug('Searching for ore %s...', tries)

            # If current rock is full, begin mining it.
            # Move the mouse away from the rock so it doesn't
            #   interfere with matching the needle.
            rock_full = vis.Vision(ltwh=vis.game_screen, loop_num=1, needle=full_rock_needle, conf=0.8) \
                .click_image(sleep_range=(0, 100, 0, 100,), move_duration_range=(0, 500), move_away=True)
            if rock_full is True:
                log.info('Waiting for mining to start.')

                # Small chance to do nothing for a short while.
                misc.wait_rand(chance=100, wait_min=10000, wait_max=60000)

                # Once the rock has been clicked on, wait for mining to
                #   start by monitoring chat.
                mining_started = vis.Vision(ltwh=vis.chat_menu_recent, loop_num=5, conf=0.9,
                                            needle='./needles/chat-menu/mining-started.png',
                                            loop_sleep_range=(100, 200)).wait_for_image()

                # If mining hasn't started after looping has finished,
                #   check to see if the inventory is full.
                if mining_started is False:
                    log.debug('Timed out waiting for mining to start.')

                    inv_full = vis.Vision(ltwh=vis.chat_menu, loop_num=1,
                                          needle='./needles/chat-menu/'
                                                 'mining-inventory-full.png').wait_for_image()

                    # If the inventory is full, empty the ore and
                    #   return.
                    if inv_full is True:
                        log.info('Inventory is full.')
                        if drop_ore is True:
                            fdrop_ore(ore)
                        else:
                            behavior.open_side_stone('inventory')
                            # Bank from mining spot.
                            behavior.travel([((253, 181), 5, (35, 35), (1, 6)),
                                            ((112, 158), 5, (20, 20), (1, 6)),
                                            ((108, 194), 1, (10, 4), (3, 8))],
                                            './haystacks/varrock-east-mine.png')
                            behavior.open_bank('south')
                            vis.Vision(ltwh=vis.inv, needle=ore).click_image()
                            for gem in gems:
                                vis.Vision(ltwh=vis.inv, needle=gem, loop_num=1).click_image()
                            misc.sleep_rand(500, 3000)
                            # Mining spot from bank.
                            behavior.travel([((240, 161), 5, (35, 35), (1, 6)),
                                            ((262, 365), 5, (25, 25), (1, 6)),
                                            ((240, 399), 1, (4, 4), (3, 8))],
                                            './haystacks/varrock-east-mine.png')
                            misc.sleep_rand(300, 800)
                        elapsed_time = misc.run_duration(human_readable=True)
                        log.info('Script has been running for %s (HH:MM:SS)',
                                 elapsed_time)
                        return
                    return

                log.info('Mining started.')

                # Wait until the rock is empty by waiting for the
                #   "empty" version of the rock_needle tuple.
                rock_empty = vis.Vision(ltwh=vis.game_screen, loop_num=35,
                                        conf=0.85, needle=empty_rock_needle,
                                        loop_sleep_range=(100, 200)).wait_for_image()

                if rock_empty is True:
                    log.info('Rock is empty.')
                    log.debug('%s empty.', rock_needle)
                    behavior.human_behavior_rand(chance=100)
                else:
                    log.info('Timed out waiting for mining to finish.')
    return


def fdrop_ore(ore):
    """
    Drops ore and optionally gems in inventory.

    Returns:

    """

    # Create tuples of whether or not to drop the item and the item's path.
    drop_sapphire = (start.config_file['drop_sapphire'],
                     './needles/items/uncut-sapphire.png')
    drop_emerald = (start.config_file['drop_emerald'],
                    './needles/items/uncut-emerald.png')
    drop_ruby = (start.config_file['drop_ruby'],
                 './needles/items/uncut-ruby.png')
    drop_diamond = (start.config_file['drop_diamond'],
                    './needles/items/uncut-diamond.png')
    drop_clue_geode = (start.config_file['drop_clue_geode'],
                       './needles/items/clue-geode.png')
    ore_dropped = behavior.drop_item(item=ore)
    if ore_dropped is False:
        behavior.logout()
        # This runtime error will occur if the
        #   player's inventory is full, but they
        #   don't have any ore to drop.
        raise RuntimeError("Could not find ore to drop!")

    # Iterate through the other items that could
    #   be dropped. If any of them is true, drop that item.
    # The for loop is iterating over a tuple of tuples.
    for item in (drop_sapphire, drop_emerald, drop_ruby,
                 drop_diamond, drop_clue_geode):
        # Unpack the tuple
        (drop_item, path) = item
        if drop_item is True:
            behavior.drop_item(item=str(path), track=False)

import logging as log

from ocvbot import behavior, vision as vis, misc, startup as start


def miner_double_drop(rock1, rock2, ore, ore_type):
    """
    A 2-rock drop mining script.

    This function alternates mining between two different rocks that
    contain the same type of ore. All mined ore, gems, and clue geodes
    are dropped by default when the inventory becomes full.

    Args:
        rock1 (tuple): Tuple containing two filepaths: The first file
                       must be a needle showing the first rock is
                       full. The second file must be a needle showing
                       the first rock is empty.
        rock2 (tuple): Tuple containing two filepaths: The first file
                       must be a needle showing the second rock is
                       full. The second file must be a needle showing
                       the second rock is empty.
        ore (file): Filepath to a needle of the item icon of the ore
                    being mined, as it appears in the player's
                    inventory.
        ore_type (str): The type of ore being mined, used for generating
                        stats. Available options are: "copper", "iron"

    Raises:
        Raises a runtime error if the player's inventory is full, but
        the function can't find any ore in the player's inventory to
        drop.
    """

    # Vision objects have to be imported within functions because the
    #   init_vision() function has to run before the objects get valid
    #   values.

    # Create tuples of whether or not to drop the item and the item's path.
    drop_sapphire = (start.config_file['drop_sapphire'],
                     './needles/items/uncit-sapphire.png')
    drop_emerald = (start.config_file['drop_emerald'],
                    './needles/items/uncit-emerald.png')
    drop_ruby = (start.config_file['drop_ruby'],
                 './needles/items/uncit-ruby.png')
    drop_diamond = (start.config_file['drop_diamond'],
                    './needles/items/uncit-diamond.png')
    drop_clue_geode = (start.config_file['drop_clue_geode'],
                       './needles/items/clue-geode.png')

    for attempts in range(1, 100):

        # TODO: allow rotating through an arbitrary number of rocks
        for rock_needle in (rock1, rock2):
            # Unpack the "rock_needle" tuple to obtain "full" and
            #   "empty" versions of each needle.
            (full_rock_needle, empty_rock_needle) = rock_needle

            log.debug('Searching for ore ' + str(attempts) + '...')

            # If current rock is full, begin mining it.
            # Move the mouse away from the rock so it doesn't
            #   interfere with matching the needle.
            rock_full = vis.Vision(ltwh=vis.game_screen, loop_num=1,
                                   needle=full_rock_needle, conf=0.8) \
                .click_image(sleep_range=(0, 100, 0, 1), move_away=True)
            if rock_full is True:
                log.info('Waiting for mining to start.')

                # Small chance to do nothing for a short while.
                misc.wait_rand(chance=100, wait_min=10000, wait_max=60000)

                # Once the rock has been clicked on, wait for mining to
                #   start by monitoring chat.
                mining_started = vis.Vision(ltwh=vis.chat_menu_recent,
                                            loop_num=5, conf=0.9,
                                            needle='./needles/chat-menu/'
                                                   'mining-started.png',
                                            loop_sleep_range=(100, 200)) \
                    .wait_for_image()

                # If mining hasn't started after looping has finished,
                #   check to see if the inventory is full.
                if mining_started is False:
                    log.debug('Timed out waiting for mining to start.')

                    inv_full = vis.Vision(ltwh=vis.chat_menu,
                                          loop_num=1,
                                          needle='./needles/chat-menu/'
                                                 'mining-inventory-full.png') \
                        .wait_for_image()

                    # If the inventory is full, empty the ore and
                    #   return.
                    if inv_full is True:
                        log.info('Inventory is full.')
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

                        elapsed_time = misc.run_duration(human_readable=True)
                        log.info(
                            'Script has been running for  ' + str(elapsed_time)
                            + ' (HH:MM:SS)')
                        return
                    return

                log.info('Mining started.')

                # Wait until the rock is empty by waiting for the
                #   "empty" version of the rock_needle tuple.
                rock_empty = vis.Vision(ltwh=vis.chat_menu,
                                        loop_num=100, conf=0.85,
                                        needle=empty_rock_needle,
                                        loop_sleep_range=(100, 200)) \
                    .wait_for_image()

                if rock_empty is True:
                    log.info('Rock is empty.')
                    log.debug(str(rock_needle) + ' empty.')
                else:
                    log.info('Timed out waiting for mining to finish.')
    return

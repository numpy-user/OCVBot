# coding=UTF-8
"""
Contains all functions related to training skills.

"""
import logging as log

from ocvbot import behavior, vision as vis, misc, startup as start, input


def wait_for_level_up(wait_time):
    """
    Waits the specified number of seconds for a level-up message to
    appear in the chat menu.

    Args:
        wait_time: Approximately the number of seconds to wait for a
                   level-up message to appear. Checks for a level-up
                   message about once every second.

    Returns:
        If a level-up message appears, returns True.
        Returns False otherwise.

    """
    log.info('Checking for level-up')
    level_up = vis.Vision(region=vis.chat_menu,
                          needle='./needles/chat-menu/level-up.png',
                          loop_num=wait_time,
                          loop_sleep_range=(900, 1100)).wait_for_needle()
    if level_up is True:
        return True
    else:
        return False


class Cooking:
    """
    Class for all cooking-related functions.

    """
    def __init__(self, item_inv, item_bank, heat_source, logout=False):
        self.item_inv = item_inv
        self.item_bank = item_bank
        self.heat_source = heat_source
        self.logout = logout

    def cook_item(self):
        """
        Cooks all instances of the given item in the player's inventory.

        Returns:

        """
        # Select the raw food in the inventory.
        # Confidence must be higher than normal since raw food is very
        #   similar in appearance to cooked food.
        behavior.open_side_stone('inventory')
        item_selected = vis.Vision(region=vis.client,
                                   needle=self.item_inv,
                                   loop_num=3,
                                   conf=0.99).click_needle()
        if item_selected is False:
            log.error('Unable to find item!')
            return False

        # Select the range or fire.
        heat_source_selected = vis.Vision(region=vis.game_screen,
                                          needle=self.heat_source,
                                          loop_num=3,
                                          loop_sleep_range=(500, 1000),
                                          conf=0.85).click_needle()
        if heat_source_selected is False:
            log.error('Unable to find heat source!')
            return False
        misc.sleep_rand_roll(chance_range=(15, 35), sleep_range=(1000, 10000))

        # Wait for the "how many of this item do you want to cook" chat
        #   menu.
        do_x_screen = vis.Vision(region=vis.chat_menu,
                                 needle='./needles/chat-menu/do-x.png',
                                 loop_num=30,
                                 loop_sleep_range=(500, 1000)).wait_for_needle()
        if do_x_screen is False:
            log.error('Timed out waiting for "Make X" screen!')
            return False

        # Begin cooking food.
        input.Keyboard().keypress(key='space')
        misc.sleep_rand(1000, 3000)

        # Wait for either a level-up or for the player to stop cooking.
        # To determine when the player is done cooking, look for the
        #   bright red Staff of Water orb. The player must have this item
        #   equipped.
        for _ in range(1, 60):
            misc.sleep_rand(1000, 3000)
            level_up = wait_for_level_up(1)
            if level_up is True:
                self.cook_item()
            cooking_done = vis.Vision(region=vis.game_screen,
                                      needle='./needles/game-screen/staff-of-water-top.png',
                                      conf=0.9,
                                      loop_num=1).wait_for_needle()
            if cooking_done is True:
                break

        misc.sleep_rand_roll(chance_range=(15, 35), sleep_range=(20000, 120000))
        return True


class Magic:
    """
    Class for all activities related to the Magic skill.

    Args:
        spell (file): Filepath to the spell to cast as it appears in the
                      player's spellbook (NOT greyed-out).
        target (file): Filepath to an image of the target to cast the
                       spell on, as it appears in the game world.
        conf (float): Confidence required to match the target.
        haystack (tuple): The 4-tuple to use when searching for the
                          target. This will either be "vis.inv" or
                          "vis.game_screen".
        logout (bool): Whether or not to logout once out of runes or the
                       target cannot be found, default is False.

    """
    def __init__(self, spell, target, conf, haystack,
                 move_duration_range=(10, 1000), logout=False):
        self.spell = spell
        self.haystack = haystack
        self.logout = logout
        self.target = target
        self.conf = conf
        self.move_duration_range = move_duration_range

    def _select_spell(self):
        """
        Activates the desired spell.

        Returns:
            Returns True if spell was activated, False if otherwise.

        """
        for _ in range(1, 5):
            spell_available = vis.Vision(needle=self.spell, region=vis.inv,
                                         loop_num=30) \
                .click_needle(sleep_range=(50, 800, 50, 800,),
                              move_duration_range=(10, 1000))
            if spell_available is False:
                behavior.open_side_stone('spellbook')
                misc.sleep_rand(100, 300)
            else:
                return True
        return False

    def _select_target(self):
        """
        Attempt to find the target to cast the spell on.

        Returns:
            Returns True if target was found and selected, False if
            otherwise.

        """
        for _ in range(1, 5):
            target = vis.Vision(needle=self.target, region=self.haystack,
                                loop_num=10, conf=self.conf) \
                .click_needle(sleep_range=(10, 500, 10, 500,),
                              move_duration_range=self.move_duration_range)

            if target is False:
                if vis.orient()[0] == 'logged_out':
                    behavior.login_full()
                misc.sleep_rand(1000, 3000)
            else:
                return True
        return False

    def cast_spell(self):
        """
        Casts a spell at a target. Optionally can require the player to be
        in a specific location.

        Returns:
            Returns True if spell was cast, false if otherwise.

        """
        spell_selected = self._select_spell()
        if spell_selected is False:
            if self.logout is True:
                log.critical('Out of runes! Logging out in 10-20 seconds!')
                misc.sleep_rand(10000, 20000)
                behavior.logout()
            else:
                log.critical('All done!')
                return False

        target_selected = self._select_target()
        if target_selected is False:
            if self.logout is True:
                log.critical('Unable to find target! Logging out in 10-20 seconds!')
                misc.sleep_rand(10000, 20000)
                behavior.logout()
            else:
                log.critical('All done!')
                return False

        # Wait for spell to be cast.
        misc.sleep_rand(int(start.config.get('magic', 'min_cast_delay')),
                        int(start.config.get('magic', 'max_cast_delay')))
        # Roll for random wait.
        misc.sleep_rand_roll(chance_range=(100, 400))

        if self.logout is True:
            # Roll for logout after the configured period of time.
            behavior.logout_break_range()

        return True


def mine(rocks, ore, ore_type, drop_ore, position=None, conf=(0.8, 0.85)):
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

    Returns:
        Returns True if a full inventory of ore was mined and banked or
        dropped, or if script timed out looking for ore.

    """
    gems = ['./needles/items/uncut-sapphire.png',
            './needles/items/uncut-emerald.png',
            './needles/items/uncut-ruby.png',
            './needles/items/uncut-diamond.png',
            './needles/items/clue-geode.png']

    # Vision objects have to be imported within functions because the
    #   init_vision() function has to run before the objects get valid
    #   values.

    # TODO: Count the number of items in the inventory to make sure
    #   the function never receives an "inventory is already full" message.

    # TODO: Refactor a mine_rock() function out of this one.

    # Make sure inventory is selected.
    behavior.open_side_stone('inventory')

    for tries in range(100):

        # Confirm player is in the correct mining spot. This is also
        #   used to re-adjust the player if a mis-click moves the player
        #   out of position.
        # Applies to Varrock East mine only.
        # TODO: These coords should be passed in from
        #   main.py, not hard-coded.

        if position is not None:
            behavior.travel(position[0], position[1])

        for rock_needle in rocks:
            # Unpack each tuple in the rocks[] list to obtain the "full"
            #   and "empty" versions of each ore.
            (full_rock_needle, empty_rock_needle) = rock_needle

            log.debug('Searching for ore %s...', tries)

            # If current rock is full, begin mining it.
            # Move the mouse away from the rock so it doesn't
            #   interfere with matching the needle.
            rock_full = vis.Vision(region=vis.game_screen, loop_num=1,
                                   needle=full_rock_needle, conf=conf[0]) \
                .click_needle(sleep_range=(0, 100, 0, 100,),
                              move_duration_range=(0, 500), move_away=True)
            if rock_full is True:
                log.info('Waiting for mining to start.')

                # Small chance to do nothing for a short while.
                misc.sleep_rand_roll(chance_range=(1, 200))

                # Once the rock has been clicked on, wait for mining to
                #   start by monitoring chat.
                mining_started = vis.Vision(region=vis.chat_menu_recent, loop_num=5, conf=0.9,
                                            needle='./needles/chat-menu/mining-started.png',
                                            loop_sleep_range=(100, 200)).wait_for_needle()

                # If mining hasn't started after looping has finished,
                #   check to see if the inventory is full.
                if mining_started is False:
                    log.debug('Timed out waiting for mining to start.')

                    inv_full = vis.Vision(region=vis.chat_menu, loop_num=1,
                                          needle='./needles/chat-menu/mining-inventory-full.png'). \
                        wait_for_needle()

                    # If the inventory is full, empty the ore and
                    #   return.
                    if inv_full is True:
                        log.info('Inventory is full.')
                        if drop_ore is True:
                            fdrop_ore(ore)
                        else:
                            behavior.open_side_stone('inventory')
                            # Bank from mining spot.
                            # TODO: These coords should be passed in from
                            #   main.py, not hard-coded.
                            behavior.travel([((253, 181), 5, (35, 35), (1, 6)),
                                             ((112, 158), 5, (20, 20), (1, 6)),
                                             ((108, 194), 1, (10, 4), (3, 8))],
                                            './haystacks/varrock-east-mine.png')
                            behavior.open_bank('south')
                            vis.Vision(region=vis.inv, needle=ore).click_needle()
                            for gem in gems:
                                vis.Vision(region=vis.inv, needle=gem, loop_num=1).click_needle()
                            # TODO: Instead of waiting a hard-coded period of time,
                            #   wait until the item can no longer be found in the
                            #   player's inventory.
                            misc.sleep_rand(500, 3000)
                            # Mining spot from bank.
                            behavior.travel([((240, 161), 5, (35, 35), (1, 6)),
                                             ((262, 365), 5, (25, 25), (1, 6)),
                                             ((240, 399), 1, (4, 4), (3, 8))],
                                            './haystacks/varrock-east-mine.png')
                            misc.sleep_rand(300, 800)
                        elapsed_time = misc.session_duration(human_readable=True)
                        log.info('Script has been running for %s (HH:MM:SS)', elapsed_time)
                        return True
                    return True

                log.info('Mining started.')

                # Wait until the rock is empty by waiting for the
                #   "empty" version of the rock_needle tuple.
                rock_empty = vis.Vision(region=vis.game_screen, loop_num=35,
                                        conf=conf[1], needle=empty_rock_needle,
                                        loop_sleep_range=(100, 200)).wait_for_needle()

                if rock_empty is True:
                    log.info('Rock is empty.')
                    log.debug('%s empty.', rock_needle)
                    behavior.human_behavior_rand(chance=100)
                else:
                    log.info('Timed out waiting for mining to finish.')
    return True


def fdrop_ore(ore):
    """
    Drops ore and optionally gems in inventory.

    Returns:

    """

    # Create tuples of whether or not to drop the item and the item's path.
    drop_sapphire = (start.config.get('mining', 'drop_sapphire'), './needles/items/uncut-sapphire.png')
    drop_emerald = (start.config.get('mining', 'drop_emerald'), './needles/items/uncut-emerald.png')
    drop_ruby = (start.config.get('mining', 'drop_ruby'), './needles/items/uncut-ruby.png')
    drop_diamond = (start.config.get('mining', 'drop_diamond'), './needles/items/uncut-diamond.png')
    drop_clue_geode = (start.config.get('mining', 'drop_clue_geode'), './needles/items/clue-geode.png')
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
            return True

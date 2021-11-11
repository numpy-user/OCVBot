# coding=UTF-8
"""
Contains all functions related to training skills.

"""
import logging as log

from ocvbot import behavior
from ocvbot import inputs
from ocvbot import misc
from ocvbot import startup as start
from ocvbot import vision as vis


def wait_for_level_up(wait_time: int):
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
    log.debug("Checking for level-up")
    level_up = vis.Vision(
        region=vis.CHAT_MENU,
        needle="./needles/chat-menu/level-up.png",
        loop_num=wait_time,
        loop_sleep_range=(900, 1100),
    ).wait_for_needle()

    if level_up is True:
        return True
    return False


class Cooking:
    """
    Class for all functions related to training the Cooking skill.

    Args:
        item_inv (file): Filepath to the food to cook as it appears in
                         the player's inventory. This is the raw version.
        item_bank (file): Filepath to the food to cook as it appears in
                          the players' bank. Make sure this image doesn't
                          include the stack count if this item is stacked.
        heat_source (file): Filepath to the fire or range to cook the
                            item with as it appears in the game world.

    """

    def __init__(self, item_inv: str, item_bank: str, heat_source: str):
        self.item_inv = item_inv
        self.item_bank = item_bank
        self.heat_source = heat_source

    def cook_item(self) -> bool:
        """
        Cooks all instances of the given food in the player's inventory.

        Returns:
            Returns True if all items were cooked. Returns False in all
            other cases.

        """
        log.info("Attempting to cook food.")
        behavior.open_side_stone("inventory")
        # Select the raw food in the inventory.
        # Confidence must be higher than normal since raw food is very
        #   similar in appearance to its cooked version.
        item_selected = vis.Vision(
            region=vis.CLIENT, needle=self.item_inv, loop_num=3, conf=0.99
        ).click_needle()
        if item_selected is False:
            log.error("Unable to find item %s!", self.item_inv)
            return False

        # Select the range or fire.
        heat_source_selected = vis.Vision(
            region=vis.GAME_SCREEN,
            needle=self.heat_source,
            loop_num=3,
            loop_sleep_range=(500, 1000),
            conf=0.80,
        ).click_needle()
        if heat_source_selected is False:
            log.error("Unable to find heat source %s!", self.heat_source)
            return False

        # Wait for the "how many of this item do you want to cook" chat
        #   menu to appear.
        do_x_screen = vis.Vision(
            region=vis.CHAT_MENU,
            needle="./needles/chat-menu/do-x.png",
            loop_num=30,
            loop_sleep_range=(500, 1000),
        ).wait_for_needle()
        if do_x_screen is False:
            log.error('Timed out waiting for "Make X" screen!')
            return False

        # Begin cooking food.
        inputs.Keyboard().keypress(key="space")
        misc.sleep_rand(3000, 5000)

        # Wait for either a level-up or for the player to stop cooking.
        # To determine when the player is done cooking, look for the
        #   bright blue "Staff of Water" orb to re-appear (equipped weapons
        #   disappear while cooking food). The player must have this item
        #   equipped.
        for _ in range(1, 60):
            misc.sleep_rand(1000, 3000)
            level_up = wait_for_level_up(1)
            # If the player levels-up while cooking, restart cooking.
            if level_up is True:
                self.cook_item()
            cooking_done = vis.Vision(
                region=vis.GAME_SCREEN,
                needle="./needles/game-screen/staff-of-water-top.png",
                conf=0.9,
                loop_num=1,
            ).wait_for_needle()
            if cooking_done is True:
                log.info("Cooking is done.")
                break
        return True


class Magic:
    """
    Class for all activities related to training the Magic skill.

    Args:
        spell (file): Filepath to the spell to cast as it appears in the
                      player's spellbook (NOT greyed-out).
        target (file): Filepath to the target to cast the spell on as it
                       appears in the game world. If the spell is a non-
                       combat spell, this would be an item as it appears
                       in the player's inventory.
        conf (float): Confidence required to match the target.
        region (tuple): The coordinate region to use when searching for
                        the target. This will either be "vis.inv" or
                        "vis.game_screen".
        inventory (bool): Whether the spell is being cast on an item in
                          the player's inventory (as opposed to a monster),
                          default is False.
        move_duration_range (tuple): A 2-tuple of the minimum and maximum
                                     number of miliseconds the mouse cursor
                                     will take while moving to the spell
                                     icon and the target, default is
                                     (10, 1000).
    """

    def __init__(
        self,
        spell: str,
        target: str,
        conf: float,
        region: tuple[int, int, int, int],
        inventory: bool = False,
        move_duration_range: tuple[int, int] = (10, 1000),
    ):
        self.spell = spell
        self.target = target
        self.conf = conf
        self.region = region
        self.inventory = inventory
        self.move_duration_range = move_duration_range

    def _select_spell(self) -> None:
        """
        Activate the desired spell.

        Raises:
            Raises an exception if the spell could not be found.

        """
        for _ in range(5):
            spell_available = vis.Vision(
                needle=self.spell, region=vis.INV, loop_num=30
            ).click_needle(
                sleep_range=(
                    50,
                    800,
                    50,
                    800,
                ),
                move_duration_range=self.move_duration_range,
            )
            if spell_available is False:
                behavior.open_side_stone("spellbook")
            else:
                return
        raise Exception("Could not select spell!")

    def _select_target(self) -> None:
        """
        Attempt to find the target to cast the spell on. Can be either a
        monster in the game world or an item in the inventory.

        Raises:
            Raises an exception if the target could not be found.

        """
        for _ in range(5):
            target = vis.Vision(
                needle=self.target, region=self.region, loop_num=5, conf=self.conf
            ).click_needle(
                sleep_range=(
                    10,
                    500,
                    10,
                    500,
                ),
                move_duration_range=self.move_duration_range,
            )
            if target is False:
                # Make sure the inventory is active when casting on items.
                if self.inventory is True:
                    behavior.open_side_stone("inventory")
            else:
                return
        raise Exception("Could not find target!")

    def cast_spell(self) -> None:
        """
        Cast a spell at a target.

        Returns:
            Returns once spell has been cast.

        """
        self._select_spell()
        self._select_target()

        # Wait for spell to be cast.
        misc.sleep_rand(
            int(start.config["magic"]["min_cast_delay"]),
            int(start.config["magic"]["max_cast_delay"]),
        )


class Mining:
    """
    Class for all activities related to training the Mining skill.

    Args:
        rocks (list): A list containing an arbitrary number of 2-tuples. Each
                      tuple must contain two filepaths: The first filepath
                      must be a needle of the rock in its "full" state. The
                      second filepath must be a needle of the same rock in its
                      "empty" state.
        ore (file): Filepath to a needle of the item icon of the ore
                    being mined, as it appears in the player's
                    inventory.

        drop_sapphire (bool): Whether to drop mined sapphires. Ignored if
                              banking is enabled.
        drop_emerald (bool): Whether to drop mined emeralds. Ignore if
                             banking is enabled.
        drop_ruby (bool): Whether to drop mined rubies. Ignore if
                          banking is enabled.
        drop_diamond (bool): Whether to drop mined diamonds. Ignore if
                             banking is enabled.
        drop_clue_geode (bool): Whether to drop mined clue geodes. Ignore if
                                banking is enabled.

    Example:
            skills.Mining(
                rocks=[
                    ("./needles/game-screen/camdozaal-mine/west-full",
                     "./needles/game-screen/camdozaal-mine/west-empty"),
                    ("./needles/game-screen/camdozaal-mine/east-full",
                     "./needles/game-screen/camdozaal-mine/east-empty"),
                ],
                ore="./needles/items/barronite-deposit.png",
                drop_sapphire=True
                drop_emerald=True
                drop_ruby=True
                drop_diamond=False
                drop_clue_geode=False
            )
    """

    def __init__(
        self,
        rocks: list,
        ore: str,
        drop_sapphire: bool,
        drop_emerald: bool,
        drop_ruby: bool,
        drop_diamond: bool,
        drop_clue_geode: bool,
        conf: float = 0.85,
    ):
        self.rocks = rocks
        self.ore = ore
        self.drop_sapphire = drop_sapphire
        self.drop_emerald = drop_emerald
        self.drop_ruby = drop_ruby
        self.drop_diamond = drop_diamond
        self.drop_clue_geode = drop_clue_geode
        self.conf = conf

    def _is_inventory_full(self) -> bool:
        """
        Helper function to determine if the player's inventory is full. Looks
        for a "your inventory is too full to hold any more resources" chat
        message.

        Returns:
          Returns True if the player's inventory is full,
          returns False otherwise.
        """
        log.debug("Checking for full inventory.")
        inventory_full = vis.Vision(
            region=vis.CHAT_MENU,
            loop_num=3,
            needle="./needles/chat-menu/mining-inventory-full.png",
            conf=0.85,
        ).wait_for_needle()
        if inventory_full is True:
            return True
        log.debug("Inventory is not full.")
        return False

    def _mine_rock(self, rock_full, rock_empty) -> None:
        """
        Helper function to mine a given rock until it's been depleted.

        Raises:
          Raises start.RockEmpty if the given rock is already depleted.

          Raises start.InventoryFull if the player's inventory is too full to
          mine the rock.

          Raises start.TimeoutException if it took too long to mine the rock.
        """
        # If rock is full, begin mining it.
        # Move the mouse away from the rock so it doesn't interfere with
        #   matching the needle.
        rock_full_click = vis.Vision(
            region=vis.GAME_SCREEN,
            loop_num=1,
            needle=rock_full,
            conf=self.conf,
        ).click_needle(move_away=True)

        if rock_full_click is False:
            raise start.RockEmpty("Rock is already empty!")

        if self._is_inventory_full() is True:
            raise start.InventoryFull("Inventory is full!")

        # Wait until the rock is empty.
        rock_empty = vis.Vision(
            region=vis.GAME_SCREEN,
            loop_num=50,
            conf=self.conf,
            needle=rock_empty,
            loop_sleep_range=(100, 600),
        ).wait_for_needle()
        if rock_empty is True:
            log.info("Rock has been mined.")
            return
        # If a timeout has occured, check if the inventory is full.
        if self._is_inventory_full() is True:
            raise start.InventoryFull("Inventory is full!")
        raise start.TimeoutException("Timeout waiting for rock to be mined!")

    def mine_multiple_rocks(self) -> None:
        """
        Main function used in the Mining class to mine multiple rocks in
        sequence. This function alternates mining among the rocks that were
        provided. All rocks must be of the same ore type.

        Returns:
            Returns once an attempt has been made to mine all the rocks given.

        Raises:
          Raises start.InventoryFull if the player's inventory is too full to
          mine the rock.

          Raises start.TimeoutException if it took too long to mine the rock.

        """
        for rocks in self.rocks:
            # Unpack each tuple in the rocks[] list to obtain the "full"
            #   and "empty" versions of each ore.
            (rock_full, rock_empty) = rocks
            try:
                self._mine_rock(rock_full, rock_empty)
            except start.RockEmpty:
                pass
            except start.InventoryFull as error:
                raise error
            except start.TimeoutException as error:
                raise error

    def drop_inv_ore(self) -> None:
        """
        Drops mined ore ore and other mined items from inventory.

        Returns:
            Returns if ore and/or other mined items were successfully dropped.

        Raises:
            Raises start.InefficientUseOfInventory when the number of free
            inventory spaces available would result in inefficient or overly
            arduous gameplay.

            Raises Exception if no ore could be found in the inventory to drop.
        """
        # Raise an error if we have <=5 ores in the inventory, as it's very
        #   inefficient to mine with an inventory so small.
        ores_in_inventory = vis.Vision(region=vis.INV, needle=self.ore).count_needles()
        if ores_in_inventory <= 5:
            raise start.InefficientUseOfInventory(
                "Free inventory too small! Must have at least 5 free spaces!"
            )

        ore_dropped = behavior.drop_item(item=self.ore)
        if ore_dropped is False:
            raise Exception("Could not find any ore to drop!")

        # Iterate through the other items that could be dropped. If any of them
        #   is true, drop that item.
        non_ore_items = [
            (
                self.drop_sapphire,
                "./needles/items/uncut-sapphire.png",
            ),
            (
                self.drop_emerald,
                "./needles/items/uncut-emerald.png",
            ),
            (
                self.drop_ruby,
                "./needles/items/uncut-ruby.png",
            ),
            (
                self.drop_diamond,
                "./needles/items/uncut-diamond.png",
            ),
            (
                self.drop_clue_geode,
                "./needles/items/clue-geode.png",
            ),
        ]
        for item in non_ore_items:
            (drop_item_bool, path) = item
            if drop_item_bool is True:
                behavior.drop_item(item=str(path))
                return
        return


class Smithing:
    """
    Class for all functions related to training the Smithing skill.

    Args:
        item_in_menu (file): Filepath to the item to select in the smithing menu.
                             "-bank.png" items can be used here.
        bar_type (file): Filepath to the bar to use, as it appears in the inventory.
        bars_required (int): The number of bars required to smith the desired item.
        anvil (file): Filepath to the anvil to use, as it appears in the game world.
        uncompleted_inv (file): Filepath to the uncompleted inventory needle. We
                                know we're done smithing when this needle can't
                                be found.
    """

    def __init__(
        self, item_in_menu: str, bar_type: str, bars_required: int, anvil: str
    ):
        self.item_in_menu = item_in_menu
        self.bar_type = bar_type
        self.bars_required = bars_required
        self.anvil = anvil

        if self.bars_required > 5:
            raise Exception("The value of bars_required must be <= 5!")

    def click_anvil(self) -> bool:
        """
        Clicks the given anvil.

        Returns:
            Returns True once the smithing menu appears.
        """
        log.info("Attempting to click anvil.")

        anvil_clicked = vis.Vision(
            region=vis.GAME_SCREEN,
            needle=self.anvil,
            loop_num=3,
            loop_sleep_range=(500, 1000),
            conf=0.85,
        ).click_needle()

        if anvil_clicked is False:
            log.error("Unable to find anvil %s!", self.anvil)
            return False

        smith_menu_open = vis.Vision(
            region=vis.CLIENT,
            needle="./needles/buttons/close.png",
            loop_num=30,
        ).wait_for_needle()

        misc.sleep_rand_roll(chance_range=(20, 35), sleep_range=(1000, 6000))

        if smith_menu_open is False:
            log.error("Timed out waiting for smithing menu.")
            return False

        return True

    def smith_items(self) -> bool:
        """
        Smiths an inventory of the given item.

        Returns:
            Returns True once done smithing.
        """
        clicked_anvil = self.click_anvil()
        if clicked_anvil is False:
            log.error("Unable to find anvil %s!", self.anvil)
            return False

        log.info("Attempting to select item to smith.")

        menu_clicked = vis.Vision(
            region=vis.GAME_SCREEN,
            needle=self.item_in_menu,
            loop_num=3,
            loop_sleep_range=(500, 1000),
            conf=0.85,
        ).click_needle()
        if menu_clicked is False:
            log.error("Unable to click menu item %s!", self.item_in_menu)
            return False

        log.info("Smithing...")

        # Wait for either a level-up or for smithing to finish.
        for _ in range(1, 60):
            misc.sleep_rand(1000, 3000)

            # Based the number of bars we need to smith the current item, we'll
            #   end up with a different number of bars leftover.
            if self.bars_required == 5:
                bars_leftover = 2
            elif self.bars_required == 2:
                bars_leftover = 1
            else:
                bars_leftover = 0

            # We're done smithing when the number of bars in our inventory is
            #   equal to bars_leftover.
            bars_remaining = vis.Vision(
                region=vis.INV, needle=self.bar_type, conf=0.9
            ).count_needles()
            if bars_remaining <= bars_leftover:
                log.info("Done smithing.")
                return True

            # If the player levels-up while smithing, restart.
            if wait_for_level_up(1) is True:
                self.smith_items()

        return False

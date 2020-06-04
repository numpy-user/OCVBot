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
        client_status = vis.orient(start.DISPLAY_WIDTH, start.DISPLAY_HEIGHT)
        (client_status, unused_var) = client_status
        if client_status == 'logged_out':
            behavior.login()

        skilling.miner_double_drop(
            rock1=('./needles/game-screen/lumbridge-mine/'
                   'east-full.png',
                   './needles/game-screen/lumbridge-mine/'
                   'east-empty.png'),
            rock2=('./needles/game-screen/lumbridge-mine/'
                   'south-full.png',
                   './needles/game-screen/lumbridge-mine/'
                   'south-empty.png'),
            ore='./needles/items/copper-ore.png',
            ore_type='copper')

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
        client_status = vis.orient(start.DISPLAY_WIDTH, start.DISPLAY_HEIGHT)
        (client_status, unused_var) = client_status
        if client_status == 'logged_out':
            behavior.login(),
        skilling.miner_double_drop(
            rock1=('./needles/game-screen/varrock-east-mine/'
                   'north-full2.png',
                   './needles/game-screen/varrock-east-mine/'
                   'north-empty.png'),
            rock2=('./needles/game-screen/varrock-east-mine/'
                   'west-full.png',
                   './needles/game-screen/varrock-east-mine/'
                   'west-empty.png'),
            ore='./needles/items/iron-ore.png',
            ore_type='iron')

        # Roll for randomized actions when the script returns.
        behavior.human_behavior_rand(chance=100)
        behavior.logout_rand_range()


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

'''
def cannonball_smelter():

    # Click on the bank booth.
    bank_booth = vis.Vision(needle='./bank_booth').click_image()
    if bank_booth is True:
        #logout()
        raise RuntimeError('couldnt find bank booth')

    # Wait for the bank window to appear.
    bank_window = vis.Vision(needle='./bank_window').wait_for_image()
    if bank_window is True:
        #logout()
        raise RuntimeError ('timed out waiting for bank booth to open')

    # Withdrawl the steel bars.
    #   Right click icon of steel bars.
    right_click_steel = vis.Vision(needle='./steel_bar_in_bank').\
                                     click_image(button='right')
    if right_click_steel is True:
        sys.exit(1)

    #   Select withdrawl option in right-click ocvbot-menu.
    withdrawl_steel = vis.Vision(needle='./windrawl_all').click_image()
    if withdrawl_steel is True:
        sys.exit(1)

    #   Wait for the items to appear in the player's inventory.
    steel_bars_in_inventory = vis.Vision(needle='./steel_bar_in_inv')\
        .wait_for_image(xmin=inv_xmin, xmax=inv_xmax, ymin=inv_ymin, 
        ymax=inv_ymax)
    if steel_bars_in_inventory is True:
        print('timed out waiting for steel bars to show up in inv')

    # Move to the furnace room from the bank.
     vis.click_image('./minimap_furnace_from_bank')
     vis.wait_for_image('./minimap_at_furnace')
     vis.click_image('furnace')
     vis.wait_for_image('smelting_menu')
     vis.keypress('space')

    ### wait for smelting to finish
    for i in range(1, 1000)
        lo.mlocate('./inv_empty')
        lo.mlocate('./login_screen')

        if lo.mlocate('./inv_empty') = 0:
            lo.click_image('./minimap_bank_from_furnace')
            lo.wait_forImage('./minimap_at_bank')
            lo.click_image('./bank_teller')
            lo.wait_for_image('./bank_window')
            lo.click_image('./steel_bars_in_inv',button='right')
            lo.click_image('./deposit_all')
            lo.wait_for_image('./empty_inventory')
    return
    ###

    click on bank
    wait for bank window to open -- mlocate(neelde=bank_window)
if bank is open, continue
look for steel bar -- mlocate(needle=steel_bar, haystack=bank_window)
right click steel bar -- click(button=right)
     click 'withdrawal all' -- mlocate(needle=withdrawal_all), click
     check for warnings -- mlocate(needle=warnings)
 wait for steel bar to appear in inventory -- mlocate(needle=steel_bar, 
 haystack=inventory)
 click on minimap objective -- mlocate(needle=minimap_furance_from_bank, 
 haystack=minimap)
 wait for palyer to reach objective -- mlocate(needle=minimap_at_furnace, 
 haystack=minimap)
 click on furnace -- mlocate(needle=furnace)
 use hotkeys to select correct options for smelting steel bars -- hotkey(1,2,3)
 while bars are smelting, run checks
     random chat messages -- random_chat()
     check for steel bars depleted -- mlocate(needle=steel_bar, haystack=inv)
     check for warning messages -- mlocate(needle=warning_message)
     check for logout -- mlocate(needle=login_page)
 when empty, click on bank objective -- mlocate(
 needle=minimap_bank_from_furnace,
 haystack=minimap)
 wait to reach bank -- mlocate(needle=at_bank)
 when at bank, re-test_orient player
 click on bank -- 
 wait for bank window to open
 right click steel bars in inv
     click 'deposit all'
     check for warnings
 wait for steel bars to deposit
 restart script
 return    
'''


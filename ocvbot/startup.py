import time

import pyautogui as pag

# Constants ------------------------------------------------------------

# See ./docs/client_anatomy.png for more info.
# Width and height of the entire game client.
CLIENT_WIDTH = 765
CLIENT_HEIGHT = 503

# Width and height of the inventory screen, in pixels.
INV_WIDTH = 186
INV_HEIGHT = 262
INV_HALF_WIDTH = round((INV_WIDTH / 2) + 5)
INV_HALF_HEIGHT = round(INV_HEIGHT / 2)

SIDE_STONES_WIDTH = 248
SIDE_STONES_HEIGHT = 366

# Width and height of just the game screen in the game client.
GAME_SCREEN_WIDTH = 512
GAME_SCREEN_HEIGHT = 334

CHAT_MENU_WIDTH = 506
CHAT_MENU_HEIGHT = 129

# Dimensions of the most recent "line" in the chat history.
CHAT_MENU_RECENT_WIDTH = 490
CHAT_MENU_RECENT_HEIGHT = 17

# Get the display size in pixels.
DISPLAY_WIDTH = pag.size().width
DISPLAY_HEIGHT = pag.size().height

# Stats ----------------------------------------------------------------

# Used for tracking how long the script has been running.
start_time = time.time()

# The number of inventories a script has gone through.
inventories = 0
# The number of items gathered, approximately.
items_gathered = 0
# The amount of experience gained since the script started, approximately.
xp_gained = 0
# TODO:
# The amount of experience gained since installing this package
xp_per_hour = 0

ore_xp_dict = {
    'copper': 16.5,
    'iron': 35.5
}

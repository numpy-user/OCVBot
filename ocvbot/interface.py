# coding=UTF-8
"""
Convenience functions for interacting with the buttons, toggles,
switches, and various other game interface elements.

"""
import logging as log

from ocvbot import vision as vis


# TODO: Add a set_compass(direction) function, as the client now supports
#       right-clicking on the compass to set specific cardinal directions.


def enable_button(
    button_disabled: str,
    button_disabled_region: tuple[int, int, int, int],
    button_enabled: str,
    button_enabled_region: tuple[int, int, int, int],
    conf: float = 0.95,
    loop_num: int = 5,
    attempts: int = 5,
    invert_match: bool = False,
):
    """
    Enables a button in the interface. Tries multiple times to ensure the
    button has been enabled. Assumes the button's "enabled" state looks
    different from its "disabled" state.

    More generically, this function can also be used to confirm certain actions
    have taken place (see example #2).

    Args:
        button_disabled (str): Filepath to an image of the disabled version
                               of the button.
        button_disabled_region (tuple): Vision region to use to search for the
                                        button_disabled image (e.g. `vis.inv` or
                                        `vis.side_stones` or `vis.game_screen`)
        button_enabled (str): Filepath to an image of the enabled version of
                              the button.
        button_enabled_region (tuple): Vision region to use to search for the
                                       button_enabled image.
        conf (float): Confidence required to match button images. See the `conf`
                      arg in the docstring of the `Vision` class for more info.
                      Default is `0.95`.
        loop_num (int): Number of times to search button_enabled after clicking
                        button_disabled. Default is 5.
        attempts (int): Number of times the function will try clicking on
                        button_disabled. Default is 5.
        invert_match (bool): Setting this to True will cause the function to
                             check for the absence of button_enabled instead
                             of its presence (see example #3). Default is False.

    Examples:
        Open a side stone:
            enable_button("./needles/side-stones/attacks-deselected.png",
                          vis.side_stones,
                          "./needles/side-stones/attacks-selected.png",
                          vis.side_stones)

        Logout of the game client:
            enable_button("./needles/buttons/logout.png", vis.inv,
                          "./needles/login-menu/orient.png", vis.game_screen)

        Close the bank window. Since the "close" button disappears after
        clicking on it, we must invert the match:
            enable_button("./needles/buttons/close.png", vis.game_screen,
                          "./needles/buttons/close.png", vis.game_screen,
                          0.95, True)

    Returns:
        Returns True if the button was enabled or was already enabled.

    Raises:
        Raises an exception if the button could not be enabled.

    """
    # Check if the button has already been enabled first.
    button_is_enabled = vis.Vision(
        region=button_enabled_region, needle=button_enabled, loop_num=1, conf=conf
    ).wait_for_needle()
    if invert_match is False:
        if button_is_enabled is True:
            log.debug("Button %s was already enabled", button_enabled)
            return True
    elif invert_match is True:
        if button_is_enabled is False:
            log.debug("Button %s was already enabled (invert_match)", button_enabled)
            return True

    # Try multiple times to enable the button.
    for _ in range(attempts):

        log.debug("Attempting to enable button %s", button_enabled)

        # Move mouse out of the way after clicking so the function can
        #   tell if the button is enabled.
        vis.Vision(
            region=button_disabled_region,
            needle=button_disabled,
            loop_num=3,
        ).click_needle(sleep_range=(0, 100, 0, 100), move_away=True)

        # See if the button has been enabled.
        button_is_enabled = vis.Vision(
            region=button_enabled_region,
            needle=button_enabled,
            loop_num=loop_num,
            conf=conf,
        ).wait_for_needle()
        if invert_match is False:
            if button_is_enabled is True:
                log.debug("Button %s has been enabled", button_enabled)
                return True
        elif invert_match is True:
            if button_is_enabled is False:
                log.debug("Button %s has been enabled (invert_match)", button_enabled)
                return True

    raise Exception("Could not enable button!", button_enabled)

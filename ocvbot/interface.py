# coding=UTF-8
"""
Convenience functions for interacting with the buttons, toggles,
switches, and various other game interface elements.

"""
import logging as log

from ocvbot import vision as vis


def enable_button(
    button_disabled: str,
    button_disabled_region: tuple[int, int, int, int],
    button_enabled: str,
    button_enabled_region: tuple[int, int, int, int],
    conf: float = 0.95,
):
    """
    Enables a button in the interface. Tries multiple times to ensure the
    button has been enabled. Assumes the button's "enabled" state looks
    different from its "disabled" state.

    More generically, this function can also be used to confirm certain actions
    have taken place (see second example).

    Args:
        button_disabled (str): Filepath to an image of the disabled version
                               of the button.
        button_disabled_region (tuple): Vision region to use to search for the
                                        button_disabled image (e.g. `vis.inv` or
                                        `vis.side_stones` or `vis.game_screen`.)
        button_enabled (str): Filepath to an image of the enabled version of
                              the button.
        button_enabled_region (tuple): Vision region to use to search for the
                                       button_enabled image.
        conf (float): Confidence required to match button images. See the `conf`
                      arg in the docstring of the `Vision` class for more info.
                      Default is `0.95`.

    Examples:
        Open a side stone:
            enable_button("./needles/side-stones/attacks-deselected.png",
                          vis.side_stones,
                          "./needles/side-stones/attacks-selected.png",
                          vis.side_stones)
        Logout of the game client:
            enable_button("./needles/buttons/logout.png", vis.inv,
                          "./needles/login-menu/orient.png", vis.game_screen)

    Returns:
        Returns True if the button was enabled or was already enabled.

    Raises:
        Raises an exception if the button could not be enabled after multiple
        attempts.

    """
    # Try multiple times to enable the button.
    for _ in range(5):

        button_enabled_needle = vis.Vision(
            region=button_enabled_region, needle=button_enabled, loop_num=1, conf=conf
        ).wait_for_needle()
        if button_enabled_needle is True:
            log.debug("Button %s is enabled", button_enabled)
            return True

        log.debug("Attempting to enable button %s", button_enabled)
        # Move mouse out of the way after clicking so the function can
        #   tell if the button is enabled.
        vis.Vision(
            region=button_disabled_region,
            needle=button_disabled,
            loop_num=3,
        ).click_needle(sleep_range=(0, 100, 0, 100), move_away=True)

    raise Exception("Could not enable button ", button_enabled)

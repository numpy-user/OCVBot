## OCVbot: The OSRS Computer Vision Bot

**Currently under development.**

## INSTALLATION

1. Download the correct archive from the Releases page, according to your
OS.

1. Decompress the archive somewhere in your home directory.

1. Create a file in the `credentials` directory called 'username.txt' and add
your account's login to it.
1. Create another file in the `credentials` directory called `password.txt` and
and your account's password to it. Accounts with 2-factor authentication are
not supported.

1. Rename `ocvbot/config.ini.example` to `ocvbot/config.ini`.
1. Edit `ocvbot/config.ini` with your desired configuration settings.

1. Check `docs/client-configuration` for the proper client
configuration settings. Configurations in the `common/` directory are shared by
all scripts. Configurations in all other directories are unique to that script
only.

1. Launch the OldSchool Runescape client and configure your client accordingly.
 Make sure your character is in the correct starting position.
> Third-party clients have not been tested.

1. Launch the executable.

1. Move the mouse cursor to a corner of the screen to stop the bot.

## CONFIGURATION

Currently OCVBot is configured via a few basic settings in the `ocvbot/config.ini`
file. Please see the comments in that file for information on how to configure
each parameter.

The bot takes random short breaks, so don't be alarmed if it appears to do
nothing for a short while.

For more technical users, comprehensive API documentation is located at
`docs/build/html/`

*This bot was written for educational purposes only. I am not responsible for how
you use this software.*

## OCVbot: The OSRS Computer Vision Bot

**Currently under development. Two mining scripts have been completed
and are currently functional. Version 0.1 coming soon.**

## INSTALLATION (Windows)

1. Clone this repository:
> It is assumed you've cloned this repository into the root of your home
directory.
```bash
git clone https://github.com/takelley1/ocvbot
```

1. Navigate into the root of the cloned repo and open the Command Prompt. Run
the following command:
> Your Python command may be different. Python 2 is not supported.
```bash
python3 setup.py
```

1. Create a file and add your account's login username to
`ocvbot\ocvbot\credentials\username.txt`
1. Create another file and add your account's login password to
`ocvbot\ocvbot\credentials\password.txt`

1. Rename `ocvbot\ocvbot\config.yaml.example` to `ocvbot\ocvbot\config.yaml`.
1. Edit `ocvbot\ocvbot\config.yaml` with your desired configuration settings.

1. Check `ocvbot\docs\client-configuration\` for the proper client
configuration settings. Configuration in the `common\` directory are shared by
all scripts. Configurations in all other directories are unique to that script
only.

1. Launch the OldSchool Runescape client and configure your client accordingly.
 Make sure your character is in the correct starting position.
> Third-party clients are not supported.

1. Open a Command Prompt at `ocvbot\ocvbot\` and run the following command:
```bash
python3 main.py
```

1. Type `CTRL-SHIFT-k` or move the mouse cursor to a corner of the screen to
stop the bot.


## INSTALLATION (Linux)

1. Clone this repository:
```bash
git clone https://github.com/takelley1/ocvbot
```

1. Run setup.py
> Your `python` command may be different. Python 2 is not supported.
```bash
python3 ./ocvbot/setup.py
```

1. Create a file and add your account's login username to
`./ocvbot/ocvbot/credentials/username.txt`
1. Create another file and add your account's login password to
`./ocvbot/ocvbot/credentials/password.txt`

1. Rename `./ocvbot/ocvbot/config.yaml.example` to `./ocvbot/ocvbot/config.yaml`.
1. Edit `./ocvbot/ocvbot/config.yaml` with your desired configuration settings.

1. Check `./ocvbot/docs/client-configuration/` for the proper client
configuration settings. Configurations in the `common/` directory are shared by
all scripts. Configurations in all other directories are unique to that script
only.

1. Launch the OldSchool Runescape client and configure your client accordingly.
 Make sure your character is in the correct starting position.
> Third-party clients may work but are not supported.

1. Run the bot
> For the "quit" hotkey to work, the bot must be run with sudo rights.
```bash
sudo python3 ./ocvbot/ocvbot/main.py
```

1. Type `CTRL-SHIFT-k` or move the mouse cursor to a corner of the screen to
stop the bot.

## CONFIGURATION

Currently OCVBot is configured via a few basic settings in the `config.yaml`
file. Please see the comments in that file for information on how to configure
each parameter.

The bot takes random short breaks, so don't be alarmed if it appears to do
nothing for a short while.

For more technical users, comprehensive API documentation is located at
`docs/build/html/`

# OCVbot

The OSRS Computer Vision bot

## INSTALLATION

1. Clone this repository into your home directory
```bash
cd ~
git clone --depth 1 https://github.com/takelley1/OCVBot.git
```

2. Create a Python virtual environment
```bash
cd OCVBot
python3 -m venv ocvbot-env
source ocvbot-env/bin/activate
```

3. Install Python module dependencies into your virtual environment
    - (For developers, use `pip install -r requirements.txt` instead)
```bash
python3 ./setup.py install
```

4. Create a file in the `credentials` directory called `username.txt` and add
   your account's username to it.
```bash
echo "ThisIsMyUsername" > credentials/username.txt
```

5. Create another file in the `credentials` directory called `password.txt` and
   and your account's password to it. Accounts with 2-factor authentication are
   not supported.
```bash
echo "ThisIsMySuperSecretPassword" > credentials/password.txt
```

6. Rename `ocvbot/config.yaml.example` to `ocvbot/config.yaml`.
```bash
mv ocvbot/config.yaml.example ocvbot/config.yaml
```

7. Edit `ocvbot/config.ini` with your desired configuration settings.

8. Check `docs/client-configuration` for the proper client. configuration
   settings. Configurations in the `common/` directory are shared by all
   scripts. Configurations in all other directories are unique to that script
   only.

9. Launch the OldSchool Runescape client. A wrapper script is provided in
   this repository.
```bash
./tools/osrs.sh
```

10. Configure your client to match the screenshots in `docs/client-configuration`.
    Make sure your character is in the correct starting position before running
    the bot. Third-party clients like Runelite have not been tested.

11. Start the bot.
```
python3 ./ocvbot/main.py
```

## CONFIGURATION

Currently OCVBot is configured via a few basic settings in the `ocvbot/config.ini`
file. Please see the comments in that file for information on how to configure
each parameter.

The bot takes random short breaks, so don't be alarmed if it appears to do
nothing for a short while.

For more technical users, comprehensive API documentation is located at
`docs/build/html/`.

*This bot was written for educational purposes only. I am not responsible for how
you use this software.*

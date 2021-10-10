# OCVbot

The OSRS Computer Vision bot

## INSTALLATION

1. Clone this repository into your home directory.
```bash
cd ~
git clone --depth 1 https://github.com/takelley1/OCVBot.git
```

2. Create and enter a Python virtual environment.
```bash
cd OCVBot
python3 -m venv ocvbot_venv
source ocvbot_venv/bin/activate
```

3. Install OCVBot's Python dependencies into your virtual environment.
```bash
pip3 install -r requirements.txt
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

7. Read and edit `ocvbot/config.yaml` with your desired configuration settings.

8. Check `docs/client-configuration` for the proper client configuration
   settings. Configurations in the `common/` directory are shared by all
   scripts. Configurations in all other directories are unique to that script
   only.

9. Launch the OldSchool Runescape client. A wrapper script is provided in
   this repository.
```bash
bash ./tools/osrs.sh
```

10. Adjust your client to match the screenshots in `docs/client-configuration`.
    Make sure your character is in the correct starting position before running
    the bot. Third-party clients like Runelite have not been tested.

11. Start the bot.
```
python3 ./ocvbot/main.py
```

- To stop the bot, use CTRL-C on the terminal window running the bot.
- To exit the virtual environment, run `deactivate`.
> NOTE: You must activate the virtual environment every time you wish to run the bot!

## CONFIGURATION

Currently OCVBot is configured via a few basic settings in the `ocvbot/config.yaml`
file. Please see the comments in that file for information on how to configure
each parameter.

The bot takes random short breaks, so don't be alarmed if it appears to do
nothing for a short while.

For more technical users, comprehensive API documentation is located at
`docs/build/html/`.

*This bot was written for educational purposes only. I am not responsible for how
you use this software.*

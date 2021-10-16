# coding=UTF-8
"""
Quickly logs the user in. Pass a name for "user" on the command line
to specify the user to use.

SETUP:
Your user credentials file must have the format of:
`username-{USER}.txt`
Where {USER} is to be replaced with your account's username.

Your user password credentials file must have the format of:
`password-{USER}.txt`
Where {USER} is to be replaced with your account's username.

RUNNING:
If your username is `alice123`, run the script like this:
`python3 login_user.py alice123`
"""
import pathlib
import sys

# Ensure ocvbot files are added to sys.path.
SCRIPTPATH = str(pathlib.Path(__file__).parent.parent.absolute())
sys.path.insert(1, SCRIPTPATH)

from ocvbot import behavior as behav

user = sys.argv[1]


def main():
    """
    Quickly logs in the desired user.
    """
    behav.login_basic(
        username_file="../ocvbot/credentials/username-" + user + ".txt",
        password_file="../ocvbot/credentials/password-" + user + ".txt",
        cred_sleep_range=(50, 100),
    )


if __name__ == "__main__":
    main()

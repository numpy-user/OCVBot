# Testing

- Testing with OCVBot is accomplished using directories of screenshots.
  These directories are opened with `feh` as an image album. When a test
  is started, the displayed screenshot "tricks" OCVBot into thinking it's
  interacting with the real game client. When the bot clicks on the
  screenshot, the next image in the album is displayed. This allows us
  to roughly simulate interactions with the real game client.

## Setup

1. Install `feh` using your package manager of choice.
2. Copy the feh config files in the `feh` directory into `~/.config/feh/`
   - These files configure `feh` to display the next image in the album when the
     image is clicked.
  ```bash
  mkdir -p ~/.config/feh/
  cp ./feh/* ~/.config/feh/
  ```

## Running all tests

1. Execute the `./run_all_tests.sh` file to run the entire test suite. The correct
  `config.yaml` settings are automatically applied.
```bash
./run_all_tests.sh
```

## Running individual tests

1. Make sure `ctrl_click_run` in your `config.yaml` is set to `False`.
  - This is required because `feh` can only have a single mouse binding set for the
    `next_img` action, and we need that binding to be the left mouse button. Using
    modifiers with the left mouse button requires a separate mouse binding in the
    `feh` config file, which isn't supported.
2. Enable your virtual environment for OCVBot (See the `Installation` section of
   the `README.md` file at the root of this repository)
```bash
source ../ocvbot_venv/bin/activate
```
3. Launch PyTest for the desired test.
```bash
pytest test_banking.py
```

## Code Coverage

1. `pip install coverage` = Install `coverage` package.
2. `cd tests` = Enter testing directory.
3. `coverage run --source=ocvbot -m pytest test_banking.py` = Run coverage tests.
4. `coverage html` = Generate html report.
5. `firefox htmlcov/index.html` = View report with browser.

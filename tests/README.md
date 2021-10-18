## Setup

- Copy the feh config files in this directory into `~/.config/feh/`
  ```bash
  cp ./feh/* ~/.config/feh/
  ```

- Make sure `ctrl_click_run` in your `config.yaml` is set to `False`. This is
  required because feh can only have a single mouse binding set for the
  `next_img` action, and we need that binding to be the left mouse button.

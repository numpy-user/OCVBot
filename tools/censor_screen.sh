#!/usr/bin/env bash

usage() {
    cat <<EOF

./censor_screen.sh {OPTIONS} {FILE}

Censors OSRS screen elements. This is used for creating screenshots for testing
  that are extremely small. A backup.png file is created automatically.
  Assumes the image provided is an OSRS screenshot with dimensions of 765x503.
  Compresses censored image with pngcrush afterwards.

  -b   Censor the primary bank window, excluding bank tabs and settings.
  -g   Censor the game screen.
  -c   Censor the chat menu.
  -i   Censor the inventory.
  -m   Censor the action orbs and minimap.
  -s   Censor the side stones and columns around the inventory.
  -S   Censor the bank settings at the bottom of the bank window.
  -t   Censor the bank tabs at the top of the bank window.

  -h   Print this help message.

Examples:
  censor_screen.sh -gcm image_01.png = Censor game screen, chat menu, and minimap.
  censor_screen.sh -i image_02.png = Censor the inventory.
  censor_screen.sh -tS myscreenshot.png = Censor bank tabs and bank settings.

EOF
    exit 1
}

if ! hash 2>/dev/null convert; then echo "Missing ImageMagick!" && exit 1; fi
if ! hash 2>/dev/null pngcrush; then echo "Missing pngcrush!" && exit 1; fi

bank_window=0
game_screen=0
chat_menu=0
inventory=0
minimap=0
side_stones=0
bank_settings=0
bank_tabs=0
while getopts ":bgcimhsSt" opt; do
    case "${opt}" in
    b) bank_window=1 ;;
    g) game_screen=1 ;;
    c) chat_menu=1 ;;
    i) inventory=1 ;;
    m) minimap=1 ;;
    s) side_stones=1 ;;
    S) bank_settings=1 ;;
    t) bank_tabs=1 ;;
    h) usage ;;
    *) usage ;;
    esac
done
shift $((OPTIND - 1))

if [[ -z "${1}" ]]; then
    usage
fi

set -euo pipefail
IFS=$'\n\t'

cp -f -- "${1}" "backup.png"

# -b = Censors the primary bank window, excluding tabs and settings.
if [[ "${bank_window}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 82 516 295" \
        "${1}"
fi

# -c = Censors the chat menu.
if [[ "${chat_menu}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 340 524 503" \
        "${1}"
fi

# -g = Censors the primary game screen.
if [[ "${game_screen}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 0 516 340" \
        "${1}"
fi

# -i = Censors and inventory.
if [[ "${inventory}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 550 205 734 467" \
        "${1}"
fi

# -m = Censors the compass, status orbs, and minimap.
if [[ "${minimap}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 517 0 765 169" \
        "${1}"
fi

# -s = Censors the side stones and columns.
if [[ "${side_stones}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 517 170 765 205" \
        -draw "rectangle 517 467 765 503" \
        -draw "rectangle 517 205 550 467" \
        -draw "rectangle 734 205 765 467" \
        "${1}"
    # -draw "rectangle 517 170 765 205" \ = Top side stones
    # -draw "rectangle 517 467 765 503" \ = Bottom side stones
    # -draw "rectangle 517 205 550 467" \ = Left column
    # -draw "rectangle 734 205 765 467" \ = Right column
fi

# -S = Censors the bank settings.
if [[ "${bank_settings}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 295 516 340" \
        "${1}"
fi

# -t = Censors the bank tabs.
if [[ "${bank_tabs}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 37 516 82" \
        "${1}"
fi

# Compress image with pngcrush.
# -ow = Overwrite image.
pngcrush -ow "${1}"
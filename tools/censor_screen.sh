#!/usr/bin/env bash
#
# Censors screen elements. This is used for creating screenshots for testing
#   that are extremely small.
#
# This script can be run multiple times on the same image to censor multiple
#   screen elements.
#
# Example:
#   `censor_screen.sh game image_01.png` = Censor the game screen.
#   `censor_screen.sh inv image_01.png`  = Additionally censor the side stones and inventory.

set -euo pipefail

if ! hash 2>/dev/null convert; then echo "Missing ImageMagick!" && exit 1; fi
if ! hash 2>/dev/null pngcrush; then echo "Missing pngcrush!" && exit 1; fi

cp "${2}" "backup.png"

# Censors the primary game screen.
if [[ "${1}" == "game" ]]; then
    convert "${2}" \
        -fill black \
        -draw "rectangle 0 0 516 340" \
        "${2}"

# Censors the chat menu.
elif [[ "${1}" == "chat" ]]; then
    convert "${2}" \
        -fill black \
        -draw "rectangle 0 340 524 503" \
        "${2}"

# Censors the side stones and inventory.
elif [[ "${1}" == "inv" ]]; then
    convert "${2}" \
        -fill black \
        -draw "rectangle 516 169 765 503" \
        "${2}"

# Censors the compass, status orbs, and minimap.
elif [[ "${1}" == "map" ]]; then
    convert "${2}" \
        -fill black \
        -draw "rectangle 517 0 765 169" \
        "${2}"

else
    printf "%s\n" "Incorrect options!"
    exit 1
fi

pngcrush -ow "${2}"

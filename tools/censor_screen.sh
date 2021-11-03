#!/usr/bin/env bash

usage() {
    cat <<EOF

./censor_screen.sh [OPTIONS] {FILE}

Censors OSRS screen elements. This is used for creating screenshots for testing
  that are extremely small.  A backup.png file is created automatically.

  -b   Censor the primary bank window, excluding tabs and settings.
  -g   Censor the game screen.
  -c   Censor the chat menu.
  -i   Censor the side stones and inventory.
  -m   Censor the action orbs and minimap.
  -s   Censor the bank settings at the bottom of the bank window.
  -t   Censor the bank tabs at the top of the bank window.

  -h   Print this help message.

Examples:
  censor_screen.sh -gc image_01.png   = Censor the game screen and chat menu.
  censor_screen.sh -i image_02.png    = Censor the side stones and inventory.

EOF
    exit 1
}

if ! hash 2>/dev/null convert; then echo "Missing ImageMagick!" && exit 1; fi
if ! hash 2>/dev/null pngcrush; then echo "Missing pngcrush!" && exit 1; fi

bank_window=0
game=0
chat=0
inv=0
map=0
bank_settings=0
bank_tabs=0
while getopts ":bgcimhst" opt; do
    case "${opt}" in
    b) bank_window=1 ;;
    g) game=1 ;;
    c) chat=1 ;;
    i) inv=1 ;;
    m) map=1 ;;
    s) bank_settings=1 ;;
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

# Censors the primary game screen.
if [[ "${game}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 0 516 340" \
        "${1}"
fi

# Censors the chat menu.
if [[ "${chat}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 340 524 503" \
        "${1}"
fi

# Censors the side stones and inventory.
if [[ "${inv}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 516 169 765 503" \
        "${1}"
fi

# Censors the compass, status orbs, and minimap.
if [[ "${map}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 517 0 765 169" \
        "${1}"
fi

# Censors the primary bank window, excluding tabs and settings.
if [[ "${bank_window}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 82 516 295" \
        "${1}"
fi

# Censors the bank settings.
if [[ "${bank_settings}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 295 516 340" \
        "${1}"
fi

# Censors the bank tabs.
if [[ "${bank_tabs}" -eq 1 ]]; then
    convert "${1}" \
        -fill black \
        -draw "rectangle 0 37 516 82" \
        "${1}"
fi

pngcrush -ow "${1}"

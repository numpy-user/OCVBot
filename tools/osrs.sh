#!/usr/bin/env bash

# Downloads and runs the OSRS client on Linux.
# Requires p7zip, wget, and java-11-openjdk.

java_path="/usr/lib/jvm/java-11-openjdk/bin/java"

# These varaiables are unlikely to change.
server="http://oldschool.runescape.com/jav_config.ws"
dmg_url="https://www.runescape.com/downloads/OldSchool.dmg"

# ------------------------------------------------------------------------

set -euo pipefail

print() {
    printf \
        "\n%s %s\n\n" \
        "[$(date +%F_%T)]" \
        "INFO: $* ####################################################################################################"
}

if ! hash wget 2>/dev/null; then echo "wget missing!" && exit 1; fi
if ! hash 7z 2>/dev/null; then echo "7z missing!" && exit 1; fi
if ! hash java 2>/dev/null; then echo "java missing!" && exit 1; fi

cleanup() {
    print "Cleaning up"
    rm -rf -- \
        /tmp/osrs*dmg \
        "${HOME}/random.dat" \
        "${HOME}/jagex_cl_oldschool_LIVE.dat" \
        "${HOME}/jagexappletviewer.preferences"

    if [[ -d "${HOME}/jagexcache" ]]; then
        mv -- "${HOME}/jagexcache" "${HOME}/.jagexcache"
    fi
}

# Clean up when killed.
trap cleanup EXIT

# Un-hide the cache directory if it exists.
if [[ -d "${HOME}/jagexcache" ]]; then
    mv -v -- "$HOME/jagexcache" "$HOME/.jagexcache"
fi

# Pull the latest client version.
print "Pulling latest image"
wget --no-check-certificate --no-verbose "${dmg_url}" --output-document="/tmp/osrs.dmg"

# Extract the JAR file from the DMG.
print "Extracting image"
7z x -y "/tmp/osrs.dmg" -o"/tmp/osrs-dmg/"

# Change working directory.
print "Entering image directory"
cd "/tmp/osrs-dmg/Old School RuneScape/Old School RuneScape.app/Contents/Java"

# Launch the OSRS client JAR file.
print "Launching Java applet"
"${java_path}" \
    -Djava.class.path=./jagexappletviewer.jar \
    -Dsun.java2d.nodraw=true \
    -Dcom.jagex.config="${server}" \
    -Xmx512m \
    -Xss2m \
    -XX:CompileThreshold=1500 \
    jagexappletviewer "."

exit 0


# Downloads and runs the OSRS client on Linux.
# Requires p7zip, wget, and java.

# Your OpenJDK installation path may be different. To find out your path,
#   run `which java`.
java_path="/usr/bin/java"

# These varaiables are unlikely to change.
server="http://oldschool.runescape.com/jav_config.ws"
dmg_url="https://www.runescape.com/downloads/OldSchool.dmg"

# ------------------------------------------------------------------------

set -u

# Clean up when killed.
trap 'rm -rf -- "/tmp/osrs.dmg" "/tmp/osrs-dmg" "$HOME/random.dat" "$HOME/jagex_cl_oldschool_LIVE.dat" "$HOME/jagexappletviewer.preferences" &>/dev/null ; mv -- "$HOME/jagexcache" "$HOME/.jagexcache" &>/dev/null' EXIT

# Un-hide the cache directory if it exists.
mv "$HOME/.jagexcache" "$HOME/jagexcache" &>/dev/null

# Pull the latest client version.
wget "${dmg_url}" --output-document="/tmp/osrs.dmg" --no-check-certificate &>/dev/null

# Extract the JAR file from the DMG.
7z x -y "/tmp/osrs.dmg" -o"/tmp/osrs-dmg/" &>/dev/null

# Change working directory.
cd '/tmp/osrs-dmg/Old School RuneScape/Old School RuneScape.app/Contents/Java' || exit 1

# Launch the OSRS client JAR file.
"${java_path}" -Djava.class.path=./jagexappletviewer.jar \
               -Dsun.java2d.nodraw=true                  \
               -Dcom.jagex.config=$server                \
               -Xmx512m -Xss2m                           \
               -XX:CompileThreshold=1500                 \
               -XX:+UseConcMarkSweepGC                   \
               jagexappletviewer "." &>/dev/null

# Clean up when exited.
rm -rf -- "/tmp/osrs.dmg" \
          "/tmp/osrs-dmg" \
          "$HOME/random.dat" \
          "$HOME/jagex_cl_oldschool_LIVE.dat" \
          "$HOME/jagexappletviewer.preferences" \
          &>/dev/null
mv -- "$HOME/jagexcache" \
      "$HOME/.jagexcache" \
      &>/dev/null

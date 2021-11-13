#!/usr/bin/env bash
#
# Script for running the entire OCVBot test suite.
# Automatically temporarily sets the config.yaml file to use the correct values.

set -euo pipefail

# Locate the main config file.
readonly script_path="$(realpath "${0}")"
readonly script_dir="$(dirname "${script_path}")"
readonly config_file="${script_dir}/../ocvbot/config.yaml"

readonly current_dir="$(pwd)"

readonly config_file_backup="$(mktemp)"

cleanup() {
    # Restore the original config file.
    mv -- "${config_file_backup}" "${config_file}"
    cd "${current_dir}" || exit 1
}
trap cleanup EXIT

# Backup the original config file before it's edited.
cp -f -- "${config_file}" "${config_file_backup}"

# Edit the config file.
sed -i \
    -e 's/ctrl_click_run:.*/ctrl_click_run: False/' \
    -e 's/random_waits:.*/random_waits: False/' \
    "${config_file}"

# Run the test suite with coverage check.
cd "${script_dir}" || exit 1
source "${script_dir}/../ocvbot_venv/bin/activate"
coverage run --source=ocvbot -m pytest .
coverage html

exit 0

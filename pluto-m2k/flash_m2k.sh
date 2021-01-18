#!/bin/bash

# Wrapper script for flashing an M2k board
# This script only handles flashing, no extra steps.
#
# Can be called with:  ./flash_m2k.sh
#
# The ./update_m2k_release.sh must be called to update release files

SCRIPT_DIR="$(readlink -f $(dirname $0))"

source $SCRIPT_DIR/lib/flash.sh

#----------------------------------#
# Main section                     #
#----------------------------------#

flash "m2k"

#!/bin/bash

SCRIPT_DIR="$(readlink -f $(dirname $0))"

source $SCRIPT_DIR/test_util.sh

TEST_NAME="TEST_ETH"

TEST_ID="01"
SHORT_DESC="Ethernet 0 is connected?"
CMD="sudo ethtool eth0 | grep -q \"Link detected: yes\""
run_test $TEST_ID "$SHORT_DESC" "$CMD"

TEST_ID="02"
SHORT_DESC="Ethernet 1 is connected?"
CMD="sudo ethtool -s eth1 speed 100 duplex full autoneg off;"
CMD+="sleep 3;"
CMD+="sudo ethtool eth1 | grep -q \"Link detected: yes\""
run_test $TEST_ID "$SHORT_DESC" "$CMD"

TEST_ID="03"
SHORT_DESC="Router ping test"
CMD="addr=\$(ip r | grep -i 'default via'| awk '{print \$3 }');"
CMD+="sudo ping -q -W2 -c2 \$addr > /dev/null"
run_test $TEST_ID "$SHORT_DESC" "$CMD"

 : #if reached this point, ensure exito code 0

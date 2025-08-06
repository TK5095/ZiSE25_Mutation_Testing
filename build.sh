#!/bin/bash

set -eu

usage() {
    echo "Usage: $0 <BOARD>"
    exit 2
}

if [ $# -ne 1 ]
then
    usage
fi

. ../.venv/bin/activate

BOARD="$1"

west build -b "${BOARD}" -- \
	-DZEPHYR_SCA_VARIANT=eclair \
	-DECLAIR_RULESET_FIRST_ANALYSIS=OFF \
	-DECLAIR_RULESET_USER=ON \
	-DECLAIR_USER_RULESET_NAME=MC \
	-DECLAIR_USER_RULESET_PATH=ECLAIR

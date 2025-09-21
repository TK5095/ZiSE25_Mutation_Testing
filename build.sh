#!/bin/bash

set -eu

usage() {
    echo "Usage: $0 <BOARD>"
    exit 2
}

if [ $# -ne 2 ]
then
    usage
fi

BOARD="$1"
RULESET="$2"

. ../.venv/bin/activate

west build -b "${BOARD}" -- \
	-DZEPHYR_SCA_VARIANT=eclair \
	-DECLAIR_RULESET_FIRST_ANALYSIS=OFF \
	-DECLAIR_RULESET_USER=ON \
	-DECLAIR_USER_RULESET_NAME="${RULESET}" \
	-DECLAIR_USER_RULESET_PATH=ECLAIR

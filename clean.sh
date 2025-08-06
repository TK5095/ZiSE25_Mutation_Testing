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

BOARD="$1"

. ../.venv/bin/activate

west build -t pristine -b "${BOARD}"

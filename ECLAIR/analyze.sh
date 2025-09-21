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

HERE=$( (
  cd "$(dirname "$0")"
  echo "${PWD}"
))

cd "${HERE}"

TOP=${HERE%/*}

export ECLAIR_PROJECT_NAME=temp_alert
export ECLAIR_PROJECT_ROOT="${TOP}"
export ECLAIR_OUTPUT_DIR="${HERE}/out"
export ECLAIR_DATA_DIR="${ECLAIR_OUTPUT_DIR}/.data"
export ECLAIR_WORKSPACE="${ECLAIR_OUTPUT_DIR}/eclair_workspace"
export ECLAIR_DIAGNOSTICS_OUTPUT="${ECLAIR_OUTPUT_DIR}/ANALYSIS.log"

rm -rf "${ECLAIR_OUTPUT_DIR}"
mkdir -p "${ECLAIR_OUTPUT_DIR}"
mkdir -p "${ECLAIR_DATA_DIR}"

(
    cd ..
    echo "Cleaning project."
    ./clean.sh "${BOARD}"
    echo "Starting ECLAIR Analysis."
    ./build.sh "${BOARD}" MC
)

echo "Analysis completed."

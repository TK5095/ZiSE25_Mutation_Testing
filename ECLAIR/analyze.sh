#!/bin/bash

set -eu

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
export ECLAIR_DIAGNOSTICS_OUTPUT="${ECLAIR_OUTPUT_DIR}/DIAGNOSTICS.txt"

rm -rf "${ECLAIR_OUTPUT_DIR}"
mkdir -p "${ECLAIR_OUTPUT_DIR}"
mkdir -p "${ECLAIR_DATA_DIR}"

../prepare.sh
../clean.sh

echo "Starting ECLAIR Analysis."

../build.sh

echo "Analysis done. Producing reports."
"${ECLAIR_PATH}eclair_report" "eval_file='${HERE}/report.ecl'"

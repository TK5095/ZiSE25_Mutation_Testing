#!/bin/bash

ECLAIR_PATH=${ECLAIR_PATH:/opt/bugseng/eclair/bin/}

HERE=$( (
  cd "$(dirname "$0")"
  echo "${PWD}"
))

find "${HERE}/../src" "${HERE}/../inc" -name '*.[ch]' -print0 | while IFS= read -r -d '' k; do
    echo "Formatting $k" 1>&2
    "${ECLAIR_PATH}eclair_format" -i 2 -l C "$k" || echo "$k"
done

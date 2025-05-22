#!/bin/bash

set -eu

west init -m https://github.com/BUGSENG/ZiSe25.git .
west update
pip install -r deps/zephyr/scripts/requirements.txt

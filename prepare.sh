#!/bin/bash

set -eu

cd ..
rm -fr .venv
python3 -m venv .venv
. .venv/bin/activate
pip3 install wheel
pip3 install west
west init -l --mf west.yml ZiSe25 || true
west update
west zephyr-export
west packages pip --install

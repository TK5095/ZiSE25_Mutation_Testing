#!/bin/bash

set -eu

# Zephyr deps

apt-get update
apt-get install -y --no-install-recommends \
    build-essential \
    autoconf \
    git \
    cmake \
    ninja-build \
    gperf \
    dfu-util \
    device-tree-compiler \
    curl \
    wget \
    python3-dev \
    python3-venv \
    python3-tk \
    xz-utils \
    file \
    make \
    gcc \
    gcc-multilib \
    g++-multilib \
    libsdl2-dev \
    libmagic1

# Set up SDK

SDK_VER="0.17.2"
ZEPHYR_SDK="zephyr-sdk-${SDK_VER}_Linux-x86_64.tar.xz"
SDK_DIR="/opt/zephyr-sdk-${SDK_VER}"

if [ ! -f "${ZEPHYR_SDK}" ]
then
  wget "https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v${SDK_VER}/${ZEPHYR_SDK}" > /dev/null
fi

if [ ! -d "${SDK_DIR}" ]
then
  tar -C /opt -xf "${ZEPHYR_SDK}"

  pushd "${SDK_DIR}"
  ./setup.sh -t x86_64-zephyr-elf
  popd
fi

# Prepare environment

rm -fr ../.venv
rm -fr ../.west
rm -fr ZiSE25
rm -fr deps
python3 -m venv ../.venv
. ../.venv/bin/activate
pip install wheel
pip install west
pip install pyelftools
pip install gcovr

west init -l --mf west.yml || true
west update
west zephyr-export
west packages pip --install

# For requirements

pip install strictdoc

#!/bin/bash

set -eu

cd temp_alert
west build -b frdm_mcxn947/mcxn947/cpu0 -- \
	-DZEPHYR_SCA_VARIANT=eclair \
	-DECLAIR_RULESET_FIRST_ANALYSIS=OFF \
	-DECLAIR_RULESET_USER=ON \
	-DECLAIR_RULESET_NAME=MC

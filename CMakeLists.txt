# SPDX-License-Identifier: Apache-2.0

cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(temp_alert)

target_include_directories(app PRIVATE inc)

target_sources(app PRIVATE src/main.c)
target_sources_ifdef(CONFIG_APP_DISPLAY app PRIVATE src/display.c)
target_sources_ifdef(CONFIG_APP_DISPLAY app PRIVATE src/tm1637.c)
target_sources_ifdef(CONFIG_APP_BUZZER app PRIVATE src/buzzer.c)
target_sources_ifdef(CONFIG_APP_LEDS app PRIVATE src/leds.c)




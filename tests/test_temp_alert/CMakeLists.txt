cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(test_temp_alert)

target_include_directories(app PRIVATE ${CMAKE_CURRENT_SOURCE_DIR}/../../inc)

target_sources(app
  PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/../../src/display.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../src/tm1637.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../src/buzzer.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../src/leds.c
    ${CMAKE_CURRENT_SOURCE_DIR}/../../src/main.c
    ${CMAKE_CURRENT_SOURCE_DIR}/test_display.c
    ${CMAKE_CURRENT_SOURCE_DIR}/test_buzzer.c
    ${CMAKE_CURRENT_SOURCE_DIR}/test_leds.c
)
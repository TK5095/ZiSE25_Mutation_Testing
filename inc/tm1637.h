/* tm1637.h – public API for TM1637 4-digit 7-segment display
 * SPDX-License-Identifier: Apache-2.0
 */

#ifndef TM1637_H_
#define TM1637_H_

#include <zephyr/drivers/gpio.h>
#include <zephyr/sys/util.h>
#include <stdint.h>

/* brightness level 0..7 (0 = off, 7 = max) */
#define TM1637_BRIGHTNESS_MAX 7

/* device instance */
struct tm1637
{
  struct gpio_dt_spec clk;
  struct gpio_dt_spec dio;

};

/* Initialize the two GPIO lines (CLK and DIO) */
int tm1637_init(const struct tm1637 * dev);

/* Set display brightness (0–7) */
int tm1637_set_brightness(const struct tm1637 * dev, uint8_t brightness);

/* Write exactly 4 raw segment bytes; bits 0–6 = segments A–G, bit 7 = dot */
int tm1637_write_segments(const struct tm1637 * dev, const uint8_t segs[4]);

/* Standard hex-digit → segment map (0–F) */
extern const uint8_t tm1637_segment_map[16];

#endif /* TM1637_H_ */


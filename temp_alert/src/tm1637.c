/* tm1637.c – TM1637 implementation
 * SPDX-License-Identifier: Apache-2.0
 */

 #include "tm1637.h"
 #include <zephyr/kernel.h>
 #include <zephyr/device.h>
 #include <zephyr/drivers/gpio.h>
 
 /* TM1637 command bytes */
 #define CMD_DATA_AUTO    0x40
 #define CMD_ADDR         0xC0
 #define CMD_DISPLAY_CTRL 0x88
 
 /* timing: ~50 µs */
 static inline void _delay(void)
 {
     k_busy_wait(50);
 }
 
 static void _start(const struct tm1637 *dev)
 {
     gpio_pin_set_dt(&dev->dio, 1);
     gpio_pin_set_dt(&dev->clk, 1);
     _delay();
     gpio_pin_set_dt(&dev->dio, 0);
     _delay();
 }
 
 static void _stop(const struct tm1637 *dev)
 {
     gpio_pin_set_dt(&dev->clk, 0);
     _delay();
     gpio_pin_set_dt(&dev->dio, 0);
     _delay();
     gpio_pin_set_dt(&dev->clk, 1);
     _delay();
     gpio_pin_set_dt(&dev->dio, 1);
     _delay();
 }
 
 static void _send_byte(const struct tm1637 *dev, uint8_t byte)
 {
     for (int i = 0; i < 8; i++) {
         gpio_pin_set_dt(&dev->clk, 0);
         gpio_pin_set_dt(&dev->dio, byte & 0x01);
         _delay();
         gpio_pin_set_dt(&dev->clk, 1);
         _delay();
         byte >>= 1;
     }
     /* ACK cycle (we just pulse CLK with DIO as input, then back) */
     gpio_pin_set_dt(&dev->clk, 0);
     gpio_pin_configure_dt(&dev->dio, GPIO_INPUT);
     _delay();
     gpio_pin_set_dt(&dev->clk, 1);
     _delay();
     gpio_pin_configure_dt(&dev->dio, GPIO_OUTPUT);
 }
 
 /* Public data */
 const uint8_t tm1637_segment_map[16] = {
     0x3f, /* 0 */
     0x06, /* 1 */
     0x5b, /* 2 */
     0x4f, /* 3 */
     0x66, /* 4 */
     0x6d, /* 5 */
     0x7d, /* 6 */
     0x07, /* 7 */
     0x7f, /* 8 */
     0x6f, /* 9 */
     0x77, /* A */
     0x7c, /* b */
     0x39, /* C */
     0x5e, /* d */
     0x79, /* E */
     0x71  /* F */
 };
 
 int tm1637_init(const struct tm1637 *dev)
 {
     if (!device_is_ready(dev->clk.port) ||
         !device_is_ready(dev->dio.port)) {
         return -ENODEV;
     }
     /* start both low */
     int err = gpio_pin_configure_dt(&dev->clk, GPIO_OUTPUT_INACTIVE);
     if (err) {
         return err;
     }
     return gpio_pin_configure_dt(&dev->dio, GPIO_OUTPUT_INACTIVE);
 }
 
 int tm1637_set_brightness(const struct tm1637 *dev, uint8_t brightness)
 {
     if (brightness > TM1637_BRIGHTNESS_MAX) {
         return -EINVAL;
     }
     _start(dev);
     _send_byte(dev, CMD_DISPLAY_CTRL | brightness);
     _stop(dev);
     return 0;
 }
 
 int tm1637_write_segments(const struct tm1637 *dev, const uint8_t segs[4])
 {
     /* 1) set auto-increment mode */
     _start(dev);
     _send_byte(dev, CMD_DATA_AUTO);
     _stop(dev);
 
     /* 2) write four digits starting at address 0 */
     _start(dev);
     _send_byte(dev, CMD_ADDR);
     for (int i = 0; i < 4; i++) {
         _send_byte(dev, segs[i]);
     }
     _stop(dev);
 
     return 0;
 }
 
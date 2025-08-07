/*
 * SPDX-License-Identifier: Apache-2.0
 */

 #include "display.h"
 #include "tm1637.h"
 
 #include <zephyr/device.h>
 #include <zephyr/devicetree.h>
 #include <zephyr/drivers/gpio.h>
 #include <zephyr/logging/log.h>
 #include <zephyr/kernel.h>
 
 LOG_MODULE_DECLARE(temp_alarm);
 
 /* Bring in the same DT-spec you use in main.c */
 #define CLK_NODE DT_NODELABEL(tm1637_clk)
 #define DIO_NODE DT_NODELABEL(tm1637_din)
 
 static const struct tm1637 disp = {
     .clk = GPIO_DT_SPEC_GET(CLK_NODE, gpios),
     .dio = GPIO_DT_SPEC_GET(DIO_NODE, gpios),
 };
 
 int display_init(void)
 {
     int err;
 
     /* tm1637_init() will configure both pins for us */
     err = tm1637_init(&disp);
     if (err != 0) {
         LOG_ERR("TM1637 init failed: %d", err);
         return err;
     }
 
     /* clear display (all zeros) */
     {
         const uint8_t zeros[4] = {0, 0, 0, 0};
         tm1637_write_segments(&disp, zeros);
     }
 
     /* set a reasonable brightness (0–7) */
     tm1637_set_brightness(&disp, TM1637_BRIGHTNESS_MAX / 2);
 
     LOG_INF("TM1637 display ready");
     return 0;
 }
 
 int display_write(const uint8_t segs[4])
 {
     return tm1637_write_segments(&disp, segs);
 }
 
 /* run at APPLICATION init level */
 /* -E> deliberate MC4.R17.12 1 function name is concatenated with '__init_' token */
 SYS_INIT(display_init, APPLICATION, CONFIG_APPLICATION_INIT_PRIORITY);
 

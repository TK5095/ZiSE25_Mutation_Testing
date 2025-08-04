/*
 * SPDX-License-Identifier: Apache-2.0
 */

 #include "buzzer.h"
 #include "utils.h"
 #include <zephyr/drivers/gpio.h>
 #include <zephyr/device.h>
 #include <zephyr/devicetree.h>
 #include <zephyr/kernel.h>
 #include <zephyr/logging/log.h>
 
 LOG_MODULE_DECLARE(temp_alarm);
 
 /* Buzzer GPIO */
 #define BUZZER_NODE DT_ALIAS(buzzer)
 static const struct gpio_dt_spec buzzer = GPIO_DT_SPEC_GET(BUZZER_NODE, gpios);
 
 #define TONE_FREQ_HZ 2000U
 
 static void play_tone(uint32_t freq_hz, uint32_t duration_ms)
 {
     uint32_t half_period_us = 500000U / freq_hz;
     uint32_t cycles = (freq_hz * duration_ms) / 1000U;
     for (uint32_t i = 0; i < cycles; i++) {
         gpio_pin_set_dt(&buzzer, 1);
         k_sleep(K_USEC(half_period_us));
         gpio_pin_set_dt(&buzzer, 0);
         k_sleep(K_USEC(half_period_us));
     }
 }
 
 void buzzer_fire_pattern(void)
 {
     for (int i = 0; i < 3; i++) {
         play_tone(TONE_FREQ_HZ, 500);
         k_sleep(K_MSEC(500));
     }
     k_sleep(K_MSEC(1500));
 }
 
 void noreturn buzzer_thread_fn(void *a, void *b, void *c)
 {
     ARG_UNUSED(a); ARG_UNUSED(b); ARG_UNUSED(c);
     while (1) {
         if (atomic_get(&alarm_flag)) {
             buzzer_fire_pattern();
         } else {
             k_sleep(K_MSEC(200));
         }
     }
 }
 
 static int buzzer_init(void)
 {
     int ret;
 
     if (!device_is_ready(buzzer.port)) {
         LOG_ERR("Buzzer GPIO %s not ready", buzzer.port->name);
         return -ENODEV;
     }
     ret = gpio_pin_configure_dt(&buzzer, GPIO_OUTPUT_INACTIVE);
     if (ret) {
         LOG_ERR("Failed to configure buzzer (%d)", ret);
         return ret;
     }
     LOG_INF("Buzzer initialized on %s", buzzer.port->name);
     return 0;
 }

 /* -E> deliberate MC4.R17.12 1 function name is concatenated with '__init_' token */
 SYS_INIT(buzzer_init, APPLICATION, CONFIG_APPLICATION_INIT_PRIORITY);
 
 K_THREAD_DEFINE(buzzer_thread, BUZZER_THREAD_STACK,
                 buzzer_thread_fn, NULL, NULL, NULL,
                 THREAD_PRIORITY, 0, 0);
 

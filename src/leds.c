/*
 * SPDX-License-Identifier: Apache-2.0
 */

#include "leds.h"
#include "utils.h"
#include <zephyr/drivers/gpio.h>
#include <zephyr/device.h>
#include <zephyr/devicetree.h>
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_DECLARE(temp_alarm);

/* LED aliases */
#define LED0_NODE DT_ALIAS(led0)
#define LED1_NODE DT_ALIAS(led1)
#define LED2_NODE DT_ALIAS(led2)
#define LED3_NODE DT_ALIAS(led3)

static const struct gpio_dt_spec leds[] =
{
  GPIO_DT_SPEC_GET(LED0_NODE, gpios),
  GPIO_DT_SPEC_GET(LED1_NODE, gpios),
  GPIO_DT_SPEC_GET(LED2_NODE, gpios),
  GPIO_DT_SPEC_GET(LED3_NODE, gpios),
};

/**
 * @implements SRS-05
 */
void noreturn leds_thread_fn (void * a, void * b, void * c)
{
  ARG_UNUSED(a);
  ARG_UNUSED(b);
  ARG_UNUSED(c);

  while (true)
  {
    if (atomic_get(&alarm_flag) != 0)
    {
      for (size_t i = 0; i < ARRAY_SIZE(leds); i++)
      {
        gpio_pin_set_dt(&leds[i], 1);
        k_sleep(K_MSEC(100));
        gpio_pin_set_dt(&leds[i], 0);
      }
    }
    else
    {
      k_sleep(K_MSEC(200));
    }
  }
}

int leds_init (void)
{
  int err;

  for (size_t i = 0; i < ARRAY_SIZE(leds); i++)
  {
    if (!device_is_ready(leds[i].port))
    {
      LOG_ERR("LED%u port %s not ready",
              (unsigned) i, leds[i].port->name);
      return -ENODEV;
    }

    err = gpio_pin_configure_dt(&leds[i], GPIO_OUTPUT_INACTIVE);

    if (err != 0)
    {
      LOG_ERR("Failed to configure LED%u (%d)", (int) i, err);
      return err;
    }
  }

  LOG_INF("All LEDs initialized");
  return 0;
}

/* -E> deliberate MC4.R17.12 1 function name is concatenated with '__init_'
   token */
SYS_INIT(leds_init, APPLICATION, CONFIG_APPLICATION_INIT_PRIORITY);

K_THREAD_DEFINE(leds_thread, LED_THREAD_STACK,
                &leds_thread_fn, NULL, NULL, NULL,
                THREAD_PRIORITY, 0, 0);


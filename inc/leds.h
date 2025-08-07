#ifndef LEDS_H_
#define LEDS_H_

#include <zephyr/sys/atomic.h>

#define LED_THREAD_STACK    512
#define THREAD_PRIORITY       5

/* Initialize all LEDs */
int leds_init(void);

/* Thread that flashes LEDs when alarm_flag is set */
void leds_thread_fn(void *a, void *b, void *c);

extern atomic_t alarm_flag;

#endif /* LEDS_H_ */

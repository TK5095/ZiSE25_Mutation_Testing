#ifndef BUZZER_H_
#define BUZZER_H_

#include <zephyr/sys/atomic.h>

#define THREAD_PRIORITY       5
#define BUZZER_THREAD_STACK 512

/* Fire the Temporal-3 pattern once */
void buzzer_fire_pattern(void);

/* Thread that runs the alarm when alarm_flag is set */
void buzzer_thread_fn(void *, void *, void *);

extern atomic_t alarm_flag;

#endif /* BUZZER_H_ */
